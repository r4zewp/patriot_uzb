from aiogram import types
from loader import *

## Localization
from lang.localization import *
from data.core import language_global


@dp.message_handler(text=lcl[language_global]['contact_us'])
async def about(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, 
    parse_mode='Markdown',
    text=f"{lcl[language_global]['contact_us_label']}{lcl[language_global]['instagram_label']}{lcl[language_global]['instagram']}\n"
    f"{lcl[language_global]['phone_label']}{lcl[language_global]['phone_number']}\n\n"
    f"{lcl[language_global]['website_label']}{lcl[language_global]['website']}{lcl[language_global]['website_label_two']}"
    )