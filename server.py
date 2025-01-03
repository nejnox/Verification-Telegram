from flask import Flask, request, jsonify
from telethon import TelegramClient, errors
import asyncio
import random

# Учетные данные для Telethon
api_id = 21814411  # Ваш API ID
api_hash = '7af506bc5633b7dc324b539ee4f97f1b'  # Ваш API Hash
phone_number = '+447405085904'  # Ваш номер телефона (без пробелов)

# Flask-приложение
app = Flask(__name__)

# Хранилище кодов подтверждения
verification_codes = {}

# Инициализация Telethon клиента
client = TelegramClient('user_session', api_id, api_hash)

async def start_client():
    if not await client.is_user_authorized():
        await client.start(phone=phone_number)

# Инициализируем клиент при запуске
asyncio.run(start_client())

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
        # Отправка сообщения
        asyncio.run(send_message(phone, code))
        return jsonify({"status": "Код отправлен"})
    except Exception as e:
        return jsonify({"status": "Ошибка", "message": str(e)}), 500

async def send_message(phone, code):
    try:
        user = await client.get_entity(phone)
        await client.send_message(user, f"Ваш код подтверждения: {code}")
    except errors.FloodWaitError as e:
        raise Exception(f"Слишком много запросов. Подождите {e.seconds} секунд.")
    except errors.UserPrivacyRestrictedError:
        raise Exception("Пользователь ограничил получение сообщений.")
    except errors.PeerIdInvalidError:
        raise Exception("Неверный идентификатор пользователя.")
    except Exception as e:
        raise Exception(f"Ошибка: {e}")

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
