import os, requests, threading, time, re
from flask import Flask
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
print(f"Token ok: {bool(BOT_TOKEN)}")

if not BOT_TOKEN or ":" not in BOT_TOKEN:
    app = Flask(__name__)
    @app.route('/')
    def home(): return "BOT_TOKEN нест!"
    app.run(host="0.0.0.0", port=10000)
else:
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
        time.sleep(1)
    except: pass

    SITE = "https://cryptotj.blogspot.com"
    FIAT_BASE = {"USD":10.90,"EUR":11.85,"RUB":0.115,"GBP":12.34,"TRY":1.37,"CHF":11.17,"AED":2.51,"SAR":2.45,"INR":0.097,"KZT":0.022,"CNY":1.51,"KGS":0.124,"TMT":3.11,"UZS":0.000844,"JPY":0.073,"KRW":0.0081,"AFN":0.15,"AZN":6.41,"AMD":0.028,"BYN":3.33,"GEL":4.05,"MDL":0.60,"TJS":1.0,"UAH":0.26}
    CRYPTO_BASE = {"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","BNB":"binancecoin","XRP":"ripple","DOGE":"dogecoin","TON":"the-open-network","USDT":"tether","TRX":"tron","AVAX":"avalanche-2","SHIB":"shiba-inu","PEPE":"pepe","NOT":"notcoin","PI":"pi-network","BONK":"bonk"}

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

    def get_price(cid):
        try:
            r=requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd", timeout=15).json()
            return r.get(cid,{}).get('usd')
        except: return None

    def search_crypto(q):
        try:
            res=requests.get(f"https://api.coingecko.com/api/v3/search?query={q}", timeout=15).json()
            coins=res.get('coins',[])
            if coins:
                cid=coins[0]['id']
                sym=coins[0]['symbol'].upper()
                name=coins[0]['name']
                price=get_price(cid)
                return sym,name,price
        except: pass
        return None,None,None

    def find_code(t):
        tl=t.lower()
        # Тоҷикӣ
        if "сом" in tl and "самсунг" not in tl: return "USD_SPECIAL"
        if "рубл" in tl or "рубул" in tl or "рубь" in tl or "rubl" in tl: return "RUB"
        if "доллар" in tl or "долар" in tl or "dollar" in tl or "usd" in tl or tl.strip()=="$": return "USD"
        if "евро" in tl or "eur" in tl: return "EUR"
        if "йена" in tl or "yena" in tl or "jpy" in tl or "йен" in tl: return "JPY"
        if "вон" in tl or "won" in tl or "krw" in tl: return "KRW"
        if "сум" in tl or "so'm" in tl or "uzs" in tl: return "UZS"
        if "тенге" in tl or "kzt" in tl: return "KZT"
        if "афгон" in tl or "afgh" in tl or "afn" in tl: return "AFN"
        if "манат" in tl or "azn" in tl: return "AZN"
        if "лари" in tl or "gel" in tl: return "GEL"
        if "сомон" in tl: return "USD"
        if "гривна" in tl or "uah" in tl: return "UAH"
        if "лира" in tl or "try" in tl: return "TRY"
        if "фунт" in tl or "gbp" in tl: return "GBP"
        if "юан" in tl or "cny" in tl or "йуан" in tl: return "CNY"
        if "дирхам" in tl or "aed" in tl: return "AED"
        if "риал" in tl or "sar" in tl: return "SAR"
        # Крипто
        if "биткоин" in tl or "btc" in tl or "bitcoin" in tl: return "BTC"
        if "эфир" in tl or " eth" in tl: return "ETH"
        if "доге" in tl or "дож" in tl or "doge" in tl: return "DOGE"
        if "тон" in tl or " ton" in tl: return "TON"
        if "рипл" in tl or "xrp" in tl: return "XRP"
        if "солана" in tl or "sol" in tl: return "SOL"
        if "трон" in tl or "trx" in tl: return "TRX"
        if "тетер" in tl or "usdt" in tl: return "USDT"
        if "бнб" in tl or "bnb" in tl: return "BNB"
        if "авакс" in tl or "avax" in tl: return "AVAX"
        if "шиба" in tl or "shib" in tl: return "SHIB"
        if "пепе" in tl or "pepe" in tl: return "PEPE"
        # Коди 3-ҳарфӣ
        up=t.upper()
        m=re.search(r'\b[A-Z]{3,5}\b', up)
        if m:
            c=m.group(0)
            if len(c)>=3: return c
        return None

    @bot.message_handler(commands=['start'])
    def start_cmd(message):
        kb=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
        kb.add(telebot.types.KeyboardButton("Сом чанд"),telebot.types.KeyboardButton("Рубл чанд"),telebot.types.KeyboardButton("Доллар чанд"))
        kb.add(telebot.types.KeyboardButton("Йена чанд"),telebot.types.KeyboardButton("Евро чанд"),telebot.types.KeyboardButton("Вон чанд"))
        kb.add(telebot.types.KeyboardButton("BTC"),telebot.types.KeyboardButton("ETH"),telebot.types.KeyboardButton("DOGE"))
        kb.add(telebot.types.KeyboardButton("TON"),telebot.types.KeyboardButton("PEPE"),telebot.types.KeyboardButton("SHIB"))
        kb.add(telebot.types.KeyboardButton("14 курс"),telebot.types.KeyboardButton("160 пул"),telebot.types.KeyboardButton("10 крипто"))
        bot.send_message(message.chat.id, f"✅ Тайёр! Ҳамаи пулҳо!\n\n🌍 160+ давлат: Рубл, Доллар, Йена, Вон, Афғонӣ, Манат, Евро...\n🚀 20000+ крипто: BTC, ETH, PEPE, SHIB, PI, NOT, BONK...\n\nНавиш:\n• Сом чанд\n• Рубл чанд\n• Йена чанд\n• PEPE чанд\n🌐 {SITE}", reply_markup=kb)

    @bot.message_handler(content_types=['text'])
    def text_handler(message):
        try:
            txt=message.text
            low=txt.lower()
            code=find_code(txt)
            print(f"📩 {txt} -> {code}")

            if code=="USD_SPECIAL" or "сом чанд" in low or low.strip()=="сом":
                r=get_all_fiat()
                bot.send_message(message.chat.id, f"💰 Курси Сомонӣ имрӯз:\n\n💵 1 USD = {r.get('USD',10.9):.2f} TJS\n💶 1 EUR = {r.get('EUR',11.85):.2f} TJS\n💴 1 RUB = {r.get('RUB',0.115):.4f} TJS\n💴 1 JPY = {r.get('JPY',0.073):.4f} TJS\n\nБоз: Йена чанд, Вон чанд, Афғонӣ чанд{footer()}", reply_markup=markup())
                return

            if "160 пул" in low or "хамаи пул" in low or "ҳамаи пул" in low:
                rates=get_all_fiat()
                msg="🌍 160+ ПУЛИ ҶАҲОН (40-тои аввал):\n\n"
                i=0
                for k,v in sorted(rates.items()):
                    if i>=40: break
                    msg+=f"• 1 {k} = {v:.4f} TJS\n"
                    i+=1
                msg+=f"\n...ҳамагӣ {len(rates)} пул!\nНавиш: KRW чанд, AFN чанд{footer()}"
                bot.send_message(message.chat.id, msg, reply_markup=markup())
                return

            if code:
                rates=get_all_fiat()
                if code in rates:
                    rv=rates[code]
                    bot.send_message(message.chat.id, f"💰 1 {code} = {rv:.6f} TJS\n💵 100 {code} = {rv*100:.2f} TJS{footer()}", reply_markup=markup())
                    return
                if code in CRYPTO_BASE:
                    p=get_price(CRYPTO_BASE[code])
                    if p:
                        bot.send_message(message.chat.id, f"🟡 {code}:\n🟢 {p} $\n🔴 {p*10.9:.4f} TJS{footer()}", reply_markup=markup())
                    else:
                        bot.send_message(message.chat.id, f"⏳ {code} ҳозир банд{footer()}", reply_markup=markup())
                    return
                # Агар коди нав - масалан KRW
                if len(code)>=3:
                    p_rates=get_all_fiat()
                    if code in p_rates:
                        bot.send_message(message.chat.id, f"💰 1 {code} = {p_rates[code]:.6f} TJS{footer()}", reply_markup=markup())
                        return
                    # Криптои нав
                    sym,name,price=search_crypto(code.lower())
                    if price:
                        bot.send_message(message.chat.id, f"🟡 {sym} ({name}):\n🟢 {price} $\n🔴 {price*10.9:.6f} TJS{footer()}", reply_markup=markup())
                        return

            clean=re.sub(r'чанд|чика|сколка|price|нарх|курс|пул', '', low).strip()
            clean=re.sub(r'[^a-zA-Z0-9]', '', clean).strip()
            if len(clean)>=2:
                sym,name,price=search_crypto(clean)
                if price:
                    bot.send_message(message.chat.id, f"🟡 {sym} ({name}):\n🟢 {price:.10f} $\n🔴 {price*10.9:.6f} TJS{footer()}", reply_markup=markup())
                    return

            if "курс" in low:
                rates=get_all_fiat()
                msg="💱 14 КУРСИ АСОСӢ:\n\n"
                for k in ["USD","EUR","RUB","GBP","TRY","JPY","KRW","AFN","AZN","KZT","UZS","CNY","AED","SAR"]:
                    msg+=f"• 1 {k} = {rates.get(k,0):.4f} TJS\n"
                msg+=f"\n🌍 Ҳама: 160 пул навиш{footer()}"
                bot.send_message(message.chat.id, msg, reply_markup=markup())
                return

            if "крипто" in low:
                ids=",".join(CRYPTO_BASE.values())
                try:
                    data=requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd", timeout=15).json()
                    msg="💰 15 КРИПТО:\n\n"
                    for s,c in CRYPTO_BASE.items():
                        msg+=f"• {s}: {data.get(c,{}).get('usd','-')} $\n"
                    msg+=f"\n🚀 Ҳамаро медонам: PEPE чанд навиш{footer()}"
                    bot.send_message(message.chat.id, msg, reply_markup=markup())
                except:
                    bot.send_message(message.chat.id, f"⏳ Бандаст{footer()}", reply_markup=markup())
                return

            rates=get_all_fiat()
            bot.send_message(message.chat.id, f"💱 Курси имрӯз:\n💵 1 USD = {rates.get('USD',10.9):.2f} TJS\nНавиш:\n• Сом чанд\n• Йена чанд\n• PEPE чанд{footer()}", reply_markup=markup())

        except Exception as e:
            print(f"Error: {e}")
            try: bot.send_message(message.chat.id, f"⚠️ Хато{footer()}", reply_markup=markup())
            except: pass

    app = Flask(__name__)
    @app.route('/')
    def home(): return "✅ Bot Live - 160+ FIAT + 20000+ CRYPTO"

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
        app.run(host="0.0.0.0", port=10000)
