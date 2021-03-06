import logging

import pandas as pd
import time 
import datetime as dt
from googletest import*

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler,CallbackQueryHandler)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

#Bot token
TOKEN = '1179255354:AAGhVBHGiaJ8b2Xn7C7hoP4J7K3nf351JMA'

# Stages
CREATE, DONE, POINTS = range(3)



def start(update, context):
    bot = context.bot
    chat_id = update.message.chat_id
    bot.send_message(chat_id,text='Hi i am social media game bot')
    if(chat_id!=chat_id):
        bot.send_message(chat_id,text='Use /link to link your social media to redeem rewards')


def link(update, context):
    bot = context.bot
    chat_id = update.message.chat_id
    user = update.message.from_user
    if(checkUsernameExistInGS("Players", chat_id)):
        bot.send_message(chat_id,text='Your social media is linked') 
        return ConversationHandler.END
    else:
        update.message.reply_text('Enter your instagram handle')
        return CREATE


def reply(update, context):
    user_input = update.message.text
    user = update.message.from_user
    bot = context.bot
    print(user['username'])
    chat_id = update.message.chat_id
    nameList = extractAllDataFromGS("Players")
    row = {'name':chat_id,'username':user_input,'points':'0'}
    nameList = nameList.append(row,ignore_index=True)
    save("Players",nameList)
    bot.send_message(chat_id,text='{} has been linked'.format(user_input)) 
    return ConversationHandler.END


def rewards(update, context):
    r = extractAllDataFromGS("rewards")
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
    user = update.callback_query.from_user
    bot = context.bot
    if(checkUsernameExistInGS("Players", user['username'])):
        point = extractTodayPointsFromGS("Players", user['username'])
        result = point-int(query.data)
        if(result>0):
            updatePlayerPointsToGS("Players",user['username'],result)
    query.answer()
    return ConversationHandler.END

def mypoints(update, context):
    user = update.message.from_user
    if(checkUsernameExistInGS("Players", user['username'])):
        point = extractTodayPointsFromGS("Players", user['username'])
        update.message.reply_text('you have {} points'.format(point))
    else:
        update.message.reply_text('Please link your social media')

def dailychallenge(update, context):
    date = dt.datetime.today().strftime("%Y/%m/%d")
    user_input = extractTodayChallengeFromGS("Challenges",date)
    bot = context.bot
    chat_id = update.message.chat_id
    text = 'Daily Challenges\n'
    i = 0
    for index, row in user_input.iterrows():
        text += str(i+1)+" : "+row['description']+"\nPoints: "+row['points']
        text += "\n"+row['hashtags'] +"\n"
        i += 1
    bot.send_message(chat_id=chat_id, 
                 text=text)

def rank(update, context):
    ranking = extractAllDataFromGS("Players").sort_values(by='points', ascending=False)
    bot = context.bot
    chat_id = update.message.chat_id
    i = 0
    text = ":medal:Rankings\n"
    for index, row in ranking.iterrows():
        text += str(i+1)+ "User: "+row['username']+"\n   Points: "+row['points']+"\n"
        i += 1
        if(i>30):
            break
    bot.send_message(chat_id=chat_id, 
                 text=text)

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
        entry_points=[CommandHandler('rewards', rewards)],

        states={
            POINTS : [CallbackQueryHandler(points)]
        },

        fallbacks=[CommandHandler('rewards', rewards)]
    )

    dp.add_handler(conv_handler2)

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('rank', rank))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('points', mypoints))
    dp.add_handler(CommandHandler('dailyChallenge', dailychallenge))
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()