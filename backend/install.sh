#!/bin/bash
# SafeMind Auto-Installer for Yandex Cloud / Ubuntu 22.04
# Run as root on fresh server: bash install.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_ok() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "This script must be run as root"
        exit 1
    fi
}

install_system() {
    log_info "Updating system..."
    apt update && apt upgrade -y
    
    log_info "Installing packages..."
    apt install -y \
        python3.10 python3-pip python3-venv \
        postgresql postgresql-contrib \
        nginx git curl ufw fail2ban \
        certbot python3-certbot-nginx
    
    log_ok "System packages installed"
}

setup_postgres() {
    log_info "Setting up PostgreSQL..."
    systemctl enable postgresql
    systemctl start postgresql
    
    # Check if database exists
    if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw safemind; then
        log_warn "Database 'safemind' already exists, skipping creation"
    else
        sudo -u postgres psql -c "CREATE DATABASE safemind;"
        log_ok "Database 'safemind' created"
    fi
    
    # Check if user exists
    if sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='safemind'" | grep -q 1; then
        log_warn "User 'safemind' already exists, skipping creation"
    else
        sudo -u postgres psql -c "CREATE USER safemind WITH PASSWORD 'safemind_secure_pass_2026';"
        sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE safemind TO safemind;"
        log_ok "User 'safemind' created"
    fi
}

clone_repo() {
    log_info "Cloning SafeMind repository..."
    if [ -d "/opt/safemind" ]; then
        log_warn "Directory /opt/safemind exists, pulling latest changes..."
        cd /opt/safemind
        git pull
    else
        git clone https://github.com/kimicito/safemind-landing.git /opt/safemind
        log_ok "Repository cloned"
    fi
    
    # Determine user (ubuntu or root or other)
    DEPLOY_USER="${SUDO_USER:-ubuntu}"
    if [ "$DEPLOY_USER" = "root" ]; then
        DEPLOY_USER="ubuntu"
    fi
    
    # Create user if doesn't exist
    if ! id "$DEPLOY_USER" &>/dev/null; then
        useradd -m -s /bin/bash "$DEPLOY_USER"
        log_ok "User '$DEPLOY_USER' created"
    fi
    
    chown -R "$DEPLOY_USER:$DEPLOY_USER" /opt/safemind
    log_ok "Ownership set to $DEPLOY_USER"
}

setup_python() {
    log_info "Setting up Python environment..."
    cd /opt/safemind/backend
    
    python3 -m venv venv
    source venv/bin/activate
    
    pip install --upgrade pip
    pip install -r requirements.txt
    
    log_ok "Python environment ready"
}

create_env() {
    log_info "Creating .env configuration..."
    cd /opt/safemind/backend
    
    if [ -f ".env" ]; then
        log_warn ".env already exists, backing up to .env.backup"
        cp .env .env.backup.$(date +%s)
    fi
    
    # Get server public IP
    SERVER_IP=$(curl -s ifconfig.me || echo "YOUR_SERVER_IP")
    
    cat > .env <<EOF
DATABASE_URL=postgresql://safemind:safemind_secure_pass_2026@localhost:5432/safemind
UNISENDER_API_KEY=YOUR_UNISENDER_KEY_HERE
FROM_EMAIL=hello@safemind.pro
ADMIN_TOKEN=$(openssl rand -hex 16)
FRONTEND_URL=https://safemind.pro
PORT=8000
EMAIL_PROVIDER=unisender
EOF
    
    chown "${DEPLOY_USER}:${DEPLOY_USER}" .env
    chmod 600 .env
    
    log_ok ".env created with random ADMIN_TOKEN"
    log_warn "IMPORTANT: Edit /opt/safemind/backend/.env and set your UNISENDER_API_KEY!"
}

setup_systemd() {
    log_info "Creating systemd service..."
    
    cat > /etc/systemd/system/safemind.service <<EOF
[Unit]
Description=SafeMind Backend API
After=network.target postgresql.service

[Service]
Type=simple
User=${DEPLOY_USER}
Group=${DEPLOY_USER}
WorkingDirectory=/opt/safemind
Environment=PATH=/opt/safemind/backend/venv/bin
EnvironmentFile=/opt/safemind/backend/.env
ExecStart=/opt/safemind/backend/venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable safemind
    
    log_ok "Systemd service created"
}

