import os
import threading
from flask import Flask
import telebot
import requests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=False)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is Live!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Bot kor mekunad! /price btc")

@bot.message_handler(commands=['price'])
def price_cmd(message):
    try:
        parts = message.text.split()
        coin = "bitcoin"
        if len(parts) > 1:
            c = parts[1].lower()
            if c == "btc": c = "bitcoin"
            if c == "eth": c = "ethereum"
            coin = c
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd", timeout=10)
        j = r.json()
        if coin in j:
            bot.reply_to(message, f"{coin}: ${j[coin]['usd']}")
        else:
            bot.reply_to(message, "Coin yoft nashud")
    except Exception as e:
        bot.reply_to(message, f"Xato: {e}")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
