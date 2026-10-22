import os, re, time, threading, requests, telebot
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

CHANNEL = "@cryptotj_tj" # номи каналат

@app.route('/')
def home(): return "CryptoTJ Full - Tajik + 160 fiat + 100 crypto + Force Sub"

# Базаи ибтидоӣ
fiat_rates = {"USD":9.22, "TJS":1.0, "RUB":0.115, "EUR":11.85, "AED":2.97, "TRY":0.32, "UZS":0.00084, "KZT":0.022, "AFN":0.15, "CNY":1.51, "GBP":13.80, "JPY":0.073, "KRW":0.008, "AFN":0.15}

def get_fiat():
    try:
        r=requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()
        if "rates" in r:
            tjs=r["rates"].get("TJS",9.22)
            for k in r["rates"]:
                if k=="TJS": continue
                fiat_rates[k]=tjs / r["rates"][k] if r["rates"][k]!=0 else fiat_rates.get(k,1)
            print(f"Fiat loaded {len(fiat_rates)} coins")
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

# --- МАЧБУРӢ ОБУНА ---
def is_subscribed(uid):
    try:
        m=bot.get_chat_member(CHANNEL, uid)
        return m.status in ['member','administrator','creator']
    except Exception as e:
        print(f"SUB ERROR: {e} -> Ботро дар канал админ кун!")
        return False

def sub_keyboard():
    mk=InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("📢 Обуна ба канал", url=f"https://t.me/{CHANNEL[1:]}"))
    mk.add(InlineKeyboardButton("✅ Ман обуна шудам", callback_data="check"))
    return mk

# --- ЛУҒАТИ ЗӮРИ ТОҶИКӢ ---
def find_code(txt):
    tl = txt.lower().strip()
    # салом
    if tl in ["салом","салом алейкум","алейкум","hi","hello","привет","салам","salom"]:
        return "SALOM"
    tl = tl.replace("чанд","").replace("пул","").replace("курс","").replace("курби","").replace("нарх","").replace("?","").replace("!","").replace("сӯм","сум").strip()

    mp = {
        "доллар":"USD","долар":"USD","бакс":"USD","доллари":"USD","долари":"USD","долларӣ":"USD","usd":"USD","dollar":"USD","долаp":"USD",
        "евро":"EUR","йевро":"EUR","еврои":"EUR","eur":"EUR","euro":"EUR",
        "рубл":"RUB","рубли":"RUB","руси":"RUB","рӯбл":"RUB","рубли руси":"RUB","rub":"RUB",
        "сомон":"TJS","сомони":"TJS","сом":"TJS","соми":"TJS","сомонӣ":"TJS","точик":"TJS","тоҷик":"TJS","tjs":"TJS",
        "сум":"UZS","суми узбек":"UZS","узбек":"UZS","узб":"UZS","uzs":"UZS",
        "тенге":"KZT","танге":"KZT","қазоқ":"KZT","казок":"KZT","kzt":"KZT",
        "дирхам":"AED","дирҳам":"AED","дирами":"AED","дубай":"AED","араб":"AED","аморот":"AED","аед":"AED","aed":"AED",
        "лира":"TRY","турк":"TRY","туркия":"TRY","try":"TRY",
        "афгон":"AFN","афғон":"AFN","afn":"AFN",
        "юан":"CNY","хитои":"CNY","чинои":"CNY","cny":"CNY",
        "йен":"JPY","япони":"JPY","jpy":"JPY",
        "фунт":"GBP","англис":"GBP","gbp":"GBP",
        "вон":"KRW","корея":"KRW","krw":"KRW",
        # крипто
        "биткоин":"BTC","биткойн":"BTC","биток":"BTC","бит":"BTC","btc":"BTC",
        "эфириум":"ETH","эфир":"ETH","eth":"ETH",
        "солана":"SOL","солано":"SOL","sol":"SOL",
        "рипл":"XRP","xrp":"XRP","репла":"XRP",
        "шиба":"SHIB","шибаину":"SHIB","shib":"SHIB",
        "пепе":"PEPE","пеп":"PEPE","pepe":"PEPE","курбока":"PEPE",
        "бонк":"BONK","bonk":"BONK",
        "трон":"TRX","trx":"TRX",
        "тон":"TON","тонкоин":"TON","ton":"TON",
        "бнб":"BNB","бинанс":"BNB","bnb":"BNB",
        "кардано":"ADA","ада":"ADA","ada":"ADA",
        "дот":"DOT","полкадот":"DOT","dot":"DOT",
        "лайт":"LTC","лайткоин":"LTC","ltc":"LTC",
        "флоки":"FLOKI","floki":"FLOKI",
        "тетеp":"USDT","юсдт":"USDT","usdt":"USDT","доллари крипто":"USDT",
        "доги":"DOGE","догикоин":"DOGE","doge":"DOGE",
        "линк":"LINK","чейнлинк":"LINK","link":"LINK",
        "авакс":"AVAX","аваланч":"AVAX","avax":"AVAX",
    }
    # аввал калимаи дарозро санҷ
    for k in sorted(mp.keys(), key=len, reverse=True):
        if k in tl:
            return mp[k]
            
    m=re.search(r'\b[A-Z]{2,5}\b', txt.upper())
    if m: return m.group(0)
    return None

