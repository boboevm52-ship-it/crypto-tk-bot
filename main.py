import os, threading, requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Bot Running"

def run_flask():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

async def start(update, context):
    await update.message.reply_text("👋 Салом! /btc /price /eth")

async def btc(update, context):
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
        await update.message.reply_text(f"BTC: ${r['bitcoin']['usd']:,}")
    except: await update.message.reply_text("Хато")

async def price(update, context):
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,toncoin&vs_currencies=usd").json()
        await update.message.reply_text(f"BTC: ${r['bitcoin']['usd']:,}\nETH: ${r['ethereum']['usd']:,}\nTON: ${r['toncoin']['usd']:,}")
    except: await update.message.reply_text("Хато")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("eth", btc))
    app.run_polling()
