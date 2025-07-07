FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_NO_CACHE=1 UV_PYTHON_DOWNLOADS=0 UV_LINK_MODE=copy

# Устанавливаем необходимые утилиты
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv sync --frozen

# Копируем приложение
COPY auth_service/ ./auth_service/

# Копируем скрипт запуска
COPY auth_service/entrypoint.sh auth_service/entrypoint.sh
RUN chmod +x auth_service/entrypoint.sh

EXPOSE 8000

# Используем скрипт запуска в качестве точки входа
CMD ["auth_service/entrypoint.sh"]
