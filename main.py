import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is running! Bot kor mekunad!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! 👋\n\n"
        "Crypto Bot tayyor!\n\n"
        "/btc - Narxi Bitcoin\n"
        "/eth - Narxi Ethereum\n"
        "/price - Hama narxho"
    )

async def btc_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=10)
        price = r.json()['bitcoin']['usd']
        await update.message.reply_text(f"₿ BTC: ${price} dollar")
    except:
        await update.message.reply_text("Xato: Narx girifta nashud!")

async def eth_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd", timeout=10)
        price = r.json()['ethereum']['usd']
        await update.message.reply_text(f"♦ ETH: ${price} dollar")
    except:
        await update.message.reply_text("Xato!")

async def all_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        data = r.json()
        btc = data['bitcoin']['usd']
        eth = data['ethereum']['usd']
        await update.message.reply_text(f"₿ BTC: ${btc}\n♦ ETH: ${eth}")
    except:
        await update.message.reply_text("Xato!")

if __name__ == "__main__":
    # Flask-ro dar thread-i alohida sari kun - IN MUHIM AST!
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Telegram bot-ro sari kun
    print("Bot starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc_price))
    app.add_handler(CommandHandler("eth", eth_price))
    app.add_handler(CommandHandler("price", all_price))
    print("Bot polling started!")
    app.run_polling()
