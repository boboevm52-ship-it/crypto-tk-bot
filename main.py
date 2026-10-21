import os
import requests
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

SITE_URL = "https://cryptotj-dushanbe.blogspot.com"
TOKEN = os.getenv("BOT_TOKEN")

# --- Веб барои Render ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot Alive - Точики Трейд"

def get_rates():
    try:
        data = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=15).json()
        usd = data['rates']['TJS']
        rub = data['rates']['TJS'] / data['rates']['RUB']
        return usd, rub
    except Exception as e:
        print(f"Rate error: {e}")
        return 10.92, 0.115

def promo_keyboard():
    kb = [
        [InlineKeyboardButton("🌐 Сомона - Курси пурра", url=SITE_URL)],
        [InlineKeyboardButton("📢 Обунашав", url=SITE_URL)]
    ]
    return InlineKeyboardMarkup(kb)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usd, rub = get_rates()
    txt = f"Салом! 👋\n\n💵 1 USD = {usd:.2f} TJS\n💵 1 RUB = {rub:.3f} TJS\n\nНавис: Рубл чанд?"
    await update.message.reply_text(txt, reply_markup=promo_keyboard())

async def kurs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usd, rub = get_rates()
    txt = f"💱 КУРС ИМРУЗ\n\n💵 1 USD = {usd:.3f} TJS\n💵 1 RUB = {rub:.4f} TJS\n💵 1000 RUB = {rub*1000:.1f} TJS"
    await update.message.reply_text(txt, reply_markup=promo_keyboard())

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    if not TOKEN:
        print("ХАТО: BOT_TOKEN нест!")
    else:
        Thread(target=run_flask, daemon=True).start()
        print("Бот сар шуд...")
        bot_app = ApplicationBuilder().token(TOKEN).build()
        bot_app.add_handler(CommandHandler("start", start))
        bot_app.add_handler(CommandHandler("kurs", kurs))
        bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kurs))
        bot_app.run_polling()
