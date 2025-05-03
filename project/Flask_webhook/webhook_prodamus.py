from flask import Flask, request, jsonify
import requests
from common.database import db
from datetime import datetime
import re
from common.config import TELEGRAM_BOT_TOKEN, CHANNEL_ID, SECRET_KEY
from bot.admin import get_invite_link_sync
import time

app = Flask(__name__)

SECRET_KEY_1 = SECRET_KEY.encode('utf-8')

def send_telegram_message(chat_id, text, parse_mode=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text,
    }
    if parse_mode:
        params["parse_mode"] = parse_mode
    response = requests.post(url, params=params)
    return response.json()


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.form.to_dict()
    print("Полученные данные:", data)  # Для отладки
    phone = data.get("customer_phone")
    print("Номер телефона из продамуса", phone)
    if not phone:
        return jsonify({"status": "error", "message": "Не указан номер телефона"}), 400

    phone = re.sub(r'[^0-9]', '', phone)
    phone = phone[-10:]
    amount_str = data.get("sum")
    try:
        amount = float(amount_str)
    except (TypeError, ValueError):
        amount = None

    chat_id = db.get_chat_id_by_phone(phone)
    phone_1 = db.get_phone_by_id(chat_id)
    print("Номер телефона из базы данных", phone_1)

    if chat_id and amount is not None and data.get("payment_status") == "success":
        db.set_join_date(chat_id, datetime.now())
        user_name = get_username(chat_id, TELEGRAM_BOT_TOKEN)
        process_payment(chat_id, user_name)
        send_telegram_message(
            chat_id=chat_id,
            text="Спасибо за покупку! Ваш аккаунт активирован."
        )
    else:
        print("Пользователь с этим телефоном не найден или сумма не указана.")
    return jsonify({"status": "ok"})




def send_telegram_notification(chat_id: str, message: str):
    """Отправка сообщения в Telegram пользователю"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    print(f"Отправляю сообщение пользователю {chat_id}")
    try:
        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            },
            timeout=5
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False

def get_username(chat_id, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getChat"
    resp = requests.get(url, params={"chat_id": chat_id}).json()
    if resp.get("ok"):
        user = resp["result"]
        username = user.get("username")
        if username:
            return f"@{username}"
        else:
            return f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    return "Пользователь"
def process_payment(chat_id: int, user_name: str):
    # Устанавливаем срок действия ссылки: 15 секунд от текущего времени
    expire_date = int(time.time()) + 365
    # Ограничиваем ссылку одним пользователем
    invite_link = get_invite_link_sync(
        TELEGRAM_BOT_TOKEN,
        CHANNEL_ID,
        user_name,
        limit=1,
        expire_date=expire_date
    )
    print(invite_link)
    if not invite_link:
        send_telegram_message(chat_id, "Не удалось создать ссылку на канал. Обратитесь к администратору.")
        return
    message = f"""💳 <b>Платеж успешен!</b>
👤 Пользователь: {user_name}
<a href="{invite_link}">Вступить в закрытый канал</a>"""
    send_telegram_message(chat_id, message, parse_mode="HTML")




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
