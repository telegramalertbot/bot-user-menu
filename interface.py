# https://pypi.org/project/python-telegram-bot/

from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler
from telegram.ext import ConversationHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging

## need in telegram token!!

telegram_token = ''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

LANG = "EN"
SET_LANG, MENU, SET_STAT, STREAM, CALL, ABOUT, EMERGORG= range(7)
STATE = SET_LANG


def start(bot, update):
    keyboard = [[ 'EN' ]]

    message = "Hey, I'm IntelligentNurse bot!  \n\n\
Please select a language to start."

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)

    return SET_LANG


def set_lang(bot, update):
    global LANG
    LANG = update.message.text
    user = update.message.from_user

    logger.info("Language set by {} to {}.".format(user.first_name, LANG))
    update.message.reply_text(lang_selected[LANG],
                              reply_markup=ReplyKeyboardRemove())

    return MENU


def menu(bot, update):
    keyboard = [[start_stream[LANG], view_arhive[LANG]],
                [emergency_call[LANG], view_about[LANG],
                 [emerg_org[LANG]]]]

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    user = update.message.from_user
    logger.info("Menu command requested by {}.".format(user.first_name))
    update.message.reply_text(main_menu[LANG], reply_markup=reply_markup)

    return SET_STAT


def set_state(bot, update):
    global STATE
    user = update.message.from_user
    if update.message.text == start_stream[LANG]:
        STATE = STREAM
        stream(bot, update)
        return STREAM
    elif update.message.text == view_archive[LANG]:
        STATE = ARHIVE
        view_archive(bot, update)
        return MENU
    elif update.message.text == emergency_call[LANG]:
        STATE = CALL
        call(bot, update)
        return MENU
    elif update.message.text == view_about[LANG]:
        STATE = ABOUT
        about_bot(bot, update)
        return MENU
    elif update.message.text == emerg_org[LANG]:
        STATE = EMERGORG
        emerg_org(bot, update)
        return EMERGORG
    else:
        STATE = MENU
        return MENU

def update_error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User {} canceled the conversation.".format(user.first_name))
    update.message.reply_text(goodbye[LANG],
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def help(bot, update):
    user = update.message.from_user
    logger.info("User {} asked for help.".format(user.first_name))
    update.message.reply_text(help_info[LANG],
                              reply_markup=ReplyKeyboardRemove())

def about_bot(bot, update):
    user = update.message.from_user
    logger.info("About info requested by {}.".format(user.first_name))
    bot.send_message(chat_id=update.message.chat_id, text=about_info[LANG])
    bot.send_message(chat_id=update.message.chat_id, text=back2menu[LANG])
    return


def stream(bot, update):
    return 0

def view_archive(bot, update):
    return 0

def call(bot, update):
    return 0

def emerg_org(bot, update):
    return 0
    

def main():
    global LANG
    # Create the EventHandler and pass it bot's token.
    updater = Updater(telegram_token)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SET_LANG: [RegexHandler('^(EN)$', set_lang)],

            MENU: [CommandHandler('menu', menu)],

            SET_STAT: [RegexHandler(
                        '^({}|{}|{}|{})$'.format(
                            start_stream['EN'], view_arhive['EN'],
                            emergency_call['EN'], view_about['EN']),
                        emerg_org)]
        },

        fallbacks=[CommandHandler('cancel', cancel),
                   CommandHandler('help', help)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()