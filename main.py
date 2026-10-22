import telebot, requests, os, re
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
SECRET = "CRYPTO2025"

bot = telebot.TeleBot(BOT_TOKEN)

# Дар хотир мондан
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
    mk.add(types.InlineKeyboardButton("📖 Ба сайт даро ва кодро ёб 👇", url=BLOG_URL))
    return mk

def get_rates():
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=8).json()['rates']
        return r.get('TJS',10.9), r
    except:
        return 10.9, {'TJS':10.9,'RUB':89,'EUR':0.91,'USD':1,'GBP':0.8}

def get_crypto(coin):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        d = requests.get(url, timeout=8, headers={"User-Agent":"Mozilla"}).json()
        return d.get(coin,{}).get('usd')
    except:
        return None

@bot.message_handler(commands=['start'])
def start(m):
    if m.chat.id in passed:
        bot.send_message(m.chat.id, "Салом! 🇹🇯 Тайёрам! Тугмаро пахш кун 👇", reply_markup=menu())
    else:
        bot.send_message(m.chat.id, f"👋 Салом! Барои истифода:\n👉 {BLOG_URL}\nКод дар мақола пинҳон аст! Ёб ва навиш!", reply_markup=forced())

@bot.message_handler(func=lambda x: True)
def all_msg(m):
    txt = m.text or ""
    uid = m.chat.id
    low = txt.lower()

    # --- МАҶБУРӢ БА САЙТ ---
    if uid not in passed:
        if SECRET in txt.upper():
            passed.add(uid)
            open("passed.txt","a").write(str(uid)+"\n")
            bot.send_message(uid, "✅ ОФАРИН! Дуруст ёфтӣ! Ҳамааш кушод шуд! 👇", reply_markup=menu())
            return
        else:
            bot.send_message(uid, f"⛔️ Аввал ба сайт даро!\n👉 {BLOG_URL}\nКод дар дохили мақола аст!", reply_markup=forced())
            return

    # --- РУБЛ - ҲАМАИ НАВИШТҲО: рубл, рубул, рубил ---
    if "руб" in low or "рубул" in low or "рубил" in low or "рбл" in low or "rub" in low:
        tjs, rates = get_rates()
        bot.send_message(uid, f"💷 **1 Рубл = {tjs/rates.get('RUB',89):.4f} сомонӣ**\n(1 Доллар = {tjs:.4f} TJS)", reply_markup=menu())
        return

    # --- ДОЛЛАР ---
    if "доллар" in low or "долар" in low or "usd" in low:
        tjs,_ = get_rates()
        bot.send_message(uid, f"💵 **1 Доллар = {tjs:.4f} сомонӣ**", reply_markup=menu())
        return

    # --- ЕВРО ---
    if "евро" in low or "eur" in low:
        tjs, rates = get_rates()
        bot.send_message(uid, f"💶 **1 Евро = {tjs/rates.get('EUR',0.91):.4f} сомонӣ**", reply_markup=menu())
        return

    # --- ҲАМАИ ПУЛҲОИ ҶАҲОН (160+) ---
    if "ҳамаи пул" in low or "хамаи пул" in low or "пулҳо" in low:
        tjs, rates = get_rates()
        msg = f"🌍 **ҲАМАИ ПУЛҲОИ ҶАҲОН**\n1 USD = {tjs:.4f} TJS\n\n"
        for c in ['EUR','RUB','GBP','TRY','KZT','UZS','CNY','AED','KGS','TMT','AZN','UAH','BYN','INR','JPY','CHF','CAD','AUD','SEK','NOK','DKK','PLN','SAR','KWD','QAR']:
            if c in rates:
                msg += f"1 {c} = {tjs/rates[c]:.4f} TJS\n"
        bot.send_message(uid, msg, reply_markup=menu())
        return

    # --- КРИПТО: БИТКОИН, ТОН, ЭФИР ---
    if "бит" in low or "btc" in low or "₿" in txt:
        p = get_crypto("bitcoin")
        tjs,_ = get_rates()
        if p: bot.send_message(uid, f"₿ **Биткоин = ${p} = {p*tjs:.2f} TJS**", reply_markup=menu())
        else: bot.send_message(uid, f"₿ **Биткоин = $67000**", reply_markup=menu())
        return

    if "тон" in low or "токен" in low or "💎" in txt:
        p = get_crypto("toncoin")
        tjs,_ = get_rates()
        if p: bot.send_message(uid, f"💎 **Тон = ${p} = {p*tjs:.2f} TJS**", reply_markup=menu())
        else: bot.send_message(uid, f"💎 **Тон = $6.20**", reply_markup=menu())
        return

    if "эфир" in low or "eth" in low or "🌐" in txt:
        p = get_crypto("ethereum")
        tjs,_ = get_rates()
        if p: bot.send_message(uid, f"🌐 **Эфир = ${p} = {p*tjs:.2f} TJS**", reply_markup=menu())
        else: bot.send_message(uid, f"🌐 **Эфир = $2500**", reply_markup=menu())
        return

    # --- ҲАМАИ КРИПТОҲО ---
    if "крипто" in low:
        try:
            tjs,_ = get_rates()
            r = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=30&page=1", timeout=10).json()
            msg = "🚀 **ТОП 30 КРИПТО**\n\n"
            for c in r:
                msg += f"{c['symbol'].upper()} = ${c['current_price']} = {c['current_price']*tjs:.2f} TJS\n"
            bot.send_message(uid, msg[:4000], reply_markup=menu())
        except:
            bot.send_message(uid, "⏳ Интернет суст, боз кӯшиш кун!", reply_markup=menu())
        return

    bot.send_message(uid, "🇹🇯 Навиш: Доллар чанд, Рубл чанд, Тон чанд, Биткоин чанд 👇", reply_markup=menu())

bot.infinity_polling()
