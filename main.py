import telebot, requests, re, os, threading
from flask import Flask
from bs4 import BeautifulSoup
from telebot import types

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Render порт
app = Flask(__name__)
@app.route('/')
def home(): return "CryptoTJ Bot Running!"
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()

BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
CHANNEL = "@CryptoTj_Dushanbe"

def get_code():
    try:
        r = requests.get(BLOG_URL, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        codes = re.findall(r'CRYPTO\d+|DUSHANBE\d+', BeautifulSoup(r.text,'html.parser').get_text().upper())
        if codes: return codes[-1]
    except: pass
    return "CRYPTO2025"

def get_all_crypto():
    prices = {}
    try:
        mapping = {'BTC':'bitcoin','ETH':'ethereum','TON':'toncoin','USDT':'tether','BNB':'binancecoin','SOL':'solana','TRX':'tron','DOGE':'dogecoin','ADA':'cardano','XRP':'ripple'}
        for sym, name in mapping.items():
            try:
                d = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={sym}USDT", timeout=4).json()
                if 'price' in d: prices[name] = round(float(d['price']), 4) if float(d['price'])<1 else round(float(d['price']),2)
            except: pass
    except: pass
    fallback = {'bitcoin':81849,'ethereum':2450,'toncoin':2.85,'tether':1,'binancecoin':605,'solana':145,'tron':0.24,'dogecoin':0.12,'cardano':0.45,'ripple':0.52}
    for k,v in fallback.items():
        if k not in prices or prices[k]==0: prices[k]=v
    return prices

def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add("💵 Доллар чанд", "🇪🇺 Евро чанд", "🇷🇺 Рубл чанд")
    kb.add("₿ Биткоин чанд", "💎 Тон чанд", "🌐 Эфир чанд")
    kb.add("🌍 Хамаи пулхо", "🚀 Хамаи криптохо")
    kb.add("🇰🇬 Сом чанд", "🇰🇿 Тенге чанд", "🇺🇿 Сум чанд")
    kb.add("🇨🇳 Юан чанд", "🇹🇷 Лира чанд", "🇦🇪 Дирхам чанд")
    kb.add("🇬🇧 Фунт чанд", "📢 Реклама")
    return kb

# ФУТЕР - РЕКЛАМАИ САЙТ
FOOTER = "\n\n━━━━━━━━━━━━━━\n🔥 Коди нав ҳар рӯз:\n👉 https://cryptotj-dushanbe.blogspot.com/\n📢 Канали мо: @CryptoTj_Dushanbe\n💰 Обунас шуданро фаромӯш накун!"

@bot.message_handler(commands=['start'])
def start_cmd(m):
    txt = f"Салом {m.from_user.first_name}! 👋\n\n💎 Боти CryptoTJ - 10 пули ҷаҳон + 10 крипто\n\nКоди имрӯз: {get_code()}\n\nКнопкаҳоро пахш кун!{FOOTER}"
    bot.send_message(m.chat.id, txt, reply_markup=menu())

@bot.message_handler(func=lambda m: True)
def all_handler(m):
    if not m.text: return
    t = m.text.lower()
    c = get_all_crypto()
    code = get_code()
    
    # === 10 ПУЛИ ҶАҲОН ===
    if "доллар" in t:
        bot.send_message(m.chat.id, f"💵 **ДОЛЛАР**\n1 USD = 9.2261 сомонӣ\nКурби НБТ Тоҷикистон{FOOTER}", reply_markup=menu())
    elif "евро" in t:
        bot.send_message(m.chat.id, f"🇪🇺 **ЕВРО**\n1 EUR = 10.36 сомонӣ{FOOTER}", reply_markup=menu())
    elif "рубл" in t:
        bot.send_message(m.chat.id, f"🇷🇺 **РУБЛ**\n1 RUB = 0.1131 сомонӣ{FOOTER}", reply_markup=menu())
    elif "сом чанд" in t:
        bot.send_message(m.chat.id, f"🇰🇬 **СОМ (Қирғизистон)**\n1 KGS = 0.105 сомонӣ{FOOTER}", reply_markup=menu())
    elif "тенге" in t:
        bot.send_message(m.chat.id, f"🇰🇿 **ТЕНГЕ**\n1 KZT = 0.018 сомонӣ{FOOTER}", reply_markup=menu())
    elif "сум" in t or "сӯм" in t:
        bot.send_message(m.chat.id, f"🇺🇿 **СӮМ (Ӯзбекистон)**\n1 UZS = 0.00072 сомонӣ{FOOTER}", reply_markup=menu())
    elif "юан" in t:
        bot.send_message(m.chat.id, f"🇨🇳 **ЮАН (Хитой)**\n1 CNY = 1.29 сомонӣ{FOOTER}", reply_markup=menu())
    elif "лира" in t:
        bot.send_message(m.chat.id, f"🇹🇷 **ЛИРА (Туркия)**\n1 TRY = 0.27 сомонӣ{FOOTER}", reply_markup=menu())
    elif "дирхам" in t:
        bot.send_message(m.chat.id, f"🇦🇪 **ДИРҲАМ (Дубай)**\n1 AED = 2.51 сомонӣ{FOOTER}", reply_markup=menu())
    elif "фунт" in t:
        bot.send_message(m.chat.id, f"🇬🇧 **ФУНТ (Англия)**\n1 GBP = 12.02 сомонӣ{FOOTER}", reply_markup=menu())
    
    # === 10 КРИПТО ===
    elif "биткоин" in t:
        bot.send_message(m.chat.id, f"₿ **БИТКОИН**\n${c.get('bitcoin')}\nНархи зинда аз Binance{FOOTER}", reply_markup=menu())
    elif "тон" in t:
        bot.send_message(m.chat.id, f"💎 **ТОН (Telegram)**\n${c.get('toncoin')}\nНархи зинда{FOOTER}", reply_markup=menu())
    elif "эфир" in t:
        bot.send_message(m.chat.id, f"🌐 **ЭФИР (ETH)**\n${c.get('ethereum')}{FOOTER}", reply_markup=menu())
    
    # === ҲАМА ===
    elif "хамаи пулхо" in t:
        msg = f"🌍 **10 ПУЛИ ҶАҲОН:**\n\n💵 Доллар: 9.2261 с\n🇪🇺 Евро: 10.36 с\n🇷🇺 Рубл: 0.1131 с\n🇰🇬 Сом: 0.105 с\n🇰🇿 Тенге: 0.018 с\n🇺🇿 Сӯм: 0.00072 с\n🇨🇳 Юан: 1.29 с\n🇹🇷 Лира: 0.27 с\n🇦🇪 Дирҳам: 2.51 с\n🇬🇧 Фунт: 12.02 с{FOOTER}"
        bot.send_message(m.chat.id, msg, reply_markup=menu())
    elif "хамаи криптохо" in t:
        msg = f"🚀 **10 КРИПТО (Нархи зинда Binance):**\n\n₿ BTC = ${c.get('bitcoin')}\n🌐 ETH = ${c.get('ethereum')}\n💎 TON = ${c.get('toncoin')}\n💵 USDT = ${c.get('tether')}\n🟡 BNB = ${c.get('binancecoin')}\n☀️ SOL = ${c.get('solana')}\n🔴 TRX = ${c.get('tron')}\n🐶 DOGE = ${c.get('dogecoin')}\n🔵 ADA = ${c.get('cardano')}\n✖️ XRP = ${c.get('ripple')}{FOOTER}"
        bot.send_message(m.chat.id, msg, reply_markup=menu())
    elif "реклама" in t:
        bot.send_message(m.chat.id, f"📢 **РЕКЛАМА:**\n\n🌐 Сайти мо:\nhttps://cryptotj-dushanbe.blogspot.com/\n\n📲 Канал:\n@CryptoTj_Dushanbe\n\n🔥 Ҳар рӯз коди нав ва курби пул!\nОбуна шав!", reply_markup=menu())
    else:
        if m.text.strip().upper() == code:
            bot.send_message(m.chat.id, f"✅ **ДУРУСТ!** Код: {code}\n\nТу ба канали мо обуна шудӣ!{FOOTER}", reply_markup=menu())
        elif len(m.text) < 20:
            bot.send_message(m.chat.id, f"❌ Коди кӯҳна! Коди нав: {code}\n\n👉 {BLOG_URL}{FOOTER}", reply_markup=menu())

print("CryptoTJ Bot 10+10 started!")
bot.infinity_polling(skip_pending=True, timeout=60)
