import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

TOKEN = os.getenv("BOT_TOKEN")
print(f"Token exists: {bool(TOKEN)}")

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is Live!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Bot kor mekunad! 🚀\n/price btc - narx")

async def price_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = "bitcoin"
    if context.args:
        coin = context.args[0].lower()
        if coin == "btc":
            coin = "bitcoin"
        if coin == "eth":
            coin = "ethereum"
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        j = r.json()
        if coin in j:
            await update.message.reply_text(f"{coin.upper()}: ${j[coin]['usd']}")
        else:
            await update.message.reply_text("Coin yoft nashud. /price btc")
    except Exception as e:
        await update.message.reply_text(f"Xato: {e}")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

def run_bot():
    print("Bot starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price_cmd))
    print("Bot polling started!")
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
