import telebot, requests, re, os, threading
from flask import Flask
from bs4 import BeautifulSoup
from telebot import types

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home(): return "CryptoTj 13 LIVE + USERS OK"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()

BLOG = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
FOOT = "\n\n━━━━━━━━━━━━━━\n🔥 13 LIVE:\n👉 https://cryptotj-dushanbe.blogspot.com/\n📢 @CryptoTj_Dushanbe"
USERS_FILE = "users.txt"
users = set()

def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                for l in f:
                    if l.strip(): users.add(int(l.strip()))
    except: pass
load_users()

def add_user(uid):
    if uid not in users:
        users.add(uid)
        try:
            with open(USERS_FILE, "a") as f: f.write(f"{uid}\n")
        except: pass

def get_code():
    try:
        r = requests.get(BLOG, headers={'User-Agent':'Mozilla/5.0'}, timeout=8)
        f = re.findall(r'CRYPTO\d+|DUSHANBE\d+', BeautifulSoup(r.text,'html.parser').get_text().upper())
        if f: return f[-1]
    except: pass
    return "CRYPTO2025"

def get_all_live():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,the-open-network,pi-network,dogecoin,ripple,solana&vs_currencies=usd"
        d = requests.get(url, timeout=10).json()
        return {
            'BTC': d['bitcoin']['usd'], 'ETH': d['ethereum']['usd'],
            'TON': d['the-open-network']['usd'], 'PI': d.get('pi-network',{}).get('usd',0.08),
            'DOGE': d['dogecoin']['usd'], 'XRP': d['ripple']['usd'], 'SOL': d['solana']['usd'],
            'USD': 10.82, 'EUR': 10.35, 'CNY': 1.38, 'RUB': 0.13, 'GBP': 13.95, 'GOLD': 1247.80
        }
    except:
        return {'BTC':82790,'ETH':2444,'TON':1.35,'PI':0.08,'DOGE':0.08,'XRP':1.34,'SOL':90,'USD':10.82,'EUR':10.35,'CNY':1.38,'RUB':0.13,'GBP':13.95,'GOLD':1247.80}

def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add("🌍 13 LIVE","💵 Доллар","🇪🇺 Евро")
    kb.add("🇨🇳 Юан","🇷🇺 Рубл","🇬🇧 Фунт")
    kb.add("₿ Биткоин","💎 Тон","☀️ Солана")
    kb.add("🌐 Эфир","🐶 Доге","💧 XRP")
    kb.add("🟡 Тилло","🟣 Pi")
    kb.add("👥 Одам ҳисоб")
    return kb

@bot.message_handler(commands=['start'])
def s(m):
    add_user(m.chat.id)
    bot.send_message(m.chat.id, f"Салом! Ту нафари {len(users)}-ум ҳастӣ! 🚀\n\n💵 USD 10.82 | 🇪🇺 EUR 10.35 | 🇨🇳 CNY 1.38\n🇷🇺 RUB 0.13 | 🇬🇧 GBP 13.95\nКоди: {get_code()}{FOOT}", reply_markup=menu())

@bot.message_handler(func=lambda m: True)
def h(m):
    if not m.text: return
    t=m.text.lower()
    p=get_all_live()
    if "13 live" in t or "11 live" in t:
        txt=f"📊 MARKETS - 13 LIVE\n\n🟡 Gold {p['GOLD']}\n₿ BTC ${p['BTC']}\n💎 TON ${p['TON']}\n🟣 PI ${p['PI']}\n🐶 DOGE ${p['DOGE']}\n💵 USD {p['USD']}\n💧 XRP ${p['XRP']}\n🌐 ETH ${p['ETH']}\n🇪🇺 EUR {p['EUR']}\n🇨🇳 CNY {p['CNY']}\n🇷🇺 RUB {p['RUB']}\n🇬🇧 GBP {p['GBP']}\n☀️ SOL ${p['SOL']}{FOOT}"
        bot.send_message(m.chat.id, txt, reply_markup=menu())
    elif "одам" in t or "ҳисоб" in t:
        bot.send_message(m.chat.id, f"👥 СТАТИСТИКА\n\n👤 Ҳамагӣ: {len(users)} нафар даромад\n🆕 Ту: {m.chat.id}\n📊 Бот фаъол!\n\nХоҳӣ рӯйхати ҳамаро фиристам?{FOOT}", reply_markup=menu())
    elif "доллар" in t: bot.send_message(m.chat.id, f"💵 Dollar {p['USD']} TJS{FOOT}", reply_markup=menu())
    elif "евро" in t: bot.send_message(m.chat.id, f"🇪🇺 Euro {p['EUR']} TJS{FOOT}", reply_markup=menu())
    elif "юан" in t: bot.send_message(m.chat.id, f"🇨🇳 Yuan {p['CNY']} TJS{FOOT}", reply_markup=menu())
    elif "рубл" in t: bot.send_message(m.chat.id, f"🇷🇺 Рубл {p['RUB']} TJS | 1000={round(p['RUB']*1000)} TJS{FOOT}", reply_markup=menu())
    elif "фунт" in t: bot.send_message(m.chat.id, f"🇬🇧 Фунт {p['GBP']} TJS{FOOT}", reply_markup=menu())
    elif "биткоин" in t: bot.send_message(m.chat.id, f"₿ BTC ${p['BTC']} = {round(p['BTC']*p['USD'])} TJS{FOOT}", reply_markup=menu())
    elif "тон" in t: bot.send_message(m.chat.id, f"💎 TON ${p['TON']}{FOOT}", reply_markup=menu())
    elif "солана" in t: bot.send_message(m.chat.id, f"☀️ SOL ${p['SOL']}{FOOT}", reply_markup=menu())
    elif "эфир" in t: bot.send_message(m.chat.id, f"🌐 ETH ${p['ETH']}{FOOT}", reply_markup=menu())
    elif "доге" in t: bot.send_message(m.chat.id, f"🐶 DOGE ${p['DOGE']}{FOOT}", reply_markup=menu())
    elif "xrp" in t: bot.send_message(m.chat.id, f"💧 XRP ${p['XRP']}{FOOT}", reply_markup=menu())
    elif "тилло" in t: bot.send_message(m.chat.id, f"🟡 Gold {p['GOLD']} TJS/g{FOOT}", reply_markup=menu())
    elif "pi" in t: bot.send_message(m.chat.id, f"🟣 PI ${p['PI']}{FOOT}", reply_markup=menu())
    else:
        real=get_code()
        if m.text.strip().upper()==real: bot.send_message(m.chat.id, f"✅ Дуруст! {real}{FOOT}", reply_markup=menu())

bot.remove_webhook()
import time; time.sleep(1)
print(f"13 LIVE + {len(users)} USERS STARTED")
bot.infinity_polling(skip_pending=True)
