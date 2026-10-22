import os, re, time, threading, requests
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

CHANNEL = "@cryptotj_tj"
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2026/10/blog-post_22.html"
SECRET_CODE = "CRYPTO2025"

# Базаи одамоне ки кодро ёфтанд
user_passed = {}

fiat_rates = {"USD": 9.22, "TJS": 1.0, "RUB": 0.11, "EUR": 10.5}

def get_fiat():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5).json()
        return r.get("rates", {})
    except:
        return {}

def get_crypto_price(symbol):
    try:
        # CoinGecko
        ids = {"BTC":"bitcoin","ETH":"ethereum","BNB":"binancecoin","SOL":"solana","XRP":"ripple","DOGE":"dogecoin","TON":"the-open-network","USDT":"tether","TRX":"tron","ADA":"cardano","SHIB":"shiba-inu","AVAX":"avalanche-2","DOT":"polkadot","LINK":"chainlink","MATIC":"matic-network","LTC":"litecoin","UNI":"uniswap"}
        coin_id = ids.get(symbol.upper(), symbol.lower())
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd", timeout=5).json()
        return r[coin_id]["usd"]
    except:
        return None

def check_sub(user_id):
    try:
        m = bot.get_chat_member(CHANNEL, user_id)
        return m.status in ['member','administrator','creator']
    except:
        return False

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💵 Сом чанд?", callback_data="fiat_USD"),
        InlineKeyboardButton("💶 Евро чанд?", callback_data="fiat_EUR"),
        InlineKeyboardButton("💷 Рубл чанд?", callback_data="fiat_RUB"),
        InlineKeyboardButton("₿ Биткоин чанд?", callback_data="crypto_BTC"),
        InlineKeyboardButton("Ξ Эфириум чанд?", callback_data="crypto_ETH"),
        InlineKeyboardButton("💎 Тон чанд?", callback_data="crypto_TON"),
        InlineKeyboardButton("🌐 Ҳамаи криптоҳо", callback_data="all_crypto"),
        InlineKeyboardButton("🌍 Ҳамаи пулҳо", callback_data="all_fiat")
    )
    return markup

@app.route('/')
def home():
    return "CryptoTJ Full - Tajik Bot Ishlayapti!"

