FROM python:3.12-slim

WORKDIR /app

RUN pt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Копируем фалы зависимостей
COPY pyproject.toml poetry.lock ./

# Создаем venv внутри образа и ставим зависимости (без dev дл production-образа)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Копируем весь код
COPY . .

# Открываем порт дл Django
EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi.application --bind 0.0.0.0:8000"]
