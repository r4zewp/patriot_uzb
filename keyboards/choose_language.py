from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.localization import *

def create_language_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(text=lcl['ru']['lang']), KeyboardButton(text=lcl['uz']['lang']))

    return markup

