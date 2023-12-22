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
from fsm import register_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    start_handler = CommandHandler(('start', 'help'), start)
    wish__1_handler = CommandHandler('wish_1', wish_1)
    wish__2_handler = CommandHandler('wish_2', wish_2)
    wish__3_handler = CommandHandler('wish_3', wish_3)
    keyboard_handler = CommandHandler('keyboard', keyboard)
    inline_keyboard_handler = CommandHandler('inline_keyboard', inline_keyboard)
    set_wish_timer_handler = CommandHandler('set', set_wish_timer)
    stop_wish_timer_handler = CommandHandler('stop', stop_wish_timer)
    react_echo_kbt_handler = MessageHandler(Filters.text, react_echo_kbt)
    callback_wish_handler = CallbackQueryHandler(keyboard_react_wish)
    links_music_handler = CommandHandler('music', links_music)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(wish__1_handler)
    dispatcher.add_handler(wish__2_handler)
    dispatcher.add_handler(wish__3_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(inline_keyboard_handler)
    dispatcher.add_handler(links_music_handler)
    dispatcher.add_handler(set_wish_timer_handler)
    dispatcher.add_handler(stop_wish_timer_handler)
    dispatcher.add_handler(register_handler)
    dispatcher.add_handler(react_echo_kbt_handler)
    dispatcher.add_handler(callback_wish_handler)

    updater.start_polling()
    logger.info(updater.bot.getMe())
    updater.idle()


def react_echo_kbt(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    text = update.message.text
    if text == 'Запустить таймер':
        user_id = update.effective_user.id
        context.bot_data['user_id'] = user_id
        context.bot_data['timer'] = datetime.datetime.now()
        context.bot_data['timer_job'] = context.job_queue.run_repeating(show_seconds, 1)
    elif text == 'Остановить таймер':
        user_id = update.effective_user.id
        logger.info(f'{user_id} запутсил delete_timer')
        timer = datetime.datetime.now() - context.bot_data['timer']
        context.bot_data['timer_job'].schedule_removal()
        update.message.reply_text(f'Таймер молитв остановлен. Ты молился {timer} секунд.')
        context.bot_data["message_id"] = None
    else:
        logger.info(f'{username=}({user_id=}) воззвал к Богу. Снизойти ли до его {text}?..')
        answer = f'Ты, {first_name}, взывающий(ая) к Богу, изрек(ла) {text}'
        update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())


def start(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name

    logger.info(f'{username=} решил, что достоен диалога с Богом (/start).')
    text = [
        f'Приветствую тебя, {first_name}, смотрю, ты решил(a), что достоин диалога с Богом..',
        '<b>Дмитрий Валерьевич, доброго времени суток, советую Вам не вчитываться в текст, а просто смотреть'
        ' за работой функций:)</b>',
        'В моей келье ты можешь:',
        '/start - посмотреть команды и поприветствовать твоего сегодняшнего наставника.',
        '/keyboard - вызвать клавиатуру, чтобы управлять таймером.',
        '/inline_keyboard - вызвать прикрепленную к сообщению клавиатуру с текстами молитв.',
        '/music - вызвать клавиатуру с музыкой',
        '/register - регистрация собеседником Божьим.',
        '/set - запустить таймер.',
        '/stop - остановить таймер.',
        '/wish_1 - прочитать молитву на день грядущий.',
        '/wish_2 - прочитать Отче наш.',
        '/wish_3 - прочитать утреннюю молитву.'
    ]
    text = '\n'.join(text)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def keyboard(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} ленится и вызвал инлайн клаву.')
    buttons = [
        ['Запустить таймер', 'Остановить таймер']
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    text = 'Ну раз ты так ленив, запусти таймер.'
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )
    logger.info('живем, не ломаемся')


def inline_keyboard(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} вызвал инлайн с молитвами.')
    buttons = [
        [InlineKeyboardButton(text='молитва на день грядущий', callback_data='wish 1'),
         InlineKeyboardButton(text='Отче наш', callback_data='wish 2')],
        [InlineKeyboardButton(text='утренняя молитва', callback_data='wish 3')]
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    text = 'Ну раз ты так ленив, выбери свою молитву на сегодня.'
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )
    logger.info('инлайн клава с молитвами выводится (inline_keyboard)')


def wish_1(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} хочет прочитать 1-ю молитву.')

    text = [
        'Господи, дай мне с душевным спокойствием встретить все, что даст мне сей день.',
        'Господи, дай мне вполне предаться воле Твоей Святой.',
        'Господи, на всякий час сего дня во всем наставь и поддержи меня.',
        'Господи, открой мне волю Твою для меня и окружающих меня.'
    ]
    text = '\n'.join(text)
    update.message.reply_text(text)


def wish_2(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} хочет прочитать 2-ю молитву.')

    text = [
        'Отче наш, сущий на небесах! Да святится имя Твое, да приидет Царствие Твое;',
        'да будет воля Твоя и на земле, как на небе;',
        'хлеб наш насущный дай нам на сей день;',
        'и прости нам долги наши, как и мы прощаем должникам нашим;',
        'и не введи нас в искушение, но избавь нас от лукавого.',
        'Ибо Твое есть Царство и сила и слава во веки.'
    ]
    text = '\n'.join(text)
    update.message.reply_text(text)


def wish_3(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} хочет прочитать 3-ю молитву.')

    text = [
        'Святый Боже, Святый Крепкий, Святый Безсмертный, помилуй нас.',
        '<i>Читается трижды, с крестным знамением и поясным поклоном.</i>',
        'Слава Отцу и Сыну и Святому Духу, и ныне и присно и во веки веков.Аминь'

    ]
    text = '\n'.join(text)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def keyboard_react_wish(update: Update, context: CallbackContext):
    query = update.callback_query
    username = update.effective_user.username
    logger.info(f'{username=} вызвал реакцию клавы с молитвами (keyboard_react_wish).')
    buttons = [
        [InlineKeyboardButton(text='молитва на день грядущий', callback_data='wish 1'),
         InlineKeyboardButton(text='Отче наш', callback_data='wish 2')],
        [InlineKeyboardButton(text='утренняя молитва', callback_data='wish 3')]
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    text = 'Ну раз ты смеешь быть недовольным, выбери другую молитву на сегодня.'
    # query.edit_message_text(
    #     text,       'если тебе надо, чтобы сообщение изменялось, смотри с какой клавиатуры пришла кнопка'
    #     (( 'создай массив...'
    #     reply_markup=keyboard
    # )
    if query.data == 'wish 1':
        answer = [
            'Господи, дай мне с душевным спокойствием встретить все, что даст мне сей день.',
            ' Господи, дай мне вполне предаться воле Твоей Святой.',
            ' Господи, на всякий час сего дня во всем наставь и поддержи меня.',
            ' Господи, открой мне волю Твою для меня и окружающих меня.'
        ]
        answer = '\n'.join(answer)
        query.message.reply_text(answer)
        logger.info('молитва 1 в инлайн клаве работает')
    elif query.data == 'wish 2':
        answer = [
            'Отче наш, сущий на небесах! Да святится имя Твое, да приидет Царствие Твое;',
            'да будет воля Твоя и на земле, как на небе;',
            'хлеб наш насущный дай нам на сей день;',
            'и прости нам долги наши, как и мы прощаем должникам нашим;',
            'и не введи нас в искушение, но избавь нас от лукавого.',
            'Ибо Твое есть Царство и сила и слава во веки.'
        ]
        answer = '\n'.join(answer)
        query.message.reply_text(answer)
        logger.info('молитва 2 в инлайн клаве работает')
    elif query.data == 'wish 3':
        answer = [
            'Святый Боже, Святый Крепкий, Святый Безсмертный, помилуй нас.',
            '<i>Читается трижды, с крестным знамением и поясным поклоном.</i>',
            'Слава Отцу и Сыну и Святому Духу, и ныне и присно и во веки веков.Аминь'

        ]
        answer = '\n'.join(answer)
        query.message.reply_text(answer, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        logger.info('молитвы инлайн клавы выводятся (keyboard_react_wish)')


def links_music(update: Update, context: CallbackContext):
    query = update.callback_query
    username = update.effective_user.username
    logger.info(f'{username=} вызвал ссылки на музыку (links_music).')
    buttons = [
        [('Пслушать Miserere mei', 'https://youtu.be/rs5bc_P1kKo?si=1etaiNhMsFP4tk_g'),('Послушать реквием',
        'https://youtu.be/MlAuHoRXLes?si=hFE90zXhziauS4TQ')],
        [('Послушать '
        'Оду к Радости', 'https://youtu.be/RPCv9rk_hH4?si=ei_Jm9Ct6ZyjN5-D')]
    ]
    # for row in buttons:
    #     if query.data in row:
    #         row.pop(row.index(query.data))
    keyboard_buttons = [[InlineKeyboardButton(text=text[0], url=text[1]) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    text = 'Ну раз ты смеешь быть недовольным, выбери другую молитву на сегодня.'
    # query.edit_message_text(
    #     text,       'если тебе надо, чтобы сообщение изменялось, смотри с какой клавиатуры пришла кнопка' (( 'создай массив...'
    #     reply_markup=keyboard
    # )
    text = 'Выбери, чем ты хочешь насладиться сегодня.'
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )
    logger.info('музыка не ломается (links_music)')

def set_wish_timer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    context.bot_data['user_id'] = user_id
    context.bot_data['timer'] = datetime.datetime.now()
    context.bot_data['timer_job'] = context.job_queue.run_repeating(show_seconds, 1)


def show_seconds(context: CallbackContext):
    logger.info(f'таймер работает {context.job_queue.jobs()}')
    message_id = context.bot_data.get('message_id', None)
    logger.info(f"{message_id}")
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
    timer = timer.seconds
    context.bot_data['timer_job'].schedule_removal()
    update.message.reply_text(f'Таймер молитв остановлен. Ты молился {timer} секунд.')
    context.bot_data["message_id"] = None


if __name__ == '__main__':
    main()
