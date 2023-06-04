from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

## Localization
from lang.localization import *

def create_order_type_keyboard(language: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    ship = KeyboardButton(text=lcl[language]['ship'])
    takeaway = KeyboardButton(text=lcl[language]['takeaway'])

    markup.add(takeaway, ship)

    return markup
