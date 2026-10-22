import telebot, requests, os
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
SECRET = "CRYPTO2025"
bot = telebot.TeleBot(BOT_TOKEN)

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
        return 10.9, {'TJS':10.9,'RUB':89,'EUR':0.91,'USD':1,'GBP':0.8,'TRY':38}

def get_crypto(coin):
    MAP = {"bitcoin":"BTC","toncoin":"TON","ethereum":"ETH","dogecoin":"DOGE","solana":"SOL","pepe":"PEPE"}
    sym = MAP.get(coin,"BTC")
    # 1. Binance
    try:
        r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}USDT", timeout=5).json()
        if 'price' in r: return float(r['price'])
    except: pass
    # 2. CryptoCompare
    try:
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={sym}&tsyms=USD", timeout=5).json()
        if 'USD' in r: return float(r['USD'])
    except: pass
    # 3. Fallback
    FALLBACK = {"bitcoin":67500,"toncoin":6.2,"ethereum":2550,"dogecoin":0.14,"solana":145,"pepe":0.000008}
    return FALLBACK.get(coin)

@bot.message_handler(commands=['start'])
def start(m):
    if m.chat.id in passed:
        bot.send_message(m.chat.id,"Салом! Тайёрам! 👇",reply_markup=menu())
    else:
        bot.send_message(m.chat.id,f"Барои истифода:\n{BLOG_URL}\nКод дар мақола аст!",reply_markup=forced())

@bot.message_handler(func=lambda x: True)
def all_msg(m):
    txt=m.text or ""; uid=m.chat.id; low=txt.lower()
    
    if uid not in passed:
        if SECRET in txt.upper():
            passed.add(uid); open("passed.txt","a").write(str(uid)+"\n")
            bot.send_message(uid,"✅ Офарин! Кушод шуд! 👇",reply_markup=menu()); return
        else:
            bot.send_message(uid,f"⛔️ Кодро аз сайт ёб:\n{BLOG_URL}",reply_markup=forced()); return

    if "руб" in low or "рубул" in low or "rub" in low:
        tjs,rates=get_rates()
        bot.send_message(uid,f"💷 1 Рубл = {tjs/rates.get('RUB',89):.4f} сомонӣ",reply_markup=menu()); return

    if "доллар" in low or "долар" in low or "usd" in low:
        tjs,_=get_rates()
        bot.send_message(uid,f"💵 1 Доллар = {tjs:.4f} сомонӣ",reply_markup=menu()); return

    if "евро" in low or "eur" in low:
        tjs,rates=get_rates()
        bot.send_message(uid,f"💶 1 Евро = {tjs/rates.get('EUR',0.91):.4f} сомонӣ",reply_markup=menu()); return

    if "ҳамаи пул" in low or "хамаи пул" in low or "пулҳо" in low:
        tjs,rates=get_rates()
        msg=f"🌍 ҲАМАИ ПУЛҲО\n1 USD = {tjs:.4f} TJS\n\n"
        for c in ['EUR','RUB','GBP','TRY','KZT','UZS','CNY','AED','KGS','TMT','AZN','UAH','BYN','INR','JPY','CHF','CAD','AUD']:
            if c in rates: msg+=f"1 {c} = {tjs/rates[c]:.4f} TJS\n"
        bot.send_message(uid,msg,reply_markup=menu()); return

    if "бит" in low or "btc" in low or "₿" in txt:
        p=get_crypto("bitcoin"); tjs,_=get_rates()
        bot.send_message(uid,f"₿ Биткоин = ${p} = {p*tjs:.2f} сомонӣ",reply_markup=menu()); return

    if "тон" in low or "💎" in txt:
        p=get_crypto("toncoin"); tjs,_=get_rates()
        bot.send_message(uid,f"💎 Тон = ${p} = {p*tjs:.2f} сомонӣ",reply_markup=menu()); return

    if "эфир" in low or "eth" in low or "🌐" in txt:
        p=get_crypto("ethereum"); tjs,_=get_rates()
        bot.send_message(uid,f"🌐 Эфир = ${p} = {p*tjs:.2f} сомонӣ",reply_markup=menu()); return

    if "крипто" in low:
        tjs,_=get_rates()
        try:
            coins=["bitcoin","ethereum","toncoin","solana","dogecoin"]
            msg="🚀 КРИПТО:\n"
            for coin in coins:
                p=get_crypto(coin)
                msg+=f"{coin.upper()} = ${p} = {p*tjs:.2f} TJS\n"
            bot.send_message(uid,msg,reply_markup=menu())
        except:
            bot.send_message(uid,"⏳ Интернет суст!",reply_markup=menu())
        return

    bot.send_message(uid,"Навиш: Доллар чанд, Рубл чанд, Тон чанд 👇",reply_markup=menu())

bot.infinity_polling()
