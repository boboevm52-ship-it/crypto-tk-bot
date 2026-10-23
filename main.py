import telebot, requests, re, os
from telebot import types
from bs4 import BeautifulSoup

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TOKEN")
print(f"TOKEN: {TOKEN[:12] if TOKEN else 'NO TOKEN'}")
bot = telebot.TeleBot(TOKEN)

BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"

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

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(types.KeyboardButton("💰 Доллар чанд"), types.KeyboardButton("🇷🇺 Рубл чанд"))
    kb.add(types.KeyboardButton("₿ Биткоин чанд"), types.KeyboardButton("💎 Тон чанд"), types.KeyboardButton("🌐 Эфир чанд"))
    kb.add(types.KeyboardButton("🌍 Хамаи пулхо"), types.KeyboardButton("🚀 Хамаи криптохо"))
    kb.add(types.KeyboardButton("🇦🇪 Дирхам чанд"), types.KeyboardButton("🇰🇿 Тенге чанд"), types.KeyboardButton("🇺🇿 Сум чанд"))
    return kb

FOOTER = "\n\n━━━━━━━━━━━━━━\n🔥 Коди нав: https://cryptotj-dushanbe.blogspot.com/\n📢 @CryptoTj_Dushanbe"

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f"Салом! Коди имрӯз: {get_code()}{FOOTER}", reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def all_handler(m):
    if not m.text: return
    txt = m.text.lower()
    c = get_crypto()
    
    if "доллар" in txt:
        bot.send_message(m.chat.id, f"💵 Доллар = 9.2261 сомонӣ{FOOTER}", reply_markup=main_menu())
    elif "рубл" in txt:
        bot.send_message(m.chat.id, f"🇷🇺 Рубл = 0.1131 сомонӣ{FOOTER}", reply_markup=main_menu())
    elif "дирхам" in txt:
        bot.send_message(m.chat.id, f"🇦🇪 Дирҳам = 2.51 сомонӣ{FOOTER}", reply_markup=main_menu())
    elif "тенге" in txt:
        bot.send_message(m.chat.id, f"🇰🇿 Тенге = 0.018 сомонӣ{FOOTER}", reply_markup=main_menu())
    elif "сум" in txt or "сӯм" in txt:
        bot.send_message(m.chat.id, f"🇺🇿 Сӯм = 0.00072 сомонӣ{FOOTER}", reply_markup=main_menu())
    elif "биткоин" in txt or "btc" in txt:
        bot.send_message(m.chat.id, f"₿ Биткоин = ${c.get('bitcoin',{}).get('usd','--')}{FOOTER}", reply_markup=main_menu())
    elif "тон" in txt or "ton" in txt:
        bot.send_message(m.chat.id, f"💎 Тон = ${c.get('the-open-network',{}).get('usd','--')}{FOOTER}", reply_markup=main_menu())
    elif "эфир" in txt or "eth" in txt:
        bot.send_message(m.chat.id, f"🌐 Эфир = ${c.get('ethereum',{}).get('usd','--')}{FOOTER}", reply_markup=main_menu())
    elif "хамаи пулхо" in txt:
        bot.send_message(m.chat.id, f"🌍 10 пул: Доллар=9.22, Евро=10.36, Рубл=0.113, Сом=0.105, Тенге=0.018, Сӯм=0.00072, Юан=1.29, Лира=0.27, Дирҳам=2.51, Фунт=12.02{FOOTER}", reply_markup=main_menu())
    elif "хамаи криптохо" in txt:
        bot.send_message(m.chat.id, f"🚀 10 крипто: BTC=${c.get('bitcoin',{}).get('usd',0)} ETH=${c.get('ethereum',{}).get('usd',0)} TON=${c.get('the-open-network',{}).get('usd',0)} USDT=${c.get('tether',{}).get('usd',0)}{FOOTER}", reply_markup=main_menu())
    else:
        real = get_code()
        if m.text.strip().upper() == real:
            bot.send_message(m.chat.id, f"✅ Дуруст! {real}{FOOTER}", reply_markup=main_menu())
        else:
            # агар код набошад, чизе нагӯй ё коди навро нишон де
            if len(m.text) > 15: # паёми дароз - нодида гир
                return
            bot.send_message(m.chat.id, f"❌ Коди куҳна! Нав: {real}\n{BLOG_URL}{FOOTER}", reply_markup=main_menu())

print("Bot started polling...")
bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
