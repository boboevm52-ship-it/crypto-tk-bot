import telebot, requests, os, threading, re
from flask import Flask
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
DEFAULT_SECRET = "CRYPTO2025"

bot = telebot.TeleBot(BOT_TOKEN)

# БАРОИ RENDER
app = Flask(__name__)
@app.route('/')
def home(): return "Bot Running ✅"
def run_flask(): app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()

def get_secret():
    try:
        html = requests.get(BLOG_URL, timeout=8).text
        m = re.search(r'[Кк]од[^:]*:\s*([A-Z0-9_]{4,20})', html)
        if m: return m.group(1).strip().upper()
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
    kb.row("₿ Биткоин чанд","💎 Тон чанд","🌐 Эфир чанд")
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
    except: return 10.9, {}

def get_crypto(sym):
    try:
        d = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}USDT", timeout=5).json()
        if 'price' in d: return float(d['price'])
    except: pass
    return 0

# ЛУҒАТИ ТОҶИКӢ - ҲАМАШ!
TJ_MAP = {
    # Ҳамсоя
    "рубл": ("RUB","Рубл Русия"), "рубул": ("RUB","Рубл"), "руб": ("RUB","Рубл"), "rub": ("RUB","Рубл"),
    "тенге": ("KZT","Тенге Қазоқ"), "тнг": ("KZT","Тенге"), "тенгэ": ("KZT","Тенге"), "kzt": ("KZT","Тенге"),
    "сӯм": ("UZS","Сӯм Узбек"), "сум": ("UZS","Сӯм"), "uzs": ("UZS","Сӯм"), "узб": ("UZS","Сӯм"),
    "сом": ("TJS","Сомонӣ"), "сомон": ("TJS","Сомонӣ"), "tjs": ("TJS","Сомонӣ"),
    "киргиз": ("KGS","Сом Қирғиз"), "kgs": ("KGS","Сом Қирғиз"),
    "туркман": ("TMT","Манат Туркман"), "tmt": ("TMT","Манат"),
    "манат": ("AZN","Манат Озарӣ"), "azn": ("AZN","Манат"),
    "лира": ("TRY","Лира Турк"), "try": ("TRY","Лира"),
    "юан": ("CNY","Юан Чин"), "cny": ("CNY","Юан"),
    "дирхам": ("AED","Дирҳам Дубай"), "дирҳам": ("AED","Дирҳам"), "aed": ("AED","Дирҳам"), "дубай": ("AED","Дирҳам"),
    # Ҷаҳон
    "доллар": ("USD","Доллар"), "долар": ("USD","Доллар"), "usd": ("USD","Доллар"), "💵": ("USD","Доллар"), "бакс": ("USD","Доллар"),
    "евро": ("EUR","Евро"), "eur": ("EUR","Евро"), "еуро": ("EUR","Евро"),
    "фунт": ("GBP","Фунт"), "gbp": ("GBP","Фунт"),
    "йена": ("JPY","Йена"), "йен": ("JPY","Йена"), "jpy": ("JPY","Йена"),
    "франк": ("CHF","Франк"), "chf": ("CHF","Франк"),
    "риал": ("SAR","Риял"), "sar": ("SAR","Риял"),
    "гривна": ("UAH","Гривна"), "uah": ("UAH","Гривна"),
    # Крипто - АВТОМАТИКӢ
    "биткоин": ("BTC","Биткоин"), "бит": ("BTC","Биткоин"), "btc": ("BTC","Биткоин"), "₿": ("BTC","Биткоин"),
    "токен": ("TON","Тон"), "тон": ("TON","Тон"), "ton": ("TON","Тон"), "💎": ("TON","Тон"),
    "эфир": ("ETH","Эфир"), "эфириум": ("ETH","Эфир"), "eth": ("ETH","Эфир"), "🌐": ("ETH","Эфир"),
    "солана": ("SOL","Солана"), "sol": ("SOL","Солана"),
    "доге": ("DOGE","Догекоин"), "doge": ("DOGE","Доге"),
}

@bot.message_handler(commands=['start'])
def s(m):
    if m.chat.id in passed:
        bot.send_message(m.chat.id, "Салом! Ман ҳамаи пулҳоро мефаҳмам! Чиро пурсон мешавӣ? 👇", reply_markup=menu())
    else:
        bot.send_message(m.chat.id, f"👋 Аввал ба сайт даро ва Коди имрӯзро ёб:\n{BLOG_URL}", reply_markup=forced())

@bot.message_handler(func=lambda x: True)
def a(m):
    txt=m.text or ""; uid=m.chat.id; low=txt.lower()
    SECRET_NOW = get_secret()

    # МАҶБУРӢ
    if uid not in passed:
        if SECRET_NOW in txt.upper():
            passed.add(uid); open("passed.txt","a").write(str(uid)+"\n")
            bot.send_message(uid, f"✅ Офарин! Код {SECRET_NOW} дуруст! Ҳоло ҳар пулро пурс!", reply_markup=menu()); return
        else:
            bot.send_message(uid, f"⛔️ Коди имрӯз: {SECRET_NOW}\nАввал аз сайт ёб:\n{BLOG_URL}", reply_markup=forced()); return

    # ҲАМАИ ПУЛҲО
    if "ҳамаи пул" in low or "хамаи пул" in low or "🌍" in txt:
        tjs,rates=get_rates()
        msg=f"🌍 **ҲАМАИ ПУЛҲО**\n1 USD = {tjs:.4f} TJS\n\n"
        for c in ['EUR','RUB','KZT','UZS','KGS','TMT','AZN','TRY','CNY','AED','GBP','JPY','CHF','SAR','UAH']:
            if c in rates: msg+=f"1 {c} = {tjs/rates[c]:.4f} TJS\n"
        bot.send_message(uid, msg, reply_markup=menu()); return

    if "крипто" in low or "🚀" in txt:
        tjs,_=get_rates()
        msg="🚀 **КРИПТО**\n"
        for sym,name in [("BTC","Биткоин"),("ETH","Эфир"),("TON","Тон"),("SOL","Солана"),("DOGE","Доге")]:
            p=get_crypto(sym)
            if p: msg+=f"{name} = ${p} = {p*tjs:.2f} TJS\n"
        bot.send_message(uid, msg, reply_markup=menu()); return

    # ФАҲМИДАНИ АВТОМАТИКӢ - ҲАР КАЛИМАИ ТОҶИКӢ
    for key,(code,full) in TJ_MAP.items():
        if key in low:
            tjs,rates=get_rates()
            if code in ["BTC","TON","ETH","SOL","DOGE"]:
                p=get_crypto(code)
                bot.send_message(uid, f"{'₿' if code=='BTC' else '💎' if code=='TON' else '💰'} **{full} = ${p} = {p*tjs:.2f} сомонӣ**", reply_markup=menu())
                return
            else:
                if code=="USD": val=tjs
                else: val=tjs/rates.get(code,1)
                bot.send_message(uid, f"💱 **1 {full} ({code}) = {val:.4f} сомонӣ**", reply_markup=menu())
                return

    bot.send_message(m.chat.id, "Нафаҳмидам, лекин инҳоро мефаҳмам:\nДирхам чанд, Тенге чанд, Сом чанд, Токен чанд, Доллар чанд, Рубл чанд 👇", reply_markup=menu())

bot.infinity_polling()
