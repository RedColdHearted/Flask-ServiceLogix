# Используем базовый образ python
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    pkg-config \
    libpq-dev \
    build-essential \
    && apt-get clean

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt /app/

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию контейнера
COPY . /app/

# Устанавливаем переменные окружения для Flask
ENV PYTHONUNBUFFERED=1

# Открываем порт 5000 для доступа к приложению
# EXPOSE 5000

# Команда запускается при старте контейнера
CMD ["gunicorn", "app:create_app()"]