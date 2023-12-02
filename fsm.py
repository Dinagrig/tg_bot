from telegram import Update, ParseMode
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Dispatcher
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
from telegram.ext import Filters

from db import write_to_db, find_user_by_id
import logging

logger = logging.getLogger(__name__)

WAIT_OK, WAIT_NAME, WAIT_SURNAME, WAIT_BIRTHDAY, WAIT_TEETH, WAIT_HAIRCLR = range(6)


def check_register(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username=} {user_id=} хочет проверить регистрацию.')
    user = find_user_by_id(user_id)
    if not user:
        return ask_name(update, context)
    answer = [f'Приветствую.',
              f'Ты уже есть в списке собеседников Божьих со следующими данными:',
              f'Имя твое: {user[1]},',
              f'Фамилия твоя: {user[2]}',
              f'День рождения твоего: {user[3]}',
              f'Пломбы в устах твоих (ложь): {user[4]}',
              f'Цвет воолос твоих: {user[5]}']
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())

    buttons = [InlineKeyboardButton(text='Да', callback_data='Да'),
               InlineKeyboardButton(text='Нет', callback_data='Нет')]
    keyboard = InlineKeyboardMarkup.from_row(buttons)
    update.message.reply_text(text='Ты хочешь повторно стать собеседников Божьим?', reply_markup=keyboard)
    return WAIT_OK


def get_yes_no(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username=} {user_id=} ответил, хочет ли регаться снова.')
    query = update.callback_query
    if query.data == 'Да':
        return ask_name(update, context)
    return ConversationHandler.END


def ask_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    context.user_data['userid'] = user_id
    username = update.message.from_user.username
    logger.info(f'{username}{user_id} хочет сообщить имя свое ("ask_name").')
    answer = [
        f'Приветствую!\n'
        f'Назови мне имя свое.\n'

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
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    textb = update.message.text
    context.user_data['birthday'] = textb
    logger.info(f'{username}{user_id} запросил день рождения своего ("get_birthday").')
    answer = [
        f'Твой день рождения - {textb}\n'

    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())
    return ask_teeth(update, context)

def ask_teeth(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username}{user_id} хочет доложить про пломбы)))))) ("ask_teeth").')
    answer = [
        f'Ладно....\n'
        f'Назови мне количество пломб в устах твоих.\n'

    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())
    return WAIT_TEETH

def get_teeth(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    textt = update.message.text
    context.user_data['teeth'] = textt
    logger.info(f'{username}{user_id} спросил про зубы свои ("get_teeth").')
    answer = [
        f'Я, конечно знаю, что ты солгал, но зачту. Количество пломб в устах твоих - {textt}\n'

    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())
    return ask_hairclr(update, context)

def ask_hairclr(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username}{user_id} хочет сказать цвет волос своих ("ask_hairclr").')
    answer = [
        f'Учту..\n'
        f'Назови мне цвет волос своих.\n'

    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())
    return WAIT_HAIRCLR


def get_hairclr(update: Update, context: CallbackContext):
    return register(update, context)


def register(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    texth = update.message.text
    context.user_data['hair'] = texth
    logger.info(f'{username}{user_id}: допрос завершен.')
    answer = 'Благодарю.'
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())

    userid = context.user_data['userid']
    name = context.user_data['name']
    surname = context.user_data['surname']
    birthday = context.user_data['birthday']
    teeth = context.user_data['teeth']
    hair = context.user_data['hair']
    write_to_db(userid, name, surname, birthday)

    return ConversationHandler.END

register_handler = ConversationHandler(
    entry_points=[CommandHandler('register', ask_name)],
    states={
        WAIT_NAME: [MessageHandler(Filters.text, get_name)],
        WAIT_SURNAME: [MessageHandler(Filters.text, get_surname)],
        WAIT_BIRTHDAY: [MessageHandler(Filters.text, get_birthday)],
        WAIT_TEETH: [MessageHandler(Filters.text, get_teeth)],
        WAIT_HAIRCLR: [MessageHandler(Filters.text, get_hairclr)],
    },
    fallbacks=[]
)
