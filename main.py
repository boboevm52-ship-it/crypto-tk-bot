import telebot, requests, re, time, os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
BLOG_URL = "https://cryptotj-dushanbe.blogspot.com/2025/10/blog-post.html"
bot = telebot.TeleBot(BOT_TOKEN)

passed_users = set()
last_code = ""

def get_secret():
    global last_code
    try:
        url = f"{BLOG_URL}?t={int(time.time())}&r={os.urandom(2).hex()}"
        r = requests.get(url, timeout=10, headers={'User-Agent':'Mozilla/5.0','Cache-Control':'no-cache'})
        m = re.search(r'Коди имрӯз:\s*([A-Z0-9]+)', r.text, re.IGNORECASE)
        if m:
            new_code = m.group(1).upper()
            if last_code != "" and new_code != last_code:
                print(f"🔄 КОД ИВАЗ ШУД: {last_code} -> {new_code}")
                passed_users.clear()
            last_code = new_code
            return new_code
    except Exception as e:
        print(f"Хато: {e}")
    return last_code if last_code else "DUSHANBE777"

def get_fiat():
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=8).json()
        rates = r.get("rates", {})
        tjs = rates.get("TJS", 9.22)
        return {
            "USD": tjs, "EUR": tjs / rates.get("EUR",0.92), "RUB": tjs / rates.get("RUB",82),
            "CNY": tjs / rates.get("CNY",7.1), "KZT": tjs / rates.get("KZT",490),
            "UZS": tjs / rates.get("UZS",12800), "GBP": tjs / rates.get("GBP",0.79),
            "JPY": tjs / rates.get("JPY",155), "TRY": tjs / rates.get("TRY",34),
            "AED": tjs / rates.get("AED",3.67), "KGS": tjs / rates.get("KGS",89),
        }
    except:
        return {"USD":9.22,"EUR":10.34,"RUB":0.11,"CNY":1.38,"KZT":0.0205,"UZS":0.00072,"GBP":11.6,"JPY":0.059,"TRY":0.27,"AED":2.51,"KGS":0.103}

def get_crypto():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,solana,ripple,dogecoin,cardano,toncoin,tron,tether,notcoin,hamster-kombat,dogs-2,pepe,shiba-inu,litecoin,avalanche-2,polkadot,matic-network&vs_currencies=usd"
        r = requests.get(url, timeout=10).json()
        return {
            "BTC": r["bitcoin"]["usd"], "ETH": r["ethereum"]["usd"], "BNB": r["binancecoin"]["usd"],
            "SOL": r["solana"]["usd"], "XRP": r["ripple"]["usd"], "DOGE": r["dogecoin"]["usd"],
            "ADA": r["cardano"]["usd"], "TON": r["toncoin"]["usd"], "TRX": r["tron"]["usd"],
            "USDT": r["tether"]["usd"], "NOT": r["notcoin"]["usd"], "HAMSTER": r["hamster-kombat"]["usd"],
            "DOGS": r["dogs-2"]["usd"], "PEPE": r["pepe"]["usd"], "SHIB": r["shiba-inu"]["usd"],
            "LTC": r["litecoin"]["usd"], "AVAX": r["avalanche-2"]["usd"], "DOT": r["polkadot"]["usd"],
            "MATIC": r["matic-network"]["usd"],
        }
    except:
        return {"BTC":67500,"ETH":3500,"BNB":600,"SOL":160,"XRP":0.55,"DOGE":0.15,"ADA":0.45,"TON":6.5,"TRX":0.12,"USDT":1,"NOT":0.007,"HAMSTER":0.002,"DOGS":0.0005,"PEPE":0.000008,"SHIB":0.00002,"LTC":70,"AVAX":30,"DOT":6,"MATIC":0.5}

def full_kurs():
    fiat = get_fiat()
    crypto = get_crypto()
    today = datetime.now().strftime("%d.%m.%Y")
    real = get_secret()
    t = f"💱 КУРСИ ПУРРА - {today}\nКод: {real}\n\n💵 ФИАТ (11):\n"
    t += f"🇺🇸 1$ = {fiat['USD']:.2f} TJS\n🇪🇺 1€ = {fiat['EUR']:.2f} TJS\n🇷🇺 1₽ = {fiat['RUB']:.3f} TJS\n"
    t += f"🇨🇳 1¥ = {fiat['CNY']:.2f} TJS\n🇰🇿 1₸ = {fiat['KZT']:.4f} TJS\n🇺🇿 1000 СЎМ = {fiat['UZS']*1000:.2f} TJS\n"
    t += f"🇬🇧 1 ФУНТ = {fiat['GBP']:.2f} TJS\n🇯🇵 100 ЙЕН = {fiat['JPY']*100:.2f} TJS\n"
    t += f"🇹🇷 1 ЛИРА = {fiat['TRY']:.2f} TJS\n🇦🇪 1 ДИРҲАМ = {fiat['AED']:.2f} TJS\n🇰🇬 1 СОМ KG = {fiat['KGS']:.2f} TJS\n\n"
    t += "₿ КРИПТО (19):\n"
    t += f"BTC ${crypto['BTC']:,.0f} | ETH ${crypto['ETH']:,.0f}\nBNB ${crypto['BNB']:,.0f} | SOL ${crypto['SOL']:,.0f}\n"
    t += f"TON ${crypto['TON']:.2f} | XRP ${crypto['XRP']:.3f}\nDOGE ${crypto['DOGE']:.4f} | TRX ${crypto['TRX']:.3f}\n"
    t += f"USDT ${crypto['USDT']:.2f} | NOT ${crypto['NOT']:.5f}\nHAMSTER ${crypto['HAMSTER']:.6f}\n"
    t += f"DOGS ${crypto['DOGS']:.6f} | PEPE ${crypto['PEPE']:.8f}\nSHIB ${crypto['SHIB']:.8f} | LTC ${crypto['LTC']:.2f}\n"
    t += f"AVAX ${crypto['AVAX']:.2f} | DOT ${crypto['DOT']:.2f} | MATIC ${crypto['MATIC']:.3f}\n\n"
    t += "Навиш: '100 РУБЛ' ё 'BTC' ё 'КУРС'"
    return t, fiat, crypto

