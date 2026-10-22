import os, requests, threading, time, re
from flask import Flask
import telebot
from telebot.apihelper import ApiTelegramException

BOT_TOKEN = os.getenv("BOT_TOKEN","").strip()
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

def clear():
 try:
  requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=15)
  requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/close", timeout=10)
  time.sleep(2)
 except: pass
clear()

# 14 АСОСӢ - БОҚИМОНДА АЗ API МЕГИРЕМ
FIAT_BASE={"USD":10.90,"EUR":11.85,"RUB":0.115,"GBP":12.34,"TRY":1.37,"CHF":11.17,"AED":2.51,"SAR":2.45,"INR":0.097,"KZT":0.022,"CNY":1.51,"KGS":0.124,"TMT":3.11,"UZS":0.000844}
CRYPTO={"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","BNB":"binancecoin","XRP":"ripple","DOGE":"dogecoin","TON":"the-open-network","USDT":"tether","TRX":"tron","AVAX":"avalanche-2"}

# ЛУҒАТИ КАЛОНИ ПУЛИ ДАВЛАТҲО
COUNTRY_MONEY={
 "USD":["usd","доллар","амрико","america","$","dollar"],
 "EUR":["eur","евро","europa"],
 "RUB":["rub","рубл","русия","russia","рубль"],
 "UZS":["uzs","сум","узбек","uzbek","сўм"],
 "KZT":["kzt","тенге","қазоқ","kazak","kazakh"],
 "KGS":["kgs","сом","киргиз","кыргыз"],
 "TJS":["tjs","сомонӣ","сомони","tajik"],
 "TRY":["try","лира","туркия","turkey"],
 "CNY":["cny","юан","чиноӣ","china","юань"],
 "AED":["aed","дирҳам","дубай","dubai","дирхам"],
 "SAR":["sar","риёл","саудӣ","saudi","саудия"],
 "INR":["inr","рупия","ҳинд","india","хинд"],
 "GBP":["gbp","фунт","британия","англия","pound"],
 "JPY":["jpy","йена","япония","japan","йен"],
 "KRW":["krw","вон","корея","korea"],
 "AZN":["azn","манат","озарбойҷон","azerbaijan"],
 "BYN":["byn","рубли беларус","belarus"],
 "TMT":["tmt","манат туркман","туркман"],
 "AFN":["afn","афғонӣ","afghan"],
 "PKR":["pkr","рупияи покистон","pakistan"],
}

SITE="https://cryptotj.blogspot.com"
CHANNEL="https://cryptotj.blogspot.com"

def footer(): return f"\n\n━━━━━━━━━━━━━━\n🌐 {SITE}\n💰 Ба сайти асли мо обуна шавед!"
def markup():
 m=telebot.types.InlineKeyboardMarkup(row_width=1)
 m.add(telebot.types.InlineKeyboardButton("💰 Бо Канали мо обуна шавед", url=CHANNEL),telebot.types.InlineKeyboardButton("🌐 Сайти асли мо", url=SITE))
 return m

CACHE_FIAT={}
CACHE_TIME=0

def get_all_fiat_rates():
 global CACHE_FIAT, CACHE_TIME
 # Ҳар 1 соат нав мекунем
 if time.time()-CACHE_TIME<3600 and CACHE_FIAT:
  return CACHE_FIAT
 try:
  # API-и ройгон - ҳамаи 160+ пулро медиҳад
  r=requests.get("https://open.er-api.com/v6/latest/USD", timeout=15).json()
  rates=r.get('rates',{})
  # Ба TJS табдил - USD=10.90 TJS
  usd_to_tjs=10.90
  converted={}
  for code, rate_vs_usd in rates.items():
   # rate_vs_usd = чанд дона аз ин пул = 1 USD
   # Мо мехоҳем 1 дона = чанд TJS
   # 1 USD = rate_vs_usd * [currency] => 1 [currency] = usd_to_tjs / rate_vs_usd
   if rate_vs_usd>0:
    converted[code]=usd_to_tjs/rate_vs_usd
  # Ҳамчунин 14-и худмонро нигоҳ медорем
  for k,v in FIAT_BASE.items():
   converted[k]=v
  CACHE_FIAT=converted
  CACHE_TIME=time.time()
  return converted
 except:
  return FIAT_BASE

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
   return symbol, name, coin_id, price
 except: pass
 return None, None, None, None

def find_fiat(text):
 text=text.lower()
 rates=get_all_fiat_rates()
 # Аз луғати калон
 for code, words in COUNTRY_MONEY.items():
  for w in words:
   if w in text:
    return code
 # Коди мустақим - JPY, KRW, AFN
 up=text.upper()
 for code in rates.keys():
  if re.search(r'\b'+code+r'\b', up):
   return code
 return None

