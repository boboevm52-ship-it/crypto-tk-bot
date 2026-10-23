import telebot, requests, re, os
from bs4 import BeautifulSoup

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    TOKEN = "8253409959:AAE_TOKEN_I_KHATOGI_DORA"

bot = telebot.TeleBot(TOKEN)

BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
USD_TJS = 9.2261

def get_code():
    try:
        r = requests.get(BLOG_URL, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        t = BeautifulSoup(r.text, 'html.parser').get_text().upper()
        codes = re.findall(r'CRYPTO\d+|DUSHANBE\d+', t)
        if codes: return codes[-1]
    except: pass
    return "CRYPTO2025"

def get_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,the-open-network,tether,binancecoin,solana,tron,dogecoin,cardano,ripple&vs_currencies=usd"
        return requests.get(url, timeout=10).json()
    except: return {}

FOOTER = "\n\n━━━━━━━━━━━━━━\n🔥 Коди нав:\n👉 https://cryptotj-dushanbe.blogspot.com/\n📢 @CryptoTj_Dushanbe"

@bot.message_handler(func=lambda m: m.text and "Доллар чанд" in m.text)
def p1(m): bot.send_message(m.chat.id, f"💵 Доллар = {USD_TJS} сомонӣ{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Евро чанд" in m.text)
def p2(m): bot.send_message(m.chat.id, f"🇪🇺 Евро = 10.3655 сомонӣ{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Рубл чанд" in m.text)
def p3(m): bot.send_message(m.chat.id, f"🇷🇺 Рубл = 0.1131 сомонӣ{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Сом чанд" in m.text)
def p4(m): bot.send_message(m.chat.id, f"🇰🇬 Сом = 0.105 сомонӣ{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Тенге чанд" in m.text)
def p5(m): bot.send_message(m.chat.id, f"🇰🇿 Тенге = 0.018 сомонӣ{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Сум чанд" in m.text)
def p6(m): bot.send_message(m.chat.id, f"🇺🇿 Сӯм = 0.72 / 1000{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Юан чанд" in m.text)
def p7(m): bot.send_message(m.chat.id, f"🇨🇳 Юан = 1.29 сомонӣ{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Лира чанд" in m.text)
def p8(m): bot.send_message(m.chat.id, f"🇹🇷 Лира = 0.27 сомонӣ{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Дирхам чанд" in m.text)
def p9(m): bot.send_message(m.chat.id, f"🇦🇪 Дирҳам = 2.51 сомонӣ{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Фунт чанд" in m.text)
def p10(m): bot.send_message(m.chat.id, f"🇬🇧 Фунт = 12.02 сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Биткоин чанд" in m.text)
def c1(m):
    c=get_crypto(); p=c.get('bitcoin',{}).get('usd',0)
    bot.send_message(m.chat.id, f"₿ Биткоин = ${p}{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Эфир чанд" in m.text)
def c2(m):
    c=get_crypto(); p=c.get('ethereum',{}).get('usd',0)
    bot.send_message(m.chat.id, f"🌐 Эфир = ${p}{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Тон чанд" in m.text)
def c3(m):
    c=get_crypto(); p=c.get('the-open-network',{}).get('usd',0)
    bot.send_message(m.chat.id, f"💎 Тон = ${p}{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "USDT чанд" in m.text)
def c4(m):
    c=get_crypto(); p=c.get('tether',{}).get('usd',0)
    bot.send_message(m.chat.id, f"💵 USDT = ${p}{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "BNB чанд" in m.text)
def c5(m):
    c=get_crypto(); p=c.get('binancecoin',{}).get('usd',0)
    bot.send_message(m.chat.id, f"🟡 BNB = ${p}{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Solana чанд" in m.text)
def c6(m):
    c=get_crypto(); p=c.get('solana',{}).get('usd',0)
    bot.send_message(m.chat.id, f"☀️ Solana = ${p}{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Tron чанд" in m.text)
def c7(m):
    c=get_crypto(); p=c.get('tron',{}).get('usd',0)
    bot.send_message(m.chat.id, f"🔴 Tron = ${p}{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Doge чанд" in m.text)
def c8(m):
    c=get_crypto(); p=c.get('dogecoin',{}).get('usd',0)
    bot.send_message(m.chat.id, f"🐶 Doge = ${p}{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "Cardano чанд" in m.text)
def c9(m):
    c=get_crypto(); p=c.get('cardano',{}).get('usd',0)
    bot.send_message(m.chat.id, f"🔵 Cardano = ${p}{FOOTER}")
@bot.message_handler(func=lambda m: m.text and "XRP чанд" in m.text)
def c10(m):
    c=get_crypto(); p=c.get('ripple',{}).get('usd',0)
    bot.send_message(m.chat.id, f"✖️ XRP = ${p}{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Хамаи пулхо" in m.text)
def all1(m):
    bot.send_message(m.chat.id, f"🌍 10 пул:\n🇺🇸 Доллар=9.2261\n🇪🇺 Евро=10.36\n🇷🇺 Рубл=0.1131\n🇰🇬 Сом=0.105\n🇰🇿 Тенге=0.018\n🇺🇿 Сӯм=0.00072\n🇨🇳 Юан=1.29\n🇹🇷 Лира=0.27\n🇦🇪 Дирҳам=2.51\n🇬🇧 Фунт=12.02{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Хамаи криптохо" in m.text)
def all2(m):
    c=get_crypto()
    bot.send_message(m.chat.id, f"🚀 10 крипто:\n₿ BTC=${c.get('bitcoin',{}).get('usd',0)}\n🌐 ETH=${c.get('ethereum',{}).get('usd',0)}\n💎 TON=${c.get('the-open-network',{}).get('usd',0)}\n💵 USDT=${c.get('tether',{}).get('usd',0)}\n🟡 BNB=${c.get('binancecoin',{}).get('usd',0)}\n☀️ SOL=${c.get('solana',{}).get('usd',0)}\n🔴 TRON=${c.get('tron',{}).get('usd',0)}\n🐶 DOGE=${c.get('dogecoin',{}).get('usd',0)}\n🔵 ADA=${c.get('cardano',{}).get('usd',0)}\n✖️ XRP=${c.get('ripple',{}).get('usd',0)}{FOOTER}")

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f"Салом! 10 пул + 10 крипто!\nКоди имрӯз: {get_code()}{FOOTER}")

@bot.message_handler(func=lambda m: True)
def last(m):
    if "чанд" in m.text.lower() or "пулхо" in m.text.lower() or "криптохо" in m.text.lower(): return
    if "/start" in m.text: return
    real=get_code()
    if m.text.strip().upper()==real:
        bot.send_message(m.chat.id, f"✅ Дуруст! {real}{FOOTER}")
    else:
        bot.send_message(m.chat.id, f"❌ Коди кӯҳна! Нав: {real}\n{BLOG_URL}{FOOTER}")

print("Bot started...")
bot.infinity_polling()
