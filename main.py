import telebot, os, threading, requests
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN", "123456:ABC") # ТОКЕНАТРО ДАР RENDER ГУЗОР
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

FIAT = {
    "USD": [9.15, 9.25, "💵 Доллар"],
    "RUB": [0.1126, 0.1146, "🇷🇺 Рубл"],
    "EUR": [10.22, 10.42, "🇪🇺 Евро"],
    "CNY": [1.25, 1.29, "🇨🇳 Юан"],
    "GBP": [11.80, 12.10, "🇬🇧 Фунт"],
    "KZT": [0.018, 0.020, "🇰🇿 Тенге"],
    "TRY": [0.25, 0.28, "🇹🇷 Лира"],
    "UZS": [0.0007, 0.0008, "🇺🇿 Сум"],
    "KGS": [0.10, 0.11, "🇰🇬 Сом"],
    "AED": [2.48, 2.52, "🇦🇪 Дирхам"],
}
AD = "\n\n🌍 13 LIVE: https://cryptotj-dushanbe.blogspot.com/\n📢 @CryptoTjDushanbe"

@app.route('/')
def home(): return "OK"

def kb():
    m = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    m.add("🌍 13 LIVE","💵 Доллар","🇷🇺 Рубл","🇪🇺 Евро","🇨🇳 Юан","🇬🇧 Фунт","🇰🇿 Тенге","🇹🇷 Лира","🇺🇿 Сум","🇰🇬 Сом","🇦🇪 Дирхам","₿ BTC","🌐 ETH","💎 TON","☀️ SOL","🐶 DOGE","💧 XRP","🟡 BNB","🔴 TRX","💲 USDT","🟣 PI")
    return m

def price(sym):
    try:
        ids={"BTC":"bitcoin","ETH":"ethereum","TON":"the-open-network","SOL":"solana","DOGE":"dogecoin","XRP":"ripple","BNB":"binancecoin","TRX":"tron","USDT":"tether","PI":"pi-network"}
        r=requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids[sym]}&vs_currencies=usd", timeout=5).json()
        return r[ids[sym]]['usd']
    except: return "дастрас нест"

@bot.message_handler(commands=['start'])
def s(m): bot.send_message(m.chat.id, f"👋 CryptoTj 10+10\n\n💵 9.25\n🇷🇺 0.1146 = 1000=114.6\n🇪🇺 10.42{AD}", reply_markup=kb())

@bot.message_handler(func=lambda x: True)
def all(m):
    t=m.text
    for k,v in FIAT.items():
        if v[2].split()[1] in t or k in t:
            extra = "\n🔴 1000 = 114.6 TJS" if k=="RUB" else ""
            bot.send_message(m.chat.id, f"{v[2]}\nХарид: {v[0]}\nФурӯш: {v[1]}{extra}{AD}", reply_markup=kb())
            return
    if "LIVE" in t:
        bot.send_message(m.chat.id, f"🌍 LIVE: https://cryptotj-dushanbe.blogspot.com/{AD}", reply_markup=kb())
        return
    for s_name in ["BTC","ETH","TON","SOL","DOGE","XRP","BNB","TRX","USDT","PI"]:
        if s_name in t:
            bot.send_message(m.chat.id, f"₿ {s_name}: ${price(s_name)}{AD}", reply_markup=kb())
            return

threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000))), daemon=True).start()
while True:
    try: bot.infinity_polling()
    except: continue
