from telebot import TeleBot
from telebot.types import Message
from googletrans import Translator
from telebot.types import ReplyKeyboardRemove

from configs import TOKEN
from keyboards import generate_languages
from queries import insert_translate_history, select_history

bot = TeleBot(token=TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start', 'history', 'about_dev', 'continue'])
def command_start(message: Message):
    user_id = message.from_user.id
    if message.text == '/start':
        full_name = message.from_user.full_name
        bot.send_message(user_id, f"""Welcome to our telegram bot!!! <i>{full_name}</i>""")
        ask_first_language(message)
    elif message.text == '/history':
        show_history(message)
    elif message.text == '/about_dev':
        bot.send_message(user_id, f"""This bot created by https://t.me/Jaf_the_Coder""")
        ask_first_language(message)
    elif message.text == '/continue':
        msg = bot.send_message(user_id, 'OK')
        bot.register_next_step_handler(msg, ask_text, translate)


def show_history(message: Message):
    user_id = message.from_user.id
    translates = select_history(user_id)

    for tr in translates[:-6:-1]:
        bot.send_message(user_id, f"""
<b>From language:</b> {tr[0]}
<b>To language:</b> {tr[1]}
<b>Original text:</b> {tr[2]}
<b>Translated text:</b> {tr[3]}
""")

    ask_first_language(message)


def ask_first_language(message: Message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id,
                           f"""Please choose <b>from which</b> language do you want to translate:""",
                           reply_markup=generate_languages())

    bot.register_next_step_handler(msg, ask_second_language)


def ask_second_language(message: Message):
    if message.text in ['/start', '/history', '/about_dev']:
        command_start(message)
    else:
        user_id = message.from_user.id
        first_language = message.text
        msg = bot.send_message(user_id,
                               f"""Please choose <b>to which</b> language do you want to translate:""",
                               reply_markup=generate_languages())
        bot.register_next_step_handler(msg, ask_text, first_language)


def ask_text(message: Message, first_language):
    if message.text in ['/start', '/history', '/about_dev', 'continue']:
        command_start(message)
    else:
        user_id = message.from_user.id
        second_language = message.text
        msg = bot.send_message(user_id,
                               f"""Please write your <b>text or words</b>: """,
                               reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, translate, first_language, second_language)




def translate(message: Message, first_language, second_language):
    global user_id
    if message.text in ['/start', '/history', '/about_dev']:
        command_start(message)
    else:
         user_id = message.from_user.id
         original_text = message.text
         translator = Translator()
         translated_text = translator.translate(src=first_language.split(' ')[0],
                                               dest=second_language.split(' ')[0],
                                                text=original_text).text
         bot.send_message(user_id, translated_text)


         insert_translate_history(telegram_id=user_id,
                                    src=first_language,
                                    dest=second_language,
                                    org_text=original_text,
                                    tr_text=translated_text)


         ask_first_language(message)





bot.infinity_polling()
