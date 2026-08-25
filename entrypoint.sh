#!/bin/sh
set -e

echo "Waiting for DB..."
# Простая проверка, что порт БД открыт (можно усложнить, если нужно)
until pg_isready -h "${HOST:-db}" -p 5432 -U "${USERNAME}" -d "${NAMEDB}" > /dev/null 2>&1; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "PostgreSQL is up!"

# Применяем миграции
echo "Running migrations..."
poetry run python manage.py migrate --noinput

# Опционально: collectstatic (если не делаешь это отдельным шагом в CI)
# poetry run python manage.py collectstatic --noinput --clear

# Запускаем Gunicorn (или то, что передано в CMD)
echo "Starting Gunicorn..."
exec "$@"
