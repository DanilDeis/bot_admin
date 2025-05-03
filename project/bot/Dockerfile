FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY common/ ./common/
#COPY .env .env
COPY bot/ ./bot/
CMD ["python3", "-m", "bot.admin"]