setup_nginx() {
    log_info "Configuring Nginx..."
    
    # Get server IP for initial config
    SERVER_IP=$(curl -s ifconfig.me || echo "localhost")
    
    cat > /etc/nginx/sites-available/safemind <<EOF
server {
    listen 80;
    server_name safemind.pro www.safemind.pro ${SERVER_IP};
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF
    
    if [ -f /etc/nginx/sites-enabled/default ]; then
        rm /etc/nginx/sites-enabled/default
    fi
    
    ln -sf /etc/nginx/sites-available/safemind /etc/nginx/sites-enabled/safemind
    
    nginx -t && systemctl reload nginx
    systemctl enable nginx
    
    log_ok "Nginx configured"
}

setup_firewall() {
    log_info "Configuring firewall..."
    
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow 22/tcp   # SSH
    ufw allow 80/tcp   # HTTP
    ufw allow 443/tcp  # HTTPS
    ufw --force enable
    
    log_ok "Firewall configured (ports 22, 80, 443 open)"
}

start_backend() {
    log_info "Starting SafeMind backend..."
    systemctl start safemind
    sleep 3
    
    if systemctl is-active --quiet safemind; then
        log_ok "Backend is running!"
    else
        log_error "Backend failed to start. Check logs: journalctl -u safemind -n 50"
        exit 1
    fi
}

check_health() {
    log_info "Checking health endpoint..."
    sleep 2
    
    HEALTH=$(curl -s http://localhost:8000/health || echo "failed")
    if echo "$HEALTH" | grep -q '"status":"ok"'; then
        log_ok "Health check passed!"
        echo "$HEALTH" | python3 -m json.tool 2>/dev/null || echo "$HEALTH"
    else
        log_warn "Health check returned: $HEALTH"
        log_warn "Backend may need UNISENDER_API_KEY configured"
    fi
}

print_summary() {
    ADMIN_TOKEN=$(grep ADMIN_TOKEN /opt/safemind/backend/.env | cut -d= -f2)
    
    echo ""
    echo "=========================================="
    echo -e "${GREEN}SafeMind Backend Installation Complete!${NC}"
    echo "=========================================="
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Edit .env file:"
    echo "   nano /opt/safemind/backend/.env"
    echo "   Set your UNISENDER_API_KEY"
    echo ""
    echo "2. Restart backend after editing .env:"
    echo "   systemctl restart safemind"
    echo ""
    echo "3. Your ADMIN_TOKEN is: ${YELLOW}${ADMIN_TOKEN}${NC}"
    echo "   Save it! You'll need it for the admin panel."
    echo ""
    echo "4. Configure DNS for safemind.pro -> $(curl -s ifconfig.me)"
    echo ""
    echo "5. After DNS propagates, get SSL:"
    echo "   certbot --nginx -d safemind.pro -d www.safemind.pro"
    echo ""
    echo -e "${BLUE}Useful commands:${NC}"
    echo "   systemctl status safemind     - Check backend status"
    echo "   journalctl -u safemind -f     - View real-time logs"
    echo "   systemctl restart safemind   - Restart backend"
    echo "   curl http://localhost:8000/health - Local health check"
    echo ""
    echo -e "${BLUE}API Endpoints:${NC}"
    echo "   POST /subscribe              - Subscribe new lead"
    echo "   GET /leads                   - Admin: list all leads (needs X-Admin-Token)"
    echo "   GET /leads/count             - Admin: statistics"
    echo "   POST /trigger-drip           - Admin: trigger drip campaign"
    echo "   GET /health                  - Health check"
    echo ""
    echo "=========================================="
}

# ─── Main ────────────────────────────────────────────────────────
check_root
log_info "Starting SafeMind auto-installation..."

install_system
setup_postgres
clone_repo
setup_python
create_env
setup_systemd
setup_nginx
setup_firewall
start_backend
check_health
print_summary

log_ok "Installation complete!"
