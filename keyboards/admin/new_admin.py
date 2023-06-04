from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_new_adm():
    markup = InlineKeyboardMarkup()

    become_adm = InlineKeyboardButton(text='Стать админом', switch_inline_query_current_chat='asd')

    markup.add(become_adm)

    return markup