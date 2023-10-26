from telegram import Update, ParseMode
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import Dispatcher
import logging
import datetime
from key import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    start_handler = CommandHandler(('start', 'help'), start)
    keyboard_handler = CommandHandler('keyboard', keyboard)
    inline_keyboard_handler = CommandHandler('inline_keyboard', inline_keyboard)
    set_wish_timer_handler = CommandHandler('set', set_wish_timer)
    stop_wish_timer_handler = CommandHandler('stop', stop_wish_timer)
    echo_handler = MessageHandler(Filters.text, do_echo)
    callback_handler = CallbackQueryHandler(keyboard_react)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(inline_keyboard_handler)
    dispatcher.add_handler(set_wish_timer_handler)
    dispatcher.add_handler(stop_wish_timer_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(callback_handler)


    updater.start_polling()
    logger.info(updater.bot.getMe())
    updater.idle()


def do_echo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    text = update.message.text

    logger.info(f'{username=}({user_id=}) воззвал к Богу. Снизойти ли до его {text}?..')
    answer = f'Ты, {first_name}, взывающий(ая) к Богу, изрек(ла) {text}'
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove)


def start(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name

    logger.info(f'{username=} решил, что достоен диалога с Богом.')
    text = [
        f'Приветствую тебя, {first_name}, смотрю, ты решил(a), что достоен диалога с Богом..',
        'В моей келье ты можешь:',
        '/start - посмотреть команды и поприветствовать твоего сегодняшнего наставника.',
        '/keyboard - вызвать клавиатуру, коли ты так ленив.',
        '/inline_keyboard - вызвать прикрепленную к сообщению клавиатуру, коли ты совсем ленив.',
        '/set - начать подсчет времени молитвы.',
        '/stop - закончить подсчет времени молитвы.'
        ]
    text = '\n'.join(text)
    update.message.reply_text(text)


def keyboard(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} ленится и вызвал инлайн клаву.')
    buttons = [
        ['Прочитать молитву 1', 'Прочитать молитву 2'],
        ['Прочитать молитву 3','Прочитать молитву 4'],
        ['Прочитать молитву 5']
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)


    text = 'Ну раз ты так ленив, выбери свою молитву на сегодня.'
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )
    logger.info('живем, не ломаемся')

def inline_keyboard(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} ленится и вызвал инлайн клаву.')
    buttons = [
        ['Прочитать молитву 1', 'Прочитать молитву 2'],
        ['Прочитать молитву 3', 'Прочитать молитву 4'],
        ['Прочитать молитву 5']
    ]
    keyboard_buttons = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    text = 'Ну раз ты так ленив, выбери свою молитву на сегодня.'
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )
    logger.info('живем, не ломаемся')


def keyboard_react(update: Update, context: CallbackContext):
    query = update.callback_query
    username = update.effective_user.username
    logger.info(f'{username=} решил поиграться кнопочками.')
    buttons = [
        ['Прочитать молитву 1', 'Прочитать молитву 2'],
        ['Прочитать молитву 3', 'Прочитать молитву 4'],
        ['Прочитать молитву 5']
    ]
    for row in buttons:
        if query.data in row:
            row.pop(row.index(query.data))
    keyboard_buttons = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    text = 'Ну раз ты так ленив, выбери другую молитву на сегодня.'
    query.edit_message_text(
        text,
        reply_markup=keyboard
    )
    logger.info('живем, не ломаемся')


def set_wish_timer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    context.bot_data['user_id'] = user_id
    context.bot_data['timer'] = datetime.datetime.now()
    context.bot_data['timer_job'] = context.job_queue.run_repeating(show_seconds, 1)


def show_seconds(context: CallbackContext):
    logger.info(f'{context.job_queue.jobs()}')
    message_id = context.bot_data.get('message_id', None)
    user_id = context.bot_data['user_id']
    timer = datetime.datetime.now() - context.bot_data['timer']
    timer = timer.seconds
    text = f'ты молишься уже {timer} секунд.'
    text += '\nнажми /stop, чтобы остановить таймер.'
    if not message_id:
        message = context.bot.send_message(user_id, text)
        context.bot_data['message_id'] = message.message_id
    else:
        context.bot.edit_message_text(text, chat_id=user_id, message_id=message_id)


def stop_wish_timer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    logger.info(f'{user_id} запутсил delete_timer')
    timer = datetime.datetime.now() - context.bot_data['timer']
    context.bot_data['timer_job'].schedule_removal()
    update.message.reply_text(f'Таймер молитв остановлен. Ты молился {timer} секунд.')

if __name__ == '__main__':
    main()