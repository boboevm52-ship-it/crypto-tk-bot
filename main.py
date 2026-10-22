
import telebot, requests, re
from bs4 import BeautifulSoup

TOKEN = "ТОКЕНАТРО_ИНҶО_ГУЗОР"
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
bot = telebot.TeleBot(TOKEN)

# ҚУЛФ
unlocked = set()

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
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,the-open-network,tether&vs_currencies=usd"
        d = requests.get(url, timeout=10).json()
        btc = d.get('bitcoin',{}).get('usd', 81561)
        eth = d.get('ethereum',{}).get('usd', 2441)
        ton = d.get('the-open-network',{}).get('usd', 1.60)
        return btc, eth, ton
    except:
        return 81561, 2441, 1.60

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f"Салом! 👇\n\n🔒 Кодро ворид кун!\nСайт: {BLOG_URL}\n\nКод: {get_code()}")

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    cid = m.chat.id
    txt = m.text.strip()
    up = txt.upper()
    code = get_code()

    # 1. КОД
    if up == code:
        unlocked.add(cid)
        bot.reply_to(m, f"✅ Дуруст! {code}\n\nҲоло:\n💵 Доллар чанд\n💎 Тон чанд\n₿ Биткоин чанд\n🇷🇺 Рубл чанд")
        return

    # 2. ҚУЛФ
    if cid not in unlocked:
        bot.reply_to(m, f"🔒 Аввал код!\n👉 {BLOG_URL}\nКод: {code}")
        return

    # 3. ҚУРБҲО
    btc, eth, ton = get_crypto()
    
    if "ДОЛЛАР" in up:
        bot.reply_to(m, "💵 1 Доллар = 9.2261 сомонӣ")
    elif "ЕВРО" in up:
        bot.reply_to(m, "🇪🇺 1 Евро = 10.3655 сомонӣ")
    elif "РУБЛ" in up:
        bot.reply_to(m, "🇷🇺 1 Рубл = 0.1126 сомонӣ")
    elif "ДИРХАМ" in up:
        bot.reply_to(m, "🇦🇪 1 Дирхам = 2.5117 сомонӣ")
    elif "ТЕНГЕ" in up:
        bot.reply_to(m, "🇰🇿 1 Тенге = 0.02057 сомонӣ")
    elif "ТОН" in up or up == "TON":
        som = ton * 9.2261
        bot.reply_to(m, f"💎 Тон = ${ton} = {som:.2f} сомонӣ")
    elif "БИТКОИН" in up or "BTC" in up:
        som = btc * 9.2261
        bot.reply_to(m, f"₿ Биткоин = ${btc} = {som:.0f} сомонӣ")
    elif "ЭФИР" in up or "ETH" in up:
        bot.reply_to(m, f"♦️ Эфир = ${eth}")
    else:
        bot.reply_to(m, "Навиш: Доллар чанд, Тон чанд, Биткоин чанд, Рубл чанд")

print("Бот кор мекунад...")
bot.infinity_polling()
