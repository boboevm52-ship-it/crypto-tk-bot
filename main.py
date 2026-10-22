import telebot, requests, os, threading, re
from flask import Flask
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
DEFAULT_SECRET = "CRYPTO2025" # Ин фақат агар блог кор накунад

bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Running ✅"
def run_flask(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()

# --- ХОНДАНИ КОД АЗ БЛОГ - АВТОМАТИКӢ ---
def get_secret():
    try:
        r = requests.get(BLOG_URL, timeout=10, headers={'User-Agent':'Mozilla/5.0'})
        html = r.text
        # Ҳама шакл
        m = re.search(r'Коди имрӯз:\s*([A-Z0-9_]{3,20})', html, re.IGNORECASE)
        if m: return m.group(1).upper().strip()
        m = re.search(r'Код:\s*([A-Z0-9_]{3,20})', html, re.IGNORECASE)
        if m: return m.group(1).upper().strip()
        # Агар дар блог калимаи калон ба монанди DUSHANBE777 бошад
        m = re.search(r'\b([A-Z]{4,}\d{2,}[A-Z0-9_]*)\b', html)
        if m: return m.group(1).upper().strip()
    except Exception as e:
        print(f"Error blog: {e}")
    return DEFAULT_SECRET

passed = {}
# passed[user_id] = secret_бо_кадом_гузашт

def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("💵 Доллар чанд","💷 Рубл чанд")
    kb.row("₿ Биткоин чанд","💎 Тон чанд","🌐 Эфир чанд")
    kb.row("🌍 Ҳамаи пулҳо","🚀 Ҳамаи криптоҳо")
    kb.row("Дирхам чанд","Тенге чанд","Сӯм чанд")
    return kb

def forced(secret):
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton(f"📖 Коди навро аз сайт ёб: {secret}", url=BLOG_URL))
    return mk

def get_rates():
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=8).json()['rates']
        return r.get('TJS',10.9), r
    except: return 10.9, {}

def get_crypto(sym):
    try:
        d = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}USDT", timeout=5).json()
        if 'price' in d: return float(d['price'])
    except: pass
    return 0

TJ_MAP = {
    "рубл": ("RUB","Рубл"), "рубул": ("RUB","Рубл"), "руб": ("RUB","Рубл"), "rub": ("RUB","Рубл"),
    "тенге": ("KZT","Тенге"), "тнг": ("KZT","Тенге"), "kzt": ("KZT","Тенге"),
    "сӯм": ("UZS","Сӯм"), "сум": ("UZS","Сӯм"), "uzs": ("UZS","Сӯм"),
    "сом": ("TJS","Сомонӣ"), "tjs": ("TJS","Сомонӣ"),
    "киргиз": ("KGS","Сом Қирғиз"), "kgs": ("KGS","Сом"),
    "манат": ("AZN","Манат"), "лира": ("TRY","Лира"), "try": ("TRY","Лира"),
    "юан": ("CNY","Юан"), "дирхам": ("AED","Дирҳам"), "дирҳам": ("AED","Дирҳам"), "aed": ("AED","Дирҳам"),
    "доллар": ("USD","Доллар"), "долар": ("USD","Доллар"), "usd": ("USD","Доллар"), "💵": ("USD","Доллар"), "бакс": ("USD","Доллар"),
    "евро": ("EUR","Евро"), "eur": ("EUR","Евро"),
    "фунт": ("GBP","Фунт"), "йена": ("JPY","Йена"),
    "биткоин": ("BTC","Биткоин"), "бит": ("BTC","Биткоин"), "btc": ("BTC","Биткоин"), "₿": ("BTC","Биткоин"),
    "токен": ("TON","Тон"), "тон": ("TON","Тон"), "ton": ("TON","Тон"), "💎": ("TON","Тон"),
    "эфир": ("ETH","Эфир"), "eth": ("ETH","Эфир"), "🌐": ("ETH","Эфир"),
    "солана": ("SOL","Солана"), "sol": ("SOL","Солана"), "доге": ("DOGE","Доге"), "doge": ("DOGE","Доге"),
}

@bot.message_handler(commands=['start','secret','код'])
def s(m):
    SECRET_NOW = get_secret()
    uid = m.chat.id
    # Агар коди ҳозира бо коди гузаштаи ин одам баробар набошад -> маҷбур
    if passed.get(uid) != SECRET_NOW:
        bot.send_message(uid, f"👋 Коди имрӯз нав шуд!\n\nКоди ҳозира: **{SECRET_NOW}**\nАз сайт ёб:\n{BLOG_URL}\n\nКоди навро навиш:", reply_markup=forced(SECRET_NOW), parse_mode='Markdown')
    else:
        bot.send_message(uid, "Салом! Тайёрам! 👇", reply_markup=menu())

@bot.message_handler(func=lambda x: True)
def a(m):
    txt=m.text or ""; uid=m.chat.id; low=txt.lower()
    SECRET_NOW = get_secret()

    # САНҶИШИ АВТОМАТИКӢ - АГАР КОД НАВ БОШАД, ҲАМАРО АЗ НАВ МЕПУРСАД
    if passed.get(uid) != SECRET_NOW:
        if SECRET_NOW in txt.upper():
            passed[uid] = SECRET_NOW
            bot.send_message(uid, f"✅ Дуруст! Код {SECRET_NOW} қабул! Ҳоло пурс: Дирхам чанд, Тенге чанд...", reply_markup=menu()); return
        else:
            bot.send_message(uid, f"⛔️ Коди кӯҳна не! Коди НАВ: **{SECRET_NOW}**\nАз сайт ёб:\n{BLOG_URL}", reply_markup=forced(SECRET_NOW), parse_mode='Markdown'); return

    # ПУЛҲО
    for key,(code,full) in TJ_MAP.items():
        if key in low:
            tjs,rates=get_rates()
            if code in ["BTC","TON","ETH","SOL","DOGE"]:
                p=get_crypto(code)
                bot.send_message(uid, f"💰 {full} = ${p} = {p*tjs:.2f} сомонӣ", reply_markup=menu()); return
            else:
                val = tjs if code=="USD" else tjs/rates.get(code,1)
                bot.send_message(uid, f"💱 1 {full} = {val:.4f} сомонӣ", reply_markup=menu()); return

    if "ҳамаи пул" in low or "🌍" in txt:
        tjs,rates=get_rates(); msg=f"🌍 1 USD = {tjs:.4f} TJS\n"; 
        for c in ['EUR','RUB','KZT','UZS','KGS','TRY','CNY','AED','GBP','JPY']:
            if c in rates: msg+=f"1 {c} = {tjs/rates[c]:.4f}\n"
        bot.send_message(uid, msg, reply_markup=menu()); return
    if "крипто" in low or "🚀" in txt:
        tjs,_=get_rates(); msg="🚀 Крипто:\n"
        for sym,name in [("BTC","Биткоин"),("ETH","Эфир"),("TON","Тон")]:
            p=get_crypto(sym); msg+=f"{name} = ${p}\n"
        bot.send_message(uid, msg, reply_markup=menu()); return

    bot.send_message(uid, "Чиро пурсӣ? Навиш: Дирхам чанд, Тенге чанд, Доллар чанд 👇", reply_markup=menu())

bot.infinity_polling()
