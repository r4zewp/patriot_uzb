from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

## Localization
import data.core as core
from lang.localization import *

def create_back_from_cats(language: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    back = KeyboardButton(text=lcl[core.language_global]['back_to_category'])

    markup.add(back)

    return markup