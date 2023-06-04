from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.localization import *

def create_request_loc(language: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    text = 'Поделиться геолокацией'
    loc = KeyboardButton(text=text, request_location=True)

    markup.add(loc)

    return markup
    