from telegram import Update, ParseMode
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Dispatcher
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
from telegram.ext import Filters

from db import write_to_db
import logging

logger = logging.getLogger(__name__)

WAIT_NAME, WAIT_SURNAME, WAIT_BIRTHDAY = range(3)


def ask_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    context.user_data['userid'] = user_id
    username = update.message.from_user.username
    logger.info(f'{username}{user_id} хочет сообщить имя свое ("ask_name").')
    answer = [
        f'Приветствую!\n'
        f'Скажи мне имя свое.\n'

    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())

    return WAIT_NAME

def get_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    textn = update.message.text
    context.user_data['name'] = textn
    logger.info(f'{username}{user_id} спросил имя свое ("get_name").')
    answer = [
        f'Твое имя - {textn}!\n'

    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())
    return ask_surname(update, context)

def ask_surname(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username}{user_id} хочет сообщить фамилию свою ("ask_surname").')
    answer = [
        f'Приветствую!\n'
        f'Скажи мне фамилию свою.\n'

    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())

    return WAIT_SURNAME

def get_surname(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    texts = update.message.text
    context.user_data['surname'] = texts
    logger.info(f'{username}{user_id} спросил фамилию свою ("get_surname").')
    answer = [
        f'Твоя фамилия - {texts}!\n'

    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())
    return ask_birthday(update, context)

def ask_birthday(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username}{user_id} хочет сообщить день рождения своего ("ask_birthday").')
    answer = [
        f'Привествую!\n'
        f'Скажи мне дату рождения своего.\n'

    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())
    return WAIT_BIRTHDAY

def get_birthday(update: Update, context: CallbackContext):
    return register(update, context)


def register(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    textb = update.message.text
    context.user_data['birthday'] = textb
    userid = context.user_data['userid']
    name = context.user_data['name']
    surname = context.user_data['surname']
    birthday = context.user_data['birthday']
    write_to_db(userid, name, surname, birthday)
    logger.info(f'{username}{user_id} ??"".')
    answer = [
        f'Благодарю!\n'

    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

register_handler = ConversationHandler(
    entry_points=[CommandHandler('register', ask_name)],
    states={
        WAIT_NAME: [MessageHandler(Filters.text, get_name)],
        WAIT_SURNAME: [MessageHandler(Filters.text, get_surname)],
        WAIT_BIRTHDAY: [MessageHandler(Filters.text, get_birthday)]
    },
    fallbacks=[]
)
