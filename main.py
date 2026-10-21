import os, time, requests
from flask import Flask
from threading import Thread

SITE_URL = "https://cryptotj-dushanbe.blogspot.com"
TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)
@app.route('/')
def home(): return "Bot 14 kurs Alive!"

CURRENCIES = {
    'USD': 'Доллар', 'EUR': 'Евро', 'RUB': 'Рубл', 'GBP': 'Фунт',
    'CNY': 'Юан', 'TRY': 'Лира', 'KZT': 'Тенге', 'UZS': 'Сум',
    'KGS': 'Сом', 'JPY': 'Йен', 'CHF': 'Франк', 'AED': 'Дирхам',
    'SAR': 'Риял', 'INR': 'Рупия'
}

def get_rates():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()
        tjs = r['rates']['TJS']
        res = {}
        for c in CURRENCIES:
            if c == 'USD': res[c] = tjs
            else: res[c] = tjs / r['rates'].get(c, 1)
        return res
    except:
        return {c: 10.9 for c in CURRENCIES}

def send(chat_id, text):
    kb = {"inline_keyboard": [[{"text": "🌐 Сомона - 14 курс", "url": SITE_URL}]]}
    requests.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": text, "reply_markup": kb})

def run_bot():
    offset = 0
    while True:
        try:
            data = requests.get(f"{API}/getUpdates?offset={offset}&timeout=30").json()
            for upd in data.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                txt_in = msg.get("text","").lower()
                if not chat_id: continue
                k = get_rates()

                found = None
                for code, name in CURRENCIES.items():
                    if code.lower() in txt_in or name.lower() in txt_in:
                        found = code; break

                if found:
                    txt = f"💰 1 {found} ({CURRENCIES[found]}) = {k[found]:.4f} TJS\n1000 {found} = {k[found]*1000:.1f} TJS"
                else:
                    txt = "💱 КУРСИ 14 АРЗ:\n\n"
                    for code, name in CURRENCIES.items():
                        txt += f"• 1 {code} ({name}) = {k[code]:.4f} TJS\n"
                
                send(chat_id, txt)
        except: time.sleep(5)

def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    run_bot()
