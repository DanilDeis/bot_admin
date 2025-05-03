from common.database import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from common.config import ADMIN_CHAT_ID, bot


scheduler = AsyncIOScheduler(timezone="UTC")


async def daily_cleanup():
    print("⏰ [DEBUG] Задача очистки запущена")
    expired_count = db.remove_expired_users()
    print(f"✅ [DEBUG] Удалено пользователей: {expired_count}")

    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"Ежедневная очистка: удалено {expired_count} пользователей"
        )
    except Exception as e:
        print(f"🚨 [DEBUG] Ошибка отправки сообщения: {e}")

# Настройка расписания
def schedule_jobs():
    scheduler.add_job(daily_cleanup, 'interval',  days=30)
async def on_startup():
    schedule_jobs()
    scheduler.start()