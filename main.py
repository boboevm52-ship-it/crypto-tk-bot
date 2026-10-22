import os, sys, requests, threading, time, re, logging
from flask import Flask
import telebot

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
print(f"Token ok: {bool(BOT_TOKEN)} len={len(BOT_TOKEN) if BOT_TOKEN else 0}", flush=True)
sys.stdout.flush()

SITE = "https://cryptotj.blogspot.com"
FIAT_BASE = {"USD":10.90,"EUR":11.85,"RUB":0.115,"GBP":12.34,"TRY":1.37,"CHF":11.17,"AED":2.51,"SAR":2.45,"INR":0.097,"KZT":0.022,"CNY":1.51,"KGS":0.124,"TMT":3.11,"UZS":0.000844,"JPY":0.073,"KRW":0.0081,"AFN":0.15,"AZN":6.41,"UAH":0.26}
CRYPTO_BASE = {"BTC":"bitcoin","ETH":"ethereum","BNB":"binancecoin","XRP":"ripple","SOL":"solana","DOGE":"dogecoin","TON":"the-open-network","ADA":"cardano","AVAX":"avalanche-2","SHIB":"shiba-inu","DOT":"polkadot","TRX":"tron","LINK":"chainlink","LTC":"litecoin","PEPE":"pepe","BONK":"bonk","NOT":"notcoin","PI":"pi-network","FLOKI":"floki","WIF":"dogwifcoin","USDT":"tether","USDC":"usd-coin","DAI":"dai","ARB":"arbitrum","NEAR":"near","OP":"optimism","SUI":"sui","APT":"aptos","FIL":"filecoin","HBAR":"hedera","MKR":"maker","TAO":"bittensor","RUNE":"thorchain","SEI":"sei-network","ENA":"ethena","ONDO":"ondo-finance","ALGO":"algorand","VET":"vechain","ICP":"internet-computer","FTM":"fantom","SAND":"the-sandbox","MANA":"decentraland","AXS":"axie-infinity","GALA":"gala","ZEC":"zcash","EOS":"eos","XTZ":"tezos","1INCH":"1inch","CAKE":"pancakeswap-token"}

H = {"User-Agent":"Mozilla/5.0"}

def footer(): return f"\n\n━━━━━━━━━━━━━━\n🌐 {SITE}\n💰 Обуна шавед!"
def markup():
    m=telebot.types.InlineKeyboardMarkup()
    m.add(telebot.types.InlineKeyboardButton("💰 Канали мо", url=SITE))
    return m

def get_all_fiat():
    try:
        r=requests.get("https://open.er-api.com/v6/latest/USD", headers=H, timeout=15).json()
        rates=r.get('rates',{})
        conv={}
        for k,v in rates.items():
            if v>0: conv[k]=round(10.9/v, 6)
        for k,v in FIAT_BASE.items(): conv[k]=v
        return conv
    except: return FIAT_BASE

def get_price(sym):
    sym=sym.upper().strip()
    for s,c in CRYPTO_BASE.items():
        if c==sym.lower(): sym=s
    if sym in ["USDT","USDC","DAI"]: return 1.0
    try:
        r=requests.get(f"https://api.mexc.com/api/v3/ticker/price?symbol={sym}USDT", headers=H, timeout=5).json()
        if 'price' in r: return float(r['price'])
    except: pass
    try:
        r=requests.get(f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={sym}USDT", headers=H, timeout=5).json()
        lst=r.get('result',{}).get('list',[])
        if lst and lst[0].get('lastPrice'): return float(lst[0]['lastPrice'])
    except: pass
    try:
        r=requests.get(f"https://api.coinbase.com/v2/prices/{sym}-USD/spot", headers=H, timeout=5).json()
        if 'data' in r and 'amount' in r['data']: return float(r['data']['amount'])
    except: pass
    try:
        r=requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}USDT", headers=H, timeout=5).json()
        if 'price' in r: return float(r['price'])
    except: pass
    return None

def find_code(t):
    tl=t.lower()
    if "сом" in tl and "самсунг" not in tl: return "USD_SPECIAL"
    if "рубл" in tl or "рубул" in tl or "rubl" in tl: return "RUB"
    if "доллар" in tl or "долар" in tl or "dollar" in tl or "usd" in tl: return "USD"
    if "евро" in tl or "eur" in tl: return "EUR"
    if "биткоин" in tl or "btc" in tl: return "BTC"
    if "эфир" in tl: return "ETH"
    if "доге" in tl or "doge" in tl: return "DOGE"
    if "тон" in tl: return "TON"
    if "рипл" in tl or "xrp" in tl: return "XRP"
    if "солана" in tl or "sol" in tl: return "SOL"
    if "трон" in tl or "trx" in tl: return "TRX"
    if "тетер" in tl or "usdt" in tl: return "USDT"
    if "шиба" in tl or "shib" in tl: return "SHIB"
    if "пепе" in tl or "pepe" in tl: return "PEPE"
    if "бонк" in tl or "bonk" in tl: return "BONK"
    up=t.upper()
    m=re.search(r'\b[A-Z]{2,5}\b', up)
    if m: return m.group(0)
    return None

