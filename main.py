import os, requests, threading, time, re
from flask import Flask
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
print(f"Token ok: {bool(BOT_TOKEN)}")

if not BOT_TOKEN or ":" not in BOT_TOKEN:
    app = Flask(__name__)
    @app.route('/')
    def home(): return "❌ BOT_TOKEN нест!"
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=10000)
else:
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
        time.sleep(1)
    except: pass

    SITE = "https://cryptotj.blogspot.com"
    FIAT_BASE = {"USD":10.90,"EUR":11.85,"RUB":0.115,"GBP":12.34,"TRY":1.37,"CHF":11.17,"AED":2.51,"SAR":2.45,"INR":0.097,"KZT":0.022,"CNY":1.51,"KGS":0.124,"TMT":3.11,"UZS":0.000844,"JPY":0.073,"KRW":0.0081,"AFN":0.15,"AZN":6.41,"UAH":0.26}
    CRYPTO_BASE = {
        "BTC":"bitcoin","ETH":"ethereum","BNB":"binancecoin","XRP":"ripple","SOL":"solana",
        "DOGE":"dogecoin","TON":"the-open-network","ADA":"cardano","AVAX":"avalanche-2","SHIB":"shiba-inu",
        "DOT":"polkadot","TRX":"tron","LINK":"chainlink","MATIC":"matic-network","LTC":"litecoin",
        "BCH":"bitcoin-cash","UNI":"uniswap","XLM":"stellar","ATOM":"cosmos","ETC":"ethereum-classic",
        "PEPE":"pepe","BONK":"bonk","NOT":"notcoin","PI":"pi-network","FLOKI":"floki",
        "WIF":"dogwifcoin","WLD":"worldcoin","RENDER":"render-token","FET":"fetch-ai","INJ":"injective-protocol",
        "USDT":"tether","USDC":"usd-coin","DAI":"dai","AAVE":"aave","ARB":"arbitrum",
        "NEAR":"near","OP":"optimism","SUI":"sui","APT":"aptos","STX":"stacks"
    }

    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    def footer(): return f"\n\n━━━━━━━━━━━━━━\n🌐 {SITE}\n💰 Обуна шавед!"
    def markup():
        m=telebot.types.InlineKeyboardMarkup()
        m.add(telebot.types.InlineKeyboardButton("💰 Канали мо", url=SITE))
        m.add(telebot.types.InlineKeyboardButton("🌐 Сайти аслӣ", url=SITE))
        return m

    def get_all_fiat():
        try:
            r=requests.get("https://open.er-api.com/v6/latest/USD", headers=HEADERS, timeout=15).json()
            rates=r.get('rates',{})
            conv={}
            for k,v in rates.items():
                if v>0: conv[k]=10.9/v
            for k,v in FIAT_BASE.items(): conv[k]=v
            return conv
        except: return FIAT_BASE

    def get_price(cid_or_symbol):
        symbol = cid_or_symbol.upper()
        for s, c in CRYPTO_BASE.items():
            if c == cid_or_symbol:
                symbol = s
                break
        if symbol in ["USDT","USDC","DAI"]: return 1.0

        # 1. Coinbase - беҳтарин, ҳеҷ гоҳ банд намешавад!
        try:
            url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
            r = requests.get(url, headers=HEADERS, timeout=8).json()
            if 'data' in r and 'amount' in r['data']:
                p = float(r['data']['amount'])
                print(f"Coinbase OK {symbol}={p}")
                return p
        except Exception as e:
            print(f"Coinbase fail {symbol}: {e}")

        # 2. Binance бо User-Agent
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
            r = requests.get(url, headers=HEADERS, timeout=8).json()
            if 'price' in r:
                p = float(r['price'])
                print(f"Binance OK {symbol}={p}")
                return p
        except Exception as e:
            print(f"Binance fail {symbol}: {e}")

        # 3. CoinCap
        try:
            # id лозим
            cid = CRYPTO_BASE.get(symbol, symbol.lower())
            url = f"https://api.coincap.io/v2/assets/{cid}"
            r = requests.get(url, headers=HEADERS, timeout=8).json()
            if 'data' in r and 'priceUsd' in r['data']:
                p = float(r['data']['priceUsd'])
                print(f"CoinCap OK {symbol}={p}")
                return p
        except Exception as e:
            print(f"CoinCap fail {symbol}: {e}")

        # 4. CryptoCompare
        try:
            url = f"https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USD"
            r = requests.get(url, headers=HEADERS, timeout=8).json()
            if 'USD' in r:
                p = float(r['USD'])
                print(f"CryptoCompare OK {symbol}={p}")
                return p
        except Exception as e:
            print(f"CryptoCompare fail {symbol}: {e}")

        # 5. CoinGecko охирин
        try:
            cid = CRYPTO_BASE.get(symbol, cid_or_symbol)
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd"
            r = requests.get(url, headers=HEADERS, timeout=8).json()
            if cid in r and 'usd' in r[cid]:
                p = float(r[cid]['usd'])
                print(f"CoinGecko OK {symbol}={p}")
                return p
        except Exception as e:
            print(f"CoinGecko fail {symbol}: {e}")

        return None

    def search_crypto(q):
        # Binance зуд
        try:
            sym = q.upper().strip()
            if 2 <= len(sym) <= 5:
                p = get_price(sym)
                if p: return sym, sym, p
        except: pass
        # CoinGecko search + price
        try:
            res=requests.get(f"https://api.coingecko.com/api/v3/search?query={q}", headers=HEADERS, timeout=10).json()
            coins=res.get('coins',[])
            if coins:
                cid=coins[0]['id']
                sym=coins[0]['symbol'].upper()
                name=coins[0]['name']
                price=get_price(cid)
                if not price: price=get_price(sym)
                return sym,name,price
        except: pass
        return None,None,None

    def find_code(t):
        tl=t.lower()
        if "сом" in tl and "самсунг" not in tl: return "USD_SPECIAL"
        if "рубл" in tl or "рубул" in tl or "rubl" in tl: return "RUB"
        if "доллар" in tl or "долар" in tl or "dollar" in tl or "usd" in tl: return "USD"
        if "евро" in tl or "eur" in tl: return "EUR"
        if "йена" in tl or "jpy" in tl: return "JPY"
        if "вон" in tl or "krw" in tl: return "KRW"
        if "сум" in tl or "uzs" in tl: return "UZS"
        if "тенге" in tl or "kzt" in tl: return "KZT"
        if "афгон" in tl or "afn" in tl: return "AFN"
        if "биткоин" in tl or "btc" in tl or "bitcoin" in tl: return "BTC"
        if "эфир" in tl: return "ETH"
        if "доге" in tl or "doge" in tl: return "DOGE"
        if "тон" in tl: return "TON"
        if "рипл" in tl or "xrp" in tl: return "XRP"
        if "солана" in tl or "sol" in tl: return "SOL"
        if "трон" in tl or "trx" in tl: return "TRX"
        if "тетер" in tl or "usdt" in tl: return "USDT"
        if "бнб" in tl or "bnb" in tl: return "BNB"
        if "авакс" in tl or "avax" in tl: return "AVAX"
        if "шиба" in tl or "shib" in tl: return "SHIB"
        if "пепе" in tl or "pepe" in tl: return "PEPE"
        if "бонк" in tl or "bonk" in tl: return "BONK"
        up=t.upper()
        m=re.search(r'\b[A-Z]{3,5}\b', up)
        if m: return m.group(0)
        return None

    @bot.message_handler(commands=['start'])
    def start_cmd(message):
        kb=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
        kb.add(telebot.types.KeyboardButton("Сом чанд"),telebot.types.KeyboardButton("Рубл чанд"),telebot.types.KeyboardButton("Доллар чанд"))
        kb.add(telebot.types.KeyboardButton("BTC"),telebot.types.KeyboardButton("ETH"),telebot.types.KeyboardButton("PEPE"))
        kb.add(telebot.types.KeyboardButton("14 курс"),telebot.types.KeyboardButton("160 пул"),telebot.types.KeyboardButton("100 крипто"))
        bot.send_message(message.chat.id, f"✅ Тайёр! 160 пул + 100 крипто!\n🌐 {SITE}", reply_markup=kb)

    @bot.message_handler(content_types=['text'])
    def text_handler(message):
        try:
            txt=message.text
            low=txt.lower()
            code=find_code(txt)
            print(f"📩 {txt} -> {code}")

            if "10 крипто" in low or "100 крипто" in low or "хамаи крипто" in low or "ҳамаи крипто" in low:
                try:
                    msg="💰 ТОП 20 КРИПТО (Live):\n\n"
                    for s in list(CRYPTO_BASE.keys())[:20]:
                        p=get_price(s)
                        if p:
                            msg+=f"• {s}: {p:.4f} $\n"
                        else:
                            msg+=f"• {s}: ҳозир банд\n"
                    msg+=f"\n🚀 Ҳамаро медонам!{footer()}"
                    bot.send_message(message.chat.id, msg, reply_markup=markup())
                except Exception as e:
                    print(e)
                    bot.send_message(message.chat.id, f"⏳ Бандаст{footer()}", reply_markup=markup())
                return

            if code=="USD_SPECIAL" or "сом чанд" in low:
                rates=get_all_fiat()
                bot.send_message(message.chat.id, f"💰 1 USD = {rates.get('USD',10.9):.2f} TJS\n💶 1 EUR = {rates.get('EUR',11.85):.2f} TJS\n💴 1 RUB = {rates.get('RUB',0.115):.4f} TJS{footer()}", reply_markup=markup())
                return

            if "160 пул" in low or "хамаи пул" in low:
                rates=get_all_fiat()
                msg="🌍 160+ ПУЛИ ҶАҲОН (40-то):\n\n"
                for k,v in list(sorted(rates.items()))[:40]:
                    msg+=f"• 1 {k} = {v:.4f} TJS\n"
                msg+=f"\n...ҳамагӣ {len(rates)} пул!{footer()}"
                bot.send_message(message.chat.id, msg, reply_markup=markup())
                return

            if "курс" in low and "крипто" not in low:
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
                    bot.send_message(message.chat.id, f"💰 1 {code} = {rates[code]:.6f} TJS\n💵 100 {code} = {rates[code]*100:.2f} TJS{footer()}", reply_markup=markup())
                    return
                if code in CRYPTO_BASE or len(code)>=2:
                    p=get_price(code if code in CRYPTO_BASE else CRYPTO_BASE.get(code, code))
                    if not p:
                        p=get_price(code)
                    if p:
                        bot.send_message(message.chat.id, f"🟡 {code}:\n🟢 {p} $\n🔴 {p*10.9:.4f} TJS{footer()}", reply_markup=markup())
                        return
                    sym,name,price=search_crypto(code.lower())
                    if price:
                        bot.send_message(message.chat.id, f"🟡 {sym} ({name}):\n🟢 {price} $\n🔴 {price*10.9:.6f} TJS{footer()}", reply_markup=markup())
                        return

            clean=re.sub(r'чанд|чика|сколка|price|нарх|курс|пул', '', low).strip()
            clean=re.sub(r'[^a-zA-Z0-9]', '', clean).strip()
            if len(clean)>=2:
                sym,name,price=search_crypto(clean)
                if price:
                    bot.send_message(message.chat.id, f"🟡 {sym} ({name}):\n🟢 {price:.8f} $\n🔴 {price*10.9:.4f} TJS{footer()}", reply_markup=markup())
                    return

            rates=get_all_fiat()
            bot.send_message(message.chat.id, f"💱 1 USD = {rates.get('USD',10.9):.2f} TJS\nНавиш: Сом чанд, Рубл чанд, PEPE чанд{footer()}", reply_markup=markup())

        except Exception as e:
            print(f"Error: {e}")
            try: bot.send_message(message.chat.id, f"⚠️ Хато{footer()}", reply_markup=markup())
            except: pass

    app = Flask(__name__)
    @app.route('/')
    def home(): return "✅ Bot Live - Coinbase + Binance + CoinCap"

    def run_bot():
        while True:
            try:
                print("🚀 Polling...")
                bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
            except Exception as e:
                print(f"Polling error: {e}")
                time.sleep(10)

    if __name__ == "__main__":
        threading.Thread(target=run_bot, daemon=True).start()
        print("✅ Flask on 10000")
        app.run(host="0.0.0.0", port=10000)
