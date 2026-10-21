import os, threading, time
from flask import Flask
import telebot, requests

TOKEN = os.getenv("BOT_TOKEN")
MY_SITE = "https://cryptotj-dushanbe.blogspot.com"

bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
time.sleep(1)
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Bot is alive!"

def get_crypto():
    coins = "bitcoin,ethereum,binancecoin,solana,dogecoin,toncoin,tether,tron,cardano,ripple,shiba-inu,avalanche-2,polkadot,litecoin"
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd"
    return requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15).json()

def get_fiat():
    try:
        fr = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()
        return fr['rates']['TJS'], fr['rates']['TJS']/fr['rates']['RUB'], fr['rates']['TJS']/fr['rates']['EUR']
    except:
        return 10.85, 0.1220, 11.80

def footer():
    return f"\n\n🌐 Сайти мо: {MY_SITE}\n📲 Обуна шавед!"

@bot.message_handler(commands=['start','kurs'])
def kurs_cmd(message):
    try:
        r = get_crypto()
        usd, rub, eur = get_fiat()
        msg = f"💱 14 КУРС {time.strftime('%d.%m %H:%M')}\n\n"
        msg += f"₿ BTC ${r.get('bitcoin',{}).get('usd',0):,.0f}\nΞ ETH ${r.get('ethereum',{}).get('usd',0):,.0f}\nBNB ${r.get('binancecoin',{}).get('usd',0):,.0f}\nSOL ${r.get('solana',{}).get('usd',0):,.0f}\nDOGE ${r.get('dogecoin',{}).get('usd',0):,.3f}\n"
        msg += f"TON ${r.get('toncoin',{}).get('usd',0):,.2f}\nUSDT ${r.get('tether',{}).get('usd',0):,.2f}\nTRX ${r.get('tron',{}).get('usd',0):,.3f}\nADA ${r.get('cardano',{}).get('usd',0):,.2f}\nXRP ${r.get('ripple',{}).get('usd',0):,.2f}\n"
        msg += f"SHIB ${r.get('shiba-inu',{}).get('usd',0):,.6f}\nAVAX ${r.get('avalanche-2',{}).get('usd',0):,.0f}\nDOT ${r.get('polkadot',{}).get('usd',0):,.2f}\nLTC ${r.get('litecoin',{}).get('usd',0):,.0f}\n"
        msg += f"\n💵 Доллар: {usd:.2f} TJS\n₽ Рубл: {rub:.4f} TJS\n💶 Евро: {eur:.2f} TJS"
        msg += footer()
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"Хато: {e}")

@bot.message_handler(func=lambda m: True)
def qa(message):
    text = message.text.lower()
    try:
        r = get_crypto()
        usd, rub, eur = get_fiat()
        if "биткоин" in text or "btc" in text or "биток" in text:
            p = r.get('bitcoin',{}).get('usd',0)
            bot.reply_to(message, f"₿ Биткоин: ${p:,.2f}\nБо 14%: ${p*1.14:,.2f}{footer()}")
        elif "эфир" in text or "eth" in text:
            p = r.get('ethereum',{}).get('usd',0)
            bot.reply_to(message, f"Ξ Эфириум: ${p:,.2f}{footer()}")
        elif "доги" in text or "doge" in text:
            bot.reply_to(message, f"🐶 DOGE: ${r.get('dogecoin',{}).get('usd',0):,.4f}{footer()}")
        elif "тон" in text or "ton" in text:
            bot.reply_to(message, f"💎 TON: ${r.get('toncoin',{}).get('usd',0):,.2f}{footer()}")
        elif "доллар" in text or "usd" in text or "$" in text:
            bot.reply_to(message, f"💵 1 Доллар = {usd:.2f} сомонӣ\nБо 14% = {usd*1.14:.2f} TJS\n1000$ = {usd*1000:.0f} TJS{footer()}")
        elif "рубл" in text or "рубл" in text or "rub" in text or "₽" in text:
            bot.reply_to(message, f"₽ 1 Рубл = {rub:.4f} сомонӣ\nБо 14% = {rub*1.14:.4f} TJS\n1000 ₽ = {rub*1000:.2f} сомонӣ{footer()}")
        elif "евро" in text or "eur" in text:
            bot.reply_to(message, f"💶 1 Евро = {eur:.2f} сомонӣ{footer()}")
        elif "салом" in text:
            bot.reply_to(message, f"Салом! 👋\nСавол деҳ: 'Рубл чанд?', 'Биткоин чанд?' ё /kurs навиш{footer()}")
        else:
            bot.reply_to(message, f"Нафаҳмидам 🤔\nНавиш:\n• Рубл чанд?\n• Доллар чанд?\n• Биткоин чанд?\n• /kurs - 14 курс{footer()}")
    except Exception as e:
        bot.reply_to(message, f"Хато: {e}")

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def run_bot():
    while True:
        try: bot.infinity_polling(timeout=20, long_polling_timeout=20)
        except: time.sleep(5)
if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