# BOT
if BOT_TOKEN and ":" in BOT_TOKEN:
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
        print("Webhook deleted", flush=True)
    except Exception as e:
        print(f"Webhook err {e}", flush=True)

    @bot.message_handler(commands=['start'])
    def start_cmd(message):
        kb=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
        kb.add(telebot.types.KeyboardButton("Сом чанд"),telebot.types.KeyboardButton("Рубл чанд"),telebot.types.KeyboardButton("Доллар чанд"))
        kb.add(telebot.types.KeyboardButton("BTC"),telebot.types.KeyboardButton("ETH"),telebot.types.KeyboardButton("PEPE"))
        kb.add(telebot.types.KeyboardButton("14 курс"),telebot.types.KeyboardButton("160 пул"),telebot.types.KeyboardButton("100 крипто"))
        bot.send_message(message.chat.id, f"✅ Тайёр! 160+ пул + 100+ крипто!\n🌐 {SITE}", reply_markup=kb)

    @bot.message_handler(content_types=['text'])
    def text_handler(message):
        try:
            txt=message.text
            low=txt.lower()
            code=find_code(txt)
            print(f"📩 {txt} -> {code}", flush=True)

            if "100 крипто" in low or "хамаи крипто" in low:
                bot.send_message(message.chat.id, "⏳ 100 крипто ҷамъоварӣ...")
                msg="💰 100 КРИПТО (Live MEXC):\n\n"
                for s in list(CRYPTO_BASE.keys())[:40]:
                    p=get_price(s)
                    if p:
                        if p<0.01: msg+=f"• {s}: {p:.8f} $\n"
                        else: msg+=f"• {s}: {p:.4f} $\n"
                msg+=footer()
                bot.send_message(message.chat.id, msg, reply_markup=markup())
                return

            if "160 пул" in low or "хамаи пул" in low:
                rates=get_all_fiat()
                msg="🌍 160+ ПУЛИ ҶАҲОН:\n\n"
                for k,v in list(sorted(rates.items()))[:80]:
                    msg+=f"• 1 {k} = {v:.4f} TJS\n"
                msg+=f"\n...ҳамагӣ {len(rates)} пул!{footer()}"
                bot.send_message(message.chat.id, msg, reply_markup=markup())
                return

            if code=="USD_SPECIAL" or "сом чанд" in low:
                rates=get_all_fiat()
                bot.send_message(message.chat.id, f"💰 1 USD = {rates.get('USD',10.9):.2f} TJS\n💶 1 EUR = {rates.get('EUR',11.85):.2f} TJS\n💴 1 RUB = {rates.get('RUB',0.115):.4f} TJS{footer()}", reply_markup=markup())
                return

            if "курс" in low:
                rates=get_all_fiat()
                msg="💱 14 КУРС:\n\n"
                for k in ["USD","EUR","RUB","GBP","TRY","JPY","KRW","AFN","AZN","KZT","UZS","CNY","AED","SAR"]:
                    msg+=f"• 1 {k} = {rates.get(k,0):.4f} TJS\n"
                msg+=footer()
                bot.send_message(message.chat.id, msg, reply_markup=markup())
                return

            if code:
                rates=get_all_fiat()
                if code in rates:
                    bot.send_message(message.chat.id, f"💰 1 {code} = {rates[code]:.6f} TJS{footer()}", reply_markup=markup())
                    return
                p=get_price(code)
                if p:
                    if p<0.01: bot.send_message(message.chat.id, f"🟡 {code}:\n🟢 {p:.10f} $\n🔴 {p*10.9:.10f} TJS{footer()}", reply_markup=markup())
                    else: bot.send_message(message.chat.id, f"🟡 {code}:\n🟢 {p:.6f} $\n🔴 {p*10.9:.4f} TJS{footer()}", reply_markup=markup())
                    return

            rates=get_all_fiat()
            bot.send_message(message.chat.id, f"💱 1 USD = {rates.get('USD',10.9):.2f} TJS\nНавиш: Сом чанд, BTC, PEPE чанд{footer()}", reply_markup=markup())
        except Exception as e:
            print(f"Error: {e}", flush=True)

    def run_bot():
        while True:
            try:
                print("🚀 Polling started...", flush=True)
                bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
            except Exception as e:
                print(f"Polling error: {e}", flush=True)
                time.sleep(10)
    
    threading.Thread(target=run_bot, daemon=True).start()
else:
    bot = None
    print("❌ BOT_TOKEN нест! Дар Render Environment гузор!", flush=True)

app = Flask(__name__)
@app.route('/')
def home():
    if not BOT_TOKEN: return "❌ BOT_TOKEN нест!"
    return "✅ Bot Live - 160 FIAT + 100 CRYPTO"

if __name__ == "__main__":
    print("✅ Flask on 10000", flush=True)
    app.run(host="0.0.0.0", port=10000)
