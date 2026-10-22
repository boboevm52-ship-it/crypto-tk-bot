import os, requests, threading, time
from flask import Flask
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    print("❌ BOT_TOKEN нест!")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

try:
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
    print("Webhook deleted OK")
    time.sleep(1)
except:
    pass

USD_TJS = 10.90
USD_RUB = 95.50
FIAT = {"USD":10.90,"EUR":11.85,"RUB":0.115,"GBP":12.34,"TRY":1.37,"CHF":11.17,"AED":2.51,"SAR":2.45,"INR":0.097,"KZT":0.022,"CNY":1.51,"KGS":0.124,"TMT":3.11,"UZS":0.000844}
CRYPTO = {"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","BNB":"binancecoin","XRP":"ripple","DOGE":"dogecoin","TON":"the-open-network","USDT":"tether","TRX":"tron","AVAX":"avalanche-2"}
NAMES = {"USD":"Доллар","EUR":"Евро","RUB":"Рубл","GBP":"Фунт","TRY":"Лира","CHF":"Франк","AED":"Дирхам","SAR":"Риял","INR":"Рупия","KZT":"Тенге","CNY":"Юан","KGS":"Сом","TMT":"Манат","UZS":"Сум"}

def footer(): return "\n\n━━━━━━━━━━━━━━\n🌐 cryptotj.tj\n💰 Ба сайти асли мо обуна шавед!"
def markup():
    m = telebot.types.InlineKeyboardMarkup(row_width=1)
    m.add(telebot.types.InlineKeyboardButton("💰 Ба канали мо обуна шавед", url="https://t.me/CryptoTj"), telebot.types.InlineKeyboardButton("🌐 cryptotj.tj", url="https://cryptotj.tj"))
    return m

@bot.message_handler(commands=['start'])
def start(message):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(telebot.types.KeyboardButton("BTC"), telebot.types.KeyboardButton("ETH"), telebot.types.KeyboardButton("SOL"))
    kb.add(telebot.types.KeyboardButton("BNB"), telebot.types.KeyboardButton("XRP"), telebot.types.KeyboardButton("DOGE"))
    kb.add(telebot.types.KeyboardButton("TON"), telebot.types.KeyboardButton("USDT"), telebot.types.KeyboardButton("TRX"))
    kb.add(telebot.types.KeyboardButton("AVAX"))
    kb.add(telebot.types.KeyboardButton("14 курс"), telebot.types.KeyboardButton("10 крипто"))
    kb.add(telebot.types.KeyboardButton("Биткоин чанд"))
    bot.send_message(message.chat.id, "✅ Бот тайёр!\nНавиш: Биткоин чанд, Эфир чанд, Доллар чанд", reply_markup=kb)

@bot.message_handler(content_types=['text'])
def all_text(message):
    txt = message.text.strip()
    up = txt.upper()
    low = txt.lower()

    if "биткоин" in low or "биткойн" in low or "btc" in low:
        up = "BTC"
    elif "эфир" in low or up == "ETH" or "eth" in low:
        up = "ETH"
    elif "сол" in low or up == "SOL":
        up = "SOL"
    elif "доги" in low or up == "DOGE":
        up = "DOGE"
    elif "бнб" in low or up == "BNB":
        up = "BNB"

    if "доллар" in low or up == "USD":
        up = "USD"
    elif "евро" in low or up == "EUR":
        up = "EUR"
    elif "рубл" in low or up == "RUB":
        up = "RUB"
    elif "сум" in low or up == "UZS" or "uzs" in low:
        up = "UZS"

    if up in FIAT:
        rate = FIAT[up]
        name = NAMES.get(up,"")
        if up == "UZS":
            msg = f"💰 {up} ({name}):\n• 1 = {rate:.5f} TJS\n• 1000 = {rate*1000:.2f} TJS{footer()}"
        else:
            msg = f"💰 1 {up} ({name}) = {rate:.4f} TJS{footer()}"
        bot.send_message(message.chat.id, msg, reply_markup=markup())
        return

    if up in CRYPTO:
        try:
            usd = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={CRYPTO[up]}&vs_currencies=usd", timeout=15).json()[CRYPTO[up]]['usd']
            msg = f"🟡 {up}:\n🟢 Доллар: {usd} $\n🔵 Рубл: {usd*USD_RUB:,.0f} RUB\n🔴 Сомонӣ: {usd*USD_TJS:,.0f} TJS{footer()}"
            bot.send_message(message.chat.id, msg, reply_markup=markup())
        except Exception as e:
            print(e)
        return

    if "курс" in low:
        full = "💱 14 КУРС:\n\n"
        for c,r in FIAT.items():
            full += f"• 1 {c} = {r:.4f} TJS\n"
        full += footer()
        bot.send_message(message.chat.id, full, reply_markup=markup())
        return

    if "крипто" in low:
        try:
            data = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(CRYPTO.values())}&vs_currencies=usd", timeout=15).json()
            full = "💰 10 КРИПТО:\n\n"
            for s,cid in CRYPTO.items():
                if cid in data:
                    full += f"• {s}: {data[cid]['usd']} $\n"
            full += footer()
            bot.send_message(message.chat.id, full, reply_markup=markup())
        except:
            pass
        return

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot Live!"

def run_bot():
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
