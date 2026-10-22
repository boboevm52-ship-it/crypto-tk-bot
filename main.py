
import os, requests, threading, time, re
from flask import Flask
import telebot

print("🚀 Starting Bot...")

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()

if not BOT_TOKEN or ":" not in BOT_TOKEN:
    print("❌ BOT_TOKEN нест!")
    app = Flask(__name__)
    @app.route('/')
    def home(): return "❌ BOT_TOKEN нест! Дар Render Environment гузор!"
    app.run(host="0.0.0.0", port=10000)
else:
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook", timeout=10)
        time.sleep(1)
    except: pass

    # 14 КУРСИ АСОСӢ
    FIAT_BASE = {"USD":10.90,"EUR":11.85,"RUB":0.115,"GBP":12.34,"TRY":1.37,"CHF":11.17,"AED":2.51,"SAR":2.45,"INR":0.097,"KZT":0.022,"CNY":1.51,"KGS":0.124,"TMT":3.11,"UZS":0.000844}
    CRYPTO_BASE = {"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","BNB":"binancecoin","XRP":"ripple","DOGE":"dogecoin","TON":"the-open-network","USDT":"tether","TRX":"tron","AVAX":"avalanche-2"}

    SITE = "https://cryptotj.blogspot.com"
    CACHE_FIAT = {}
    CACHE_TIME = 0

    def footer(): return f"\n\n━━━━━━━━━━━━━━\n🌐 {SITE}\n💰 Ба сайти асли мо обуна шавед!"
    def markup():
        m = telebot.types.InlineKeyboardMarkup()
        m.add(telebot.types.InlineKeyboardButton("💰 Бо Канали мо обуна шавед", url=SITE))
        m.add(telebot.types.InlineKeyboardButton("🌐 Сайти асли мо", url=SITE))
        return m

    def get_all_fiat():
        global CACHE_FIAT, CACHE_TIME
        if time.time()-CACHE_TIME < 3600 and CACHE_FIAT:
            return CACHE_FIAT
        try:
            r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10).json()
            rates = r.get('rates',{})
            converted = {}
            for k,v in rates.items():
                if v>0: converted[k] = 10.9/v
            for k,v in FIAT_BASE.items(): converted[k]=v
            converted["JPY"]=converted.get("JPY",0.073)
            converted["KRW"]=converted.get("KRW",0.0081)
            converted["AFN"]=converted.get("AFN",0.15)
            CACHE_FIAT=converted
            CACHE_TIME=time.time()
            print(f"✅ {len(converted)} пул бор шуд")
            return converted
        except Exception as e:
            print(f"Fiat error: {e}")
            return FIAT_BASE

    def get_crypto_price(cid):
        try:
            r=requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd",timeout=15).json()
            return r.get(cid,{}).get('usd')
        except: return None

    def search_any_crypto(query):
        try:
            url=f"https://api.coingecko.com/api/v3/search?query={query}"
            res=requests.get(url, timeout=15).json()
            coins=res.get('coins',[])
            if coins:
                cid=coins[0]['id']
                sym=coins[0]['symbol'].upper()
                name=coins[0]['name']
                price=get_crypto_price(cid)
                return sym, name, price
        except: pass
        return None, None, None

    def find_code(text):
        t=text.lower()
        # СОМ - муҳим!
        if "сом" in t and "самсунг" not in t: return "USD_SPECIAL"
        if any(x in t for x in ["рубл","рубул","рубь","rubl"," rub "]): return "RUB"
        if any(x in t for x in ["доллар","долар","dollar","usd","$"]): return "USD"
        if any(x in t for x in ["евро","euro","eur"]): return "EUR"
        if any(x in t for x in ["йена","yena","jpy","йен"]): return "JPY"
        if any(x in t for x in ["вон","won","krw"]): return "KRW"
        if any(x in t for x in ["сум","uzs","сўм"]): return "UZS"
        if any(x in t for x in ["тенге","kzt"]): return "KZT"
        if any(x in t for x in ["афгон","afgh","afn"]): return "AFN"
        if any(x in t for x in ["лира","try","туркия"]): return "TRY"
        if any(x in t for x in ["фунт","gbp","pound"]): return "GBP"
        if any(x in t for x in ["юан","cny","china"]): return "CNY"
        if any(x in t for x in ["биткоин","bitcoin","btc"]): return "BTC"
        if any(x in t for x in ["эфир","eth "]): return "ETH"
        if any(x in t for x in ["доге","дож","doge"]): return "DOGE"
        if any(x in t for x in ["тон"," ton "]): return "TON"
        if any(x in t for x in ["рипл","xrp","ripple"]): return "XRP"
        if any(x in t for x in ["солана","sol "]): return "SOL"
        if any
