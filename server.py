from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.errors import PeerIdInvalidError
import asyncio
import random

# Учетные данные для Telethon
api_id = 21814411  # Замените на ваш API ID
api_hash = '7af506bc5633b7dc324b539ee4f97f1b'  # Замените на ваш API Hash

# Flask-приложение
app = Flask(__name__)

# Хранилище кодов подтверждения
verification_codes = {}

# Создаем клиент Telethon
client = TelegramClient('session_name', api_id, api_hash)

@app.route('/send_code', methods=['POST'])
def send_code():
    data = request.json
    phone = data.get('phone')  # Номер телефона пользователя

    if not phone:
        return jsonify({"status": "Ошибка", "message": "Номер телефона обязателен"}), 400

    # Генерация кода подтверждения
    code = random.randint(1000, 9999)
    verification_codes[phone] = code

    try:
        # Асинхронный вызов через asyncio
        asyncio.run(send_telegram_message(phone, code))
        return jsonify({"status": "Код отправлен"})
    except PeerIdInvalidError:
        return jsonify({"status": "Ошибка", "message": "Пользователь с таким номером телефона не найден в Telegram"}), 400
    except Exception as e:
        return jsonify({"status": "Ошибка", "message": str(e)}), 500

async def send_telegram_message(phone, code):
    # Отправка сообщения через Telethon
    async with client:
        user = await client.get_entity(phone)
        await client.send_message(user, f"Ваш код подтверждения: {code}")

@app.route('/verify_code', methods=['POST'])
def verify_code():
    data = request.json
    phone = data.get('phone')
    input_code = data.get('code')

    if not phone or not input_code:
        return jsonify({"status": "Ошибка", "message": "Телефон и код обязательны"}), 400

    # Проверка кода
    if verification_codes.get(phone) == int(input_code):
        return jsonify({"status": "Verified"})
    else:
        return jsonify({"status": "Invalid code"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
