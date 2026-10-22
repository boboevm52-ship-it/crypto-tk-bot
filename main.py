import telebot, requests, re
from bs4 import BeautifulSoup

TOKEN = "ТОКЕНАТРО_ИНҶО_ГУЗОР"
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
bot = telebot.TeleBot(TOKEN)

# Кӣ кодро дохил кард, дар хотир мемонад
authorized = set()

def get_code():
    try:
        r = requests.get(BLOG_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        text = BeautifulSoup(r.text, 'html.parser').get_text().upper()
        codes = re.findall(r'(?:CRYPTO|TJ|DUSHANBE|CODE)\d+[A-Z0-9]*', text)
        if codes: return codes[-1]
    except: pass
    return "CRYPTO2025"

def get_crypto_live():
    try:
        p = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd", timeout=10).json()
        return f"₿ BTC: ${p['bitcoin']['usd']}\n♦️ ETH: ${p['ethereum']['usd']}\n◎ SOL: ${p['solana']['usd']}"
    except:
        return "₿ BTC: $82,817\n♦️ ETH: $2,441\n◎ SOL: $105"

@bot.message_handler(func=lambda m: True)
def handle(m):
    chat_id = m.chat.id
    txt = m.text.strip().upper()
    code_now = get_code()

    # 1. Агар кодро дуруст нависад - иҷозат медиҳем
    if txt == code_now:
        authorized.add(chat_id)
        bot.reply_to(m, f"✅ Коди {code_now} дуруст!\n\nҲоло метавонӣ пурсӣ:\n💵 Доллар чанд\n🇷🇺 Рубл чанд\n₿ Биткоин чанд")
        return

    # 2. Агар иҷозат надошта бошад - ҚУЛФ!
    if chat_id not in authorized:
        bot.reply_to(m, f"🔒 Аввал кодро ворид кун!\n\n👉 Коди имрӯза: {BLOG_URL}\n\nКодро инҷо навиш!")
        return

    # 3. Агар иҷозат дошта бошад - қурбро медиҳем
    if "ДОЛЛАР" in txt or "DOLLAR" in txt:
        bot.reply_to(m, "💵 Доллар: 9.2261 TJS")
        return
    if "РУБЛ" in txt:
        bot.reply_to(m, "🇷🇺 Рубл: 0.1126 TJS")
        return
    if "ЕВРО" in txt:
        bot.reply_to(m, "🇪🇺 Евро: 10.3655 TJS")
        return
    if "ТЕНГЕ" in txt:
        bot.reply_to(m, "🇰🇿 Тенге: 0.02057 TJS")
        return
    if "ДИРХАМ" in txt:
        bot.reply_to(m, "🇦🇪 Дирхам: 2.5117 TJS")
        return
    if "БИТКОИН" in txt or "BTC" in txt or "КРИПТО" in txt:
        bot.reply_to(m, f"{get_crypto_live()}")
        return

    bot.reply_to(m, f"Навиш: Доллар чанд, Рубл чанд, Биткоин чанд\n\nКоди нав: {code_now}")

bot.infinity_polling()
