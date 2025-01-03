from flask import Flask, request, jsonify
import telebot
import random

# Учетные данные вашего Telegram-бота
bot_token = "7399305399:AAFceK2YHpwTRZsbZsuQjC7x7jZWwQeN47U"  # Замените на ваш API токен
bot = telebot.TeleBot(bot_token)

# Flask-приложение
app = Flask(__name__)

# Хранилище кодов подтверждения
verification_codes = {}

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
        # Отправка сообщения с кодом подтверждения
        bot.send_message(phone, f"Ваш код подтверждения: {code}")
        return jsonify({"status": "Код отправлен"})
    except Exception as e:
        return jsonify({"status": "Ошибка", "message": str(e)}), 500

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
