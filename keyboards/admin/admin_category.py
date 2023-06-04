from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.localization import *

def create_admin_categories(language: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    shirts = KeyboardButton(text=lcl[language]['shirts'])
    caps = KeyboardButton(text=lcl[language]['caps'])
    ties = KeyboardButton(text=lcl[language]['ties'])

    markup.add(shirts, caps, ties)

    return markup