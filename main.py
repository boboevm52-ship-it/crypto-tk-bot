import telebot, requests, re, os, threading
from flask import Flask
from bs4 import BeautifulSoup
from telebot import types

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home(): return "OK LIVE BOT"
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()

BLOG = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
FOOT = "\n\n━━━━━━━━━━━━━━\n🔥 Коди нав:\n👉 https://cryptotj-dushanbe.blogspot.com/\n📢 @CryptoTj_Dushanbe\n☀️ ЗИНДА АВТОМАТ"

# --- КОДИ ЗИНДА АЗ БЛОГ ---
def get_code():
    try:
        r = requests.get(BLOG, headers={'User-Agent':'Mozilla/5.0'}, timeout=8)
        f = re.findall(r'CRYPTO\d+|DUSHANBE\d+', BeautifulSoup(r.text,'html.parser').get_text().upper())
        if f: return f[-1]
    except: pass
    return "CRYPTO2025"

# --- НАРХИ ЗИНДА АЗ COINGECKO (мисли блоги ту) ---
def get_crypto_live():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,the-open-network,tether,binancecoin,solana,tron,dogecoin,cardano,ripple&vs_currencies=usd"
        data = requests.get(url, timeout=10).json()
        return {
            'bitcoin': data['bitcoin']['usd'],
            'ethereum': data['ethereum']['usd'],
            'toncoin': data['the-open-network']['usd'],
            'tether': data['tether']['usd'],
            'binancecoin': data['binancecoin']['usd'],
            'solana': data['solana']['usd'],
            'tron': data['tron']['usd'],
            'dogecoin': data['dogecoin']['usd'],
            'cardano': data['cardano']['usd'],
            'ripple': data['ripple']['usd']
        }
    except:
        return {'bitcoin':82027,'ethereum':2420,'toncoin':2.85,'tether':1,'binancecoin':602,'solana':103.87,'tron':0.24,'dogecoin':0.115,'cardano':0.42,'ripple':0.51}

def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add("💵 Доллар чанд","🇷🇺 Рубл чанд","🇪🇺 Евро чанд")
    kb.add("₿ Биткоин чанд","💎 Тон чанд","☀️ Солана чанд")
    kb.add("🌍 Хамаи пулхо","🚀 Хамаи криптохо")
    return kb

@bot.message_handler(commands=['start'])
def s(m):
    bot.send_message(m.chat.id, f"Салом! Боти ЗИНДА! ☀️\nКоди имрӯз: {get_code()}{FOOT}", reply_markup=menu())

@bot.message_handler(func=lambda m: True)
def h(m):
    if not m.text: return
    t=m.text.lower()
    c = get_crypto_live() # ХАР ДАФЪА ЗИНДА!
    usd_tjs = 9.2261

    if "доллар" in t:
        bot.send_message(m.chat.id, f"🇺🇸 Доллар = {usd_tjs} сомонӣ\n☀️ ЗИНДА{FOOT}", reply_markup=menu())
    elif "биткоин" in t:
        bot.send_message(m.chat.id, f"₿ Биткоин = ${c['bitcoin']}\n= {round(c['bitcoin']*usd_tjs)} TJS\n☀️ ЗИНДА АВТОМАТ{FOOT}", reply_markup=menu())
    elif "тон" in t:
        bot.send_message(m.chat.id, f"💎 Тон = ${c['toncoin']}{FOOT}", reply_markup=menu())
    elif "солана" in t or "solana" in t:
        tjs = round(c['solana']*usd_tjs)
        bot.send_message(m.chat.id, f"☀️ Нархи SOLANA имруз - LIVE АВТОМАТ\n\n1 SOL = {tjs} TJS\n{c['solana']} $ = 1 SOL\n\n• ЗИНДА АВТОМАТ{FOOT}", reply_markup=menu())
    elif "эфир" in t:
        bot.send_message(m.chat.id, f"🌐 Эфир = ${c['ethereum']}{FOOT}", reply_markup=menu())
    elif "хамаи криптохо" in t:
        txt = f"🚀 10 КРИПТО - ЗИНДА:\n"
        txt += f"BTC ${c['bitcoin']}\nETH ${c['ethereum']}\nTON ${c['toncoin']}\nUSDT ${c['tether']}\nBNB ${c['binancecoin']}\nSOL ${c['solana']} ({round(c['solana']*usd_tjs)} TJS)\nTRX ${c['tron']}\nDOGE ${c['dogecoin']}\nADA ${c['cardano']}\nXRP ${c['ripple']}{FOOT}"
        bot.send_message(m.chat.id, txt, reply_markup=menu())
    elif "хамаи пулхо" in t:
        bot.send_message(m.chat.id, f"🌍 10 ПУЛ:\nДоллар 9.22\nЕвро 10.36\nРубл 0.113\nСом 0.105\nТенге 0.018\nСўм 0.00072\nЮан 1.29\nЛира 0.27\nДирҳам 2.51\nФунт 12.02{FOOT}", reply_markup=menu())
    else:
        real=get_code()
        if m.text.strip().upper()==real:
            bot.send_message(m.chat.id, f"✅ Дуруст! {real}{FOOT}", reply_markup=menu())
        elif len(m.text)<15:
            bot.send_message(m.chat.id, f"❌ Нодуруст! Коди нав: {real}\n{BLOG}{FOOT}", reply_markup=menu())

print("LIVE STARTED")
bot.infinity_polling(skip_pending=True)
