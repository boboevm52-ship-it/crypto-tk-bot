import telebot
bot = telebot.TeleBot("ТОКЕНИ_ХУДАТ")

RATES = {
    # 10-ТО ПУЛИ ДАВЛАТӢ
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

    # 10-ТО КРИПТО
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

@bot.message_handler(func=lambda m: True)
def h(m):
    t = m.text.lower()
    for k,v in RATES.items():
        if k in t:
            bot.reply_to(m, v)
            return
    bot.reply_to(m, "Навиш: Доллар, Евро, Рубл, Биткоин...")

bot.infinity_polling()
