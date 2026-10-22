import telebot, requests, os
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
SECRET_CODE = "CRYPTO2025" # Коди пинҳон - дар блог навишта шудааст

bot = telebot.TeleBot(BOT_TOKEN)

# Дар хотир нигоҳ медорад ки гузашт
passed = {}
try:
    with open("passed.txt","r") as f:
        for x in f: passed[int(x.strip())]=True
except: pass

def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add("💵 Доллар чанд","💶 Евро чанд","💷 Рубл чанд","₿ Биткоин чанд","💎 Тон чанд","🌐 Эфир чанд","🌍 Ҳамаи пулҳо","🚀 Ҳамаи криптоҳо")
    return kb

def forced():
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📖 Ба сайт даро ва кодро ёб 👈", url=BLOG_URL))
    return mk

def get_fiat():
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10).json()
        return r['rates']
    except:
        return {'TJS':10.5,'RUB':92,'EUR':0.92}

def get_crypto(sym="bitcoin"):
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={sym}&vs_currencies=usd,tjs", timeout=10).json()
        return r[sym]
    except: return None

@bot.message_handler(commands=['start'])
def start(m):
    if passed.get(m.chat.id):
        bot.send_message(m.chat.id, "Салом! 👋\nМан 100% тоҷикӣ медонам!\n\nНавиш: 'Доллар чанд', 'Рубл чанд', 'Биткоин чанд', 'Тон чанд'\nЁ 'Ҳамаи пулҳо' / 'Ҳамаи криптоҳо'", reply_markup=menu())
    else:
        bot.send_message(m.chat.id, f"👋 Салом! Барои истифода:\n\n1️⃣ Ба ин сайт даро:\n👉 {BLOG_URL}\n\n2️⃣ Код дар дохили мақола пинҳон аст!\n\n3️⃣ Кодро дар ин ҷо навиш!", reply_markup=forced())

@bot.message_handler(func=lambda x: True)
def all_msg(m):
    txt = m.text.strip()
    uid = m.chat.id
    low = txt.lower()

    # Агар ҳанӯз нагузашта бошад
    if not passed.get(uid):
        if txt.upper() == SECRET_CODE:
            passed[uid]=True
            with open("passed.txt","a") as f: f.write(str(uid)+"\n")
            bot.send_message(uid, "✅ ОФАРИН! Дуруст ёфтӣ!\nАкнун ҳамааш кушод шуд! 👇", reply_markup=menu())
            return
        else:
            bot.send_message(uid, f"⛔️ Аввал ба сайт даро!\n👉 {BLOG_URL}\nКод дар мақола аст, ёбад ва навиш!", reply_markup=forced())
            return

    # --- АЗ ИН ҶО 100% ТОҶИКӢ ВА ҲАМАИ ПУЛҲО ---

    if "ҳамаи пулҳо" in low or "hамаи пулхо" in low or "14 курс" in low or "160 пул" in low:
        rates = get_fiat()
        tjs = rates.get('TJS',10.5)
        msg = f"🌍 **ҲАМАИ ПУЛҲОИ ҶАҲОН ба СОМОНӢ**\n(1 USD = {tjs:.4f} TJS)\n\n"
        # 160+ пули ҷаҳон
        for code in ['USD','EUR','RUB','GBP','TRY','KZT','UZS','CNY','AED','KGS','TMT','AZN','BYN','UAH','INR','JPY','CHF','CAD','AUD']:
            if code in rates:
                msg += f"1 {code} = {tjs/rates[code]:.4f} TJS\n"
        bot.send_message(uid, msg, reply_markup=menu())
        return

    if "ҳамаи крипто" in low or "100 крипто" in low:
        try:
            r = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1", timeout=15).json()
            rates = get_fiat()
            tjs = rates.get('TJS',10.5)
            msg = "🚀 **ТОП 100 КРИПТО**\n\n"
            for c in r[:100]:
                msg += f"{c['symbol'].upper()} = ${c['current_price']} = {c['current_price']*tjs:.2f} TJS\n"
            bot.send_message(uid, msg[:4000], reply_markup=menu())
        except:
            bot.send_message(uid, "Хатои интернет, боз кӯшиш кун!")
        return

    # Ҳар пули алоҳида
    rates = get_fiat()
    tjs = rates.get('TJS',10.5)

    if "доллар" in low or "usd" in low or low=="доллар чанд":
        bot.send_message(uid, f"💵 **1 Доллар = {tjs:.4f} сомонӣ**", reply_markup=menu()); return
    if "евро" in low or "eur" in low:
        eur = rates.get('EUR',0.92); bot.send_message(uid, f"💶 **1 Евро = {tjs/eur:.4f} сомонӣ**", reply_markup=menu()); return
    if "рубл" in low or "rub" in low or "сом чанд" not in low and "рубл чанд" in low:
        rub = rates.get('RUB',92); bot.send_message(uid, f"💷 **1 Рубл = {tjs/rub:.4f} сомонӣ**\n(Дар расми ту 0.1124 буд)", reply_markup=menu()); return
    if "сом" in low: # сом чанд
        bot.send_message(uid, f"🇹🇯 **1 Сомонӣ = 1 сомонӣ** 😊\n1 Доллар = {tjs:.4f} TJS", reply_markup=menu()); return

    if "биткоин" in low or "btc" in low or "бити" in low:
        p = get_crypto("bitcoin"); bot.send_message(uid, f"₿ **Биткоин = ${p['usd']} = {p['usd']*tjs:.2f} TJS**", reply_markup=menu()); return
    if "эфир" in low or "eth" in low:
        p = get_crypto("ethereum"); bot.send_message(uid, f"🌐 **Эфир = ${p['usd']}**", reply_markup=menu()); return
    if "тон" in low or "ton" in low:
        p = get_crypto("the-open-network"); bot.send_message(uid, f"💎 **Тон = ${p['usd']}**", reply_markup=menu()); return
    if "pepe" in low:
        p = get_crypto("pepe"); bot.send_message(uid, f"🐸 **PEPE = ${p['usd']}**", reply_markup=menu()); return

    bot.send_message(uid, "Навиш: Доллар чанд, Евро чанд, Рубл чанд, Биткоин чанд, Тон чанд\nЁ тугмаҳоро пахш кун 👇", reply_markup=menu())

bot.infinity_polling()
