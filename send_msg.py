from telegram import *
from telegram.ext import *


TELEGRAM_TOKEN = '.....'

bot = Bot(token=TELEGRAM_TOKEN)

def send_msg(chat_id, message):
    bot.send_message(chat_id, message)
