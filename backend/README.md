# SafeMind Backend — VPS Setup Guide (Russia)

## Стек
- **FastAPI** — API сервер
- **PostgreSQL** — база данных
- **Unisender** — email рассылки (РФ)
- **Nginx** — reverse proxy + SSL
- **Systemd** — автозапуск

## Быстрый старт

### 1. Купи VPS
Рекомендации:
- **Timeweb Cloud** — от 300₽/мес
- **Selectel** — от 400₽/мес
- **REG.RU** — от 350₽/мес

Требования: Ubuntu 22.04/24.04, 1 CPU, 1 GB RAM, 10 GB SSD

### 2. Подключись по SSH
```bash
ssh root@YOUR_SERVER_IP
```

### 3. Склонируй репозиторий
```bash
git clone https://github.com/kimicito/safemind-landing.git /opt/safemind
```

### 4. Запусти установку системы
```bash
cd /opt/safemind/backend
bash setup_vps.sh
```
Это установит Python 3.12, PostgreSQL, Nginx, Certbot.

### 5. Настрой базу данных
```bash
sudo -u postgres psql
\c safemind
\dt  # проверь что таблицы создались
\q
```

### 6. Настрой окружение
```bash
nano /opt/safemind/backend/.env
```

Заполни:
```
DATABASE_URL=postgresql://safemind:safemind_secure_pass_2026@localhost:5432/safemind
UNISENDER_API_KEY=your_key_here
FROM_EMAIL=hello@safemind.pro
ADMIN_TOKEN=your_strong_password_here
FRONTEND_URL=https://safemind.pro
PORT=8000
EMAIL_PROVIDER=unisender
```

### 7. Зарегистрируйся на Unisender
1. Иди на [unisender.com](https://unisender.com)
2. Создай аккаунт
3. Подтверди email
4. Скопируй **API Key**
5. Вставь в `.env`

### 8. Запусти приложение
```bash
cd /opt/safemind/backend
bash setup_app.sh
systemctl start safemind
systemctl enable safemind
```

### 9. Настрой Nginx
```bash
cp /opt/safemind/backend/nginx.conf /etc/nginx/sites-available/safemind
ln -s /etc/nginx/sites-available/safemind /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### 10. SSL (HTTPS)
```bash
certbot --nginx -d safemind.pro -d www.safemind.pro
```

### 11. Проверка
```bash
curl http://localhost:8000/health
# Должно вернуть: {"status":"ok",...}
```

Открой в браузере:
- `https://safemind.pro` — фронтенд
- `https://safemind.pro/health` — health check

### 12. Админка
```bash
curl -H "X-Admin-Token: your_token" https://safemind.pro/leads
```

## Команды

```bash
# Перезапустить backend
systemctl restart safemind

# Посмотреть логи
journalctl -u safemind -f

# Статус
systemctl status safemind

# Обновить код
cd /opt/safemind && git pull
systemctl restart safemind
```

## Переключение на Resend (для EN/ES аудитории)

Если нужен international email (лучше доставляемость за рубеж):

1. Зарегистрируйся на [resend.com](https://resend.com)
2. Получи API key
3. Измени `.env`:
```
EMAIL_PROVIDER=resend
RESEND_API_KEY=re_xxxxxxxx
```
4. Перезапусти:
```bash
systemctl restart safemind
```
