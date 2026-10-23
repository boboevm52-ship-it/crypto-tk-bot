import telebot, os
TOKEN = os.environ.get("TOKEN")
print(f"TOKEN IS: {TOKEN}")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "✅ Бот кор кард!")

bot.infinity_polling()
