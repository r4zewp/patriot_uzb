from loader import *
from aiogram.types import *
from transliterate import translit


## Localization
from lang.localization import *
from data.core import language_global

## Keyboards
from keyboards.admin.admin_yes_no import create_yes_no
from keyboards.menu_keyboard import create_menu

## States
from states.add_category import *

## Database handlers
from db.items import category_handler as cat

@dp.message_handler(text=lcl[language_global]['add_category'])
async def handle_add_category(message: types.Message):

    await NewCategory.name_ru.set()

    await bot.send_message(chat_id=message.chat.id, text=lcl[language_global]['new_category_name_ru'])

@dp.message_handler(state=NewCategory.name_ru)
async def handle_ru_name(message: types.Message, state: FSMContext):
    name_ru = message.text
    
    await state.update_data(name_ru=name_ru)
    await NewCategory.name_uz.set()

    await bot.send_message(chat_id=message.chat.id, text=lcl[language_global]['new_category_name_uz'])

@dp.message_handler(state=NewCategory.name_uz)
async def handle_new_category_name(message: types.Message, state: FSMContext):
    name_uz = message.text

    await state.update_data(name_uz=name_uz)
    await NewCategory.isSexNeeded.set()

    await bot.send_message(chat_id=message.chat.id, text=lcl[language_global]['new_category_sex'],
    reply_markup=create_yes_no(language=language_global))

@dp.message_handler(state=NewCategory.isSexNeeded)
async def handle_new_category_sex(message: types.Message, state: FSMContext):
    text = message.text

    if text == lcl[language_global]['yes_label'] or text == lcl[language_global]['no_label']:
        answer = text == lcl[language_global]['yes_label']

        await state.update_data(is_sex_needed=answer)
        data = await state.get_data()
        await state.finish()
        
        name = translit(data['name_ru'], 'ru', reversed=True)
        data['name'] = name.lower()

        await cat.create_new_category(data=data)
        await bot.send_message(chat_id=message.chat.id, text=lcl[language_global]['new_cat_success'],
        reply_markup=create_menu(language=language_global, is_admin=True))
    else:
        await bot.send_message(chat_id=message.chat.id, text=lcl[language_global]['only_kb'])