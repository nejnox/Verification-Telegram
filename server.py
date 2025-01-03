from flask import Flask, request, jsonify
import telebot
import random

# Flask-приложение и Telegram-бот
app = Flask(__name__)
bot = telebot.TeleBot("7399305399:AAFceK2YHpwTRZsbZsuQjC7x7jZWwQeN47U")  # Вставьте токен бота

# Хранилище кодов
verification_codes = {}

@app.route('/send_code', methods=['POST'])
def send_code():
    data = request.json
    phone = data['phone']
    telegram_username = data['telegram_username']

    code = random.randint(1000, 9999)
    verification_codes[phone] = code

    try:
        bot.send_message(f"@{telegram_username}", f"Ваш код подтверждения: {code}")
        return jsonify({"status": "Код отправлен"})
    except Exception as e:
        return jsonify({"status": "Ошибка", "message": str(e)}), 400

@app.route('/verify_code', methods=['POST'])
def verify_code():
    data = request.json
    phone = data['phone']
    input_code = int(data['code'])

    if verification_codes.get(phone) == input_code:
        return jsonify({"status": "Verified"})
    else:
        return jsonify({"status": "Invalid code"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)