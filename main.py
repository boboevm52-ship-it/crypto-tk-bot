import os, requests, threading, re
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("BOT_TOKEN нест!")
    exit()

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2026/10/blog-post_22.html"
SECRET_CODE = "
passed = {}

def get_fiat():
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10).json()
        return r['rates']
    except:
        return {"USD":1,"TJS":9.42,"EUR":0.92,"RUB":92.5,"KZT":490,"UZS":12800,"KGS":89,"CNY":7.2,"TRY":34,"GBP":0.79,"AED":3.67}

def get_crypto_price(sym):
    try:
        mp = {"BTC":"bitcoin","ETH":"ethereum","BNB":"binancecoin","SOL":"solana","XRP":"ripple","DOGE":"dogecoin","TON":"the-open-network","USDT":"tether","TRX":"tron","ADA":"cardano","SHIB":"shiba-inu","AVAX":"avalanche-2","DOT":"polkadot","LINK":"chainlink","MATIC":"matic-network","LTC":"litecoin","UNI":"uniswap","PEPE":"pepe","NOT":"notcoin"}
        cid = mp.get(sym.upper(), sym.lower())
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd"
        d = requests.get(url, timeout=10).json()
        return d[cid]['usd']
    except:
        return None

def menu():
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton("💵 Доллар", callback_data="USD"),
        InlineKeyboardButton("💶 Евро", callback_data="EUR"),
        InlineKeyboardButton("💷 Рубл", callback_data="RUB"),
        InlineKeyboardButton("₿ Биткоин", callback_data="BTC"),
        InlineKeyboardButton("💎 Тон", callback_data="TON"),
        InlineKeyboardButton("Ξ Эфир", callback_data="ETH"),
        InlineKeyboardButton("🌍 Ҳамаи пулҳо", callback_data="ALL_FIAT"),
        InlineKeyboardButton("🚀 Ҳамаи криптоҳо", callback_data="ALL_CRYPTO")
    )
    return mk

@app.route('/')
def home():
    return "CryptoTJ 100% Tojiki - LIVE!"

@bot.callback_query_handler(func=lambda c: True)
def cb(call):
    uid = call.from_user.id
    
    # ИСЛОҲ 1: Агар код надошта бошад - маҷбур ба сайт
    if passed.get(uid) != True:
        mk = InlineKeyboardMarkup()
        mk.add(InlineKeyboardButton("🔐 Ба сайт даро ва код ёб", url=BLOG_URL))
        bot.answer_callback_query(call.id, "Аввал ба сайт даро!")
        bot.send_message(call.message.chat.id, f"⛔️ Аввал ба сайт даро!\n👉 {BLOG_URL}\nКоди {SECRET_CODE} -ро ёб!", reply_markup=mk)
        return

    # Агар код дошта бошад
    if call.data == "ALL_FIAT":
        rates = get_fiat()
        tjs = rates.get('TJS', 9.42)
        txt = f"🌍 **Ҳамаи пулҳо ба сомонӣ:**\n\n💵 USD = {tjs} TJS\n💶 EUR = {tjs/rates.get('EUR',0.92):.2f} TJS\n💷 RUB = {tjs/rates.get('RUB',92.5):.3f} TJS\n🇨🇳 CNY = {tjs/rates.get('CNY',7.2):.2f} TJS\n🇰🇿 KZT = {tjs/rates.get('KZT',490):.4f} TJS"
        bot.send_message(call.message.chat.id, txt, parse_mode="Markdown", reply_markup=menu())
    
    elif call.data == "ALL_CRYPTO":
        bot.send_message(call.message.chat.id, "🚀 BTC, ETH, BNB, SOL, XRP, DOGE, TON, USDT, TRX, ADA, SHIB, AVAX, DOT, LINK, MATIC, LTC, UNI, PEPE, NOT ва 15000-тои дигар!\n\nНавиш: SOL чанд", reply_markup=menu())
    
    else:
        sym = call.data
        price = get_crypto_price(sym)
        if price:
            bot.send_message(call.message.chat.id, f"💰 1 {sym} = ${price} = {price*9.42:.2f} TJS", reply_markup=menu())
        else:
            rates = get_fiat()
            if sym in rates:
                tjs_price = rates['TJS'] / rates[sym] if sym != "TJS" else 1
                bot.send_message(call.message.chat.id, f"💰 1 {sym} = {tjs_price:.4f} TJS", reply_markup=menu())

@bot.message_handler(commands=['start'])
def start(m):
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("🔐 Ба сайт даро ва код ёб", url=BLOG_URL))
    bot.send_message(m.chat.id, f"Салом {m.from_user.first_name}! 👋\n\n💰 Ҳамаи пулҳои ҷаҳон\n₿ Ҳамаи криптоҳо\n\n🔐 Барои кушодан:\n1. Ба сайт даро:\n{BLOG_URL}\n2. Кодро ёб: `{SECRET_CODE}`\n3. Ин ҷо навиш!", reply_markup=mk, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    txt = m.text.strip()
    uid = m.from_user.id

    if txt.upper() == SECRET_CODE:
        passed[uid] = True
        bot.send_message(m.chat.id, f"✅ ОФАРИН! Коди {SECRET_CODE} дуруст!\n\nАкнун ҳама кушод шуд! 👇", reply_markup=menu())
        return

    if passed.get(uid) != True:
        mk = InlineKeyboardMarkup()
        mk.add(InlineKeyboardButton("🔐 Ба сайт даро", url=BLOG_URL))
        bot.send_message(m.chat.id, f"⛔️ **Маҷбурӣ ба сайт!**\n👉 {BLOG_URL}\nКодро ёб ва навиш!", reply_markup=mk, parse_mode="Markdown")
        return

    low = txt.lower()
    if "сом чанд" in low or "доллар" in low or "usd" in low:
        rates = get_fiat()
        bot.send_message(m.chat.id, f"💵 1 USD = {rates.get('TJS',9.42)} TJS", reply_markup=menu())
    else:
        sym = re.findall(r'\b([A-Z]{2,6})\b', txt.upper())
        if sym:
            p = get_crypto_price(sym[0])
            if p:
                bot.send_message(m.chat.id, f"💰 1 {sym[0]} = ${p} = {p*9.42:.2f} TJS", reply_markup=menu())
                return
        bot.send_message(m.chat.id, "Навиш: Доллар чанд, Евро чанд, Биткоин чанд, Тон чанд", reply_markup=menu())

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True)
        except Exception as e:
            print(f"Bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    import time
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
