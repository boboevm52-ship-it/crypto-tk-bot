import os, requests, threading, time, re
from flask import Flask
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
print(f"Token ok: {bool(BOT_TOKEN)}")

if not BOT_TOKEN or ":" not in BOT_TOKEN:
    app = Flask(__name__)
    @app.route('/')
    def home(): return "BOT_TOKEN нест!"
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=10000)
else:
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
        time.sleep(1)
    except: pass

    SITE = "https://cryptotj.blogspot.com"
    
    # 160+ ПУЛИ ҶАҲОН
    FIAT_BASE = {"USD":10.90,"EUR":11.85,"RUB":0.115,"GBP":12.34,"TRY":1.37,"CHF":11.17,"AED":2.51,"SAR":2.45,"INR":0.097,"KZT":0.022,"CNY":1.51,"KGS":0.124,"TMT":3.11,"UZS":0.000844,"JPY":0.073,"KRW":0.0081,"AFN":0.15,"AZN":6.41,"UAH":0.26,"BYN":3.33,"GEL":4.05,"AMD":0.028,"MDL":0.61,"BRL":2.15,"CAD":8.05,"AUD":7.15,"SGD":8.25}

    # 100+ КРИПТО
    CRYPTO_BASE = {
        "BTC":"bitcoin","ETH":"ethereum","BNB":"binancecoin","XRP":"ripple","SOL":"solana","DOGE":"dogecoin","TON":"the-open-network","ADA":"cardano","AVAX":"avalanche-2","SHIB":"shiba-inu","DOT":"polkadot","TRX":"tron","LINK":"chainlink","MATIC":"matic-network","LTC":"litecoin","BCH":"bitcoin-cash","UNI":"uniswap","XLM":"stellar","ATOM":"cosmos","ETC":"ethereum-classic","PEPE":"pepe","BONK":"bonk","NOT":"notcoin","PI":"pi-network","FLOKI":"floki","WIF":"dogwifcoin","WLD":"worldcoin","RENDER":"render-token","FET":"fetch-ai","INJ":"injective-protocol","USDT":"tether","USDC":"usd-coin","DAI":"dai","AAVE":"aave","ARB":"arbitrum","NEAR":"near","OP":"optimism","SUI":"sui","APT":"aptos","STX":"stacks","FIL":"filecoin","HBAR":"hedera","IMX":"immutable-x","MKR":"maker","TAO":"bittensor","RNDR":"render-token","GRT":"the-graph","RUNE":"thorchain","STRK":"starknet","SEI":"sei-network","JUP":"jupiter-exchange-solana","PYTH":"pyth-network","ENA":"ethena","W":"wormhole","TIA":"celestia","ONDO":"ondo-finance","PEOPLE":"constitutiondao","ENS":"ethereum-name-service","LDO":"lido-dao","FLOW":"flow","EGLD":"elrond-erd-2","SAND":"the-sandbox","MANA":"decentraland","AXS":"axie-infinity","CHZ":"chiliz","GALA":"gala","ENJ":"enjincoin","ZEC":"zcash","XMR":"monero","DASH":"dash","XTZ":"tezos","EOS":"eos","KAVA":"kava","KLAY":"klay-token","MINA":"mina-protocol","ROSE":"oasis-network","ONE":"harmony","ZIL":"zilliqa","QTUM":"qtum","BAT":"basic-attention-token","COMP":"compound-governance-token","SNX":"havven","1INCH":"1inch","CRV":"curve-dao-token","SUSHI":"sushi","YFI":"yearn-finance","BAL":"balancer","CAKE":"pancakeswap-token","ALGO":"algorand","VET":"vechain","ICP":"internet-computer","THETA":"theta-token","FTM":"fantom"
    }
    
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
        if sym in ["USDT","USDC","DAI","FDUSD"]: return 1.0

        # 1. MEXC - беҳтарин барои PEPE BONK
        try:
            r=requests.get(f"https://api.mexc.com/api/v3/ticker/price?symbol={sym}USDT", headers=H, timeout=5).json()
            if 'price' in r: return float(r['price'])
        except: pass
        # 2. Bybit
        try:
            r=requests.get(f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={sym}USDT", headers=H, timeout=5).json()
            lst=r.get('result',{}).get('list',[])
            if lst and lst[0].get('lastPrice'): return float(lst[0]['lastPrice'])
        except: pass
        # 3. Coinbase
        try:
            r=requests.get(f"https://api.coinbase.com/v2/prices/{sym}-USD/spot", headers=H, timeout=5).json()
            if 'data' in r and 'amount' in r['data']: return float(r['data']['amount'])
        except: pass
        # 4. Binance
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
        if "йена" in tl or "jpy" in tl: return "JPY"
        if "вон" in tl or "krw" in tl: return "KRW"
        if "сум" in tl or "uzs" in tl: return "UZS"
        if "тенге" in tl or "kzt" in tl: return "KZT"
        if "афгон" in tl or "afn" in tl: return "AFN"
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
        m=re.search(r'\b[A-Z]{3,5}\b', up)
        if m: return m.group(0)
        return None

    @bot.message_handler(commands=['start'])
    def start_cmd(message):
        kb=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
        kb.add(telebot.types.KeyboardButton("Сом чанд"),telebot.types.KeyboardButton("Рубл чанд"),telebot.types.KeyboardButton("Доллар чанд"))
        kb.add(telebot.types.KeyboardButton("BTC"),telebot.types.KeyboardButton("ETH"),telebot.types.KeyboardButton("PEPE"))
        kb.add(telebot.types.KeyboardButton("14 курс"),telebot.types.KeyboardButton("160 пул"),telebot.types.KeyboardButton("100 крипто"))
        bot.send_message(message.chat.id, f"✅ Тайёр! 160+ пул + 100+ крипто!\n\n💰 Сом чанд - курси сомонӣ\n🌍 160 пул - ҳамаи пули ҷаҳон\n💎 100 крипто - ҳамаи крипто\n\n🌐 {SITE}", reply_markup=kb)

    @bot.message_handler(content_types=['text'])
    def text_handler(message):
        try:
            txt=message.text
            low=txt.lower()
            code=find_code(txt)
            print(f"📩 {txt} -> {code}")

            if "100 крипто" in low or "хамаи крипто" in low or "ҳамаи крипто" in low:
                bot.send_message(message.chat.id, "⏳ 100 крипто ҷамъоварӣ... 15 сония сабр кун!")
                msg1="💰 100 КРИПТО - ҚИСМИ 1/4:\n\n"
                msg2="💰 100 КРИПТО - ҚИСМИ 2/4:\n\n"
                msg3="💰 100 КРИПТО - ҚИСМИ 3/4:\n\n"
                msg4="💰 100 КРИПТО - ҚИСМИ 4/4:\n\n"
                keys=list(CRYPTO_BASE.keys())
                for i, s in enumerate(keys[:25]):
                    p=get_price(s)
                    if p:
                        if p<0.01: msg1+=f"• {s}: {p:.8f} $\n"
                        else: msg1+=f"• {s}: {p:.4f} $\n"
                for s in keys[25:50]:
                    p=get_price(s)
                    if p:
                        if p<0.01: msg2+=f"• {s}: {p:.8f} $\n"
                        else: msg2+=f"• {s}: {p:.4f} $\n"
                for s in keys[50:75]:
                    p=get_price(s)
                    if p:
                        if p<0.01: msg3+=f"• {s}: {p:.8f} $\n"
                        else: msg3+=f"• {s}: {p:.4f} $\n"
                for s in keys[75:100]:
                    p=get_price(s)
                    if p:
                        if p<0.01: msg4+=f"• {s}: {p:.8f} $\n"
                        else: msg4+=f"• {s}: {p:.4f} $\n"
                
                bot.send_message(message.chat.id, msg1+footer(), reply_markup=markup())
                bot.send_message(message.chat.id, msg2+footer(), reply_markup=markup())
                bot.send_message(message.chat.id, msg3+footer(), reply_markup=markup())
                bot.send_message(message.chat.id, msg4+footer(), reply_markup=markup())
                return

            if "160 пул" in low or "хамаи пул" in low:
                rates=get_all_fiat()
                # 3 қисм мекунем чунки Telegram 4096 ҳарф қабул мекунад
                sorted_rates=sorted(rates.items())
                msg1="🌍 160 ПУЛ - ҚИСМИ 1/3:\n\n"
                msg2="🌍 160 ПУЛ - ҚИСМИ 2/3:\n\n"
                msg3="🌍 160 ПУЛ - ҚИСМИ 3/3:\n\n"
                for k,v in sorted_rates[:60]:
                    msg1+=f"• 1 {k} = {v:.4f} TJS\n"
                for k,v in sorted_rates[60:120]:
                    msg2+=f"• 1 {k} = {v:.4f} TJS\n"
                for k,v in sorted_rates[120:]:
                    msg3+=f"• 1 {k} = {v:.4f} TJS\n"
                
                bot.send_message(message.chat.id, msg1+footer(), reply_markup=markup())
                bot.send_message(message.chat.id, msg2+footer(), reply_markup=markup())
                bot.send_message(message.chat.id, msg3+footer(), reply_markup=markup())
                return

            if code=="USD_SPECIAL" or "сом чанд" in low:
                rates=get_all_fiat()
                bot.send_message(message.chat.id, f"💰 1 USD = {rates.get('USD',10.9):.2f} TJS\n💶 1 EUR = {rates.get('EUR',11.85):.2f} TJS\n💴 1 RUB = {rates.get('RUB',0.115):.4f} TJS\n💷 1 GBP = {rates.get('GBP',12.34):.4f} TJS{footer()}", reply_markup=markup())
                return

            if "14 курс" in low or "курс" in low and "крипто" not in low and "пул" not in low:
                rates=get_all_fiat()
                msg="💱 14 КУРСИ АСОСӢ:\n\n"
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
                p=get_price(code)
                if p:
                    if p<0.01: bot.send_message(message.chat.id, f"🟡 {code}:\n🟢 {p:.10f} $\n🔴 {p*10.9:.10f} TJS{footer()}", reply_markup=markup())
                    else: bot.send_message(message.chat.id, f"🟡 {code}:\n🟢 {p:.6f} $\n🔴 {p*10.9:.4f} TJS{footer()}", reply_markup=markup())
                    return

            rates=get_all_fiat()
            bot.send_message(message.chat.id, f"💱 1 USD = {rates.get('USD',10.9):.2f} TJS\nНавиш: Сом чанд, Рубл чанд, BTC, PEPE чанд{footer()}", reply_markup=markup())

        except Exception as e:
            print(f"Error: {e}")
            try: bot.send_message(message.chat.id, f"⚠️ Хато{footer()}", reply_markup=markup())
            except: pass

    app = Flask(__name__)
    @app.route('/')
    def home(): return "✅ Bot Live - 160 FIAT + 100 CRYPTO - MEXC+Bybit"

    def run_bot():
        while True:
            try:
                print("🚀 Polling started...")
                bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
            except Exception as e:
                print(f"Polling error: {e}")
                time.sleep(10)

    if __name__ == "__main__":
        threading.Thread(target=run_bot, daemon=True).start()
        print("✅ Flask on 10000")
        app.run(host="0.0.0.0", port=10000)
