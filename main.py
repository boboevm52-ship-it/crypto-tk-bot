import telebot, requests

TOKEN = "TOKEN-и худро инҷо гузор"
bot = telebot.TeleBot(TOKEN)

# Қурби доллар ба сомонӣ - аз Бонки Миллӣ 23.10.2026
USD_TJS = 9.2261

def get_currencies():
    try:
        # Қурбҳои ҷаҳон ба доллар
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()
        rates = r['rates']
        # 10 пули машҳур ба сомонӣ
        data = {
            "🇺🇸 Доллар": rates['TJS'] if 'TJS' in rates else 9.2261,
            "🇪🇺 Евро": rates['TJS']/rates['EUR'] if 'EUR' in rates else 10.3655,
            "🇷🇺 Рубл": 0.1131,
            "🇰🇬 Сом": 0.105,
            "🇰🇿 Тенге": 0.018,
            "🇺🇿 Сӯм": 0.00072,
            "🇨🇳 Юан": 1.29,
            "🇹🇷 Лира": 0.27,
            "🇦🇪 Дирҳам": 2.51,
            "🇬🇧 Фунт": 12.02
        }
        return data
    except:
        return {
            "🇺🇸 Доллар": 9.2261, "🇪🇺 Евро": 10.3655, "🇷🇺 Рубл": 0.1131,
            "🇰🇬 Сом": 0.105, "🇰🇿 Тенге": 0.018, "🇺🇿 Сӯм": 0.00072,
            "🇨🇳 Юан": 1.29, "🇹🇷 Лира": 0.27, "🇦🇪 Дирҳам": 2.51, "🇬🇧 Фунт": 12.02
        }

def get_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,the-open-network,tether,binancecoin,solana,tron,dogecoin,cardano,ripple&vs_currencies=usd"
        r = requests.get(url, timeout=10).json()
        return {
            "₿ Биткоин": r.get('bitcoin',{}).get('usd',0),
            "🌐 Эфириум": r.get('ethereum',{}).get('usd',0),
            "💎 Тон": r.get('the-open-network',{}).get('usd',0),
            "💵 USDT": r.get('tether',{}).get('usd',0),
            "🟡 BNB": r.get('binancecoin',{}).get('usd',0),
            "☀️ Solana": r.get('solana',{}).get('usd',0),
            "🔴 Tron": r.get('tron',{}).get('usd',0),
            "🐶 Dogecoin": r.get('dogecoin',{}).get('usd',0),
            "🔵 Cardano": r.get('cardano',{}).get('usd',0),
            "✖️ XRP": r.get('ripple',{}).get('usd',0),
        }
    except:
        return {}

FOOTER = "\n\n👉 Бо сайти мо обуна шавед:\nhttps://cryptotj-dushanbe.blogspot.com/"

@bot.message_handler(func=lambda m: m.text and "Доллар чанд" in m.text)
def dollar(m):
    bot.send_message(m.chat.id, f"💵 1 Доллар = {USD_TJS} сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Рубл чанд" in m.text)
def rubl(m):
    bot.send_message(m.chat.id, f"🇷🇺 1 Рубл = 0.1131 сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Тон чанд" in m.text)
def ton(m):
    c = get_crypto()
    ton_usd = c.get("💎 Тон", 0)
    bot.send_message(m.chat.id, f"💎 Тон = ${ton_usd} = {ton_usd*USD_TJS:.2f} сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Эфир чанд" in m.text)
def eth(m):
    c = get_crypto()
    eth_usd = c.get("🌐 Эфириум", 0)
    bot.send_message(m.chat.id, f"🌐 Эфир = ${eth_usd} = {eth_usd*USD_TJS:.2f} сомонӣ{FOOTER}")

@bot.message_handler(func=lambda m: m.text and "Хамаи пулхо" in m.text)
def all_money(m):
    cur = get_currencies()
    txt = "🌍 10 пули ҷаҳон ба сомонӣ:\n\n"
    for k,v in cur.items():
        txt += f"{k} = {v} сомонӣ\n"
    txt += FOOTER
    bot.send_message(m.chat.id, txt)

@bot.message_handler(func=lambda m: m.text and "Хамаи криптохо" in m.text)
def all_crypto(m):
    c = get_crypto()
    txt = "🚀 10 криптои машҳур:\n\n"
    for k,v in c.items():
        txt += f"{k} = ${v}\n"
    txt += "\nБа сомонӣ ҳисоб кардан хоҳӣ? Нархро ба 9.22 зарб зан."
    txt += FOOTER
    bot.send_message(m.chat.id, txt)

@bot.message_handler(func=lambda m: True)
def other(m):
    bot.send_message(m.chat.id, f"Салом! Тугмаҳоро пахш кун, ман қурбро мегӯям.{FOOTER}")

print("Bot started")
bot.infinity_polling()
