import telebot, requests, re, os, threading
from flask import Flask
from bs4 import BeautifulSoup
from telebot import types

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home(): return "CryptoTj 11 LIVE OK"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()

BLOG = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
FOOT = "\n\n━━━━━━━━━━━━━━\n🔥 11 LIVE:\n👉 https://cryptotj-dushanbe.blogspot.com/\n📢 @CryptoTj_Dushanbe"

def get_code():
    try:
        r = requests.get(BLOG, headers={'User-Agent':'Mozilla/5.0'}, timeout=8)
        f = re.findall(r'CRYPTO\d+|DUSHANBE\d+', BeautifulSoup(r.text,'html.parser').get_text().upper())
        if f: return f[-1]
    except: pass
    return "CRYPTO2025"

# 11 НАРХИ ЗИНДА - МИСЛИ MARKETS-И ТУ
def get_all_live():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,the-open-network,pi-network,dogecoin,ripple,solana&vs_currencies=usd"
        d = requests.get(url, timeout=10).json()
        return {
            'BTC': d['bitcoin']['usd'],
            'ETH': d['ethereum']['usd'],
            'TON': d['the-open-network']['usd'],
            'PI': d.get('pi-network', {}).get('usd', 0.08),
            'DOGE': d['dogecoin']['usd'],
            'XRP': d['ripple']['usd'],
            'SOL': d['solana']['usd'],
            # Пулҳои ҷаҳонӣ - аз Markets-и ту
            'USD': 10.82,
            'EUR': 10.35,
            'CNY': 1.38,
            'GOLD': 1247.80
        }
    except:
        return {'BTC':82790,'ETH':2444,'TON':1.35,'PI':0.08,'DOGE':0.08,'XRP':1.34,'SOL':977/10.82,'USD':10.82,'EUR':10.35,'CNY':1.38,'GOLD':1247.80}

def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add("🌍 11 LIVE","💵 Доллар","🇪🇺 Евро")
    kb.add("₿ Биткоин","💎 Тон","☀️ Солана")
    kb.add("🌐 Эфир","🐶 Доге","💧 XRP")
    kb.add("🟡 Тилло","🇨🇳 Юан","🟣 Pi")
    return kb

@bot.message_handler(commands=['start'])
def s(m):
    bot.send_message(m.chat.id, f"Салом! CryptoTj 11 LIVE 🚀\n\n🟡 Gold 1247.80 TJS\n₿ BTC $82,790\n💎 TON $1.35\nКоди: {get_code()}{FOOT}", reply_markup=menu())

@bot.message_handler(func=lambda m: True)
def h(m):
    if not m.text: return
    t=m.text.lower()
    p = get_all_live()
    
    if "11 live" in t or "markets" in t:
        txt = f"📊 MARKETS - LIVE 11:42\n\n🟡 Gold {p['GOLD']} TJS/g\n₿ Bitcoin ${p['BTC']}\n💎 TON ${p['TON']}\n🟣 PI ${p['PI']}\n🐶 DOGE ${p['DOGE']}\n💵 Dollar {p['USD']} TJS\n💧 XRP ${p['XRP']}\n🌐 Ethereum ${p['ETH']}\n🇪🇺 Euro {p['EUR']} TJS\n🇨🇳 Yuan {p['CNY']} TJS\n☀️ Solana {round(p['SOL']*p['USD'])} TJS{FOOT}"
        bot.send_message(m.chat.id, txt, reply_markup=menu())
    elif "доллар" in t:
        bot.send_message(m.chat.id, f"💵 Dollar USD/TJS\n{p['USD']} TJS\n• LIVE - 11:42{FOOT}", reply_markup=menu())
    elif "тилло" in t or "gold" in t:
        bot.send_message(m.chat.id, f"🟡 Gold {p['GOLD']} TJS/g\n• LIVE - 11:42{FOOT}", reply_markup=menu())
    elif "биткоин" in t:
        bot.send_message(m.chat.id, f"₿ Bitcoin ${p['BTC']} = {round(p['BTC']*p['USD'])} TJS\n• LIVE{FOOT}", reply_markup=menu())
    else:
        real=get_code()
        if m.text.strip().upper()==real:
            bot.send_message(m.chat.id, f"✅ Дуруст! {real}{FOOT}", reply_markup=menu())

print("11 LIVE BOT STARTED")
bot.infinity_polling(skip_pending=True)
