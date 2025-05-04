FROM python:3.11-slim

WORKDIR /app

# Копируем requirements.txt из папки project
COPY project/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем папку common из project
COPY project/common/ ./common/

# Копируем папку flask_webhook из project
COPY project/flask_webhook/ ./flask_webhook/

# Копируем файл users.db из project
COPY project/users.db /app/users.db

CMD ["gunicorn", "flask_webhook.webhook_prodamus:app", "-b", "0.0.0.0:8000", "-t", "120", "--access-logfile", "-", "--error-logfile", "-"]