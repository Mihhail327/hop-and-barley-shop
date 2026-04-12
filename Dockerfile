FROM python:3.13-slim

# Устанавливаем переменные окружения, чтобы Python не кешировал байт-код и сразу выводил логи
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Настройка Poetry: не создавать venv внутри контейнера
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем только файлы зависимостей, чтобы Docker кешировал этот слой
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости без dev-пакетов (оптимизация образа)
RUN poetry install --no-interaction --no-ansi --no-root

# Копируем остальной код проекта
COPY . /app/

# Открываем порт (стандартный для Django)
EXPOSE 8000

# Команда для запуска (используем manage.py для начала)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]