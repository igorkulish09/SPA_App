FROM python:3.11

# Встановлюємо залежності
RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev \
    gcc

# Створюємо та встановлюємо файли залежностей
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо усі файли Django-проекту до контейнера
COPY . /app/

# Запускаємо міграції та створюємо суперпользователя
RUN python manage.py migrate
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin3', 'admin3@example.com', 'admin')" | python manage.py shell

# Відкриваємо порт для зовнішніх з'єднань
EXPOSE 8000

# Запускаємо Django-додаток при старті контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
