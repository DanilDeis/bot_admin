from dotenv import load_dotenv
import os
from aiogram import Bot

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
SECRET_KEY = os.getenv("SECRET_KEY")
BASE_URL = os.getenv("BASE_URL")

bot = Bot(token=TELEGRAM_BOT_TOKEN)