import telebot, os, threading, requests
from flask import Flask
from datetime import datetime

TOKEN = os.environ.get("BOT_TOKEN", "ТОКЕНАТРО-ИН-ҶО-ГУЗОР")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

BACKUP_FIAT = {
    "USD": [9.15, 9.25, "💵 Доллар"],
    "RUB": [0.1126, 0.1146, "🇷🇺 Рубл"],
    "EUR": [10.22, 10.42, "🇪🇺 Евро"],
    "CNY": [1.25, 1.29, "🇨🇳 Юан"],
    "GBP": [11.80, 12.10, "🇬🇧 Фунт"],
    "KZT": [0.018, 0.020, "🇰🇿 Тенге"],
    "TRY": [0.25, 0.28, "🇹🇷 Лира"],
    "UZS": [0.0007, 0.0008, "🇺🇿 Сум"],
    "KGS": [0.10, 0.11, "🇰🇬 Сом"],
    "AED": [2.48, 2.52, "🇦🇪 Дирхам"]
}
BACKUP_CRYPTO = {"BTC": 68000, "ETH": 2600, "TON": 5.2, "SOL": 145, "DOGE": 0.13, "XRP": 0.52, "BNB": 590, "TRX": 0.16, "USDT": 1, "PI": 0.45}

AD = "\n\n🌍 13 LIVE: https://cryptotj-dushanbe.blogspot.com/\n📢 @CryptoTjDushanbe"

@app.route('/')
def home(): return "AUTO LIVE OK"

def kb():
    m = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    m.add("🌍 13 LIVE","💵 Доллар","🇷🇺 Рубл","🇪🇺 Евро","🇨🇳 Юан","🇬🇧 Фунт","🇰🇿 Тенге","🇹🇷 Лира","🇺🇿 Сум","🇰🇬 Сом","🇦🇪 Дирхам","₿ BTC","🌐 ETH","💎 TON","☀️ SOL","🐶 DOGE","💧 XRP","🟡 BNB","🔴 TRX","💲 USDT","🟣 PI")
    return m

def get_fiat_rates():
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5).json()
        tjs = r['rates']['TJS']
        rates = {}
        rates['USD'] = [round(tjs*0.99,4), round(tjs*1.01,4), "💵 Доллар"]
        rates['EUR'] = [round(tjs/r['rates']['EUR']*0.99,4), round(tjs/r['rates']['EUR']*1.01,4), "🇪🇺 Евро"]
        rates['RUB'] = [round(tjs/r['rates']['RUB']*0.99,5), round(tjs/r['rates']['RUB']*1.01,5), "🇷🇺 Рубл"]
        rates['CNY'] = [round(tjs/r['rates']['CNY']*0.99,4), round(tjs/r['rates']['CNY']*1.01,4), "🇨🇳 Юан"]
        rates['GBP'] = [round(tjs/r['rates']['GBP']*0.99,4), round(tjs/r['rates']['GBP']*1.01,4), "🇬🇧 Фунт"]
        rates['KZT'] = [round(tjs/r['rates']['KZT']*0.99,5), round(tjs/r['rates']['KZT']*1.01,5), "🇰🇿 Тенге"]
        rates['TRY'] = [round(tjs/r['rates']['TRY']*0.99,4), round(tjs/r['rates']['TRY']*1.01,4), "🇹🇷 Лира"]
        rates['AED'] = [round(tjs/r['rates']['AED']*0.99,4), round(tjs/r['rates']['AED']*1.01,4), "🇦🇪 Дирхам"]
        rates['UZS'] = [0.0007,0.0008,"🇺🇿 Сум"]
        rates['KGS'] = [0.10,0.11,"🇰🇬 Сом"]
        return rates
    except:
        return BACKUP_FIAT

def get_crypto_price(sym):
    try:
        r = requests.get(f"https://data-api.binance.vision/api/v3/ticker/price?symbol={sym}USDT", timeout=4).json()
        return float(r['price'])
    except:
        try:
            r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={sym}&tsyms=USD", timeout=4).json()
            return r['USD']
        except:
            return BACKUP_CRYPTO.get(sym, 0)

@bot.message_handler(commands=['start'])
def s(m):
    rates = get_fiat_rates()
    vaqt = datetime.now().strftime("%H:%M:%S %d.%m")
    bot.send_message(m.chat.id, f"👋 CryptoTj AUTO 10+10 LIVE\n\n💵 Доллар: {rates['USD'][1]}\n🇷🇺 Рубл: {rates['RUB'][1]} = 1000={round(rates['RUB'][1]*1000,1)} TJS\n🇪🇺 Евро: {rates['EUR'][1]}\n⏰ {vaqt}\n\nҲама курс авто аз интернет!{AD}", reply_markup=kb())

@bot.message_handler(func=lambda x: True)
def all_h(m):
    t = m.text
    rates = get_fiat_rates()
    vaqt = datetime.now().strftime("%H:%M:%S %d.%m")
    for k,v in rates.items():
        if v[2].split()[1] in t:
            extra = f"\n🔴 1000 = {round(v[1]*1000,1)} TJS" if k=="RUB" else ""
            bot.send_message(m.chat.id, f"{v[2]} AUTO\nХарид: {v[0]}\nФурӯш: {v[1]}{extra}\n⏰ {vaqt}\n♻️ Манбаъ: open.er-api.com{AD}", reply_markup=kb())
            return
    for s_name in ["BTC","ETH","TON","SOL","DOGE","XRP","BNB","TRX","USDT","PI"]:
        if s_name in t:
            p = get_crypto_price(s_name)
            bot.send_message(m.chat.id, f"₿ {s_name}/USDT: ${p}\n⏰ {vaqt}\n♻️ Манбаъ: Binance LIVE{AD}", reply_markup=kb())
            return
    bot.send_message(m.chat.id, f"🌍 LIVE: https://cryptotj-dushanbe.blogspot.com/{AD}", reply_markup=kb())

threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000))), daemon=True).start()
while True:
    try: bot.infinity_polling()
    except: continue
