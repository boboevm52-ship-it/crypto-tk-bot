import telebot, requests, os, threading
from flask import Flask
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
SECRET = "CRYPTO2025"

bot = telebot.TeleBot(BOT_TOKEN)

# --- БАРОИ RENDER - ПОРТРО МЕБАНДАД (хатои ту ҳамин буд) ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Running ✅"
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()

# Дар хотир
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
    except:
        return 10.9, {'TJS':10.9,'RUB':89,'EUR':0.91,'GBP':0.8,'TRY':38,'CNY':7.2}

def get_crypto(coin):
    MAP = {"bitcoin":"BTC","toncoin":"TON","ethereum":"ETH","solana":"SOL","dogecoin":"DOGE"}
    sym = MAP.get(coin,"BTC")
    try:
        d = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}USDT", timeout=5).json()
        if 'price' in d: return float(d['price'])
    except: pass
    try:
        d = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={sym}&tsyms=USD", timeout=5).json()
        if 'USD' in d: return float(d['USD'])
    except: pass
    return {"bitcoin":67500,"toncoin":6.2,"ethereum":2550,"solana":145,"dogecoin":0.14}.get(coin, 6.2)

@bot.message_handler(commands=['start'])
def s(m):
    if m.chat.id in passed:
        bot.send_message(m.chat.id, "Салом! Тайёрам! 👇", reply_markup=menu())
    else:
        bot.send_message(m.chat.id, f"👋 Барои истифода аввал ба сайт даро:\n{BLOG_URL}\nКод дар мақола аст!", reply_markup=forced())

@bot.message_handler(func=lambda x: True)
def a(m):
    txt=m.text or ""; uid=m.chat.id; low=txt.lower()
    
    # --- МАҶБУРӢ ---
    if uid not in passed:
        if SECRET in txt.upper():
            passed.add(uid); open("passed.txt","a").write(str(uid)+"\n")
            bot.send_message(uid, "✅ Офарин! Кушод шуд! 👇", reply_markup=menu()); return
        else:
            bot.send_message(uid, f"⛔️ Аввал ба сайт даро ва кодро ёб:\n{BLOG_URL}", reply_markup=forced()); return

    # --- РУБЛ - рубул, рубл, rub ---
    if "руб" in low or "рубул" in low or "rub" in low:
        tjs,rates=get_rates()
        bot.send_message(uid, f"💷 **1 Рубл = {tjs/rates.get('RUB',89):.4f} сомонӣ**", reply_markup=menu()); return

    if "доллар" in low or "долар" in low or "usd" in low or "💵" in txt:
        tjs,_=get_rates()
        bot.send_message(uid, f"💵 **1 Доллар = {tjs:.4f} сомонӣ**", reply_markup=menu()); return

    if "евро" in low:
        tjs,rates=get_rates()
        bot.send_message(uid, f"💶 **1 Евро = {tjs/rates.get('EUR',0.91):.4f} сомонӣ**", reply_markup=menu()); return

    if "ҳамаи пул" in low or "хамаи пул" in low or "пулҳо" in low or "🌍" in txt:
        tjs,rates=get_rates()
        msg=f"🌍 **ҲАМАИ ПУЛҲОИ ҶАҲОН**\n1 USD = {tjs:.4f} TJS\n\n"
        for c in ['EUR','RUB','GBP','TRY','KZT','UZS','CNY','AED','KGS','TMT','AZN','UAH','BYN','INR','JPY','CHF','CAD','AUD','SEK','PLN','SAR']:
            if c in rates: msg+=f"1 {c} = {tjs/rates[c]:.4f} TJS\n"
        bot.send_message(uid, msg, reply_markup=menu()); return

    if "бит" in low or "btc" in low or "₿" in txt:
        p=get_crypto("bitcoin"); tjs,_=get_rates()
        bot.send_message(uid, f"₿ **Биткоин = ${p} = {p*tjs:.2f} сомонӣ**", reply_markup=menu()); return

    if "тон" in low or "💎" in txt:
        p=get_crypto("toncoin"); tjs,_=get_rates()
        bot.send_message(uid, f"💎 **Тон = ${p} = {p*tjs:.2f} сомонӣ**", reply_markup=menu()); return

    if "эфир" in low or "eth" in low or "🌐" in txt:
        p=get_crypto("ethereum"); tjs,_=get_rates()
        bot.send_message(uid, f"🌐 **Эфир = ${p} = {p*tjs:.2f} сомонӣ**", reply_markup=menu()); return

    if "крипто" in low or "🚀" in txt:
        tjs,_=get_rates(); msg="🚀 **ТОП КРИПТО**\n\n"
        for coin in ["bitcoin","ethereum","toncoin","solana","dogecoin"]:
            p=get_crypto(coin); msg+=f"{coin.upper()} = ${p}\n"
        bot.send_message(uid, msg, reply_markup=menu()); return

    bot.send_message(uid, "Навиш: Доллар чанд, Рубл чанд, Тон чанд 👇", reply_markup=menu())

bot.infinity_polling()
