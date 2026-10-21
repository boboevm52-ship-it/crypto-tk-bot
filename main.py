import os
import time
import requests
from flask import Flask
from threading import Thread

SITE_URL = "https://cryptotj-dushanbe.blogspot.com"
TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot Alive!"

def get_rates():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()
        usd = r['rates']['TJS']
        rub = usd / r['rates']['RUB']
        return round(usd, 3), round(rub, 4)
    except:
        return 10.92, 0.115

def send_message(chat_id, text):
    usd, rub = get_rates()
    # Тугмаҳо бо реклама
    keyboard = {
        "inline_keyboard": [
            [{"text": "🌐 Сомонаро кушо", "url": SITE_URL}],
            [{"text": "📢 Обуна", "url": SITE_URL}]
        ]
    }
    url = f"{API}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": keyboard
    }
    requests.post(url, json=data)

def run_bot():
    offset = 0
    while True:
        try:
            resp = requests.get(f"{API}/getUpdates?offset={offset}&timeout=30").json()
            for upd in resp.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "").lower()
                if not chat_id: continue

                usd, rub = get_rates()
                if "/start" in text:
                    txt = f"Салом! 👋\n\n💵 1 USD = {usd} TJS\n💵 1 RUB = {rub} TJS\n\nРубл чанд? нависед"
                else:
                    txt = f"💱 КУРС ИМРУЗ\n\n💵 1 USD = {usd} TJS\n💵 1 RUB = {rub} TJS\n💵 1000 RUB = {rub*1000:.1f} TJS"
                
                send_message(chat_id, txt)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    print("Бот сар шуд...")
    run_bot()
