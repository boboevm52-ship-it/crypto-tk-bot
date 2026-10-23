import telebot, os, threading, requests
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN", "ТОКЕНАТРО_ИНҶО_ГУЗОР")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ===== 10 КУРСИ ФИЛЬТР - ЭСХАТА 23.10.2026 =====
FIAT = {
    "USD": {"buy": 9.15, "sell": 9.25, "flag": "💵"},
    "EUR": {"buy": 10.22, "sell": 10.42, "flag": "🇪🇺"},
    "RUB": {"buy": 0.1126, "sell": 0.1146, "flag": "🇷🇺"},
    "CNY": {"buy": 1.25, "sell": 1.29, "flag": "🇨🇳"},
    "GBP": {"buy": 11.80, "sell": 12.10, "flag": "🇬🇧"},
    "KZT": {"buy": 0.018, "sell": 0.020, "flag": "🇰🇿"},
    "TRY": {"buy": 0.25, "sell": 0.28, "flag": "🇹🇷"},
    "UZS": {"buy": 0.0007, "sell": 0.0008, "flag": "🇺🇿"},
    "KGS": {"buy": 0.10, "sell": 0.11, "flag": "🇰🇬"},
    "AED": {"buy": 2.48, "sell": 2.52, "flag": "🇦🇪"},
}

# 10 КРИПТО - нарх LIVE аз Binance
CRYPTO_LIST = ["BTC", "ETH", "TON", "SOL", "DOGE", "XRP", "BNB", "TRX", "USDT", "PI"]

AD = "\n\n🔥 **РЕКЛАМА:**\n🌍 13 LIVE: https://cryptotj-dushanbe.blogspot.com/\n📢 Канал: @CryptoTj_Dushanbe\n💰 Обмен: @CryptoTj_Dushanbe"

@app.route('/')
def home(): return "CryptoTj 10+10 OK"

def menu():
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(
        "🌍 13 LIVE", "💵 Доллар", "🇷🇺 Рубл",
        "🇪🇺 Евро", "🇨🇳 Юан", "🇬🇧 Фунт",
        "🇰🇿 Тенге", "🇹🇷 Лира", "🇺🇿 Сум",
        "🇰🇬 Сом", "🇦🇪 Дирхам",
        "₿ BTC", "🌐 ETH", "💎 TON",
        "☀️ SOL", "🐶 DOGE", "💧 XRP",
        "🟡 BNB", "🔴 TRX", "💲 USDT", "🟣 PI",
        "👥 Одам хисоб"
    )
    return kb

def get_crypto_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        if symbol == "PI": return "0.45"
        if symbol == "TON": symbol = "TON"
        r = requests.get(url, timeout=3).json()
        return round(float(r['price']), 4)
    except:
        return "LIVE"

@bot.message_handler(commands=['start'])
def start(m):
    txt = (
        "👋 **CryptoTj Bot - 10 КУРС + 10 КРИПТО**\n\n"
        "💵 Доллар 9.25 | 🇷🇺 Рубл 0.1146 (1000=114.6)\n"
        "🇪🇺 Евро 10.42 | 🇨🇳 Юан 1.29\n\n"
        "₿ BTC | 🌐 ETH | 💎 TON | ☀️ SOL...\n"
        f"{AD}"
    )
    bot.send_message(m.chat.id, txt, parse_mode="Markdown", reply_markup=menu())

# ФИЛЬТРҲО
@bot.message_handler(func=lambda m: any(x in m.text for x in ["Доллар","Рубл","Евро","Юан","Фунт","Тенге","Лира","Сум","Сом","Дирхам","13 LIVE"]))
def fiat_handler(m):
    text = m.text
    key = None
    if "Доллар" in text: key="USD"
    elif "Рубл" in text: key="RUB"
    elif "Евро" in text: key="EUR"
    elif "Юан" in text: key="CNY"
    elif "Фунт" in text: key="GBP"
    elif "Тенге" in text: key="KZT"
    elif "Лира" in text: key="TRY"
    elif "Сум" in text: key="UZS"
    elif "Сом" in text: key="KGS"
    elif "Дирхам" in text: key="AED"
    elif "13 LIVE" in text:
        bot.send_message(m.chat.id, f"🌍 **13 КУРС LIVE**\n👉 https://cryptotj-dushanbe.blogspot.com/\n\n💵 9.25 | 🇷🇺 0.1146 | 🇪🇺 10.42{AD}", parse_mode="Markdown", reply_markup=menu())
        return
    if key:
        r = FIAT[key]
        bot.send_message(m.chat.id,
            f"{r['flag']} **{key} - ЭСХАТА**\n\nХаридорӣ: {r['buy']}\nФурӯш: {r['sell']}\n"
            f"{'🔴 1000 RUB = 114.6 TJS' if key=='RUB' else ''}{AD}",
            parse_mode="Markdown", reply_markup=menu())

# КРИПТО 10-то
@bot.message_handler(func=lambda m: any(x in m.text for x in ["BTC","ETH","TON","SOL","DOGE","XRP","BNB","TRX","USDT","PI","Биткоин","Тон","Солана","Эфир","Доге"]))
def crypto_handler(m):
    t = m.text
    sym = "BTC"
    if "ETH" in t or "Эфир" in t: sym="ETH"
    elif "TON" in t or "Тон" in t: sym="TON"
    elif "SOL" in t or "Солана" in t: sym="SOL"
    elif "DOGE" in t or "Доге" in t: sym="DOGE"
    elif "XRP" in t: sym="XRP"
    elif "BNB" in t: sym="BNB"
    elif "TRX" in t: sym="TRX"
    elif "USDT" in t: sym="USDT"
    elif "PI" in t: sym="PI"
    price = get_crypto_price(sym)
    bot.send_message(m.chat.id, f"₿ **{sym}/USDT: ${price}**{AD}", parse_mode="Markdown", reply_markup=menu())

@bot.message_handler(func=lambda m: "Одам" in m.text)
def users(m):
    bot.send_message(m.chat.id, f"👥 Мо 1000+ нафар! @CryptoTj_Dushanbe{AD}", parse_mode="Markdown", reply_markup=menu())

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_web, daemon=True).start()

while True:
    try:
        bot.infinity_polling()
    except:
        continue