def find_crypto_main(text):
 text=text.lower()
 smart={"BTC":["btc","биткоин","bitcoin"],"ETH":["eth","эфир"],"SOL":["sol","солана"],"DOGE":["doge","доге","дож"],"TON":["ton","тон"],"XRP":["xrp","рипл"],"TRX":["trx","трон"],"USDT":["usdt","тетер"],"BNB":["bnb","бинанс"],"AVAX":["avax","авакс"]}
 for code, words in smart.items():
  for w in words:
   if w in text:
    return code
 up=text.upper()
 for k in CRYPTO.keys():
  if re.search(r'\b'+k+r'\b', up):
   return k
 return None

def find_amount(text):
 m=re.search(r'(\d+(\.\d+)?)', text)
 if m:
  try: return float(m.group(1))
  except: return None
 return None

@bot.message_handler(commands=['start'])
def start(message):
 kb=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
 kb.add(telebot.types.KeyboardButton("BTC"),telebot.types.KeyboardButton("ETH"),telebot.types.KeyboardButton("SOL"),telebot.types.KeyboardButton("DOGE"))
 kb.add(telebot.types.KeyboardButton("USD"),telebot.types.KeyboardButton("EUR"),telebot.types.KeyboardButton("RUB"),telebot.types.KeyboardButton("UZS"))
 kb.add(telebot.types.KeyboardButton("14 курс"),telebot.types.KeyboardButton("10 крипто"),telebot.types.KeyboardButton("160 пул"),telebot.types.KeyboardButton("Биткоин чанд"))
 bot.send_message(message.chat.id, f"🌍 Ман ҳозир ҲАМАРО медонам!\n\n💰 160+ пули давлатҳо\n🚀 20,000+ крипто\n\nНавиш:\n• Йена чанд?\n• Вон чанд?\n• Афғонӣ чанд?\n• PEPE чанд?\n• 100 доллар чанд?\n\n🌐 {SITE}", reply_markup=kb)

@bot.message_handler(content_types=['text'])
def all_text(message):
 low=message.text.lower().strip()
 amount=find_amount(low)

 # КУРСИ ҲАМА 160 ПУЛ
 if "160" in low or "хамаи пул" in low or "ҳамаи пул" in low:
  rates=get_all_fiat_rates()
  top=list(rates.items())[:30]
  txt="🌍 30 ПУЛИ АСОСӢ (аз 160+):\n\n"+"\n".join([f"• 1 {k} = {v:.4f} TJS" for k,v in top])
  txt+=f"\n\n...ва боз {len(rates)-30} пули дигар!\nНавиш: Йена чанд?{footer()}"
  bot.send_message(message.chat.id, txt, reply_markup=markup()); return

 # ҲИСОБ
 if amount:
  fiat=find_fiat(low)
  if fiat:
   rates=get_all_fiat_rates()
   r=rates.get(fiat)
   if r:
    bot.send_message(message.chat.id, f"🧮 {amount} {fiat} = {amount*r:,.2f} TJS{footer()}", reply_markup=markup()); return

 # ПУЛИ ДАВЛАТҲО
 fiat=find_fiat(low)
 if fiat:
  rates=get_all_fiat_rates()
  r=rates.get(fiat)
  if r:
   bot.send_message(message.chat.id, f"💰 1 {fiat} = {r:.4f} TJS\n💵 {r*100:.2f} TJS = 100 {fiat}{footer()}", reply_markup=markup()); return
  else:
   bot.send_message(message.chat.id, f"💰 {fiat} ёфт нашуд, API банд{footer()}", reply_markup=markup()); return

 # КРИПТОИ АСОСӢ
 crypto=find_crypto_main(low)
 if crypto and crypto in CRYPTO:
  usd=get_usd_by_id(CRYPTO[crypto])
  if usd:
   bot.send_message(message.chat.id, f"🟡 {crypto}:\n🟢 {usd:,.6f} $\n🔴 {usd*10.90:,.4f} TJS{footer()}", reply_markup=markup()); return

 # ҲАР КРИПТОИ ДИГАР
 clean=re.sub(r'чанд|чика|сколка|price|нарх|курс|пул', '', low).strip()
 clean=re.sub(r'[^a-zA-Z0-9]', '', clean).strip()
 if len(clean)>=2:
  sym, name, cid, price = search_any_crypto(clean)
  if price:
   bot.send_message(message.chat.id, f"🟡 {sym} ({name}):\n🟢 {price:,.8f} $\n🔴 {price*10.90:,.6f} TJS{footer()}", reply_markup=markup()); return

 # КУРСҲОИ К
