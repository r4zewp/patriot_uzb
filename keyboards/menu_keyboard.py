from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.localization import *

def create_menu(language: str, is_admin: bool):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    catalogue = KeyboardButton(text=lcl[language]['catalogue'])
    contact_us = KeyboardButton(text=lcl[language]['contact_us'])
    cart = KeyboardButton(text=lcl[language]['cart'])
    settings = KeyboardButton(text=lcl[language]['settings'])

    if is_admin:
        markup.add(catalogue, cart)
        markup.row(settings)
    else:
        markup.add(catalogue, cart)
        markup.add(contact_us)
    

    return markup