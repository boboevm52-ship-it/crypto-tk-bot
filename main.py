import telebot
import requests
import threading
from flask import Flask

BOT_TOKEN = "ТОКЕНАТРО ИН ҶО ГУЗОР"
bot = telebot.TeleBot(BOT_TOKEN)

USD_TJS = 10.90
USD_RUB = 95.50

FIAT = {
    "USD": 10.90, "EUR": 11.85, "RUB": 0.115, "GBP": 12.34,
    "TRY": 1.37, "CHF": 11.17, "AED": 2.51, "SAR": 2.45,
    "INR": 0.097, "KZT": 0.022, "CNY": 1.51, "KGS": 0.124,
    "TMT": 3.11, "UZS": 0.000844
}
CRYPTO = {
    "BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana",
    "BNB": "binancecoin", "XRP": "ripple", "DOGE": "dogecoin",
    "TON": "the-open-network", "USDT": "tether",
    "TRX": "tron", "AVAX": "avalanche-2"
}
NAMES = {
    "USD":"Доллар","EUR":"Евро","RUB":"Рубл","GBP":"Фунт",
    "TRY":"Лира","CHF":"Франк","AED":"Дирхам","SAR":"Риял",
    "INR":"Рупия","KZT":"Тенге","CNY":"Юан","KGS":"Сом","TMT":"Манат","UZS":"Сум"
}

def footer():
    return "\n\n━━━━━━━━━━━━━━\n🌐 cryptotj.tj\n💰 Ба сайти асли мо обуна шавед!"
def markup():
    m = telebot.types.InlineKeyboardMarkup(row_width=1)
    m.add(
        telebot.types.InlineKeyboardButton("💰 Сомони асли - мо обуна шавед", url="https://t.me/CryptoTj"),
        telebot.types.InlineKeyboardButton("🌐 Ба сайти асли мо", url="https://cryptotj.tj")
    )
    return m

@bot.message_handler(commands=['start'])
def start(message):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(telebot.types.KeyboardButton("BTC"), telebot.types.KeyboardButton("ETH"), telebot.types.KeyboardButton("SOL"))
    kb.add(telebot.types.KeyboardButton("BNB"), telebot.types.KeyboardButton("XRP"), telebot.types.KeyboardButton("DOGE"))
    kb.add(telebot.types.KeyboardButton("TON"), telebot.types.KeyboardButton("USDT"), telebot.types.KeyboardButton("TRX"))
    kb.add(telebot.types.KeyboardButton("AVAX"))
    kb.add(telebot.types.KeyboardButton("14 курс"), telebot.types.KeyboardButton("10 крипто"))
    kb.add(telebot.types.KeyboardButton("Сум чанд"))
    bot.send_message(message.chat.id, "✅ Бот тайёр!\n10 крипто + 14 курс", reply_markup=kb)

@bot.message_handler(content_types=['text'])
def all_text(message):
    txt = message.text.strip()
    up = txt.upper()
    if up in FIAT:
        rate = FIAT[up]
        name = NAMES.get(up, "")
        if up == "UZS":
            msg = f"💰 {up} ({name}):\n• 1 UZS = {rate:.5f} TJS\n• 1000 UZS = {rate*1000:.2f} TJS{footer()}"
        else:
            msg = f"💰 1 {up} ({name}) = {rate:.4f} TJS{footer()}"
        bot.send_message(message.chat.id, msg, reply_markup=markup())
        return
    if up in CRYPTO:
        try:
            cid = CRYPTO[up]
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd"
            usd = requests.get(url, timeout=15).json()[cid]['usd']
            tjs = usd * USD_TJS
            rub = usd * USD_RUB
            msg = f"🟡 {up}:\n🟢 Доллар: {usd} $\n🔵 Рубл: {rub:,.0f} RUB\n🔴 Сомонӣ: {tjs:,.0f} TJS{footer()}"
            bot.send_message(message.chat.id, msg, reply_markup=markup())
        except:
            bot.send_message(message.chat.id, "API банд")
        return
    if "14 курс" in txt.lower():
        full = "💱 14 КУРС:\n\n"
        for code, rate in FIAT.items():
            name = NAMES.get(code, "")
            if code == "UZS":
                full += f"• 1 UZS ({name}) = {rate:.5f} TJS\n  1000 UZS = {rate*1000:.2f} TJS\n"
            else:
                full += f"• 1 {code} ({name}) = {rate:.4f} TJS\n"
        full += footer()
        bot.send_message(message.chat.id, full, reply_markup=markup())
        return
    if "10 крипто" in txt.lower():
        try:
            ids = ",".join(CRYPTO.values())
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
            data = requests.get(url, timeout=15).json()
            full = "💰 10 КРИПТО:\n\n"
            for sym, cid in CRYPTO.items():
                if cid in data:
                    full += f"• {sym}: {data[cid]['usd']} $\n"
            full += footer()
            bot.send_message(message.chat.id, full, reply_markup=markup())
        except:
            bot.send_message(message.chat.id, "API банд")

# ===== ВЕБ-СЕРВЕР БАРОИ RENDER =====
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live! 10 crypto + 14 kurs"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
