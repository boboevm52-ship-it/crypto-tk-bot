@bot.message_handler(content_types=['text'])
def all_text(message):
    txt = message.text.strip()
    up = txt.upper()
    low = txt.lower()

    # ТОҶИКӢ -> КРИПТО
    if "биткоин" in low or "биткойн" in low or up == "BTC" or "btc" in low:
        up = "BTC"
    elif "эфир" in low or "eth" in low or up == "ETH":
        up = "ETH"
    elif "сол" in low or "sol" in low or up == "SOL":
        up = "SOL"
    elif "доги" in low or up == "DOGE":
        up = "DOGE"
    elif "тон" in low and len(low) < 10:
        up = "TON"
    elif "бнб" in low or up == "BNB":
        up = "BNB"
    elif "рипл" in low or "xrp" in low:
        up = "XRP"
    elif "трон" in low or "trx" in low:
        up = "TRX"
    elif "авакс" in low or "avax" in low:
        up = "AVAX"

    # 14 КУРС - ТОҶИКӢ
    if "доллар" in low or "доллар" in low or up == "USD":
        up = "USD"
    if "евро" in low or up == "EUR":
        up = "EUR"
    if "рубл" in low or up == "RUB":
        up = "RUB"
    if "сум" in low or "сум" in low or "uzs" in low:
        up = "UZS"

    if up in FIAT:
        rate = FIAT[up]; name = NAMES.get(up,"")
        if up == "UZS":
            msg = f"💰 {up} ({name}):\n• 1 UZS = {rate:.5f} TJS\n• 1000 UZS = {rate*1000:.2f} TJS{footer()}"
        else:
            msg = f"💰 1 {up} ({name}) = {rate:.4f} TJS{footer()}"
        bot.send_message(message.chat.id, msg, reply_markup=markup())
        return

    if up in CRYPTO:
        try:
            usd = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={CRYPTO[up]}&vs_currencies=usd", timeout=15).json()[CRYPTO[up]]['usd']
            msg = f"🟡 {up}:\n🟢 Доллар: {usd} $\n🔵 Рубл: {usd*USD_RUB:,.0f} RUB\n🔴 Сомонӣ: {usd*USD_TJS:,.0f} TJS{footer()}"
            bot.send_message(message.chat.id, msg, reply_markup=markup())
        except: pass
        return

    if "14 курс" in low or "курс" in low:
        full = "💱 14 КУРС - Бонки Миллӣ:\n\n"
        for code, rate in FIAT.items():
            name = NAMES.get(code,"")
            if code == "UZS":
                full += f"• 1 UZS ({name}) = {rate:.5f} TJS | 1000 = {rate*1000:.2f} TJS\n"
            else:
                full += f"• 1 {code} ({name}) = {rate:.4f} TJS\n"
        full += footer()
        bot.send_message(message.chat.id, full, reply_markup=markup())
        return

    if "10 крипто" in low or "крипто" in low:
        try:
            data = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(CRYPTO.values())}&vs_currencies=usd", timeout=15).json()
            full = "💰 10 КРИПТО:\n\n" + "".join([f"• {s}: {data[cid]['usd']} $\n" for s,cid in CRYPTO.items() if cid in data]) + footer()
            bot.send_message(message.chat.id, full, reply_markup=markup())
        except: pass
        return
