import logging
import db_service
import api_os
from telegram import *
from telegram.ext import *


TELEGRAM_TOKEN = '5399837848:AAFPhYs_DGb44UmxgE_gZC3xKPJXgGdKY-g'
TELEGRAM_CHAT_ID = 396296669

updater = Updater(token=TELEGRAM_TOKEN)
bot = Bot(token=TELEGRAM_TOKEN)

db_service.main()

def wake_up(update, context):
    """Starting Bot."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    if db_service.check_user(chat.id):
        buttons = ReplyKeyboardMarkup([['/AddCollection', '/GetPrice', '/SetNotifications', '/GetCollections']])
    else:
        buttons = ReplyKeyboardMarkup([['/AddCollection']])
    context.bot.send_message(
        chat_id=chat.id,
        text='{}, choose an option!'.format(name),
        reply_markup=buttons  
        )


def add_collection(update, context):
    updater.dispatcher.add_handler(MessageHandler(Filters.text, addingNFT))
    chat = update.effective_chat
    send_message(chat.id, 'Please enter name of NFT collection')


def send_message(user_id, message):
    bot.send_message(user_id, message)


def addingNFT(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    message_text = update['message']['text']
    lower_name = message_text.lower()
    if api_os.check_collection(lower_name):
        if db_service.check_unique(chat.id, lower_name):
            logging.info('{} was already added by {}'.format(lower_name, name))
            send_message(chat.id, '{} was already added.'.format(lower_name))
        else:
            db_service.add_user_to_db(chat.id, name, lower_name)
            send_message(chat.id, '{} was added.'.format(lower_name))
            wake_up(update, context)
    else:
        send_message(chat.id, '{} was not found.'.format(lower_name))
        wake_up(update, context)


def get_price(update, context):
    chat = update.effective_chat
    collection = db_service.get_collection(chat.id)
    price = api_os.get_price(collection)
    message = 'Current FP for {} is {} ETH'.format(collection, price)
    send_message(chat.id, message)


def set_notifications(chat_id):
    pass

def get_collections(update, context):
    chat = update.effective_chat
    output = db_service.get_all_collections(chat.id)
    send_message(chat.id, output)



updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('AddCollection', add_collection))
updater.dispatcher.add_handler(CommandHandler('GetPrice', get_price))
updater.dispatcher.add_handler(CommandHandler('SetNotifications', set_notifications))
updater.dispatcher.add_handler(CommandHandler('GetCollections', get_collections))


updater.start_polling()
updater.idle() 