@bot.callback_query_handler(func=lambda c: True)
def callbacks(call):
    if call.data == "check_sub":
        if not check_sub(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔️ Ту ҳанӯз обуна нашудаӣ!")
            return
        # обуна шуд - акнун ба блог фирист
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔐 Ба сайти мо даро", url=BLOG_URL))
        bot.send_message(call.message.chat.id, f"✅ Зӯр! Обуна шудӣ!\n\n🔐 Қадами 2:\nБа сайти мо даро ва КОДРО ёб:\n👉 {BLOG_URL}\n\nКоди имрӯз дар саҳифа навишта шудааст.\nКоди ёфтаатонро ин ҷо нависед:", reply_markup=markup)
    
    elif call.data.startswith("fiat_") or call.data.startswith("crypto_") or call.data.startswith("all_"):
        if user_passed.get(call.from_user.id) != True:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🔐 Кодро аз сайт ёб", url=BLOG_URL))
            bot.send_message(call.message.chat.id, f"⛔️ Барои дидани нарх, аввал ба сайти мо даро:\n{BLOG_URL}\nва кодро ин ҷо навиш!", reply_markup=markup)
            return
        
        if call.data.startswith("fiat_"):
            cur = call.data.split("_")[1]
            rates = get_fiat()
            usd_tjs = fiat_rates["USD"]
            if cur in rates:
                # USD ба TJS
                price_tjs = (1 / rates.get("TJS", 0.108)) * rates.get(cur, 1) if cur != "USD" else usd_tjs
                # содда
                bot.send_message(call.message.chat.id, f"💵 1 {cur} = {usd_tjs * rates.get(cur, 1):.2f} TJS\n\nБо CryptoTJ")
            else:
                bot.send_message(call.message.chat.id, f"💵 1 {cur} = {fiat_rates.get(cur, 'Дарёфт нашуд')} TJS")
        elif call.data == "all_fiat":
            txt = "🌍 Ҳамаи пулҳои ҷаҳон ба сомонӣ:\n\n"
            rates = get_fiat()
            for k in ["USD","EUR","RUB","CNY","KGS","KZT","UZS","TRY","GBP","AED"]:
                txt += f"• 1 {k} = ... TJS\n"
            txt += "\nНавиш: масалан 'доллар чанд' ё 'евро чанд'"
            bot.send_message(call.message.chat.id, txt)
        elif call.data == "all_crypto":
            txt = "₿ Ҳамаи криптоҳо:\n\nBTC, ETH, BNB, SOL, XRP, DOGE, TON, USDT, TRX, ADA, SHIB, AVAX, DOT, LINK, MATIC, LTC, UNI ва 1000-тои дигар\n\nНавиш: 'биткоин чанд'"
            bot.send_message(call.message.chat.id, txt)
        else:
            sym = call.data.split("_")[1]
            price = get_crypto_price(sym)
            if price:
                tjs = price * fiat_rates["USD"]
                bot.send_message(call.message.chat.id, f"₿ 1 {sym} = ${price} = {tjs:.2f} TJS")

@bot.message_handler(commands=['start'])
def start(m):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 Обуна ба канал", url=f"https://t.me/{CHANNEL[1:]}"))
    markup.add(InlineKeyboardButton("✅ Ман обуна шудам", callback_data="check_sub"))
    bot.send_message(m.chat.id, f"Салом {m.from_user.first_name}! 👋\n\nМан боти 100% тоҷикӣ ҳастам!\n\n💰 Ҳамаи пулҳои ҷаҳонро медонам\n₿ Ҳамаи криптоҳоро медонам\n\nБарои истифода аввал обуна шав:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def all_messages(m):
    text = m.text.lower().strip()
    
    # 1. Санҷиши код
    if text.upper() == SECRET_CODE:
        user_passed[m.from_user.id] = True
        bot.send_message(m.chat.id, "✅ ОФАРИН! Коди дуруст!\n\nАкнун пурра дастрасӣ дорӣ! 👇", reply_markup=main_menu())
        return

    # 2. Санҷиши обуна
    if not check_sub(m.from_user.id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Обуна ба канал", url=f"https://t.me/{CHANNEL[1:]}"))
        markup.add(InlineKeyboardButton("✅ Ман обуна шудам", callback_data="check_sub"))
        bot.send_message(m.chat.id, "⛔️ Аввал обуна шав, баъд нарх медиҳам:", reply_markup=markup)
        return

    # 3. Санҷиши блог
    if user_passed.get(m.from_user.id) != True:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔐 Ба сайт даро ва код ёб", url=BLOG_URL))
        bot.send_message(m.chat.id, f"🔐 Барои дидани нарх, ба сайти мо даро:\n👉 {BLOG_URL}\n\nКод дар саҳифа аст. Кодро ин ҷо навиш:", reply_markup=markup)
        return

    # 4. Агар ҳама корро карда бошад - ҷавоб деҳ
    if "сом чанд" in text or "доллар" in text or "usd" in text:
        bot.send_message(m.chat.id, f"💵 1 USD = {fiat_rates['USD']} TJS\n💶 1 EUR = 10.5 TJS\n💷 1 RUB = 0.11 TJS", reply_markup=main_menu())
    elif "биткоин" in text or "btc" in text:
        p = get_crypto_price("BTC")
        bot.send_message(m.chat.id, f"₿ 1 BTC = ${p} = {p*fiat_rates['USD']:.0f} TJS")
    elif "эфир" in text or "eth" in text:
        p = get_crypto_price("ETH")
        bot.send_message(m.chat.id, f"Ξ 1 ETH = ${p}")
    elif "тон" in text or "ton" in text:
        p = get_crypto_price("TON")
        bot.send_message(m.chat.id, f"💎 1 TON = ${p}")
    else:
        # ҳамаи крипто ё пул
        sym = re.findall(r'\b([A-Z]{2,5})\b', m.text.upper())
        if sym:
            p = get_crypto_price(sym[0])
            if p:
                bot.send_message(m.chat.id, f"₿ 1 {sym[0]} = ${p} = {p*fiat_rates['USD']:.2f} TJS")
                return
        bot.send_message(m.chat.id, "Навиш:\n• Сом чанд\n• Доллар чанд\n• Биткоин чанд\n• Евро чанд\n• Рубл чанд\n\nЁ номи ягон крипто: SOL, DOGE, TON", reply_markup=main_menu())

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
