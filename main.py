import logging
import db_service
import api_os
from telegram import *
from telegram.ext import *


TELEGRAM_TOKEN = '.....'

updater = Updater(token=TELEGRAM_TOKEN)
bot = Bot(token=TELEGRAM_TOKEN)

db_service.main()

def wake_up(update, context):
    """Starting Bot."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    if db_service.check_user(chat.id):
        buttons = ReplyKeyboardMarkup([['/AddCollection',
        '/GetPrice'
        ]], resize_keyboard=True)
    else:
        buttons = ReplyKeyboardMarkup([['/AddCollection']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='{}, choose an option!'.format(name),
        reply_markup=buttons  
        )


def add_collection(update, context):
    updater.dispatcher.add_handler(MessageHandler(Filters.text, addingNFT))
    chat = update.effective_chat
    send_message(chat.id, 'Please enter name of NFT collection along with percentage change upon you would like to receive an update')


def send_message(chat_id, message):
    bot.send_message(chat_id, message)


def addingNFT(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    message_text = update['message']['text']
    try:
        collection, percentage = message_text.split()
        collection = collection.lower()
    except:
        collection = message_text
    if api_os.check_collection(collection):
        if db_service.check_unique(chat.id, collection):
            logging.info('{} was already added by {}'.format(collection, name))
            send_message(chat.id, '{} was already added.'.format(collection))
        else:
            if 'percentage' in locals():
                price = api_os.get_price(collection)
                db_service.add_user_to_db(chat.id, name, collection, price, percentage)
                send_message(
                    chat.id,'{} was added. Will update on every {}% price change. Current: {} ETH.'.format(
                        collection, percentage, price))
            else:
                price = api_os.get_price(collection)
                db_service.add_user_to_db(chat.id, name, collection, price, 0)
                send_message(
                    chat.id, '{} was added. Notifications are disabled. Current price: {} ETH'.format(collection, price))
            wake_up(update, context)
    else:
        send_message(chat.id, '{} was not found.'.format(collection))
        wake_up(update, context)


def get_price(update, context):
    chat = update.effective_chat
    collections = db_service.get_collection(chat.id)
    for collection in collections:
        price = api_os.get_price(collection)
        message = 'Current FP for {} is {} ETH'.format(collection, price)
        send_message(chat.id, message)
        logging.info('FP {} ETH, {}, was sent to {} '.format(price, collection, chat.first_name))


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

