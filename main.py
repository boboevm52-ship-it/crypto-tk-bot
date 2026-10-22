
import os, requests, threading, time, re
from flask import Flask
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# Тозакунӣ
try:
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
    time.sleep(1)
except:
    pass

FIAT = {"USD":10.90,"EUR":11.85,"RUB":0.115,"GBP":12.34,"TRY":1.37,"CHF":11.17,"AED":2.51,"SAR":2.45,"INR":0.097,"KZT":0.022,"CNY":1.51,"KGS":0.124,"TMT":3.11,"UZS":0.000844}
CRYPTO_IDS = {"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","BNB":"binancecoin","XRP":"ripple","DOGE":"dogecoin","TON":"the-open-network","USDT":"tether","TRX":"tron","AVAX":"avalanche-2"}

SITE = "https://cryptotj.blogspot.com"

def footer():
    return f"\n\n━━━━━━━━━━━━━━\n🌐 {SITE}\n💰 Ба сайти асли мо обуна шавед!"

def markup():
    m = telebot.types.InlineKeyboardMarkup()
    m.add(telebot.types.InlineKeyboardButton("💰 Бо Канали мо обуна шавед", url=SITE))
    m.add(telebot.types.InlineKeyboardButton("🌐 Сайти асли мо", url=SITE))
    return m

def get_price(coin_id):
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd", timeout=15).json()
        return r.get(coin_id, {}).get('usd')
    except:
        return None

def find_code(text):
    t = text.lower()
    if "рубл" in t or "рубул" in t or "rubl" in t or " rub" in t: return "RUB"
    if "доллар" in t or "долар" in t or "dollar" in t or "usd" in t: return "USD"
    if "евро" in t or "eur" in t: return "EUR"
    if "сум" in t or "uzs" in t: return "UZS"
    if "биткоин" in t or "bitcoin" in t or "btc" in t: return "BTC"
    if "эфир" in t or " eth" in t: return "ETH"
    if "доге" in t or "дож" in t or "doge" in t: return "DOGE"
    if "тон" in t or " ton" in t: return "TON"
    if "рипл" in t or "xrp" in t: return "XRP"
    if "солана" in t or " sol" in t: return "SOL"
    if "трон" in t or "trx" in t: return "TRX"
    if "тетер" in t or "usdt" in t: return "USDT"
    if "бнб" in t or "bnb" in t: return "BNB"
    if "авакс" in t or "avax" in t: return "AVAX"
    return None

@bot.message_handler(commands=['start'])
def start_cmd(message):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(telebot.types.KeyboardButton("BTC"), telebot.types.KeyboardButton("ETH"), telebot.types.KeyboardButton("SOL"))
    kb.add(telebot.types.KeyboardButton("BNB"), telebot.types.KeyboardButton("XRP"), telebot.types.KeyboardButton("DOGE"))
    kb.add(telebot.types.KeyboardButton("TON"), telebot.types.KeyboardButton("USDT"), telebot.types.KeyboardButton("TRX"))
    kb.add(telebot.types.KeyboardButton("AVAX"), telebot.types.KeyboardButton("14 курс"), telebot.types.KeyboardButton("10 крипто"))
    kb.add(telebot.types.KeyboardButton("Биткоин чанд"), telebot.types.KeyboardButton("Рубл чанд"))
    bot.send_message(message.chat.id, f"✅ Тайёр! 14 курс + 10 крипто\n🌐 {SITE}", reply_markup=kb)

@bot.message_handler(content_types=['text'])
def text_handler(message):
    try:
        txt = message.text
        code = find_code(txt)
        print(f"Message: {txt} -> {code}")

        if code in FIAT:
            rate = FIAT[code]
            bot.send_message(message.chat.id, f"💰 1 {code} = {rate:.4f} TJS\n💵 100 {code} = {rate*100:.2f} TJS{footer()}", reply_markup=markup())
            return

        if code in CRYPTO_IDS:
            price = get_price(CRYPTO_IDS[code])
            if price:
                bot.send_message(message.chat.id, f"🟡 {code}:\n🟢 {price} $\n🔴 {price*10.9:.2f} TJS{footer()}", reply_markup=markup())
            else:
                bot.send_message(message.chat.id, f"⏳ {code} ҳозир банд аст{footer()}", reply_markup=markup())
            return

        if "курс" in txt.lower():
            msg = "💱 14 КУРС:\n\n"
            for k,v in FIAT.items():
                msg += f"• 1 {k} = {v:.4f} TJS\n"
            msg += footer()
            bot.send_message(message.chat.id, msg, reply_markup=markup())
            return

        if "крипто" in txt.lower():
            try:
                ids = ",".join(CRYPTO_IDS.values())
                data = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd", timeout=15).json()
                msg = "💰 10 КРИПТО:\n\n"
                for s,c in CRYPTO_IDS.items():
                    p = data.get(c, {}).get('usd', '-')
                    msg += f"• {s}: {p} $\n"
                msg += footer()
                bot.send_message(message.chat.id, msg, reply_markup=markup())
            except:
                bot.send_message(message.chat.id, f"⏳ Сарвер банд{footer()}", reply_markup=markup())
            return

        bot.send_message(message.chat.id, f"🤔 '{txt}' нафаҳмидам\nНавиш: Рубл чанд, Биткоин чанд{footer()}", reply_markup=markup())

    except Exception as e:
        print(f"Handler error: {e}")
        try:
            bot.send_message(message.chat.id, f"⚠️ Хато, дубора: Рубл чанд{footer()}", reply_markup=markup())
        except:
            pass

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Live"

def run_bot():
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(10)