@bot.message_handler(func=lambda m: True)
def all_msg(message):
    txt = message.text.strip().upper()
    real = get_secret()
    uid = message.from_user.id

    if txt == real:
        passed_users.add(uid)
        t,_,_ = full_kurs()
        bot.reply_to(message, f"✅ Гузаштӣ бро! Код {real}\n\n{t}")
        return

    if uid not in passed_users:
        bot.reply_to(message, f"⛔️ Аввал код зан:\n{real}\n\nБлог: cryptotj-dushanbe.blogspot.com")
        return

    if txt in ["КУРС","KURS","ҲАМАИ КУРС","КРИПТО","30"]:
        t,_,_ = full_kurs()
        bot.reply_to(message, t)
        return

    crypto_list = ["BTC","ETH","BNB","SOL","TON","XRP","DOGE","TRX","USDT","ADA","NOT","HAMSTER","DOGS","PEPE","SHIB","LTC","AVAX","DOT","MATIC"]
    for c in crypto_list:
        if c in txt:
            _, fiat, crypto = full_kurs()
            price_usd = crypto.get(c,0)
            price_tjs = price_usd * fiat["USD"]
            bot.reply_to(message, f"₿ {c} = ${price_usd} = {price_tjs:,.2f} СОМОНӢ")
            return

    _, fiat, _ = full_kurs()
    m = re.match(r"(\d+)\s*(РУБЛ|ДОЛЛАР|\$|ЕВРО|ЮАН|ТЕНГЕ|СУМ|СЎМ|ФУНТ|ЙЕН|ЛИРА|ДИРҲАМ|СОМ)", txt)
    if m:
        amt = int(m.group(1)); cur = m.group(2)
        if "РУБЛ" in cur: bot.reply_to(message, f"🇷🇺 {amt} РУБЛ = {amt*fiat['RUB']:.2f} TJS")
        elif "ДОЛЛАР" in cur or "$" in cur: bot.reply_to(message, f"🇺🇸 {amt}$ = {amt*fiat['USD']:.2f} TJS")
        elif "ЕВРО" in cur: bot.reply_to(message, f"🇪🇺 {amt} ЕВРО = {amt*fiat['EUR']:.2f} TJS")
        elif "ЮАН" in cur: bot.reply_to(message, f"🇨🇳 {amt} ЮАН = {amt*fiat['CNY']:.2f} TJS")
        elif "ТЕНГЕ" in cur: bot.reply_to(message, f"🇰🇿 {amt} ТЕНГЕ = {amt*fiat['KZT']:.2f} TJS")
        elif "СУМ" in cur or "СЎМ" in cur: bot.reply_to(message, f"🇺🇿 {amt} СЎМ = {amt*fiat['UZS']:.2f} TJS")
        elif "ФУНТ" in cur: bot.reply_to(message, f"🇬🇧 {amt} ФУНТ = {amt*fiat['GBP']:.2f} TJS")
        elif "ЙЕН" in cur: bot.reply_to(message, f"🇯🇵 {amt} ЙЕН = {amt*fiat['JPY']:.2f} TJS")
        elif "ЛИРА" in cur: bot.reply_to(message, f"🇹🇷 {amt} ЛИРА = {amt*fiat['TRY']:.2f} TJS")
        elif "ДИРҲАМ" in cur: bot.reply_to(message, f"🇦🇪 {amt} ДИРҲАМ = {amt*fiat['AED']:.2f} TJS")
        elif "СОМ" in cur: bot.reply_to(message, f"🇰🇬 {amt} СОМ KG = {amt*fiat['KGS']:.2f} TJS")
        return

    t,_,_ = full_kurs()
    bot.reply_to(message, t)

print("Бот 30 пул + худфаҳм оғоз шуд...")
bot.infinity_polling()
