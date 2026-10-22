 import telebot
import requests

TOKEN = "ТОКЕНИ_ХУДАТРО_ГУЗОР"
bot = telebot.TeleBot(TOKEN)

# 50 ДАВЛАТ
RATES = {
    "USD": 9.22, "EUR": 10.36, "RUB": 0.112, "CNY": 1.38, "KZT": 0.0206,
    "KGS": 0.104, "UZS": 0.00073, "TRY": 0.26, "GBP": 12.10, "AED": 2.51,
    "CHF": 11.2, "JPY": 0.061, "KRW": 0.0067, "INR": 0.11, "PKR": 0.033,
    "AFN": 0.13, "AZN": 5.42, "GEL": 3.40, "TMT": 2.63, "UAH": 0.22,
    "CAD": 6.75, "AUD": 6.05, "SAR": 2.45, "QAR": 2.53, "KWD": 30.1,
    "BHD": 24.4, "AMD": 0.023, "BYN": 2.82, "PLN": 2.38, "SEK": 0.89,
    "NOK": 0.86, "DKK": 1.38, "SGD": 7.05, "MYR": 1.97, "THB": 0.25,
    "BRL": 1.65, "MXN": 0.50, "EGP": 0.18, "ILS": 2.55, "CZK": 0.40,
    "RON": 2.08, "HUF": 0.025, "BGN": 5.29, "RSD": 0.088, "NZD": 5.55,
    "IDR": 0.00056, "PHP": 0.16, "VND": 0.00036, "MDL": 0.51, "IQD": 0.007
}

CRYPTO = {"BTC": 620000, "ETH": 35000, "USDT": 9.22, "BNB": 5500, "SOL": 1500, "TON": 55}

def understand(text):
    t = text.lower()
    # ТОҶИКӢ ФАҲМАД
    if any(w in t for w in ["доллар","долар","бакс","usd","$","dollar"]):
        return f"🇺🇸 Доллари Америка\n1 USD = {RATES['USD']} TJS"
    if any(w in t for w in ["евро","еуро","eur"]):
        return f"🇪🇺 Евро\n1 EUR = {RATES['EUR']} TJS"
    if any(w in t for w in ["рубл","rub"]):
        return f"🇷🇺 Рубли Руси\n1 RUB = {RATES['RUB']} TJS"
    if any(w in t for w in ["юан","cny","юани"]):
        return f"🇨🇳 Юани Хитой\n1 CNY = {RATES['CNY']} TJS"
    if any(w in t for w in ["тенге","kzt"]):
        return f"🇰🇿 Тенге\n1 KZT = {RATES['KZT']} TJS"
    if any(w in t for w in ["биткоин","btc","биток"]):
        return f"₿ Биткоин\n1 BTC = {CRYPTO['BTC']} TJS"
    if any(w in t for w in ["эфир","eth"]):
        return f"Ξ Эфириум\n1 ETH = {CRYPTO['ETH']} TJS"
    if any(w in t for w in ["курс","нарх","чанд","пул","курби","чико","хама","50"]):
        txt = "💵 КУРСИ 50 ДАВЛАТ:\n\n"
        for k,v in list(RATES.items())[:20]:
            txt += f"1 {k} = {v} TJS\n"
        txt += "\nНавиш: Доллар, Евро, Рубл, Биткоин"
        return txt
    return "Нафаҳмидам 😅\nНавиш: Доллар чанд? Евро? Биткоин? Курси хама?"

@bot.message_handler(func=lambda m: True)
def handler(m):
    bot.reply_to(m, understand(m.text))

print("Бот кор мекунад...")
bot.infinity_polling()
