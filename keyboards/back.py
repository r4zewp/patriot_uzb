from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.localization import *

def create_back_button(language: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back = KeyboardButton(text=lcl[language]['back'])
    markup.add(back)

    return markup