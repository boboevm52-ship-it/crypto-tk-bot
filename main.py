
import os, requests, threading, time
from flask import Flask
import telebot
from telebot.apihelper import ApiTelegramException

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# ҲАМА вебхук ва getUpdates-ро куш!
def clear_all():
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=15)
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/close", timeout=10)
        print("✅ All cleared")
        time.sleep(3)
    except: pass

clear_all()

FIAT={"USD":10.90,"EUR":11.85,"RUB":0.115,"GBP":12.34,"TRY":1.37,"CHF":11.17,"AED":2.51,"SAR":2.45,"INR":0.097,"KZT":0.022,"CNY":1.51,"KGS":0.124,"TMT":3.11,"UZS":0.000844}
CRYPTO={"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","BNB":"binancecoin","XRP":"ripple","DOGE":"dogecoin","TON":"the-open-network","USDT":"tether","TRX":"tron","AVAX":"avalanche-2"}
SITE="https://cryptotj.blogspot.com"
CHANNEL="https://t.me/CryptoTj"
TJS=10.90
RUB=95.50

def footer(): return f"\n\n━━━━━━━━━━━━━━\n🌐 {SITE}\n💰 Ба сайти асли мо обуна шавед!"
def markup():
 m=telebot.types.InlineKeyboardMarkup(row_width=1)
 m.add(telebot.types.InlineKeyboardButton("💰 Ба канали мо обуна шавед",url=CHANNEL),telebot.types.InlineKeyboardButton("🌐 Сайти асли мо",url=SITE))
 return m

def get_usd(cid):
 try:
  return requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd",timeout=20).json()[cid]['usd']
 except: return None

@bot.message_handler(commands=['start'])
def start(message):
 kb=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
 kb.add(telebot.types.KeyboardButton("BTC"),telebot.types.KeyboardButton("ETH"),telebot.types.KeyboardButton("SOL"))
 kb.add(telebot.types.KeyboardButton("BNB"),telebot.types.KeyboardButton("XRP"),telebot.types.KeyboardButton("DOGE"))
 kb.add(telebot.types.KeyboardButton("TON"),telebot.types.KeyboardButton("USDT"),telebot.types.KeyboardButton("TRX"))
 kb.add(telebot.types.KeyboardButton("AVAX"))
 kb.add(telebot.types.KeyboardButton("14 курс"),telebot.types.KeyboardButton("10 крипто"))
 kb.add(telebot.types.KeyboardButton("Биткоин чанд"),telebot.types.KeyboardButton("Тон чанд"))
 bot.send_message(message.chat.id,f"✅ Тайёр! 14 курс + 10 крипто\n🌐 {SITE}",reply_markup=kb)

@bot.message_handler(content_types=['text'])
def all_text(message):
 low=message.text.lower().strip()
 up=message.text.upper().strip()
 if "биткоин" in low: up="BTC"
 elif "тон" in low: up="TON"
 elif "рипл" in low or "xrp" in low: up="XRP"
 elif "доллар" in low: up="USD"
 elif "евро" in low: up="EUR"
 elif "рубл" in low: up="RUB"
 elif "сум" in low: up="UZS"

 if up in FIAT:
  r=FIAT[up]
  msg=f"💰 1 {up} = {r:.4f} TJS{footer()}" if up!="UZS" else f"💰 1000 UZS = {r*1000:.2f} TJS{footer()}"
  bot.send_message(message.chat.id,msg,reply_markup=markup()); return

 if up in CRYPTO:
  usd=get_usd(CRYPTO[up])
  if usd:
   bot.send_message(message.chat.id,f"🟡 {up}:\n🟢 {usd} $\n🔵 {usd*RUB:,.0f} RUB\n🔴 {usd*TJS:,.0f} TJS{footer()}",reply_markup=markup())
  else:
   bot.send_message(message.chat.id,f"🟡 {up} дастрас нест, боз санҷ!{footer()}",reply_markup=markup())
  return

 if "курс" in low:
  txt="💱 14 КУРС:\n\n"+"\n".join([f"• 1 {k} = {v:.4f} TJS" for k,v in FIAT.items()])+footer()
  bot.send_message(message.chat.id,txt,reply_markup=markup()); return
 if "крипто" in low:
  try:
   data=requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(CRYPTO.values())}&vs_currencies=usd",timeout=20).json()
   txt="💰 10 КРИПТО:\n\n"+"\n".join([f"• {s}: {data.get(c,{}).get('usd','-')} $" for s,c in CRYPTO.items()])+footer()
   bot.send_message(message.chat.id,txt,reply_markup=markup())
  except: pass

app=Flask(__name__)
@app.route('/')
def home(): return "Live"

def run_bot():
 while True:
  try:
   print("Polling started...")
   bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
  except ApiTelegramException as e:
   if "409" in str(e):
    print("409 Conflict - waiting 15 sec...")
    time.sleep(15)
    clear_all()
   else: time.sleep(5)
  except Exception as e:
   print(f"Poll error: {e}")
   time.sleep(10)

if __name__=="__main__":
 threading.Thread(target=run_bot,daemon=True).start()
 app.run(host="0.0.0.0",port=10000)
