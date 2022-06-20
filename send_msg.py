from telegram import *
from telegram.ext import *


TELEGRAM_TOKEN = '5399837848:AAFPhYs_DGb44UmxgE_gZC3xKPJXgGdKY-g'

bot = Bot(token=TELEGRAM_TOKEN)

def send_msg(chat_id, message):
    bot.send_message(chat_id, message)
