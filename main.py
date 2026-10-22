import os, requests, threading, time, re, traceback
from flask import Flask
import telebot
from telebot.apihelper import ApiTelegramException

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
if not BOT_TOKEN:
    print("❌ BOT_TOKEN нест!")

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

def clear():
 try:
  print("🧹 Тоза кардан...")
  requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=15)
  requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/close", timeout=10)
  time.sleep(3)
  print("✅ Тоза шуд")
 except Exception as e:
  print(f"Clear error: {e}")
clear()

FIAT_BASE={"USD":10.90,"EUR":11.85,"RUB":0.115,"GBP":12.34,"TRY":1.37,"CHF":11.17,"AED":2.51,"SAR":2.45,"INR":0.097,"KZT":0.022,"CNY":1.51,"KGS":0.124,"TMT":3.11,"UZS":0.000844}
CRYPTO={"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","BNB":"binancecoin","XRP":"ripple","DOGE":"dogecoin","TON":"the-open-network","USDT":"tether","TRX":"tron","AVAX":"avalanche-2"}

SITE="https://cryptotj.blogspot.com"

def footer(): return f"\n\n━━━━━━━━━━━━━━\n🌐 {SITE}\n💰 Ба сайти асли мо обуна шавед!"
def markup():
 m=telebot.types.InlineKeyboardMarkup(row_width=1)
 m.add(
  telebot.types.InlineKeyboardButton("💰 Бо Канали мо обуна шавед", url=SITE),
  telebot.types.InlineKeyboardButton("🌐 Сайти асли мо", url=SITE)
 )
 return m

def get_usd_by_id(cid):
 try:
  r=requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd",timeout=20).json()
  return r.get(cid,{}).get('usd')
 except: return None

def search_any_crypto(query):
 try:
  url=f"https://api.coingecko.com/api/v3/search?query={query}"
  res=requests.get(url, timeout=15).json()
  coins=res.get('coins',[])
  if coins:
   coin_id=coins[0]['id']
   symbol=coins[0]['symbol'].upper()
   name=coins[0]['name']
   price=get_usd_by_id(coin_id)
   return symbol, name, price
 except: pass
 return None, None, None

# === БОАҚЛ - ХАТОГИҲОРО МЕФАҲМАД ===
def find_any(text):
 t=text.lower()
 # Ҳатто "рубул", "рубль", "рубл" - ҳама
 if any(x in t for x in ["рубл","рубул","рубь","rubl","rub"]): return "RUB"
 if any(x in t for x in ["доллар","долар","dollar","usd","доллор"]): return "USD"
 if any(x in t for x in ["евро","euro","eur"]): return "EUR"
 if any(x in t for x in ["сум","so'm","uzs","сўм"]): return "UZS"
 if any(x in t for x in ["биткоин","биток","bitcoin","btc","битоин","биткойн"]): return "BTC"
 if any(x in t for x in ["эфир","eth","ethereum"]): return "ETH"
 if any(x in t for x in ["доге","дож","doge"]): return "DOGE"
 if any(x in t for x in ["тон","ton"]): return "TON"
 if any(x in t for x in ["рипл","xrp","ripple"]): return "XRP"
 if any(x in t for x in ["солана","sol"]): return "SOL"
 if any(x in t for x in ["трон","trx","tron"]): return "TRX"
 if any(x in t for x in ["тетер","usdt"]): return "USDT"
 if any(x in t for x in ["йена","yena","jpy","yen"]): return "JPY"
 if any(x in t for x in ["вон","won","krw"]): return "KRW"
 if any(x in t for x in ["афгон","afgh"]): return "AFN"
 return None

def get_fiat_rate(code):
 rates={}
 try:
  r=requests.get("https://open.er-api.com/v6/latest/USD", timeout=10).json()
  usd_rates=r.get('rates',{})
  for k,v in usd_rates.items():
   if v>0: rates[k]=10.9/v
 except: pass
 for k,v in FIAT_BASE.items(): rates[k]=v
 # JPY, KRW ва ғайраро илова кун
 rates.setdefault("JPY", 0.073)
 rates.setdefault("KRW", 0.0081)
 rates.setdefault("AFN", 0.15)
 return rates.get(code)

@bot.message_handler(commands=['start'])
def start(message):
 try:
  kb=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
  kb.add(telebot.types.KeyboardButton("BTC"),telebot.types.KeyboardButton("ETH"),telebot.types.KeyboardButton("Рубл чанд"),telebot.types.KeyboardButton("Доллар чанд"),telebot.types.KeyboardButton("Биткоин чанд"),telebot.types.KeyboardButton("Doge чанд"))
  bot.send_message(message.chat.id, f"✅ Салом! Ман кор мекунам!\n\nНавиш: Рубл чанд, Биткоин чанд, Йена чанд\n\n🌐 {SITE}", reply_markup=kb)
 except Exception as e:
  print(f"Start error: {e}")

@bot.message_handler(content_types=['text'])
def all_text(message):
 try:
  print(f"📩 Паём: {message.text}")
  low=message.text.lower()
  code=find_any(message.text)
  
  print(f"🔍 Ёфт: {code}")

  if code:
   if code in FIAT_BASE or code in ["RUB","USD","EUR","UZS","JPY","KRW","AFN"]:
    rate=get_fiat_rate(code)
    if rate:
     bot.send_message(message.chat.id, f"💰 1 {code} = {rate:.4f} TJS\n💵 100 {code} = {rate*100:.2f} TJS{footer()}", reply_markup=markup())
     return
   if code in CRYPTO:
    price=get_usd_by_id(CRYPTO[code])
    if price:
     bot.send_message(message.chat.id, f"🟡 {code}:\n🟢 {price:,.6f} $\n🔴 {price*10.9:,.2f} TJS{footer()}", reply_markup=markup())
    else:
     bot.send_message(message.chat.id, f"⏳ {code} ҳозир банд, 10с баъд санҷ!{footer()}", reply_markup=markup())
    return

  # Агар наёфт - криптои дигар ҷустуҷӯ
