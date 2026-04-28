#!/bin/bash
# Полный сброс nginx конфига для SafeMind

cat > /etc/nginx/sites-available/safemind << 'EOF'
server {
    listen 80;
    server_name safemind.pro www.safemind.pro 85.239.59.8;
    
    root /opt/safemind;
    index index.html;
    
    # Корневая страница — статика
    location / {
        try_files $uri $uri/ =404;
    }
    
    # API endpoints — прокси на backend
    location ~ ^/(health|subscribe|leads|trigger-drip|download) {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # PDF файлы — статика
    location /pdfs/ {
        alias /opt/safemind/pdfs/;
        add_header Content-Type application/pdf;
    }
    
    # Assets — статика
    location /assets/ {
        alias /opt/safemind/assets/;
    }
    
    # Языковые подпапки
    location ~ ^/(en|ru|es)/ {
        try_files $uri $uri/ =404;
    }
}
EOF

# Удали certbot SSL конфиг если он мешает
rm -f /etc/nginx/sites-enabled/*safemind*
ln -sf /etc/nginx/sites-available/safemind /etc/nginx/sites-enabled/safemind

# Проверь что default удалён
rm -f /etc/nginx/sites-enabled/default

# Права на файлы
chown -R www-data:www-data /opt/safemind
chmod -R 755 /opt/safemind

# Перезапусти nginx
nginx -t && systemctl restart nginx

echo "Done. Testing..."
sleep 2
curl -I http://85.239.59.8/
echo ""
curl http://85.239.59.8/ | head -10
