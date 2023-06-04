from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.localization import  *

def create_phone_keyboard(language: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    button = KeyboardButton(text=lcl[language]['complete_phone'], request_contact=True)
    # back = KeyboardButton(text=lcl[language]['back'])
    markup.add(button)

    return markup