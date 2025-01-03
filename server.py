from flask import Flask, request, jsonify
import telebot
import random

# Flask-приложение и Telegram-бот
app = Flask(__name__)
bot = telebot.TeleBot("7399305399:AAFceK2YHpwTRZsbZsuQjC7x7jZWwQeN47U")  # Замените ВАШ_API_ТОКЕН на токен вашего бота

# Хранилище кодов подтверждения
verification_codes = {}

@app.route('/send_code', methods=['POST'])
def send_code():
    # Получение данных из запроса
    data = request.json
    phone = data.get('phone')
    telegram_username = data.get('telegram_username')

    # Проверка на наличие обязательных параметров
    if not phone or not telegram_username:
        return jsonify({"status": "Ошибка", "message": "Телефон и Telegram username обязательны"}), 400

    # Генерация случайного кода
    code = random.randint(1000, 9999)
    verification_codes[phone] = code

    # Отправка кода через Telegram-бота
    try:
        bot.send_message(f"@{telegram_username}", f"Ваш код подтверждения: {code}")
        return jsonify({"status": "Код отправлен"})
    except telebot.apihelper.ApiTelegramException as e:
        return jsonify({"status": "Ошибка", "message": f"Telegram error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"status": "Ошибка", "message": str(e)}), 500

@app.route('/verify_code', methods=['POST'])
def verify_code():
    # Получение данных из запроса
    data = request.json
    phone = data.get('phone')
    input_code = data.get('code')

    # Проверка на наличие обязательных параметров
    if not phone or not input_code:
        return jsonify({"status": "Ошибка", "message": "Телефон и код обязательны"}), 400

    # Проверка кода подтверждения
    if verification_codes.get(phone) == int(input_code):
        return jsonify({"status": "Verified"})
    else:
        return jsonify({"status": "Invalid code"}), 400

# Запуск Flask-приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
