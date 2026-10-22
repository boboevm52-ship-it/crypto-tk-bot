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

    def footer(): return f"\n\n━━━━━━━━━━━━━━\n🌐 {SITE}\n💰 Обуна шавед!"
    def markup():
        m=telebot.types.InlineKeyboardMarkup()
        m.add(telebot.types.InlineKeyboardButton("💰 Канали мо", url=SITE))
        m.add(telebot.types.InlineKeyboardButton("🌐 Сайти аслӣ", url=SITE))
        return m

    def get_all_fiat():
        try:
            r=requests.get("https://open.er-api.com/v6/latest/USD", timeout=15).json()
            rates=r.get('rates',{})
            conv={}
            for k,v in rates.items():
                if v>0: conv[k]=10.9/v
            for k,v in FIAT_BASE.items(): conv[k]=v
            return conv
        except: return FIAT_BASE

    def get_price(cid_or_symbol):
        # 1. CoinGecko
        try:
            r=requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cid_or_symbol}&vs_currencies=usd", timeout=8).json()
            price=r.get(cid_or_symbol,{}).get('usd')
            if price: 
                print(f"CoinGecko ok: {cid_or_symbol} = {price}")
                return price
        except Exception as e:
            print(f"CoinGecko fail: {e}")

        # 2. Binance - асосӣ!
        try:
            symbol = cid_or_symbol.upper()
            for s, c in CRYPTO_BASE.items():
                if c == cid_or_symbol:
                    symbol = s
                    break
            if symbol in ["USDT","USDC","DAI"]: return 1.0
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
            r = requests.get(url, timeout=8).json()
            if 'price' in r:
                print(f"Binance ok: {symbol} = {r['price']}")
                return float(r['price'])
        except Exception as e:
            print(f"Binance fail: {e}")

        # 3. CryptoCompare
        try:
            symbol = cid_or_symbol.upper()
            for s, c in CRYPTO_BASE.items():
                if c == cid_or_symbol:
                    symbol = s
                    break
            url = f"https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USD"
            r = requests.get(url, timeout=8).json()
            if 'USD' in r:
                print(f"CryptoCompare ok: {symbol} = {r['USD']}")
                return float(r['USD'])
        except Exception as e:
            print(f"CryptoCompare fail: {e}")

        return None

    def search_crypto(q):
        # 1. Binance зуд
        try:
            sym = q.upper().strip()
            if 2 <= len(sym) <= 5 and sym not in ["ЧАНД","СОМ","РУБЛ"]:
                url = f"https://api.binance.com/api/v3/ticker/price?symbol={sym}USDT"
                r = requests.get(url, timeout=5).json()
                if 'price' in r:
                    return sym, sym, float(r['price'])
        except: pass

        # 2. CoinGecko search
        try:
            res=requests.get(f"https://api.coingecko.com/api/v3/search?query={q}", timeout=10).json()
            coins=res.get('coins',[])
            if coins:
                cid=coins[0]['id']
                sym=coins[0]['symbol'].upper()
                name=coins[0]['name']
                price=get_price(cid)
                if not price:
                    try:
                        r2=requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}USDT", timeout=5).json()
                        if 'price' in r2: price=float(r2['price'])
                    except: pass
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
                    msg="💰 ТОП 20 КРИПТО (Live Binance):\n\n"
                    for s in list(CRYPTO_BASE.keys())[:20]:
                        p=get_price(CRYPTO_BASE[s])
                        if not p:
                            # Кӯшиши мустақим бо символ
                            try:
                                r=requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={s}USDT", timeout=5).json()
                                if 'price' in r: p=float(r['price'])
                            except: pass
                        msg+=f"• {s}: {p if p else 'банд'} $\n"
                    msg+=f"\n🚀 Ҳамаро медонам: PEPE чанд, BONK чанд!{footer()}"
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
                if code in CRYPTO_BASE:
                    p=get_price(CRYPTO_BASE[code])
                    if p:
                        bot.send_message(message.chat.id, f"🟡 {code}:\n🟢 {p} $\n🔴 {p*10.9:.2f} TJS{footer()}", reply_markup=markup())
                    else:
                        bot.send_message(message.chat.id, f"⏳ {code} ҳозир банд, дубора кӯшиш кун{footer()}", reply_markup=markup())
                    return
                if len(code)>=2:
                    sym,name,price=search_crypto(code.lower())
                    if price:
                        bot.send_message(message.chat.id, f"🟡 {sym} ({name}):\n🟢 {price} $\n🔴 {price*10.9:.4f} TJS{footer()}", reply_markup=markup())
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
    def home(): return "✅ Bot Live - 160+ FIAT + 100+ CRYPTO - Binance"

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
