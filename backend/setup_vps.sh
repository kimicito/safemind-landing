#!/bin/bash
# SafeMind VPS Setup Script (Russia)
# Run as root on fresh Ubuntu 22.04/24.04

set -e

echo "=== SafeMind VPS Setup ==="
echo "This will install: Python 3.12, PostgreSQL 16, Nginx, Certbot"
read -p "Continue? (y/n): " confirm
[ "$confirm" != "y" ] && exit 1

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y \
    python3.12 python3.12-venv python3.12-dev python3-pip \
    postgresql postgresql-contrib \
    nginx certbot python3-certbot-nginx \
    git curl vim ufw fail2ban

# Start PostgreSQL
systemctl enable postgresql
systemctl start postgresql

# Create database and user
sudo -u postgres psql <<EOF
CREATE DATABASE safemind;
CREATE USER safemind WITH PASSWORD 'safemind_secure_pass_2026';
GRANT ALL PRIVILEGES ON DATABASE safemind TO safemind;
\q
EOF

# Save DB URL
DB_URL="postgresql://safemind:safemind_secure_pass_2026@localhost:5432/safemind"
echo "DATABASE_URL=$DB_URL" > /root/safemind_db_url.txt

# Create app directory
mkdir -p /opt/safemind
chown -R www-data:www-data /opt/safemind

echo "=== Base system ready ==="
echo "Database URL: $DB_URL"
echo "Next steps:"
echo "1. Clone repo to /opt/safemind"
echo "2. Run setup_app.sh"
