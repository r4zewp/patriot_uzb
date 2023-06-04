from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.localization import *

def create_yes_no(language: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton(text=lcl[language]['yes_label'])
    no = KeyboardButton(text=lcl[language]['no_label'])

    markup.add(no, yes)

    return markup