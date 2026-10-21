
import os
import requests
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- 1. САЙТ БАРОИ РЕКЛАМА ---
SITE_URL = "https://cryptotj-dushanbe.blogspot.com"
CHANNEL_URL = "https://t.me/tjikiston" # Агар канал надорӣ, ҳаминро ҳам SITE_URL кун

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Alive! ✅"

def get_rates():
    try:
        # Курси воқеӣ
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()
        usd_tjs = r['rates']['TJS']
        rub_tjs = r['rates']['TJS'] / r['rates']['RUB']
        return usd_tjs, rub_tjs
    except:
        return 10.9, 0.112  # Агар интернет набошад

def promo_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌐 Сомонаро кушо - Курси пурра", url=SITE_URL)],
        [InlineKeyboardButton("📢 Канал - Хабарҳои фаврӣ", url=CHANNEL_URL)]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usd, rub = get_rates()
    text = (
        f"Салом! 👋\n\n"
        f"💵 1 USD = {usd:.3f} TJS\n"
        f"💵 1 RUB = {rub:.3f} TJS\n\n"
        f"Навиш: Рубл чанд? / Доллар чанд?"
    )
    await update.message.reply_text(text, reply_markup=promo_keyboard())

async def kurs_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()
    usd, rub = get_rates()
    
    if "рубл" in msg or "rub" in msg or "/kurs" in msg:
        text = f"💰 КУРСИ РУБЛ\n\n💵 1 RUB = {rub:.4f} TJS\n💵 1000 RUB = {rub*1000:.2f} TJS\n\n📅 Имрӯз"
    elif "доллар" in msg or "доллар" in msg or "usd" in msg:
        text = f"💰 КУРСИ ДОЛЛАР\n\n💵 1 USD = {usd:.3f} TJS\n\n📅 Имрӯз"
    else:
        text = f"💱 КУРСИ АРЗ\n\n💵 1 USD = {usd:.3f} TJS\n💵 1 RUB = {rub:.4f} TJS"

    await update.message.reply_text(text, reply_markup=promo_keyboard())

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("kurs", kurs_handler))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kurs_handler))
    
    print("Бот оғоз шуд...")
    app_bot.run_polling()
