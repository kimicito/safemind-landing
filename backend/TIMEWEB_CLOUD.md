# SafeMind — Timeweb Cloud (РФ) — Полная инструкция

**Преимущества Timeweb Cloud:**
- ✅ Российский хостинг, оплата картой РФ
- ✅ VPS от 300₽/мес (или 7 дней бесплатно на тест)
- ✅ Доступ по паролю root — не нужно возиться с SSH-ключами
- ✅ Ubuntu 22.04 LTS в один клик
- ✅ Публичный IP сразу

---

## Шаг 1: Регистрация (5 минут)

1. Открой [timeweb.cloud](https://timeweb.cloud)
2. Нажми **«Регистрация»**
3. Введи email, придумай пароль
4. Подтверди email (перейди по ссылке из письма)
5. Войди в личный кабинет

---

## Шаг 2: Создание VPS (5 минут)

1. В панели нажми **«Создать сервер»** или **«Cloud» → «Создать»**

2. **Тип:** Облачный сервер (VPS)

3. **Локация:** Москва

4. **Операционная система:**
   - Выбери **Ubuntu 22.04 LTS**

5. **Конфигурация:**
   - CPU: **1 ядро** (достаточно для старта)
   - RAM: **1 GB** (можно 2 GB за небольшую доплату)
   - Диск: **15 GB SSD**
   - Итого: ~300₽/мес

6. **Сеть:**
   - **Публичный IP:** Да (IPv4)
   - Оставь всё по умолчанию

7. **Доступ:**
   - Способ: **Пароль**
   - Придумай сложный пароль для root (или оставь сгенерированный — **сохрани его!**)
   - **Важно:** Timeweb сразу даёт пароль root — это проще чем SSH-ключи

8. Нажми **«Создать»**

9. Жди 2-3 минуты пока сервер создастся

10. Скопируй **Публичный IP** (вида `85.193.xxx.xxx`) — он показан в списке серверов

---

## Шаг 3: Подключение к серверу (2 минуты)

### Mac / Linux:
```bash
ssh root@ТВОЙ_IP_АДРЕС
```
Пример: `ssh root@85.193.123.45`

Когда спросит пароль — введи тот, что сохранил при создании сервера (вводится без отображения символов).

### Windows:
1. Скачай и открой **PuTTY**
2. Host: `ТВОЙ_IP_АДРЕС`
3. Port: `22`
4. Connection type: **SSH**
5. Нажми **Open**
6. Логин: `root`
7. Пароль: тот, что сохранил

**Если спросит `Are you sure you want to continue connecting?` — напиши `yes` и Enter.**

Ты внутри сервера. Терминал покажет:
```
root@safemind-server:~#
```

---

## Шаг 4: Автоустановка SafeMind (10 минут)

Выполняй команды **по одной** прямо на сервере.

### 4.1 Обнови систему
```bash
apt update && apt upgrade -y
```

### 4.2 Запусти автоустановочный скрипт
```bash
curl -fsSL https://raw.githubusercontent.com/kimicito/safemind-landing/master/backend/install.sh | bash
```

Если curl из РФ не работает, используй:
```bash
wget https://raw.githubusercontent.com/kimicito/safemind-landing/master/backend/install.sh -O install.sh && bash install.sh
```

**Скрипт сделает всё автоматически:**
- ✅ Установит Python, PostgreSQL, Nginx
- ✅ Создаст базу данных
- ✅ Склонирует проект
- ✅ Установит Python-зависимости
- ✅ Создаст `.env` со случайным паролем
- ✅ Настроит systemd (автозапуск при загрузке)
- ✅ Настроит Nginx
- ✅ Откроет firewall
- ✅ Запустит backend

Жди 5-7 минут. В конце скрипт выведет:
- **ADMIN_TOKEN** — **обязательно сохрани!**
- IP сервера
- Полезные команды

### 4.3 Проверь что backend работает
```bash
curl http://localhost:8000/health
```

Должно вывести:
```json
{"status":"ok","email_provider":"unisender","email_configured":false}
```

`email_configured: false` — нормально, ключ Unisender ещё не вставлен.

---

## Шаг 5: Регистрация на Unisender (10 минут, параллельно)

1. Открой [unisender.com](https://unisender.com) в браузере
2. Нажми **«Регистрация»**
3. Введи email и пароль
4. Подтверди email (перейди по ссылке из письма)
5. Войди в личный кабинет
6. Перейди в раздел **«Настройки» → «API»**
7. Скопируй **API ключ** (вида `xxxxxxxxxxxxxxxxxxxx`)

---

## Шаг 6: Настройка .env и запуск (3 минуты)

На сервере выполни:

```bash
# Открой файл конфигурации
nano /opt/safemind/backend/.env
```

Файл выглядит так:
```
DATABASE_URL=postgresql://safemind:safemind_secure_pass_2026@localhost:5432/safemind
UNISENDER_API_KEY=YOUR_UNISENDER_KEY_HERE
FROM_EMAIL=hello@safemind.pro
ADMIN_TOKEN=abc123... (случайный)
FRONTEND_URL=https://safemind.pro
PORT=8000
EMAIL_PROVIDER=unisender
```

**Найди строку:**
```
UNISENDER_API_KEY=YOUR_UNISENDER_KEY_HERE
```

**Замени на свой ключ:**
```
UNISENDER_API_KEY=твой_ключ_от_unisender
```

Сохрани: **Ctrl+O** → Enter → **Ctrl+X**

Перезапусти backend:
```bash
systemctl restart safemind
```

Проверь снова:
```bash
curl http://localhost:8000/health
```

Теперь должно быть:
```json
{"status":"ok","email_provider":"unisender","email_configured":true}
```

Если `email_configured: true` — email рассылка работает!

---

## Шаг 7: Настройка домена (DNS)

1. Зайди в админку своего регистратора домена (где купил `safemind.pro`)
2. Найди раздел **DNS** или **Управление зоной**
3. Создай **A-запись**:
   - Имя: `@` (или `safemind.pro`)
   - Тип: `A`
   - Значение: **IP твоего сервера** (из шага 2.10)
   - TTL: 600
4. Сохрани
5. Подожди 5-15 минут (распространение DNS)

---

## Шаг 8: SSL (HTTPS) — бесплатно через Let's Encrypt (3 минуты)

На сервере:

```bash
# Установи Certbot
apt install -y certbot python3-certbot-nginx

# Получи сертификат
 certbot --nginx -d safemind.pro -d www.safemind.pro
```

Когда спросит email — введи свой.
Когда спросит согласие — нажми `Y` и Enter.

Проверь автообновление:
```bash
certbot renew --dry-run
```

---

## Шаг 9: Проверка работы (2 минуты)

Открой в браузере:

- **Health check:** `https://safemind.pro/health`
  - Должно показать: `{"status":"ok","email_provider":"unisender","email_configured":true}`

- **Фронтенд:** `https://safemind.pro` — твой лендинг

- **Админка (лиды):**
  ```bash
  curl -H "X-Admin-Token: ТВОЙ_ADMIN_TOKEN" https://safemind.pro/leads
  ```

---

## Шаг 10: Тестовая подписка (2 минуты)

1. Открой `https://safemind.pro`
2. Прокрути до формы «Бесплатный гид»
3. Введи свой email, выбери роль
4. Нажми «Получить гид»
5. Проверь почту — должен прийти welcome email с PDF

Если email пришёл — всё работает идеально.

---

## Полезные команды (сохрани себе)

```bash
# Подключиться к серверу
ssh root@ТВОЙ_IP

# Проверить статус backend
systemctl status safemind

# Посмотреть логи backend (в реальном времени)
journalctl -u safemind -f

# Перезапустить backend
systemctl restart safemind

# Обновить код из GitHub
cd /opt/safemind && git pull && systemctl restart safemind

# Проверить базу данных
sudo -u postgres psql safemind -c "SELECT COUNT(*) FROM leads;"

# Проверить Nginx
nginx -t && systemctl status nginx

# Обновить SSL
 certbot renew
```

---

## Если что-то пошло не так

**Backend не запускается:**
```bash
journalctl -u safemind -n 50 --no-pager
```
Пришли мне вывод — я разберу.

**Email не приходит:**
1. Проверь `UNISENDER_API_KEY` в `/opt/safemind/backend/.env`
2. Проверь статус: `curl https://safemind.pro/health`
3. Смотри логи: `journalctl -u safemind -f`, нажми «Получить гид» на сайте и смотри ошибки

**Сайт не открывается:**
1. Проверь DNS: `dig safemind.pro` (должен показать твой IP)
2. Проверь Nginx: `systemctl status nginx`
3. Проверь firewall: `ufw status`

**Забыл ADMIN_TOKEN:**
```bash
grep ADMIN_TOKEN /opt/safemind/backend/.env
```

---

## Что скинуть мне после установки

Когда всё заработает:
1. **ADMIN_TOKEN** (из вывода скрипта или из `.env`)
2. **IP сервера**
3. **Результат:** `curl https://safemind.pro/health`

Я проверю подключение к базе и начну работать с лидами. 🖤
