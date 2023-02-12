from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from configs import LANGUAGES


def generate_languages():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    for value in LANGUAGES.values():
        btn = KeyboardButton(text=value)
        buttons.append(btn)

    markup.add(*buttons)
    return markup

def ask_cont():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = ['Yes', 'No']
    markup.add(*buttons)
    return markup
