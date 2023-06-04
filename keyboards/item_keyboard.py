from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lang.localization import *

def create_item_keyboard(language: str, cur_index: int, length: int, sex: str, item_id: int, category: str, cur_amount: int):
    markup = InlineKeyboardMarkup()

    prev_text = "⬅"
    following_text = "➡"

    minus_text="-"
    plus_text="+"

    prev = InlineKeyboardButton(text=prev_text, callback_data=f"item_cat_{category}_prev_{cur_index}_{sex}_{cur_amount}")
    item_number = InlineKeyboardButton(text=f"{cur_index + 1}/{length}", callback_data="no_callback")
    following = InlineKeyboardButton(text=following_text, callback_data=f"item_cat_{category}_next_{cur_index}_{sex}_{cur_amount}")

    markup.add(prev, item_number, following)

    minus = InlineKeyboardButton(text=minus_text, callback_data=f"item_am_{category}_minus_{cur_index}_{cur_amount}_{sex}")
    plus = InlineKeyboardButton(text=plus_text, callback_data=f"item_am_{category}_plus_{cur_index}_{cur_amount}_{sex}")
    item_amount = InlineKeyboardButton(text=f"{cur_amount}", callback_data="no_callback_amount")

    markup.add(minus, item_amount, plus)

    cart = InlineKeyboardButton(text=lcl[language]['add_to_cart'], callback_data=f"add_to_cart_{item_id}_{cur_amount}")

    markup.add(cart)

    return markup