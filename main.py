import os, re, time, threading, requests, telebot
from flask import Flask

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def home(): return "CryptoTj Bot Live! 160 currencies + 100 crypto"

# КУРСҲО
fiat_rates = {
    "USD":10.90, "RUB":0.115, "EUR":11.85, "UZS":0.00084, "KZT":0.022,
    "TRY":0.32, "AFN":0.15, "JPY":0.073, "KRW":0.008, "CNY":1.51,
    "GBP":13.80, "AED":2.97, "TJS":1.0
}

def get_fiat():
    try:
        r=requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5).json()
        if "rates" in r:
            tjs=r["rates"].get("TJS",10.90)
            for k in fiat_rates.keys():
                if k=="TJS": continue
                if k in r["rates"] and r["rates"][k]!=0:
                    fiat_rates[k]=tjs / r["rates"][k]
            print("Fiat updated")
    except Exception as e:
        print(f"Fiat error {e}")

def get_crypto(code):
    code=code.upper()
    try:
        r=requests.get(f"https://api.mexc.com/api/v3/ticker/price?symbol={code}USDT", timeout=4).json()
        if "price" in r: return float(r["price"]), "MEXC"
    except: pass
    try:
        r=requests.get(f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={code}USDT", timeout=4).json()
        if r.get("result",{}).get("list"):
            return float(r["result"]["list"][0]["lastPrice"]), "Bybit"
    except: pass
    try:
        r=requests.get(f"https://api.coinbase.com/v2/prices/{code}-USD/spot", timeout=4).json()
        if "data" in r: return float(r["data"]["amount"]), "Coinbase"
    except: pass
    return None, None

def find_code(t):
    tl=t.lower().strip()
    tl=tl.replace("чан","").replace("чанд","").replace("?","").replace("!","").strip()
    
    # 1. УЗБЕК СУМ - аввал!
    if "узбек" in tl or "узумбек" in tl or tl=="сум" or "сўм" in tl or "so'm" in tl or "uzs" in tl or ("сум" in tl and "сомон" not in tl and "точик" not in tl and "тадж" not in tl):
        if "сомон" not in tl:
            return "UZS"
    
    # 2. ЮАН - Хитои
    if "юан" in tl or "юуан" in tl or "юань" in tl or "юоан" in tl or "йуан" in tl or "cny" in tl or "yuan" in tl or "чини" in tl or "хитои" in tl or "китай" in tl:
        return "CNY"
    
    # 3. СОМОНИ
    if "сомон" in tl or tl in ["сом","сом чанд"] or ("сом" in tl and "сум" not in tl and "соло" not in tl and "самсунг" not in tl):
        return "USD_SPECIAL"
    
    # 4. Дигар фиат бо точики
    if "рубл" in tl or "рубул" in tl or "рубли" in tl or "rubl" in tl or "rub" in tl: return "RUB"
    if "доллар" in tl or "долар" in tl or "долор" in tl or "dollar" in tl: return "USD"
    if "евро" in tl or "еуро" in tl or "eur" in tl: return "EUR"
    if "йена" in tl or "иен" in tl or "япон" in tl or "jpy" in tl: return "JPY"
    if "вон" in tl or "корея" in tl or "krw" in tl: return "KRW"
    if "тенге" in tl or "танге" in tl or "казах" in tl or "kzt" in tl: return "KZT"
    if "лира" in tl or "турк" in tl or "try" in tl: return "TRY"
    if "афгон" in tl or "афган" in tl or "afn" in tl: return "AFN"
    if "дирхам" in tl or "aed" in tl or "дубай" in tl: return "AED"
    if "фунт" in tl or "gbp" in tl or "англи" in tl: return "GBP"
    
    # 5. Крипто бо лахчаи ТОЧИКИ
    if "битко" in tl or "бикто" in tl or "битка" in tl or "btc" in tl: return "BTC"
    if "эфир" in tl or "эфер" in tl or "eth" in tl: return "ETH"
    if "соло" in tl or "солан" in tl or "салан" in tl or "солон" in tl or "sol" in tl: return "SOL"
    if "доге" in tl or "доги" in tl or "додж" in tl or "doge" in tl: return "DOGE"
    if "рипл" in tl or "репл" in tl or "xrp" in tl: return "XRP"
    if "шиба" in tl or "шибо" in tl or "shib" in tl: return "SHIB"
    if "пепе" in tl or "pepe" in tl: return "PEPE"
    if "бонк" in tl or "бонг" in tl or "bonk" in tl: return "BONK"
    if "трон" in tl or "тирон" in tl or "trx" in tl: return "TRX"
    if "тон" in tl or "ton" in tl: return "TON"
    if "бнб" in tl or "bnb" in tl: return "BNB"
    if "кардано" in tl or "ada" in tl: return "ADA"
    if "дот" in tl or "dot" in tl: return "DOT"
    if "лайт" in tl or "ltc" in tl: return "LTC"
    if "флоки" in tl or "floki" in tl: return "FLOKI"
    if "тетер" in tl or "usdt" in tl: return "USDT"
    if "линк" in tl or "link" in tl: return "LINK"
    if "авакс" in tl or "avax" in tl: return "AVAX"
    
    up=t.upper()
    m=re.search(r'\b[A-Z]{2,5}\b', up)
    if m: return m.group(0)
    return None

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
        "💱 Салом! Боти CryptoTj!\n\n"
        "Навиш бо точики:\n"
        "• Сом чанд\n"
        "• Сум чанд (Узбек)\n"
        "• Юан чанд / Юуан чан\n"
        "• Солоно чанд\n"
        "• Битко чанд, Пепе чанд\n"
        "• Рубл чанд, Доллар чанд\n\n"
        "🌐 https://cryptotj.blogspot.com")

@bot.message_handler(func=lambda x: True)
def handle(m):
    txt=m.text.strip()
    code=find_code(txt)
    print(f"📩 {txt} -> {code}")
    if not code:
        bot.send_message(m.chat.id, f"💱 1 USD = {fiat_rates['USD']:.2f} TJS\nНавиш: Сом чанд, Сум чанд, Юан чанд, Солоно чанд")
        return
    if code=="USD_SPECIAL":
        bot.send_message(m.chat.id, f"💵 1 USD = {fiat_rates['USD']:.2f} TJS\n\n🌐 https://cryptotj.blogspot.com\n💰 Обуна шавед!")
        return
    if code in fiat_rates:
        bot.send_message(m.chat.id, f"💱 1 {code} = {fiat_rates[code]:.4f} TJS\n\n🌐 https://cryptotj.blogspot.com")
        return
    price, src = get_crypto(code)
    if price:
        tjs_price = price * fiat_rates['USD']
        bot.send_message(m.chat.id, f"🪙 {code} = ${price:.6f}\n💵 {tjs_price:.2f} TJS\n📊 {src}\n\n🌐 https://cryptotj.blogspot.com")
    else:
        bot.send_message(m.chat.id, f"❌ {code} ёфт нашуд. BTC, SOL, PEPE, Юан навиш!")

def run_bot():
    get_fiat()
    while True:
        try:
            print("🚀 Polling started")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Poll error {e}"); time.sleep(5)

if __name__=="__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)
