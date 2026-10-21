import os, threading, time
from flask import Flask
import requests
import telebot

TOKEN = os.getenv("BOT_TOKEN")
SITE = "https://cryptotj-dushanbe.blogspot.com"

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is alive!"

# --- Flask фавран кор мекунад ---
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

# --- Bot дар паси پرده ---
def run_bot():
    time.sleep(3) # Flask аввал кушода шавад
    bot = telebot.TeleBot(TOKEN, threaded=False)
    try:
        bot.remove_webhook()
        time.sleep(2)
    except: pass

    def get_c():
        c="bitcoin,ethereum,binancecoin,solana,dogecoin,toncoin,tether,tron,cardano,ripple,shiba-inu,avalanche-2,polkadot,litecoin"
        u=f"https://api.coingecko.com/api/v3/simple/price?ids={c}&vs_currencies=usd"
        return requests.get(u,headers={"User-Agent":"Mozilla/5.0"},timeout=15).json()
    def get_f():
        try:
            fr=requests.get("https://api.exchangerate-api.com/v4/latest/USD",timeout=10).json()
            return fr['rates']['TJS'],fr['rates']['TJS']/fr['rates']['RUB'],fr['rates']['TJS']/fr['rates']['EUR']
        except: return 10.85,0.1220,11.80
    def ft(): return f"\n\n🌐 {SITE}\n📲 Обуна!"

    @bot.message_handler(commands=['start','kurs'])
    def kurs(m):
        try:
            r=get_c();usd,rub,eur=get_f()
            s=f"💱 14 КУРС {time.strftime('%H:%M')}\n\n"
            s+=f"BTC ${r['bitcoin']['usd']:,.0f}\nETH ${r['ethereum']['usd']:,.0f}\nBNB ${r['binancecoin']['usd']:,.0f}\nSOL ${r['solana']['usd']:,.0f}\nDOGE ${r['dogecoin']['usd']:.3f}\nTON ${r['toncoin']['usd']:.2f}\nUSDT ${r['tether']['usd']:.2f}\nTRX ${r['tron']['usd']:.3f}\nADA ${r['cardano']['usd']:.2f}\nXRP ${r['ripple']['usd']:.2f}\nSHIB ${r['shiba-inu']['usd']:.6f}\nAVAX ${r['avalanche-2']['usd']:.0f}\nDOT ${r['polkadot']['usd']:.2f}\nLTC ${r['litecoin']['usd']:.0f}\n\n💵 {usd:.2f} TJS\n₽ {rub:.4f} TJS\n💶 {eur:.2f} TJS"+ft()
            bot.reply_to(m,s)
        except Exception as e: bot.reply_to(m,f"Хато:{e}")

    @bot.message_handler(func=lambda m:True)
    def qa(m):
        t=m.text.lower()
        try:
            r=get_c();usd,rub,eur=get_f()
            if "рубл" in t or "rub" in t: bot.reply_to(m,f"₽ 1 Рубл = {rub:.4f} TJS\n1000 ₽ = {rub*1000:.2f} TJS"+ft())
            elif "доллар" in t: bot.reply_to(m,f"💵 1$ = {usd:.2f} TJS"+ft())
            elif "btc" in t or "биткоин" in t: bot.reply_to(m,f"₿ BTC ${r['bitcoin']['usd']:,.0f}"+ft())
            else: bot.reply_to(m,f"Навиш: Рубл чанд? Доллар чанд? /kurs"+ft())
        except Exception as e: bot.reply_to(m,f"Хато:{e}")

    while True:
        try: bot.infinity_polling(timeout=20,long_polling_timeout=20)
        except: time.sleep(5)

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    run_flask()
