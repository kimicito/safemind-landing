# SafeMind — Yandex Cloud (РФ) — Полная инструкция

**Преимущества Yandex Cloud:**
- ✅ Бесплатный тариф «Always Free» — 1 ВМ + 30 GB SSD навсегда
- ✅ Регистрация через твой Яндекс ID (уже есть)
- ✅ Российский сервер — никаких VPN
- ✅ Оплата картой РФ (если выйдешь за лимиты, а их не будет)

---

## Шаг 1: Регистрация Yandex Cloud (5 минут)

1. Открой [cloud.yandex.ru](https://cloud.yandex.ru)
2. Нажми **«Попробовать бесплатно»**
3. Войди через свой **Яндекс ID** (тот же, что для Яндекс Диска)
4. Привяжи телефон (если просит)
5. Создай **Billing account** → выбери «Физическое лицо» → привяжи карту (для верификации, деньги не спишут)
6. Дождись активации (обычно мгновенно)

---

## Шаг 2: Создание виртуальной машины (10 минут)

1. В консоли Yandex Cloud нажми **«Создать ресурс» → «Виртуальная машина»**

2. **Основные параметры:**
   - Имя: `safemind-server`
   - Зона: `ru-central1-a` (Москва)

3. **Выбор образа:**
   - Тип: **Публичный образ**
   - ОС: **Ubuntu 22.04 LTS**

4. **Диск:**
   - Тип: **SSD**
   - Размер: **30 GB** (бесплатно входит в Always Free)

5. **Вычислительные ресурсы:**
   - Платформа: **Intel Ice Lake**
   - vCPU: **2** (бесплатно в Always Free)
   - RAM: **4 GB** (бесплатно в Always Free)

6. **Сеть:**
   - Подсеть: автоматически создастся
   - **Публичный адрес: Автоматически** ← обязательно!

7. **Доступ:**
   - Способ: **SSH-ключ**
   - Нужно сгенерировать SSH-ключ. Если у тебя Mac/Linux — выполни в терминале:
     ```bash
     ssh-keygen -t ed25519 -C "safemind"
     cat ~/.ssh/id_ed25519.pub
     ```
   - Если Windows — скачай PuTTYgen, сгенерируй ключ, скопируй публичную часть
   - Вставь публичный ключ в поле **SSH-ключ** в Yandex Cloud

8. Нажми **«Создать ВМ»**

9. Дождись статуса **Running** (1-2 минуты)

10. Скопируй **Публичный IP адрес** (вида `84.252.xxx.xxx`) — он показан в списке ВМ

---

## Шаг 3: Подключение к серверу (5 минут)

### Mac / Linux:
```bash
ssh ubuntu@ТВОЙ_IP_АДРЕС
```
Пример: `ssh ubuntu@84.252.123.45`

### Windows (PuTTY):
- Host: `ubuntu@ТВОЙ_IP_АДРЕС`
- Port: `22`
- Connection → SSH → Auth → приватный ключ `id_ed25519`
- Open

**Если спрашивает `Are you sure you want to continue connecting?` — напиши `yes` и Enter.**

Ты внутри сервера. Терминал покажет:
```
ubuntu@safemind-server:~$
```

---

## Шаг 4: Установка SafeMind backend (15 минут)

Выполняй команды **по одной**, нажимая Enter после каждой:

```bash
# 1. Обнови систему
sudo apt update && sudo apt upgrade -y

# 2. Установи необходимые пакеты
sudo apt install -y python3.10 python3-pip python3-venv postgresql postgresql-contrib nginx git curl ufw fail2ban

# 3. Запусти PostgreSQL
sudo systemctl enable postgresql
sudo systemctl start postgresql

# 4. Создай базу данных и пользователя
sudo -u postgres psql -c "CREATE DATABASE safemind;"
sudo -u postgres psql -c "CREATE USER safemind WITH PASSWORD 'safemind_secure_pass_2026';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE safemind TO safemind;"

# 5. Клонируй проект
cd /opt
sudo git clone https://github.com/kimicito/safemind-landing.git safemind
sudo chown -R ubuntu:ubuntu /opt/safemind

# 6. Создай виртуальное окружение
cd /opt/safemind/backend
python3 -m venv venv
source venv/bin/activate

# 7. Установи Python-зависимости
pip install --upgrade pip
pip install -r requirements.txt

# 8. Создай .env файл
cat > /opt/safemind/backend/.env << 'EOF'
DATABASE_URL=postgresql://safemind:safemind_secure_pass_2026@localhost:5432/safemind
UNISENDER_API_KEY=YOUR_UNISENDER_KEY_HERE
FROM_EMAIL=hello@safemind.pro
ADMIN_TOKEN=CHANGE_THIS_TO_STRONG_PASSWORD
FRONTEND_URL=https://safemind.pro
PORT=8000
EMAIL_PROVIDER=unisender
EOF
```

**Важно:** после создания `.env` отредактируй его:
```bash
nano /opt/safemind/backend/.env
```

Найди строку `UNISENDER_API_KEY=YOUR_UNISENDER_KEY_HERE` и замени на свой ключ.
Найди `ADMIN_TOKEN=CHANGE_THIS_TO_STRONG_PASSWORD` и придумай сложный пароль.

Сохрани: **Ctrl+O** → Enter → **Ctrl+X** для выхода.

---

## Шаг 5: Регистрация на Unisender (10 минут)

Пока устанавливалось — сделай это параллельно:

1. Открой [unisender.com](https://unisender.com) в браузере
2. Нажми **«Регистрация»**
3. Введи email и пароль
4. Подтверди email (перейди по ссылке из письма)
5. Войди в личный кабинет
6. Перейди в раздел **«Настройки» → «API»**
7. Скопируй **API ключ** (выглядит как `xxxxxxxxxxxxxxxxxxxx`)
8. Вставь его в `/opt/safemind/backend/.env` вместо `YOUR_UNISENDER_KEY_HERE`

---

## Шаг 6: Запуск backend (5 минут)

Продолжай в терминале на сервере:

```bash
# 1. Создай systemd-сервис для автозапуска
sudo tee /etc/systemd/system/safemind.service > /dev/null << 'EOF'
[Unit]
Description=SafeMind Backend API
After=network.target postgresql.service

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/safemind
Environment=PATH=/opt/safemind/backend/venv/bin
EnvironmentFile=/opt/safemind/backend/.env
ExecStart=/opt/safemind/backend/venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 2. Перезагрузи systemd и запусти сервис
sudo systemctl daemon-reload
sudo systemctl enable safemind
sudo systemctl start safemind

# 3. Проверь статус
sudo systemctl status safemind
```

Если видишь `Active: active (running)` — всё работает!

Проверь API:
```bash
curl http://localhost:8000/health
```

Должно вернуть:
```json
{"status":"ok","email_provider":"unisender","email_configured":false}
```

`email_configured: false` — это нормально, значит ключ ещё не вставлен. Когда вставишь Unisender ключ — будет `true`.

---

## Шаг 7: Настройка Nginx + SSL (10 минут)

### 7.1 Настрой Nginx как reverse proxy
```bash
# Создай конфиг
sudo tee /etc/nginx/sites-available/safemind > /dev/null << 'EOF'
server {
    listen 80;
    server_name safemind.pro www.safemind.pro;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

# Активируй сайт
sudo ln -s /etc/nginx/sites-available/safemind /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7.2 Настрой SSL через Let's Encrypt (Certbot)
```bash
# Установи Certbot
sudo apt install -y certbot python3-certbot-nginx

# Получи сертификат (замени на свой email)
sudo certbot --nginx -d safemind.pro -d www.safemind.pro --email твой@email.ru --agree-tos --non-interactive

# Проверь автообновление
sudo certbot renew --dry-run
```

Если certbot спросит что-то — нажми `Y` и Enter.

---

## Шаг 8: Настройка домена (5 минут)

1. Зайди в админку своего регистратора домена (где купил `safemind.pro`)
2. Найди раздел **DNS** или **Управление зоной**
3. Создай или измени **A-запись**:
   - Имя: `@` (или `safemind.pro`)
   - Тип: `A`
   - Значение: **IP твоего сервера** (из шага 2.10)
   - TTL: 600
4. Сохрани
5. Подожди 5-15 минут (распространение DNS)

---

## Шаг 9: Проверка работы (2 минуты)

Открой в браузере:

- **Health check:** `https://safemind.pro/health`
  - Должно показать: `{"status":"ok","email_provider":"unisender","email_configured":true}`

- **Админка (лиды):** `https://safemind.pro/leads`
  - Должно спросить токен — отправь через Postman или curl:
    ```bash
    curl -H "X-Admin-Token: ТВОЙ_ПАРОЛЬ" https://safemind.pro/leads
    ```

- **Фронтенд:** `https://safemind.pro` — должен открыться твой сайт

---

## Шаг 10: Тестовая подписка (2 минуты)

1. Открой `https://safemind.pro`
2. Прокрути до формы «Бесплатный гид»
3. Введи свой email, выбери роль
4. Нажми «Получить гид»
5. Проверь почту — должен прийти welcome email с PDF

Если email пришёл — backend работает идеально.

---

## Команды для повседневного использования

```bash
# Подключиться к серверу
ssh ubuntu@ТВОЙ_IP

# Проверить статус backend
sudo systemctl status safemind

# Посмотреть логи backend (в реальном времени)
sudo journalctl -u safemind -f

# Перезапустить backend
sudo systemctl restart safemind

# Обновить код из GitHub
cd /opt/safemind && git pull && sudo systemctl restart safemind

# Проверить базу данных
sudo -u postgres psql safemind -c "SELECT COUNT(*) FROM leads;"

# Проверить, что Nginx работает
sudo nginx -t && sudo systemctl status nginx

# Обновить SSL сертификат (авто, но можно вручную)
sudo certbot renew
```

---

## Если что-то пошло не так

**Backend не запускается:**
```bash
sudo journalctl -u safemind -n 50 --no-pager
```
Пришли мне вывод — я разберу.

**Email не приходит:**
1. Проверь `UNISENDER_API_KEY` в `.env`
2. Проверь статус: `curl https://safemind.pro/health`
3. Смотри логи: `sudo journalctl -u safemind -f`, нажми «Получить гид» на сайте и смотри ошибки

**Сайт не открывается:**
1. Проверь DNS: `dig safemind.pro` (должен показать твой IP)
2. Проверь firewall Yandex Cloud: зайди в консоль → ВМ → сеть → убедись что порт 80 и 443 открыты
3. Проверь Nginx: `sudo systemctl status nginx`

**Я забыл ADMIN_TOKEN:**
```bash
sudo cat /opt/safemind/backend/.env | grep ADMIN_TOKEN
```

---

## Итоговая структура на сервере

```
/opt/safemind/
├── backend/
│   ├── main.py          ← API сервер
│   ├── requirements.txt ← зависимости
│   ├── .env             ← конфиг (ключи, пароли)
│   ├── venv/            ← Python окружение
│   └── README.md        ← эта инструкция
├── en/
│   └── index.html       ← английский лендинг
├── ru/
│   └── index.html       ← русский лендинг
├── es/
│   └── index.html       ← испанский лендинг
├── assets/
│   └── style.css        ← стили
└── pdfs/
    └── *.pdf            ← 24 PDF гида
```

---

**Когда всё настроено — скинь мне:**
1. Твой `ADMIN_TOKEN`
2. IP сервера
3. Проверь что `/health` работает

Я начну анализировать лиды, сегментировать аудиторию и масштабировать SafeMind. 🖤
