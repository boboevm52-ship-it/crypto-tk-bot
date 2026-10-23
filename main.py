import telebot, os
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
print(f"Bot token ok: {TOKEN[:10]}...")

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "✅ Бот кор кард! Токен дуруст аст!")

bot.infinity_polling()
