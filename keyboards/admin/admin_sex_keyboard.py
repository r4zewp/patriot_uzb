from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.localization import *

def create_choose_sex(language: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    women = KeyboardButton(text=lcl[language]['women'])
    men = KeyboardButton(text=lcl[language]['men'])

    markup.add(men, women)

    return markup