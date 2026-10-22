import telebot, requests, re
from bs4 import BeautifulSoup

bot = telebot.TeleBot("ТОКЕНАТ")

def коди_аз_сайт():
    try:
        url = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
        html = requests.get(url, timeout=10).text
        text = BeautifulSoup(html, 'html.parser').get_text()
        # Ҳамаи кодҳои дар сайт бударо меёбад
        codes = re.findall(r'[A-Z0-9]{5,15}', text)
        # Охирин кодро мегирад
        for c in reversed(codes):
            if "CRYPTO" in c or "DUSHANBE" in c or "TJ" in c:
                return c
        return "CRYPTO2025"
    except:
        return "CRYPTO2025"

@bot.message_handler(func=lambda m: True)
def auto(m):
    text = m.text.strip().upper()
    коди_дуруст = коди_аз_сайт().upper()
    
    if text == коди_дуруст:
        bot.reply_to(m, f"✅ Дуруст! Коди нав фаъол: {коди_дуруст}\n\nНавиш: Доллар, Биткоин")
    else:
        # Агар код нодуруст бошад
        if len(text) > 4:
            bot.reply_to(m, f"⛔ Коди кӯҳна!\n\n✅ Коди НАВ ва ДУРУСТ:\n{коди_дуруст}\n\nАз сайт: cryptotj-dushanbe.blogspot.com")
            return
        
        # Қурби асъор
        rates = {"ДОЛЛАР":"9.20","РУБЛ":"11.22","БИТКОИН":"625600"}
        for k,v in rates.items():
            if k in text:
                bot.reply_to(m, f"{k}: {v} TJS")
                return

bot.infinity_polling()
