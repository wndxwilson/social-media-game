import logging

import pandas as pd

import Rewards

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler,CallbackQueryHandler)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#Bot token
TOKEN = '1169087544:AAFnHKhcAqQwbWu0WL4A5zHFYwWjwnNssQw'

# Stages
CREATE, DONE, POINTS = range(3)



def start(update, context):
    bot = context.bot
    chat_id = update.message.chat_id
    bot.send_message(chat_id,text='Hi i am xxx_bot')
    if(chat_id!=chat_id):
        bot.send_message(chat_id,text='Use /link to link your social media to redeem rewards')


def link(update, context):
    bot = context.bot
    chat_id = update.message.chat_id
    if(chat_id != chat_id):
        bot.send_message(chat_id,text='Your social media is linked') 
        return DONE
    else:
        update.message.reply_text('Enter your instagram handle')
        return CREATE


def reply(update, context):
    user_input = update.message.text
    bot = context.bot
    chat_id = update.message.chat_id
    bot.send_message(chat_id,text='{} has been linked'.format(user_input)) 
    return ConversationHandler.END


def reward(update, context):
    r = Rewards.Rewards().test()
    custom_keyboard = []
    for index, row in r.iterrows():
        custom_keyboard.append([InlineKeyboardButton(str(row['name'])+" points: "+str(row['points']),callback_data=row['points'])])
    bot = context.bot
    chat_id = update.message.chat_id
    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=chat_id, 
                 text="Custom Keyboard Test", 
                 reply_markup=reply_markup)
    
    return POINTS

def points(update, context):
    query = update.callback_query
    print(query.data)
    query.answer()
    return ConversationHandler.END

def rank(update, context):
    pass
def stop(update,context):
    pass

def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('link', link)],

        states={
            CREATE : [MessageHandler(Filters.text, reply)]
        },

        fallbacks=[CommandHandler('link', link)]
    )

    dp.add_handler(conv_handler)

    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('reward', reward)],

        states={
            POINTS : [CallbackQueryHandler(points)]
        },

        fallbacks=[CommandHandler('reward', reward)]
    )

    dp.add_handler(conv_handler2)

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ranking', rank))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('help', help))

    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()