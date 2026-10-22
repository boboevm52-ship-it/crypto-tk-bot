import os, re, time, threading, requests, telebot
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

CHANNEL = "@cryptotj_tj"  # <-- ҳаминро иваз кун ба канали худ

@app.route('/')
def home(): return "CryptoTJ Final - Tajik + 160 fiat + 100 crypto"

# Базаи пул
fiat_rates = {"USD":10.90, "TJS":1.0, "RUB":0.115, "EUR":11.85, "AED":2.97, "TRY":0.32, "UZS":0.00084, "KZT":0.022, "AFN":0.15, "CNY":1.51, "GBP":13.80, "JPY":0.073, "KRW":0.008}

def get_fiat():
    try:
        r=requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()
        if "rates" in r:
            tjs=r["rates"].get("TJS",10.90)
            for k in r["rates"]:
                if k=="TJS": continue
                fiat_rates[k]=tjs / r["rates"][k] if r["rates"][k]!=0 else fiat_rates.get(k,1)
            print(f"Fiat loaded {len(fiat_rates)}")
    except Exception as e: print(f"Fiat err {e}")

def get_crypto(code):
    code=code.upper()
    for url in [
        f"https://api.mexc.com/api/v3/ticker/price?symbol={code}USDT",
        f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={code}USDT",
    ]:
        try:
            r=requests.get(url, timeout=5).json()
            if "price" in r: return float(r["price"]), "MEXC"
            if r.get("result",{}).get("list"): return float(r["result"]["list"][0]["lastPrice"]), "Bybit"
        except: pass
    try:
        r=requests.get(f"https://api.coinbase.com/v2/prices/{code}-USD/spot", timeout=5).json()
        if "data" in r: return float(r["data"]["amount"]), "Coinbase"
    except: pass
    return None, None

# --- ПАТРИСАТСИЯ ---
def is_subscribed(uid):
    try:
        m=bot.get_chat_member(CHANNEL, uid)
        return m.status in ['member','administrator','creator']
    except: return True

# --- ЛУҒАТИ ТОҶИКӢ ЗӮР ---
def find_code(txt):
    tl = txt.lower()
    tl = tl.replace("чанд","").replace("пул","").replace("курс","").replace("курби","").replace("нарх","").replace("?","").replace("сӯм","сум").strip()
    
    mp = {
        "доллар":"USD","долар":"USD","бакс":"USD","доллари":"USD","долари":"USD","usd":"USD","dollar":"USD",
        "евро":"EUR","йевро":"EUR","eur":"EUR",
        "рубл":"RUB","рубли":"RUB","руси":"RUB","рӯбл":"RUB","rub":"RUB",
        "сомон":"TJS","сомони":"TJS","точик":"TJS","тоҷик":"TJS",
        "сум":"UZS","узбек":"UZS","узб":"UZS",
        "тенге":"KZT","танге":"KZT","казок":"KZT","қазоқ":"KZT",
        "дирхам":"AED","дирҳам":"AED","дубай":"AED","араб":"AED","аморот":"AED","aed":"AED",
        "лира":"TRY","турк":"TRY","try":"TRY",
        "афгон":"AFN","афғон":"AFN",
        "юан":"CNY","хитои":"CNY","cny":"CNY",
        "йен":"JPY","япони":"JPY",
        "фунт":"GBP","англис":"GBP",
        "вон":"KRW","корея":"KRW",
        # crypto
        "биткоин":"BTC","биткойн":"BTC","биток":"BTC","бит":"BTC","btc":"BTC",
        "эфириум":"ETH","эфир":"ETH","eth":"ETH",
        "солана":"SOL","сол":"SOL","sol":"SOL",
        "рипл":"XRP","xrp":"XRP",
        "шиба":"SHIB","shib":"SHIB",
        "пепе":"PEPE","pepe":"PEPE",
        "бонк":"BONK","bonk":"BONK",
        "трон":"TRX","trx":"TRX",
        "тон":"TON","тонкоин":"TON","ton":"TON",
        "бнб":"BNB","бинанс":"BNB","bnb":"BNB",
        "кардано":"ADA","ада":"ADA","ada":"ADA",
        "дот":"DOT","полкадот":"DOT","dot":"DOT",
        "лайт":"LTC","лайткоин":"LTC","ltc":"LTC",
        "флоки":"FLOKI","floki":"FLOKI",
        "тетеp":"USDT","usdt":"USDT","юсдт":"USDT",
        "доги":"DOGE","догикоин":"DOGE","doge":"DOGE",
        "линк":"LINK","link":"LINK",
        "авакс":"AVAX","avax":"AVAX",
    }
    for k,v in mp.items():
        if k in tl: return v
    m=re.search(r'\b[A-Z]{2,5}\b', txt.upper())
    if m: return m.group(0)
    return None

def sub_keyboard():
    mk=InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("📢 Обуна ба канал", url=f"https://t.me/{CHANNEL[1:]}"))
    mk.add(InlineKeyboardButton("✅ Ман обуна шудам", callback_data="check"))
    return mk

@bot.message_handler(commands=['start'])
def start(m):
    if not is_subscribed(m.from_user.id):
        bot.send_message(m.chat.id, "⛔ Барои дидани қурб, аввал обуна шав:", reply_markup=sub_keyboard())
        return
    bot.send_message(m.chat.id, "👋 Салом! Ман қурби тоҷикӣ мефаҳмам!\n\nНавиш:\n• доллар чанд\n• рубли руси\n• дирхами дубай\n• биткоин чанд\n• шиба чанд\n\n/help - ҳамаи пулҳо")

@bot.callback_query_handler(func=lambda c: c.data=="check")
def chk(c):
    if is_subscribed(c.from_user.id):
        bot.edit_message_text("✅ Раҳмат! Обуна шудӣ! Акнун навиш: доллар, рубл, биткоин", c.message.chat.id, c.message.message_id)
    else:
        bot.answer_callback_query(c.id, "❌ Ҳоло обуна нашудаӣ! Тугмаи болоиро пахш кун", show_alert=True)

@bot.message_handler(func=lambda x: True)
def all_msg(m):
    if not is_subscribed(m.from_user.id):
        bot.send_message(m.chat.id, "⛔ Аввал обуна шав, баъд қурб медиҳам:", reply_markup=sub_keyboard())
        return
    
    code=find_code(m.text)
    if not code:
        bot.send_message(m.chat.id, f"💵 1 USD = {fiat_rates['USD']:.2f} TJS\nНавиш: доллар чанд, биткоин чанд")
        return
    if code in fiat_rates:
        bot.send_message(m.chat.id, f"💵 1 {code} = {fiat_rates[code]:.4f} TJS")
    else:
        p,src=get_crypto(code)
        if p:
            bot.send_message(m.chat.id, f"🪙 {code} = ${p:.6f} ≈ {p*fiat_rates['USD']:.2f} TJS\n({src})")
        else:
            bot.send_message(m.chat.id, f"❌ {code} ёфт нашуд. /help пахш кун")

def run_bot():
    get_fiat()
    while True:
        try: bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e: print(e); time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
