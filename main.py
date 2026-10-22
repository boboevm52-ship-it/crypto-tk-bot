import telebot, requests, re, time, os
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"

bot = telebot.TeleBot(TOKEN)
passed_users = set()
last_code = ""

# 50 ДАВЛАТ
COUNTRIES = ["USD","EUR","RUB","KZT","UZS","CNY","TRY","GBP","AED","SAR","INR","PKR","AZN","AMD","GEL","KGS","BYN","UAH","JPY","KRW","AUD","CAD","CHF","SEK","NOK","DKK","PLN","CZK","HUF","RON","BGN","RSD","MKD","THB","MYR","SGD","HKD","NZD","BRL","MXN","EGP","QAR","KWD","BHD","OMR","JOD","LBP","IQD","AFN"]

def get_secret():
    global last_code
    try:
        url = f"{BLOG_URL}?t={int(time.time())}"
        r = requests.get(url, timeout=15, headers={'User-Agent':'Mozilla/5.0','Cache-Control':'no-cache'})
        m = re.findall(r'Коди имрӯз:\s*([A-Z0-9]+)', r.text, re.I)
        if m:
            new_code = m[-1].upper().strip()
            if new_code != last_code and last_code != "":
                print(f"КОД ИВАЗ: {last_code} -> {new_code} - ҲАМА Тоза шуд!")
                passed_users.clear()
            last_code = new_code
            return new_code
    except Exception as e:
        print(f"Хатогӣ: {e}")
    return last_code or "DUSHANBE8888"

def get_data():
    try:
        rates = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()['rates']
    except:
        rates = {"RUB":95,"EUR":0.92,"KZT":490,"TRY":34,"GBP":0.79}
    try:
        ids = "bitcoin,ethereum,tether,solana,tron,binancecoin,dogecoin,cardano,ripple,toncoin"
        cg = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd", timeout=15).json()
    except:
        cg = {"bitcoin":{"usd":81364},"ethereum":{"usd":2400},"tether":{"usd":1},"solana":{"usd":105},"tron":{"usd":0.24},"binancecoin":{"usd":600},"dogecoin":{"usd":0.12},"cardano":{"usd":0.45},"ripple":{"usd":0.55},"toncoin":{"usd":5.5}}
    return rates, cg

@bot.message_handler(func=lambda m: True)
def all_handler(message):
    txt = message.text.strip()
    up = txt.upper()
    low = txt.lower()
    real = get_secret()
    uid = message.from_user.id

    # 1. КОДИ НАВ
    if up == real:
        passed_users.add(uid)
        bot.reply_to(message, f"✅ Гузаштӣ бро! Код: {real}\n\nБарои дидани курс навиш:\nкурс / пул / чанд пул / 50")
        return

    # 2. КОДИ КӮҲНА
    if "DUSHANBE" in up and up != real:
        bot.reply_to(message, f"⛔️ Ин код кӯҳна шуд бро!\n\nКоди нав: {real}\nСайт: cryptotj-dushanbe.blogspot.com")
        return

    # 3. КОД НАЗАДААСТ
    if uid not in passed_users:
        bot.reply_to(message, f"⛔️ Аввал код зан бро:\n{real}\nСайт: cryptotj-dushanbe.blogspot.com")
        return

    # 4. ТОҶИКИРО МЕФАҲМАД - КУРС
    tajik_keys = ["курс","пул","нарх","чанд","50","ҳама","биткоин","доллар","евро","рубл","btc","курси"]
    if any(k in low for k in tajik_keys):
        rates, cg = get_data()
        now = datetime.now().strftime("%d.%m.%Y %H:%M")

        text = f"💰 КУРСИ ЗИНДА {now}\nКод: {real}\n\n"
        text += f"--- 💵 50 ДАВЛАТ ---\n"
        text += f"🇺🇸 USD = 9.20 TJS\n"
        if "EUR" in rates: text += f"🇪🇺 EUR = {9.20/rates['EUR']:.2f} TJS\n"
        if "RUB" in rates: text += f"🇷🇺 100 RUB = {9.20/rates['RUB']*100:.2f} TJS\n"
        if "KZT" in rates: text += f"🇰🇿 1000 KZT = {9.20/rates['KZT']*1000:.2f} TJS\n"
        if "TRY" in rates: text += f"🇹🇷 TRY = {9.20/rates['TRY']:.2f} TJS\n"
        if "GBP" in rates: text += f"🇬🇧 GBP = {9.20/rates['GBP']:.2f} TJS\n"
        if "CNY" in rates: text += f"🇨🇳 CNY = {9.20/rates['CNY']:.2f} TJS\n"
        text += f"\n... ва боз 43 давлати дигар\n"
        
        text += f"\n--- ₿ 10 КРИПТО ---\n"
        text += f"₿ BTC = ${cg.get('bitcoin',{}).get('usd',0):,.2f}\n"
        text += f"♦️ ETH = ${cg.get('ethereum',{}).get('usd',0):,.2f}\n"
        text += f"💵 USDT = ${cg.get('tether',{}).get('usd',0)}\n"
        text += f"☀️ SOL = ${cg.get('solana',{}).get('usd',0):,.2f}\n"
        text += f"🔺 TRX = ${cg.get('tron',{}).get('usd',0):.4f}\n"
        text += f"🟡 BNB = ${cg.get('binancecoin',{}).get('usd',0):,.2f}\n"
        text += f"🐶 DOGE = ${cg.get('dogecoin',{}).get('usd',0):.4f}\n"
        text += f"🔵 ADA = ${cg.get('cardano',{}).get('usd',0):.4f}\n"
        text += f"💧 XRP = ${cg.get('ripple',{}).get('usd',0):.4f}\n"
        text += f"💎 TON = ${cg.get('toncoin',{}).get('usd',0):.2f}\n"
        text += f"\nБо забони тоҷикӣ навиш, мефаҳмам!"

        bot.reply_to(message, text)
        return

    bot.reply_to(message, f"Навиш: курс бро!")

print("Бот тайёр: 50 давлат + 10 крипто + код автоматӣ + тоҷикӣ!")
get_secret()
bot.infinity_polling()
