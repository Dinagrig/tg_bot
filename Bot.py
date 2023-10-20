from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import Dispatcher
import logging
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
    echo_handler = MessageHandler(Filters.text, do_echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(echo_handler)

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
    update.message.reply_text(answer)


def start(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name

    logger.info(f'{username=} решил, что достоен диалога с Богом.')
    text = [
        f'{first_name}, смотрю, ты решил(a), что достоен диалога с Богом..',
        'В моей келье ты можешь:',
        ''
        ]
    text = '\n'.join(text)
    update.message.reply_text(text)


def keyboard(update: Update, context: CallbackContext):
    buttons = [
        ['Прочитать молитву', 'Прочитать молитву'],
        ['Прочитать молитву','Прочитать молитву'],
        ['Прочитать молитву']
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)


    text = 'Ну раз ты так ленив, выбери свою молитву на сегодня.'
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )



main()
