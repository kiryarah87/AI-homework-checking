#!/bin/sh
set -e

# Ожидаем доступности базы данных
echo "Waiting for PostgreSQL..."
while ! nc -z $DBHOST $DBPORT; do
  sleep 0.5
done
echo "PostgreSQL started"

# Применяем миграции
echo "Running migrations..."
cd /app/auth_service
uv run alembic upgrade head

# Запускаем приложение
echo "Starting application..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
