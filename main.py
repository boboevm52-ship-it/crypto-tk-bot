import telebot
import requests

BOT_TOKEN = "ТОКЕНАТРО ИН ҶО ГУЗОР"
bot = telebot.TeleBot(BOT_TOKEN)

USD_TJS = 10.90
USD_RUB = 95.50

# 14 КУРС - НБТ (UZS ДУРУСТ!)
FIAT = {
    "USD": ("Доллар", 10.90),
    "EUR": ("Евро", 11.85),
    "RUB": ("Рубл", 0.115),
    "GBP": ("Фунт", 12.34),
    "TRY": ("Лира", 1.37),
    "CHF": ("Франк", 11.17),
    "AED": ("Дирхам", 2.51),
    "SAR": ("Риял", 2.45),
    "INR": ("Рупия", 0.097),
    "KZT": ("Тенге", 0.022),
    "CNY": ("Юан", 1.51),
    "KGS": ("Сом", 0.124),
    "TMT": ("Манат", 3.11),
    "UZS": ("Сум", 0.000844),
}

# 10 КРИПТО
CRYPTO = {
    "BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana",
    "BNB": "binancecoin", "XRP": "ripple", "DOGE": "dogecoin",
    "TON": "the-open-network", "USDT": "tether",
    "TRX": "tron", "AVAX": "avalanche-2"
}

def get_footer():
    return "\n\n━━━━━━━━━━━━━━\n🌐 cryptotj.tj\n💰 Ба сайти асли мо обуна шавед!"

def markup():
    m = telebot.types.InlineKeyboardMarkup(row_width=1)
    m.add(
        telebot.types.InlineKeyboardButton("💰 Сомони асли - мо обуна шавед", url="https://t.me/CryptoTj"),
        telebot.types.InlineKeyboardButton("🌐 Ба сайти асли мо - cryptotj.tj", url="https://cryptotj.tj")
    )
    return m

def get_14_kurs():
    txt = "💱 14 КУРС - Бонки Миллӣ:\n\n"
    for code,(nom,rate) in FIAT.items():
        if code == "UZS":
            txt += f"• 1 UZS ({nom}) = {rate:.5f} TJS\n  1000 UZS = {rate*1000:.2f} TJS\n"
        else:
            txt += f"• 1 {code} ({nom}) = {rate:.4f} TJS\n"
    txt += get_footer()
    return txt

@bot.message_handler(commands=['start'])
def start(m):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(*[telebot.types.KeyboardButton(k) for k in CRYPTO.keys()])
    kb.add(telebot.types.KeyboardButton("14 курс"), telebot.types.KeyboardButton("Сум чанд"))
    bot.send_message(m.chat.id, "✅ Бот тайёр!\n10 крипто + 14 курс\nИнтихоб кун:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text.upper() in FIAT)
def fiat_one(m):
    code = m.text.upper()
    nom, rate = FIAT[code]
    if code == "UZS":
        txt = f"💰 {code} ({nom}):\n• 1 UZS = {rate:.5f} TJS\n• 1000 UZS = {rate*1000:.2f} TJS"
    else:
        txt = f"💰 1 {code} ({nom}) = {rate:.4f} TJS"
    txt += get_footer()
    bot.send_message(m.chat.id, txt, reply_markup=markup())

@bot.message_handler(func=lambda m: m.text.upper
