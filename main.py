import telebot, requests, re, time
from bs4 import BeautifulSoup

TOKEN = "ТОКЕНАТРО_ИНҶО_ГУЗОР"
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
bot = telebot.TeleBot(TOKEN)

# cid : вақти то кай кушода аст
unlocked = {}

def get_code():
    try:
        r = requests.get(BLOG_URL, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        t = BeautifulSoup(r.text, 'html.parser').get_text().upper()
        c = re.findall(r'(?:CRYPTO|TJ|DUSHANBE|CODE)\d+[A-Z0-9]*', t)
        if c: return c[-1]
    except: pass
    return "TJ2026"

def get_crypto():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbols=%5B%22BTCUSDT%22,%22ETHUSDT%22,%22TONUSDT%22%5D"
        data = requests.get(url, timeout=8).json()
        btc = eth = ton = 0
        for item in data:
            if item['symbol'] == 'BTCUSDT': btc = float(item['price'])
            if item['symbol'] == 'ETHUSDT': eth = float(item['price'])
            if item['symbol'] == 'TONUSDT': ton = float(item['price'])
        if btc > 0: return btc, eth, ton
    except: pass
    return 81561.0, 2441.0, 1.60

@bot.message_handler(commands=['start', 'stsrt'])
def start(m):
    code = get_code()
    bot.send_message(m.chat.id, f"Салом! 👇\n\n🔒 Кодро ворид кун (1 соат эътибор дорад)!\nСайт: {BLOG_URL}\nКод: {code}")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    cid = m.chat.id
    up = m.text.upper()
    code = get_code()
    now = time.time()

    # 1. КОДРО ЗАД?
    if up == code or code in up:
        unlocked[cid] = now + 3600  # 3600 сония = 1 соат
        bot.reply_to(m, f"✅ Дуруст! {code}\n\n⏰ 1 соат кушода шуд!\nТо {time.strftime('%H:%M', time.localtime(now+3600))} метавонӣ пурсӣ:\n💵 Доллар чанд\n💎 Тон чанд\n₿ Биткоин чанд")
        return

    # 2. САНҶИШИ 1 СОАТ
    if cid not in unlocked or now > unlocked[cid]:
        if cid in unlocked: del unlocked[cid]
        left = "тамом шуд" if cid in unlocked else "вохӯрда нашуд"
        bot.reply_to(m, f"🔒 Вақти 1 соата {left}!\n\nКодро аз нав ворид кун!\n👉 {BLOG_URL}\nКод: {code}")
        return

    # 3. ВАҚТ МОНДААСТ - ҚУРБРО ДЕҲ
    left_min = int((unlocked[cid] - now) / 60)
    btc, eth, ton = get_crypto()

    if "ДОЛЛАР" in up:
        bot.reply_to(m, f"💵 1 Доллар = 9.2261 сомонӣ\n⏰ {left_min} дақ. монд")
    elif "РУБЛ" in up:
        bot.reply_to(m, f"🇷🇺 1 Рубл = 0.1124 сомонӣ\n⏰ {left_min} дақ. монд")
    elif "ЕВРО" in up:
        bot.reply_to(m, f"🇪🇺 1 Евро = 10.3655 сомонӣ")
    elif "ТОН" in up:
        bot.reply_to(m, f"💎 Тон = ${ton:.2f} = {ton*9.2261:.2f} сомонӣ\n⏰ {left_min} дақ. монд")
    elif "БИТКОИН" in up or "BTC" in up:
        bot.reply_to(m, f"₿ Биткоин = ${btc:.2f}\n⏰ {left_min} дақ. монд")
    elif "ЭФИР" in up or "ETH" in up:
        bot.reply_to(m, f"♦️ Эфир = ${eth:.2f}")
    elif "ХАМАИ" in up and "КРИПТО" in up:
        bot.reply_to(m, f"🚀 Крипто:\n₿ BTC = ${btc:.2f}\n♦️ ETH = ${eth:.2f}\n💎 TON = ${ton:.2f}\n\n⏰ {left_min} дақ. монд")
    elif "ХАМАИ" in up and "ПУЛ" in up:
        bot.reply_to(m, f"🌍 Хамаи пулхо:\n💵 Доллар: 9.2261\n🇷🇺 Рубл: 0.1124\n🇪🇺 Евро: 10.3655")
    else:
        bot.reply_to(m, f"Навиш: Доллар чанд, Тон чанд\n⏰ {left_min} дақ. монд то қулф")

bot.infinity_polling()
