import logging
from data import config
from aiogram import types, executor
from loader import *

## Handlers
import handlers.user.catalogue as catalog
import handlers.user.cart
import handlers.user.contact_us
import handlers.admin.admin
import handlers.admin.add_items
import handlers.user.order
import handlers.admin.add_category

## Localization
import data.core as core

## Keyboards
from keyboards.choose_language import create_language_markup
from keyboards.back import create_back_button
from keyboards.complete_phone import create_phone_keyboard
from keyboards.menu_keyboard import create_menu

## Localization
from lang.localization import *

## States
from states.users_creation.users_creation_state import *

## Memory
from db.db import *

## DB handlers
from db.user import user_handler as user


# Handling /start command & adding new user
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await cache.clear()

    user_result = user.does_user_exist(message.from_id)
    if user_result is not None:
        is_admin = user_result[4]
        core.set_language(user_result[1])

        await bot.send_message(chat_id=message.chat.id,
                               text=f"{lcl[user_result[1]]['menu_message_1']}{user_result[0]}!\n{lcl[user_result[1]]['menu_message_2']}",
                               reply_markup=create_menu(language=user_result[1], is_admin=is_admin))
    else:

        welcome_message = f"{lcl['ru']['greetings']}\n\n{lcl['ru']['choose_lang']}"

        await UserCreationState.lang.set()

        await bot.send_message(chat_id=message.chat.id, text=welcome_message,
                               reply_markup=create_language_markup())


### Handling language choice
@dp.message_handler(state=UserCreationState.lang)
async def process_lang(message: types.Message, state: FSMContext):
    language = message.text

    global language_global
    if language == lcl['ru']['lang']:
        core.set_language(language='ru')
        print(core.language_global)


    elif language == lcl['uz']['lang']:
        core.set_language(language='uz')
        print(core.language_global)

    await state.update_data(language=core.language_global, prev_state='lang')
    await UserCreationState.name.set()

    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['complete_name'],
                           reply_markup=create_back_button(language=core.language_global))


## TODO: needs to be usable
## Handling back to name from phone number sending
async def handle_back_to_name(message: types.Message, state: FSMContext, language: str):
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['complete_name'],
                           reply_markup=create_back_button(language=core.language_global))


## Handling 'back' from name to language
async def handle_back(message: types.Message, state: FSMContext):
    data = await state.get_data()
    prev_state = data.get('prev_state')
    if prev_state == 'lang':
        await state.set_state(prev_state)
        await send_welcome(message)
    elif prev_state == 'name':
        await state.set_state(prev_state)
        data = await state.get_data()
        language = data['language']
        await handle_back_to_name(message, state, core.language_global)


## Handling phone number completion
@dp.message_handler(state=UserCreationState.name)
async def process_phone(message: types.Message, state: FSMContext):
    if message.text == lcl['ru']['back'] or message.text == lcl['uz']['back']:
        await handle_back(message, state)
    else:
        name = message.text

        await state.update_data(name=name, prev_state='name')
        await UserCreationState.phone.set()

        data = await state.get_data('language')
        language = data['language']

        await bot.send_message(chat_id=message.chat.id, text=lcl[language]['complete_phone'],
                               reply_markup=create_phone_keyboard(language=language))


### Handling finishing form fulfillment
@dp.message_handler(state=UserCreationState.phone, content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
async def complete_user_creation(message: types.Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
        await state.update_data(phone=phone, prev_state='phone', id=message.from_id)

        data = await state.get_data()
        data['is_admin'] = 0
        user.create_new_user(data=data)
        is_admin = message.chat.id in config.ADMINS

        await state.finish()
        await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['welcome'],
                               parse_mode='Markdown',
                               reply_markup=create_menu(language=core.language_global, is_admin=is_admin))
    else:
        await bot.send_message(chat_id=message.chat.id, text='Please, send a contact')


### WEBHOOK SETTINGS
async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()

    await bot.delete_webhook()
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown():
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)

    # executor.start_webhook(
    #         dispatcher=dp,
    #         webhook_path=config.WEBHOOK_PATH,
    #         on_startup=on_startup,
    #         on_shutdown=on_shutdown,
    #         skip_updates=True,
    #         host="localhost",
    #         port="8443",
    #     )

    # executor.start_polling(dp, skip_updates=True)
