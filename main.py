import telebot, requests, os, threading, re
from flask import Flask
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
DEFAULT_SECRET = "CRYPTO2025"

bot = telebot.TeleBot(BOT_TOKEN)

# Render порт
app = Flask(__name__)
@app.route('/')
def home(): return "Bot Running ✅"
def run_flask(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()

# --- ИН НАВ - КОДРО АЗ БЛОГ ХУДАШ МЕХОНАД ---
def get_secret():
    try:
        html = requests.get(BLOG_URL, timeout=8).text
        # Коди шакли КОД: XXXX ё Код имрӯз: XXXX
        m = re.search(r'[Кк]од[^:]*:\s*([A-Z0-9_]{4,20})', html)
        if m: return m.group(1).strip().upper()
        m2 = re.search(r'CRYPTO[A-Z0-9_]{0,10}|DUSHANBE[A-Z0-9_]{0,10}|SOMONI[A-Z0-9_]{0,10}', html)
        if m2: return m2.group(0).strip().upper()
    except: pass
    return DEFAULT_SECRET

passed = set()
try:
    with open("passed.txt","r") as f:
        for l in f: passed.add(int(l.strip()))
except: pass

def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("💵 Доллар чанд","💷 Рубл чанд")
    kb.row("₿ Биткоин чанд","💎 Тон чанд")
    kb.row("🌍 Ҳамаи пулҳо","🚀 Ҳамаи криптоҳо")
    return kb

def forced():
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📖 Ба сайт даро ва кодро ёб", url=BLOG_URL))
    return mk

def get_rates():
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=8).json()['rates']
        return r.get('TJS',10.9), r
    except: return 10.9, {'TJS':10.9,'RUB':89,'EUR':0.91}

def get_crypto(coin):
    MAP = {"bitcoin":"BTC","toncoin":"TON","ethereum":"ETH"}
    sym = MAP.get(coin,"BTC")
    try:
        d = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}USDT", timeout=5).json()
        if 'price' in d: return float(d['price'])
    except: pass
    return {"bitcoin":67500,"toncoin":6.2,"ethereum":2550}.get(coin, 6.2)

@bot.message_handler(commands=['start'])
def s(m):
    if m.chat.id in passed:
        bot.send_message(m.chat.id, "Салом! Тайёрам! 👇", reply_markup=menu())
    else:
        bot.send_message(m.chat.id, f"👋 Аввал ба сайт даро ва кодро ёб:\n{BLOG_URL}", reply_markup=forced())

@bot.message_handler(func=lambda x: True)
def a(m):
    txt=m.text or ""; uid=m.chat.id; low=txt.lower()
    SECRET_NOW = get_secret() # Ҳар дафъа аз блог мехонад!

    if uid not in passed:
        if SECRET_NOW in txt.upper() or DEFAULT_SECRET in txt.upper():
            passed.add(uid); open("passed.txt","a").write(str(uid)+"\n")
            bot.send_message(uid, f"✅ Дуруст! Код {SECRET_NOW} қабул шуд!", reply_markup=menu()); return
        else:
            bot.send_message(uid, f"⛔️ Коди ҳозира: {SECRET_NOW}\nКоди имрӯзаро аз сайт ёб:\n{BLOG_URL}", reply_markup=forced()); return

    if "руб" in low or "рубул" in low:
        tjs,rates=get_rates(); bot.send_message(uid, f"💷 1 Рубл = {tjs/rates.get('RUB',89):.4f} сомонӣ", reply_markup=menu()); return
    if "доллар" in low or "долар" in low:
        tjs,_=get_rates(); bot.send_message(uid, f"💵 1 Доллар = {tjs:.4f} сомонӣ", reply_markup=menu()); return
    if "пул" in low:
        tjs,rates=get_rates(); msg=f"🌍 1 USD = {tjs:.4f} TJS\n"; bot.send_message(uid, msg, reply_markup=menu()); return
    if "бит" in low or "₿" in txt:
        p=get_crypto("bitcoin"); tjs,_=get_rates(); bot.send_message(uid, f"₿ Биткоин = ${p} = {p*tjs:.2f} сомонӣ", reply_markup=menu()); return
    if "тон" in low or "💎" in txt:
        p=get_crypto("toncoin"); tjs,_=get_rates(); bot.send_message(uid, f"💎 Тон = ${p} = {p*tjs:.2f} сомонӣ", reply_markup=menu()); return
    bot.send_message(uid, "Навиш: Доллар чанд, Рубл чанд 👇", reply_markup=menu())

bot.infinity_polling()
