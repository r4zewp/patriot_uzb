from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.localization import *

def create_admin_settings(language: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    add_item = KeyboardButton(text=lcl[language]["add_new_item"])
    add_category = KeyboardButton(text=lcl[language]['add_category'])
    back_to_menu = KeyboardButton(text=lcl[language]['back_admin'])

    ## will be added later
    remove_cat = KeyboardButton(text='Удалить категорию')

    ## add admin
    add_admin = KeyboardButton(text=lcl[language]['add_admin'])

    markup.add(add_item, add_category, add_admin)
    markup.add(back_to_menu)

    return markup