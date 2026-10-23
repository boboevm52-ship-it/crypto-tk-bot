import telebot
import requests
import re
from bs4 import BeautifulSoup

TOKEN = "TOKEN-и БОТАТРО ИНҶО ГУЗОР"
bot = telebot.TeleBot(TOKEN)

BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
USD_TJS = 9.2261

def get_code():
    try:
        r = requests.get(BLOG_URL, headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
        text = BeautifulSoup(r.text, 'html.parser').get_text().upper()
        codes = re.findall(r'CRYPTO\d+|DUSHANBE\d+', text)
        if codes:
            return codes[-1]
        m = re.search(r'КОДИ НАВ[:\s]+([A-Z0-9]+)', text)
        if m:
            return m.group(1)
    except Exception as e:
        print(e)
    return "CRYPTO2025"

def get_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,the-open-network,tether,binancecoin,solana,tron,dogecoin,cardano,ripple&vs_currencies=usd"
        r = requests.get(url, timeout=10).json()
        return r
    except:
        return {}

FOOTER = "\n\n👉 Бо сайти мо обуна шавед:\nhttps://cryptotj-dushanbe.blogspot.com/"

# ========== 1. ТУГМАҲОИ ПУЛ - ПЕШ БОЯД БОШАНД ==========

@bot.message_handler(func=lambda m: m.text and "Доллар чанд" in m.text)
def dollar(m):
    bot.send_message(m.chat.id, f"💵 1 Доллар = {USD_TJS} сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Рубл чанд" in m.text)
def rubl(m):
    bot.send_message(m.chat.id, f"🇷🇺 1 Рубл = 0.1131 сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Биткоин чанд" in m.text)
def btc(m):
    c = get_crypto()
    p = c.get('bitcoin',{}).get('usd',0)
    bot.send_message(m.chat.id, f"₿ Биткоин = ${p} = {p*USD_TJS:.2f} сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Тон чанд" in m.text)
def ton(m):
    c = get_crypto()
    p = c.get('the-open-network',{}).get('usd',0)
    bot.send_message(m.chat.id, f"💎 Тон = ${p} = {p*USD_TJS:.2f} сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Эфир чанд" in m.text)
def eth(m):
    c = get_crypto()
    p = c.get('ethereum',{}).get('usd',0)
    bot.send_message(m.chat.id, f"🌐 Эфир = ${p} = {p*USD_TJS:.2f} сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Хамаи пулхо" in m.text)
def all_money(m):
    txt = """🌍 10 пули ҷаҳон ба сомонӣ:

🇺🇸 Доллар = 9.2261 сомонӣ
🇪🇺 Евро = 10.3655 сомонӣ
🇷🇺 Рубл = 0.1131 сомонӣ
🇰🇬 Сом = 0.105 сомонӣ
🇰🇿 Тенге = 0.018 сомонӣ
🇺🇿 Сӯм = 0.00072 сомонӣ
🇨🇳 Юан = 1.29 сомонӣ
🇹🇷 Лира = 0.27 сомонӣ
🇦🇪 Дирҳам = 2.51 сомонӣ
🇬🇧 Фунт = 12.02 сомонӣ"""
    bot.send_message(m.chat.id, txt + FOOTER)

@bot.message_handler(func=lambda m: m.text and "Хамаи криптохо" in m.text)
def all_crypto(m):
    c = get_crypto()
    txt = f"""🚀 10 криптои машҳур:

₿ Биткоин = ${c.get('bitcoin',{{}}).get('usd',0)}
🌐 Эфириум = ${c.get('ethereum',{{}}).get('usd',0)}
💎 Тон = ${c.get('the-open-network',{{}}).get('usd',0)}
💵 USDT = ${c.get('tether',{{}}).get('usd',0)}
🟡 BNB = ${c.get('binancecoin',{{}}).get('usd',0)}
☀️ Solana = ${c.get('solana',{{}}).get('usd',0)}
🔴 Tron = ${c.get('tron',{{}}).get('usd',0)}
🐶 Dogecoin = ${c.get('dogecoin',{{}}).get('usd',0)}
🔵 Cardano = ${c.get('cardano',{{}}).get('usd',0)}
✖️ XRP = ${c.get('ripple',{{}}).get('usd',0)}"""
    bot.send_message(m.chat.id, txt + FOOTER)

@bot.message_handler(func=lambda m: m.text and "Дирхам чанд" in m.text)
def dirham(m):
    bot.send_message(m.chat.id, f"🇦🇪 1 Дирҳам = 2.51 сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Тенге чанд" in m.text)
def tenge(m):
    bot.send_message(m.chat.id, f"🇰🇿 1 Тенге = 0.018 сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Сум чанд" in m.text)
def sum_func(m):
    bot.send_message(m.chat.id, f"🇺🇿 1000 Сӯм = 0.72 сомонӣ{FOOTER}")

# ========== 2. САНҶИШИ КОД - ДАР ОХИР ==========

@bot.message_handler(commands=['start'])
def start(m):
    code = get_code()
    bot.send_message(m.chat.id, f"Салом! 👋\nКоди имрӯз аз сайт: {code}\n\nТугмаҳоро пахш кун, қурбро мегӯям.{FOOTER}")

@bot.message_handler(func=lambda m: True)
def check_code(m):
    text = m.text.strip()
    # Агар тугма бошад - ин функсия кор намекунад
    if "чанд" in text.lower() or "пулхо" in text.lower() or "криптохо" in text.lower() or text.startswith('/'):
        return
    
    real = get_code()
    if text.upper() == real:
        bot.send_message(m.chat.id, f"✅ Дуруст! Коди {real} қабул шуд!\n\nКанали мо: https://t.me/+YOUR_LINK{FOOTER}")
    else:
        bot.send_message(m.chat.id, f"❌ Коди кӯҳна не! Коди НАВ: {real}\nАз сайт ёб:\n{BLOG_URL}")

print("Bot started...")
bot.infinity_polling()
