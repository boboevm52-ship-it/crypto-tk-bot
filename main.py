import telebot, os, threading, requests, json
from flask import Flask
from datetime import datetime

TOKEN = os.environ.get("BOT_TOKEN", "ТОКЕН")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
user_calc = {}

# ФАЙЛ БАРОИ ҲИСОБИ ОДАМОН
USERS_FILE = "users.json"
try:
    with open(USERS_FILE, "r") as f:
        users = set(json.load(f))
except:
    users = set()

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)

def add_user(uid):
    if uid not in users:
        users.add(uid)
        save_users()

BACKUP_FIAT = {"USD":[9.15,9.25,"💵 Доллар"],"RUB":[0.1126,0.1146,"🇷🇺 Рубл"],"EUR":[10.22,10.42,"🇪🇺 Евро"],"CNY":[1.25,1.29,"🇨🇳 Юан"],"GBP":[11.80,12.10,"🇬🇧 Фунт"],"KZT":[0.018,0.020,"🇰🇿 Тенге"],"TRY":[0.25,0.28,"🇹🇷 Лира"],"UZS":[0.0007,0.0008,"🇺🇿 Сум"],"KGS":[0.10,0.11,"🇰🇬 Сом"],"AED":[2.48,2.52,"🇦🇪 Дирхам"]}
BACKUP_CRYPTO = {"BTC":68000,"ETH":2600,"TON":5.2,"SOL":145,"DOGE":0.13,"XRP":0.52,"BNB":590,"TRX":0.16,"USDT":1,"PI":0.45}
AD="\n\n🌍 13 LIVE: https://cryptotj-dushanbe.blogspot.com/"

@app.route('/')
def home(): 
    return f"OK - {len(users)} users"

def kb():
 m=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
 m.add("👥 Омор","🧮 Ҳисобкунак","🌍 13 LIVE","💵 Доллар","🇷🇺 Рубл","🇪🇺 Евро","🇨🇳 Юан","🇬🇧 Фунт","🇰🇿 Тенге","🇹🇷 Лира","🇺🇿 Сум","🇰🇬 Сом","🇦🇪 Дирхам","₿ BTC","🌐 ETH","💎 TON","☀️ SOL","🐶 DOGE","💧 XRP","🟡 BNB","🔴 TRX","💲 USDT","🟣 PI")
 return m

def get_fiat_rates():
 try:
  r=requests.get("https://open.er-api.com/v6/latest/USD",timeout=5).json()
  tjs=r['rates']['TJS']
  return {"USD":[round(tjs*0.99,4),round(tjs*1.01,4),"💵 Доллар"],"EUR":[round(tjs/r['rates']['EUR']*0.99,4),round(tjs/r['rates']['EUR']*1.01,4),"🇪🇺 Евро"],"RUB":[round(tjs/r['rates']['RUB']*0.99,5),round(tjs/r['rates']['RUB']*1.01,5),"🇷🇺 Рубл"],"CNY":[round(tjs/r['rates']['CNY']*0.99,4),round(tjs/r['rates']['CNY']*1.01,4),"🇨🇳 Юан"],"GBP":[round(tjs/r['rates']['GBP']*0.99,4),round(tjs/r['rates']['GBP']*1.01,4),"🇬🇧 Фунт"],"KZT":[round(tjs/r['rates']['KZT']*0.99,5),round(tjs/r['rates']['KZT']*1.01,5),"🇰🇿 Тенге"],"TRY":[round(tjs/r['rates']['TRY']*0.99,4),round(tjs/r['rates']['TRY']*1.01,4),"🇹🇷 Лира"],"AED":[round(tjs/r['rates']['AED']*0.99,4),round(tjs/r['rates']['AED']*1.01,4),"🇦🇪 Дирхам"],"UZS":[0.0007,0.0008,"🇺🇿 Сум"],"KGS":[0.10,0.11,"🇰🇬 Сом"]}
 except: return BACKUP_FIAT

