import os
import threading
import time
from flask import Flask
import telebot
import requests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
time.sleep(2)
flask_app = Flask(__name__)
# ... боқӣ ҳамон код
