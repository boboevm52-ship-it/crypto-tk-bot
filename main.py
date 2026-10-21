import os
import threading
import time
from flask import Flask
import telebot
import requests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=False)

# Ин хатои 409-ро нест мекунад
bot.remove_webhook()
time.sleep(1)

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is alive!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Салом! 👋 Боти крипто кор мекунад!\nНавиш: /price bitcoin")

@bot.message_handler(commands=['price'])
def price(message):
    try:
        parts = message.text.split()
        coin = parts[1] if len(parts) > 1 else "bitcoin"
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        r = requests.get(url, timeout=10).json()
        if coin in r:
            bot.reply_to(message, f"💰 {coin}: ${r[coin]['usd']}")
        else:
            bot.reply_to(message, "Коин ёфт нашуд. Мисол: /price bitcoin")
    except Exception as e:
        bot.reply_to(message, f"Хато: {e}")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
