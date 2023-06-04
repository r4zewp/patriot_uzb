from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lang.localization import *


def create_cart_keyboard(language: str, cur_index: int, length: int, item_id: int, user_id: int, amount: int):
    markup = InlineKeyboardMarkup()

    prev_text = "⬅"
    following_text = "➡"

    prev = InlineKeyboardButton(text=prev_text, callback_data=f"item_cart_prev_{cur_index}_{amount}")
    item_number = InlineKeyboardButton(text=f"{cur_index + 1}/{length}", callback_data="no_callback")
    following = InlineKeyboardButton(text=following_text, callback_data=f"item_cart_next_{cur_index}_{amount}")

    markup.add(prev, item_number, following)

    delete = InlineKeyboardButton(text=lcl[language]['delete_item'], callback_data=f"delete_item_{item_id}_{amount}")

    markup.add(delete)

    confirm = InlineKeyboardButton(text=lcl[language]['confirm_order'], callback_data=f"confirm_order_{user_id}")
    
    markup.add(confirm)

    return markup
