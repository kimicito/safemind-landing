#!/bin/bash
# SafeMind App Setup (run after setup_vps.sh)
# Run as root in /opt/safemind

set -e

APP_DIR="/opt/safemind"
USER="www-data"

echo "=== Setting up SafeMind app ==="

# Create virtual environment
python3.12 -m venv $APP_DIR/venv
source $APP_DIR/venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r $APP_DIR/backend/requirements.txt

# Add Unisender to requirements if not present
if ! grep -q "requests" $APP_DIR/backend/requirements.txt; then
    echo "requests==2.32.0" >> $APP_DIR/backend/requirements.txt
    pip install requests==2.32.0
fi

# Create .env file
if [ ! -f "$APP_DIR/backend/.env" ]; then
    cat > $APP_DIR/backend/.env <<EOF
DATABASE_URL=postgresql://safemind:safemind_secure_pass_2026@localhost:5432/safemind
UNISENDER_API_KEY=your_unisender_api_key_here
FROM_EMAIL=hello@safemind.pro
ADMIN_TOKEN=change_this_to_strong_password
FRONTEND_URL=https://safemind.pro
PORT=8000
EOF
    echo "=== Created .env file ==="
    echo "EDIT /opt/safemind/backend/.env and set your real values!"
fi

# Set permissions
chown -R $USER:$USER $APP_DIR

# Copy systemd service
cp $APP_DIR/backend/safemind.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable safemind

echo "=== App setup complete ==="
echo "1. Edit: nano /opt/safemind/backend/.env"
echo "2. Start: systemctl start safemind"
echo "3. Check: systemctl status safemind"
echo "4. Logs: journalctl -u safemind -f"