def get_crypto_price(sym):
 try:
  r=requests.get(f"https://data-api.binance.vision/api/v3/ticker/price?symbol={sym}USDT",timeout=4).json()
  return float(r['price'])
 except: return BACKUP_CRYPTO.get(sym,0)

@bot.message_handler(commands=['start','stats','stat'])
def s(m):
 add_user(m.chat.id)
 rates=get_fiat_rates()
 vaqt=datetime.now().strftime("%H:%M:%S")
 if "stat" in m.text:
  bot.send_message(m.chat.id,f"👥 ОМОРИ БОТ\n\n👤 Ҷами одам: {len(users)} нафар\n⏰ {vaqt}{AD}",reply_markup=kb())
 else:
  bot.send_message(m.chat.id,f"👋 AUTO LIVE\n💵 {rates['USD'][1]} | 🇷🇺 {round(rates['RUB'][1]*1000,1)}\n👥 Шумо {len(users)}-ум одам ҳастед!\n⏰ {vaqt}{AD}",reply_markup=kb())

@bot.message_handler(func=lambda x: True)
def all_h(m):
 add_user(m.chat.id)
 t=m.text
 uid=m.chat.id
 rates=get_fiat_rates()
 vaqt=datetime.now().strftime("%H:%M:%S")

 if "Омор" in t:
  bot.send_message(uid,f"👥 ОМОР\n\n👤 Ҷами: {len(users)} нафар\n🟢 Фаъол: Ҳама LIVE\n⏰ {vaqt}\n\nID шумо: {uid}{AD}",reply_markup=kb())
  return

 if uid in user_calc:
  try:
   miqdor=float(t.replace(",","."))
   curr=user_calc[uid]
   if curr in rates:
    natija=miqdor*rates[curr][1]
    bot.send_message(uid,f"🧮 {miqdor} {curr} = {round(natija,2)} TJS\n⏰ {vaqt}{AD}",reply_markup=kb())
   else:
    price=get_crypto_price(curr)
    natija=miqdor*price*rates['USD'][1]
    bot.send_message(uid,f"🧮 {miqdor} {curr} = ${round(miqdor*price,2)} = {round(natija,2)} TJS\n⏰ {vaqt}{AD}",reply_markup=kb())
   del user_calc[uid]
   return
  except:
   bot.send_message(uid,"❌ Рақам нависед! Масалан: 100",reply_markup=kb())
   return

 if "Ҳисобкунак" in t:
  bot.send_message(uid,"🧮 Кадом асъор? Доллар ё Рублро пахш кун, баъд рақам нависед!",reply_markup=kb())
  return

 for k,v in rates.items():
  if v[2].split()[1] in t:
   extra=f"\n🔴 1000={round(v[1]*1000,1)} TJS" if k=="RUB" else ""
   bot.send_message(uid,f"{v[2]} AUTO\nХарид: {v[0]}\nФурӯш: {v[1]}{extra}\n⏰ {vaqt}{AD}",reply_markup=kb())
   user_calc[uid]=k
   bot.send_message(uid,f"💰 Чанд {k} ҳисоб кунем? Рақам нависед:")
   return

 for s_name in ["BTC","ETH","TON","SOL","DOGE","XRP","BNB","TRX","USDT","PI"]:
  if s_name in t:
   p=get_crypto_price(s_name)
   bot.send_message(uid,f"₿ {s_name}: ${p}\n⏰ {vaqt}{AD}",reply_markup=kb())
   user_calc[uid]=s_name
   bot.send_message(uid,f"💰 Чанд {s_name}? Рақам нависед:")
   return

 bot.send_message(uid,f"🌍 LIVE: https://cryptotj-dushanbe.blogspot.com/{AD}",reply_markup=kb())

threading.Thread(target=lambda: app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000))),daemon=True).start()
while True:
 try: bot.infinity_polling()
 except: continue
