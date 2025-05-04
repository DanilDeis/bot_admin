FROM python:3.11

WORKDIR /app

COPY project/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY project/common/ ./common/
COPY project/users.db /app/users.db
COPY project/bot/ ./bot/
CMD ["python3", "-m", "bot.admin"]