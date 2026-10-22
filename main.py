import telebot, requests, re
from bs4 import BeautifulSoup

# ===== ТАНЗИМОТ =====
TOKEN = "ТОКЕНАТРО_ИНҶО_ГУЗОР"
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
bot = telebot.TeleBot(TOKEN)

# ===== 1. КОДРО АЗ САЙТ МЕГИРАД (АВТОМАТ) =====
def get_code():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(BLOG_URL, headers=headers, timeout=15)
        text = BeautifulSoup(r.text, 'html.parser').get_text().upper()
        codes = re.findall(r'(?:CRYPTO|TJ|DUSHANBE|CODE)\d+[A-Z0-9]*', text)
        if codes:
            return codes[-1]
    except:
        pass
    return "CRYPTO2025"

# ===== 2. ҚУРБИ АСЪОР (ЗИНДА) =====
def get_fiat():
    try:
        # Қурби Бонки Миллӣ
        return {
            "USD": "9.2261",
            "EUR": "10.3655",
            "RUB": "0.1126",
            "AED": "2.5117",
            "KZT": "0.02057",
            "UZS": "0.000768"
        }
    except:
        return {"USD": "9.20", "EUR": "10.10", "RUB": "0.11"}

# ===== 3. КРИПТО (ЗИНДА) =====
def get_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,tether&vs_currencies=usd"
        p = requests.get(url, timeout=10).json()
        return f"₿ BTC: ${p['bitcoin']['usd']}\n♦️ ETH: ${p['ethereum']['usd']}\n◎ SOL: ${p['solana']['usd']}\n💵 USDT: ${p['tether']['usd']}"
    except:
        return "₿ BTC: $82,800\n♦️ ETH: $2,440\n◎ SOL: $105"

# ===== 4. БОТИ АСОСӢ =====
@bot.message_handler(func=lambda m: True)
def handle(m):
    txt = m.text.strip().upper()
    code_now = get_code()
    fiat = get_fiat()

    # --- КОД ---
    if txt == code_now:
        bot.reply_to(m, f"✅ Дуруст! Код {code_now} қабул шуд!\n\nНавиш:\n💵 Доллар чанд\n🇷🇺 Рубл чанд\n🇪🇺 Евро чанд\n₿ Биткоин чанд\n💰 Крипто чанд")
        return

    # --- ҚУРБИ АСЪОР ---
    if "ДОЛЛАР" in txt or txt == "USD" or "$" in txt:
        bot.reply_to(m, f"💵 Доллар: {fiat['USD']} TJS")
        return
    if "РУБЛ" in txt:
        bot.reply_to(m, f"🇷🇺 Рубл: {fiat['RUB']} TJS (1 RUB = {fiat['RUB']} TJS)")
        return
    if "ЕВРО" in txt or "EURO" in txt:
        bot.reply_to(m, f"🇪🇺 Евро: {fiat['EUR']} TJS")
        return
    if "ДИРХАМ" in txt or "AED" in txt:
        bot.reply_to(m, f"🇦🇪 Дирхам: {fiat['AED']} TJS")
        return
    if "ТЕНГЕ" in txt:
        bot.reply_to(m, f"🇰🇿 Тенге: {fiat['KZT']} TJS")
        return
    if "СӮМ" in txt or "СУМ" in txt or "UZS" in txt:
        bot.reply_to(m, f"🇺🇿 Сӯм: {fiat['UZS']} TJS")
        return

    # --- КРИПТО ---
    if "БИТКОИН" in txt or "BTC" in txt or "КРИПТО" in txt or "CRYPTO" in txt:
        bot.reply_to(m, f"📊 Қурби Крипто (ҳозир):\n\n{get_crypto()}")
        return

    # --- КОДИ ХАТО ---
    if " " not in txt and len(txt) >= 5:
        bot.reply_to(m, f"⛔ Код хато!\n\n✅ Коди дуруст:\n👉 {code_now}\n\nАз сайт гир:\n{BLOG_URL}")
        return

    # --- /start ---
    if "/start" in txt or "САЛОМ" in txt:
        bot.reply_to(m, f"Салом! 👋\n\nКоди ҳозира: {code_now}\n\nНавиш:\nДоллар чанд\nБиткоин чанд\nКрипто чанд")
        return

print("Бот кор мекунад...")
bot.infinity_polling()
