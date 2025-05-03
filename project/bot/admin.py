import asyncio
import contextlib
from aiogram.types import ChatJoinRequest, ChatMemberUpdated
from aiogram import Dispatcher, F
import logging
import datetime
from aiogram.filters import Command
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram import types
from datetime import datetime
from common.database import Database
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton
import re
from dotenv import load_dotenv
from .scedule import on_startup
from common.config import CHANNEL_ID, ADMIN_CHAT_ID,BASE_URL, bot

load_dotenv()


db = Database('users.db')
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Поделиться номером телефона", request_contact=True)]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Для продолжения работы с ботом и подписки в закрытом канале, поделитесь своим номером телефона:",
        reply_markup=markup
    )

@dp.message(F.contact)
async def handle_contact(message: types.Message):
    # Сохраняем данные
    user_id = message.from_user.id
    phone = message.contact.phone_number
    phone = re.sub(r'[^0-9]', '', phone)
    phone = phone[-10:]
    print(phone)
    first_name = message.from_user.first_name
    username = message.from_user.username
    db.add_user(user_id, username, first_name, phone, None)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оплатить через Prodamus", url=BASE_URL)]
        ]
    )
    await message.answer("Спасибо! Ваш номер сохранён. Оплатите подписку:", reply_markup=markup)

@dp.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def handle_left_member(event: ChatMemberUpdated):
    """Обработчик выхода из канала"""
    if event.chat.id == CHANNEL_ID:
        user = event.old_chat_member.user
        try:
            db.remove_user_by_id(user.id)
            logging.info(f"🗑️ Пользователь {user.id} удален из БД")
        except Exception as e:
            logging.error(f"❌ Ошибка удаления пользователя {user.id}: {e}")
            await bot.send_message(ADMIN_CHAT_ID, f"Ошибка удаления {user.id}")

@dp.chat_join_request(F.chat.id == CHANNEL_ID)
async def approve_request(chat_join: ChatJoinRequest):
    try:
        await chat_join.approve()
        db.add_user(  # Убрали await
            user_id=chat_join.from_user.id,
            username=chat_join.from_user.username,
            first_name=chat_join.from_user.first_name,
            join_date=datetime.datetime.now()
        )

        member = await bot.get_chat_member(CHANNEL_ID, chat_join.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            try:
                await bot.send_message(
                    chat_id=chat_join.from_user.id,
                    text="Рад тебя приветствовать на своём канале!"
                )
            except Exception as e:
                logging.error(f"Не удалось отправить сообщение: {e}")
                await bot.send_message(ADMIN_CHAT_ID, f"Ошибка приветствия для {chat_join.from_user.id}")
    except Exception as e:
        error_msg = f"Ошибка обработки заявки {chat_join.from_user.id}: {str(e)}"
        logging.error(error_msg, exc_info=True)
        await bot.send_message(ADMIN_CHAT_ID, error_msg)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()
    await dp.start_polling(bot)




if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
