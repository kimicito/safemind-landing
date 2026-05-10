#!/bin/bash
# deploy.sh — быстрый деплой SafeMind на сервер
# Использование: ./deploy.sh user@server /var/www/safemind/

SERVER=${1:-"root@85.239.59.8"}
REMOTE_DIR=${2:-"/var/www/safemind/"}

echo "🚀 Деплой SafeMind на $SERVER:$REMOTE_DIR"

# Создаём архив с новыми файлами
cd /root/.openclaw/workspace/safemind
tar -czf /tmp/safemind-update.tar.gz \
  ru/matrix.html \
  ru/diagnostic.html \
  ru/support.html \
  ru/index.html \
  data/ai-matrix-ru.json \
  assets/style.css \
  index.html \
  CNAME

# Копируем на сервер
scp /tmp/safemind-update.tar.gz $SERVER:/tmp/

# Распаковываем на сервере
ssh $SERVER "
  cd $REMOTE_DIR
  tar -xzf /tmp/safemind-update.tar.gz
  chown -R www-data:www-data .
  echo '✅ Деплой завершён'
"

echo "🎉 Готово! Проверь: http://safemind.pro/ru/matrix.html"