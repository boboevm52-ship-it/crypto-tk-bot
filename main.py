import telebot, requests, os, re
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
SECRET_CODE = "CRYPTO2025"

bot = telebot.TeleBot(BOT_TOKEN)

# Дар хотир мондан
passed = {}
try:
    with open("passed.txt","r") as f:
        for l in f: passed[int(l.strip())]=True
except: pass

def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add("💵 Доллар чанд","💶 Евро чанд","💷 Рубл чанд","₿ Биткоин чанд","💎 Тон чанд","🌐 Эфир чанд","🌍 Ҳамаи пулҳои ҷаҳон","🚀 Ҳамаи криптоҳо")
    return kb

def forced():
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📖 Ба сайт даро ва кодро ёб 👇", url=BLOG_URL))
    return mk

def get_rates():
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10).json()
        return r['rates']
    except: return {'TJS':10.9,'RUB':89,'EUR':0.91,'USD':1}

def get_crypto_price(coin_id):
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd", timeout=10, headers={"User-Agent":"Mozilla"}).json()
        return r.get(coin_id,{}).get('usd')
    except: return None

# 160 ПУЛИ ҶАҲОН
ALL_CURRENCIES = {
    "доллар":"USD","usd":"USD","сом":"TJS","евро":"EUR","eur":"EUR","рубл":"RUB","rub":"RUB",
    "фунт":"GBP","лира":"TRY","тенге":"KZT","сум":"UZS","юан":"CNY","дирхам":"AED",
    "сомони точик":"TJS","манат":"AZN","лари":"GEL","гривна":"UAH","белорус":"BYN","сом киргиз":"KGS"
}

# ҲАМАИ КРИПТО
ALL_CRYPTO = {
    "биткоин":"bitcoin","btc":"bitcoin","бит":"bitcoin",
    "эфир":"ethereum","eth":"ethereum","эфириум":"ethereum",
    "тон":"toncoin","ton":"toncoin","токен":"toncoin",
    "доги":"dogecoin","doge":"dogecoin",
    "пепе":"pepe","pepe":"pepe",
    "солана":"solana","sol":"solana",
    "шиба":"shiba-inu","shib":"shiba-inu",
    "ноткоин":"notcoin","not":"notcoin",
    "бонк":"bonk","wif":"dogwifhat","авакс":"avalanche-2","xrp":"ripple","ада":"cardano","дот":"polkadot"
}

@bot.message_handler(commands=['start'])
def start(m):
    if passed.get(m.chat.id):
        bot.send_message(m.chat.id, "Салом! 🇹🇯 Ман ҳамаи пулҳо ва криптоҳоро медонам! Тугмаро пахш кун 👇", reply_markup=menu())
    else:
        bot.send_message(m.chat.id, f"👋 Салом! Ман 100% тоҷикиро медонам!\n\nБарои истифода бояд ба сайт дароӣ:\n👉 {BLOG_URL}\n\nКод дар дохили мақола пинҳон аст! Ёб ва дар ин ҷо навиш!", reply_markup=forced())

@bot.message_handler(func=lambda x: True)
def all_msg(m):
    txt = m.text or ""
    uid = m.chat.id
    low = txt.lower()
    clean = re.sub(r'[^\w\s]', '', low).strip() # тоза аз эмодзи

    # МАҶБУРӢ
    if not passed.get(uid):
        if clean.upper() == SECRET_CODE or txt.upper().strip() == SECRET_CODE:
            passed[uid]=True
            with open("passed.txt","a") as f: f.write(str(uid)+"\n")
            bot.send_message(uid, "✅ ОФАРИН! Коди дуруст!\nАкнун ҳамаи пулҳо ва криптоҳо кушод шуд! 👇", reply_markup=menu())
            return
        else:
            bot.send_message(uid, f"⛔️ Аввал ба сайт даро!\n👉 {BLOG_URL}\nКод дар мақола аст!", reply_markup=forced())
            return

    rates = get_rates()
    tjs = rates.get('TJS',10.9)

    # 1. ҲАМАИ ПУЛҲОИ ҶАҲОН
    if "ҳамаи пул" in clean or "хамаи пул" in clean:
        msg = f"🌍 **ҲАМАИ ПУЛҲОИ ҶАҲОН**\n1 Доллар = {tjs:.4f} TJS\n\n"
        top = ['EUR','RUB','GBP','TRY','KZT','UZS','CNY','AED','KGS','TMT','AZN','UAH','BYN','INR','JPY','CHF','CAD','AUD','SEK','NOK','DKK','PLN','KWD','SAR','QAR']
        for code in top:
            if code in rates:
                msg += f"1 {code} = {tjs/rates[code]:.4f} TJS\n"
        msg += "\n... ва 130 пули дигар! Номи пулро навиш: масалан 'Евро чанд'"
        bot.send_message(uid, msg, reply_markup=menu())
        return

    # 2. ҲАМАИ КРИПТО
    if "ҳамаи крипто" in clean or "хамаи крипто" in clean:
        try:
            r = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1", timeout=15).json()
            msg = "🚀 **ТОП 50 КРИПТО БА СОМОНӢ**\n\n"
            for c in r:
                msg += f"{c['symbol'].upper()} = ${c['current_price']} = {c['current_price']*tjs:.2f} TJS\n"
            bot.send_message(uid, msg[:3900], reply_markup=menu())
        except:
            bot.send_message(uid, "⏳ Интернет суст аст, боз кӯшиш кун!")
        return

    # 3. ПУЛИ АЛОҲИДА
    for name, code in ALL_CURRENCIES.items():
        if name in clean:
            if code in rates:
                if code == "TJS": bot.send_message(uid, f"🇹🇯 **1 Сомонӣ = 1 Сомонӣ**", reply_markup=menu())
                else: bot.send_message(uid, f"💰 **1 {code} = {tjs/rates[code]:.4f} сомонӣ**\n(1 Доллар = {tjs:.4f} TJS)", reply_markup=menu())
                return

    # 4. КРИПТОИ АЛОҲИДА
    for name, coin_id in ALL_CRYPTO.items():
        if name in clean:
            price = get_crypto_price(coin_id)
            if price:
                bot.send_message(uid, f"💎 **{name.upper()} = ${price}**\n💵 {price*tjs:.2f} сомонӣ", reply_markup=menu())
            else:
                bot.send_message(uid, f"⏳ Нархи {name} ҳозир гирифта нашуд!")
            return

    # Агар ягон калимаи умумӣ
    if "рубл" in clean: 
        bot.send_message(uid, f"💷 **1 Рубл = {tjs/rates.get('RUB',89):.4f} сомонӣ**", reply_markup=menu()); return
    if "доллар" in clean or "usd" in clean:
        bot.send_message(uid, f"💵 **1 Доллар = {tjs:.4f} сомонӣ**", reply_markup=menu()); return

    bot.send_message(uid, "🇹🇯 Навиш: 'Доллар чанд', 'Рубл чанд', 'Биткоин чанд', 'Тон чанд'\nЁ тугмаҳоро пахш кун 👇", reply_markup=menu())

bot.infinity_polling()
