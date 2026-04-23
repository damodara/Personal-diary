# Используем официальный образ Python
FROM python:3.14-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]