import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = "ТОКЕНИ_ХУДАТРО_ИНҶО"
bot = telebot.TeleBot(TOKEN)

def гирифтани_коди_нав():
    try:
        url = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        text = soup.get_text()
        # Кодро аз текст меёбад - масалан CRYPTO2025
        import re
        codes = re.findall(r'CRYPTO\d+|DUSHANBE\d+', text)
        if codes:
            return codes[-1]  # охирин код
        return None
    except:
        return None

RATES = {
    "доллар": "🇺🇸 1 USD = 9.20 TJS",
    "евро": "🇪🇺 1 EUR = 10.34 TJS",
    "рубл": "🇷🇺 100 RUB = 11.22 TJS",
    "тенге": "🇰🇿 1000 KZT = 20.51 TJS",
    "сом": "🇰🇬 1 KGS = 0.105 TJS",
    "сум": "🇺🇿 10000 UZS = 7.15 TJS",
    "лира": "🇹🇷 1 TRY = 0.19 TJS",
    "юан": "🇨🇳 1 CNY = 1.28 TJS",
    "фунт": "🇬🇧 1 GBP = 12.10 TJS",
    "дирхам": "🇦🇪 1 AED = 2.50 TJS",
    "биткоин": "₿ 1 BTC = 625,600 TJS",
    "эфир": "💎 1 ETH = 32,200 TJS",
    "тезер": "💵 1 USDT = 9.20 TJS",
    "сол": "◎ 1 SOL = 1,420 TJS",
    "тон": "💎 1 TON = 45 TJS",
    "доге": "🐶 1 DOGE = 1.15 TJS",
    "шиба": "🐕 1M SHIB = 210 TJS",
    "пепе": "🐸 1M PEPE = 85 TJS",
    "бнб": "🔶 1 BNB = 5,500 TJS",
    "трон": "🔴 1 TRX = 1.05 TJS",
}

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Салом! 👋\nНавиш: Рубл чанд? Биткоин чанд?\n\nКоди нав: /code")

@bot.message_handler(commands=['code'])
def code_cmd(m):
    коди_нав = гирифтани_коди_нав()
    if коди_нав:
        bot.reply_to(m, f"✅ Коди НАВ аз сайт:\n\n`{коди_нав}`\n\nСайт: cryptotj-dushanbe.blogspot.com", parse_mode="Markdown")
    else:
        bot.reply_to(m, "⛔ Коди кӯҳна не! Коди НАВ:\nCRYPTO2025\n\nАз сайт ё: https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html")

@bot.message_handler(func=lambda m: True)
def handle(m):
    t = m.text.lower()
    # Аввал код санҷ
    if "crypto" in t or "dushanbe" in t:
        код = гирифтани_коди_нав()
        if t.strip().upper() == (код.upper() if код else "CRYPTO2025"):
            bot.reply_to(m, f"✅ Код дуруст! Коди нав: {код}")
        else:
            bot.reply_to(m, f"⛔ Коди кӯҳна не! Коди НАВ: {код or 'CRYPTO2025'}")
        return
    
    for k,v in RATES.items():
        if k in t:
            bot.reply_to(m, v)
            return

print("Бот автомат кор мекунад...")
bot.infinity_polling()
