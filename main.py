
import os, requests, threading, time
from flask import Flask
import telebot

print("🚀 Starting...")

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
print(f"Token exists: {bool(BOT_TOKEN)}")

if not BOT_TOKEN or ":" not in BOT_TOKEN:
    print("❌ BOT_TOKEN нодуруст! Дар Render Environment санҷ!")
    # Барои он ки Render хомӯш нашавад, Flask-ро ҳамин тавр сар мекунем
    app = Flask(__name__)
    @app.route('/')
    def home():
        return "❌ BOT_TOKEN нест! Дар Environment гузор!"
    app.run(host="0.0.0.0", port=10000)
else:
    bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook", timeout=10)
        time.sleep(1)
    except:
        pass

    FIAT = {"USD":10.90,"EUR":11.85,"RUB":0.115,"GBP":12.34,"TRY":1.37,"CHF":11.17,"AED":2.51,"SAR":2.45,"INR":0.097,"KZT":0.022,"CNY":1.51,"KGS":0.124,"TMT":3.11,"UZS":0.000844}
    CRYPTO_IDS = {"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","BNB":"binancecoin","XRP":"ripple","DOGE":"dogecoin","TON":"the-open-network","USDT":"tether","TRX":"tron","AVAX":"avalanche-2"}
    SITE = "https://cryptotj.blogspot.com"

    def footer(): return f"\n\n🌐 {SITE}"
    def markup():
        m = telebot.types.InlineKeyboardMarkup()
        m.add(telebot.types.InlineKeyboardButton("💰 Канали мо", url=SITE))
        return m
    def get_price(cid):
        try:
            r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd", timeout=10).json()
            return r.get(cid,{}).get('usd')
        except: return None
    def find_code(t):
        t=t.lower()
        if "рубл" in t or "рубул" in t or "rub" in t: return "RUB"
        if "доллар" in t or "долар" in t or "usd" in t: return "USD"
        if "евро" in t or "eur" in t: return "EUR"
        if "биткоин" in t or "btc" in t or "bitcoin" in t: return "BTC"
        if "доге" in t or "дож" in t or "doge" in t: return "DOGE"
        if "тон" in t or " ton" in t: return "TON"
        if "рипл" in t or "xrp" in t: return "XRP"
        if "солана" in t or "sol" in t: return "SOL"
        if "трон" in t or "trx" in t: return "TRX"
        if "тетер" in t or "usdt" in t: return "USDT"
        return None

    @bot.message_handler(commands=['start'])
    def start_cmd(message):
        kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        kb.add(telebot.types.KeyboardButton("BTC"),telebot.types.KeyboardButton("ETH"),telebot.types.KeyboardButton("Рубл чанд"))
        kb.add(telebot.types.KeyboardButton("Биткоин чанд"),telebot.types.KeyboardButton("Тон чанд"),telebot.types.KeyboardButton("DOGE"))
        kb.add(telebot.types.KeyboardButton("14 курс"),telebot.types.KeyboardButton("10 крипто"))
        bot.send_message(message.chat.id, f"✅ Тайёр! 14 курс + 10 крипто\n🌐 {SITE}", reply_markup=kb)

    @bot.message_handler(content_types=['text'])
    def text_handler(message):
        try:
            code = find_code(message.text)
            if code in FIAT:
                bot.send_message(message.chat.id, f"💰 1 {code} = {FIAT[code]:.4f} TJS{footer()}", reply_markup=markup())
                return
            if code in CRYPTO_IDS:
                p = get_price(CRYPTO_IDS[code])
                if p: bot.send_message(message.chat.id, f"🟡 {code}: {p} $ = {p*10.9:.2f} TJS{footer()}", reply_markup=markup())
                return
            if "курс" in message.text.lower():
                msg="💱 14 КУРС:\n\n"+"\n".join([f"• 1 {k} = {v:.4f} TJS" for k,v in FIAT.items()])+footer()
                bot.send_message(message.chat.id, msg, reply_markup=markup())
                return
            bot.send_message(message.chat.id, f"Навиш: Рубл чанд, Биткоин чанд{footer()}", reply_markup=markup())
        except Exception as e:
            print(f"Handler error: {e}")

    app = Flask(__name__)
    @app.route('/')
    def home(): return "✅ Bot Live - cryptotj.blogspot.com"

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
        print("✅ Flask starting on 10000")
        app.run(host="0.0.0.0", port=10000)
