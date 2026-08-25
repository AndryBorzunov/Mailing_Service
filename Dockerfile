FROM python:3.12-slim

WORKDIR /app

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     curl \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# Устанавливаем системные зависимости (часто нужны для сборки Python-расширений)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \  # если используете PostgreSQL
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Копируем фалы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости. Для продакшена используем `--no-dev`, чтобы не тащить инструменты разработки
RUN poetry install --no-dev

# Создаем venv внутри образа и ставим зависимости (без dev дл production-образа)
# RUN poetry config virtualenvs.create false \
#     && poetry install --no-root

# Копируем остальной код проекта
COPY . /app

# Копируем весь код
# COPY .

# Настраиваем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Точка входа (entrypoint.sh) — скрипт, который определит, что запускать
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Определяем точку входа для контейнера
ENTRYPOINT ["/app/entrypoint.sh"].

# Открываем порт дл Django
# EXPOSE 8000
#
# CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi.application --bind 0.0.0.0:8000"]
