import telebot, os
TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TOKEN") or os.environ.get("BOT")
print(f"TOKEN loaded: {TOKEN[:10] if TOKEN else 'NOT FOUND'}")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "✅ Бот кор кард! Токен дуруст!")

bot.infinity_polling()