@bot.message_handler(commands=['start'])
def start(m):
    if not is_subscribed(m.from_user.id):
        bot.send_message(m.chat.id, f"⛔ Барои дидани қурб, аввал ба канал обуна шав:\n{CHANNEL}", reply_markup=sub_keyboard())
        return
    bot.send_message(m.chat.id, "👋 Салом! Ман ҳамаи пулҳои ҷаҳонро бо тоҷикӣ мефаҳмам!\n\nНавиш:\n• доллар чанд\n• сом чанд\n• рубли руси чанд\n• дирхами дубай чанд\n• биткоин чанд\n• шиба чанд\n\nБлоги мо:\nhttps://cryptotj.blogspot.com")

@bot.message_handler(commands=['help'])
def help_cmd(m):
    bot.send_message(m.chat.id, "🌍 160+ пул, 100+ крипто\n\nМисол:\nдоллар чанд\nевро чанд\nсом чанд\nсуми узбек чанд\nдирхами дубай чанд\nбиткоин чанд\nтон чанд\n\nhttps://cryptotj.blogspot.com")

@bot.callback_query_handler(func=lambda c: c.data=="check")
def chk(c):
    if is_subscribed(c.from_user.id):
        bot.edit_message_text("✅ Раҳмат! Обуна шудӣ! Акнун навиш: доллар чанд, сом чанд, биткоин чанд", c.message.chat.id, c.message.message_id)
    else:
        bot.answer_callback_query(c.id, "❌ Ҳоло обуна нашудаӣ! Аввал тугмаи Обуна-ро пахш кун", show_alert=True)

@bot.message_handler(func=lambda x: True)
def all_msg(m):
    if not is_subscribed(m.from_user.id):
        bot.send_message(m.chat.id, "⛔ Аввал обуна шав, баъд қурб медиҳам:", reply_markup=sub_keyboard())
        return
    code=find_code(m.text)
    if code=="SALOM":
        bot.send_message(m.chat.id, f"👋 Салом! 💵 1 USD = {fiat_rates['USD']:.2f} TJS\nНавиш: доллар чанд, сом чанд, биткоин чанд")
        return
    if not code:
        bot.send_message(m.chat.id, "❓ Нафаҳмидам.\nНавиш: доллар чанд, сом чанд, биткоин чанд")
        return
    if code in fiat_rates:
        if code=="TJS":
            bot.send_message(m.chat.id, f"💵 1 TJS = 1.00 TJS\nhttps://cryptotj.blogspot.com")
        else:
            bot.send_message(m.chat.id, f"💵 1 {code} = {fiat_rates[code]:.4f} TJS\n≈ ${fiat_rates[code]/fiat_rates['USD']:.4f}\nhttps://cryptotj.blogspot.com")
    else:
        p,src=get_crypto(code)
        if p:
            bot.send_message(m.chat.id, f"🪙 {code} = ${p:.6f}\n≈ {p*fiat_rates['USD']:.2f} TJS\n({src})\nhttps://cryptotj.blogspot.com")
        else:
            bot.send_message(m.chat.id, f"❌ {code} ёфт нашуд.\nНавиш: доллар чанд, биткоин чанд")

def run_bot():
    get_fiat()
    while True:
        try: bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e: print(e); time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
