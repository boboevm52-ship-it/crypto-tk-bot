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
def home():
    return "Bot is alive!"

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

@bot.message_handler(commands=['start', 'kurs'])
def kurs_cmd(message):
    try:
        r = get_crypto()
        usd, rub, eur = get_fiat()
        msg = f"💱 14 КУРС {time.strftime('%d.%m %H:%M')}\n\n"
        msg += f"1. BTC ${r.get('bitcoin',{}).get('usd',0):,.0f}\n"
        msg += f"2. ETH ${r.get('ethereum',{}).get('usd',0):,.0f}\n"
        msg += f"3. BNB ${r.get('binancecoin',{}).get('usd',0):,.0f}\n"
        msg += f"4. SOL ${r.get('solana',{}).get('usd',0):,.0f}\n"
        msg += f"5. DOGE ${r.get('dogecoin',{}).get('usd',0):,.3f}\n"
        msg += f"6. TON ${r.get('toncoin',{}).get('usd',0):,.2f}\n"
        msg += f"7. USDT ${r.get('tether',{}).get('usd',0):,.2f}\n"
       
