from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.localization import *

def create_categories(language: str, categories: list, is_admin: bool):
    buttons = [[]]
    rows = []

    for cat in categories:

        if language == 'ru':
            name = cat[1]

        elif language == 'uz':
            name = cat[2]

        button = KeyboardButton(text=name)
        buttons[0].append(button)

    rows = []

    last_items_amount = len(buttons[0]) % 3

    last_row = buttons[0][(len(buttons[0]) - last_items_amount)::]
    buttons[0] = buttons[0][:(len(buttons[0]) - last_items_amount):]

    rows.append(last_row)

    

    row = []

    for button in buttons[0]:
        
        row.append(button)

        if len(row) == 3:
            rows.append(row)
            row = []

    markup = ReplyKeyboardMarkup(rows, row_width=3, resize_keyboard=True)   

    if is_admin:
        return markup

    back = KeyboardButton(text=lcl[language]['back_to_main_menu'])
    markup.add(back)    

    return markup

def create_sex_choice(language: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    women = KeyboardButton(text=lcl[language]['women'])
    men = KeyboardButton(text=lcl[language]['men'])
    back = KeyboardButton(text=lcl[language]['back_to_category'])

    markup.add(men, women)
    markup.add(back)

    return markup