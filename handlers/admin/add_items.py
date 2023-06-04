from aiogram import types
from loader import *
from aiogram.types import ReplyKeyboardRemove
from io import BytesIO
import re

## Localization
from lang.localization import *
import data.core as core

## Keyboards
from keyboards.admin.admin_category import create_admin_categories
from keyboards.choose_category import create_categories
from keyboards.admin.admin_sex_keyboard import create_choose_sex
from keyboards.admin.admin_settings import create_admin_settings

## States
from states.adding_new_item.new_item_states import *

## Database handlers
from db.items import items_handler as items
from db.items import category_handler as cats


# Handling category input
@dp.message_handler(text=[lcl['ru']['add_new_item'], lcl['uz']['add_new_item']])
async def proceed_to_item_adding(message: types.Message):
    await NewItemStates.category.set()

    categories = await cats.get_all_categories()

    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_category'],
                           reply_markup=create_categories(language=core.language_global, categories=categories,
                                                          is_admin=True))


# Handling add new item choice
@dp.message_handler(state=NewItemStates.category)
async def proceed_to_name(message: types.Message, state: FSMContext):
    categories = await cats.get_all_categories()
    names = []

    for cat in categories:

        if core.language_global == 'ru':
            names.append(cat[1])

        elif core.language_global == 'uz':
            names.append(cat[2])

    if message.text in names:
        for cat in categories:
            if cat[1] == message.text or cat[2] == message.text:
                item = cat
                exit

        await state.update_data(category=item[0])
        await NewItemStates.name.set()

        await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_name'])

    else:
        await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['wrong_input'])


# Handling name insertion
@dp.message_handler(state=NewItemStates.name)
async def add_sex(message: types.Message, state: FSMContext):
    name = message.text

    await state.update_data(name=name)
    cat_id = await state.get_data('category')

    category = await cats.get_category_by_id(id=cat_id['category'])

    if category[4]:
        await NewItemStates.sex.set()
        await bot.send_message(chat_id=message.chat.id, text=[lcl['uz']['insert_sex']],
                               reply_markup=create_choose_sex(language=core.language_global))

    else:
        await NewItemStates.color.set()
        await state.update_data(sex='uni')
        await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_color'])


## Handling male sex insertion
@dp.message_handler(state=NewItemStates.sex, text=[lcl['ru']['men'], lcl['uz']['men']])
async def proceed_to_color_with_m(message: types.Message, state: FSMContext):
    sex = 'm'
    await state.update_data(sex=sex)

    await NewItemStates.color.set()
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_color'])


## Handling female sex insertion
@dp.message_handler(state=NewItemStates.sex, text=[lcl['ru']['women'], lcl['uz']['women']])
async def proceed_to_color_with_m(message: types.Message, state: FSMContext):
    sex = 'w'
    await state.update_data(sex=sex)

    await NewItemStates.color.set()
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_color'],
                           reply_markup=ReplyKeyboardRemove())


## Handling color insertion
@dp.message_handler(state=NewItemStates.color)
async def proceed_to_art(message: types.Message, state: FSMContext):
    color = message.text
    await state.update_data(color=color)

    await NewItemStates.art.set()
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_art'])


## Handling art insertion
@dp.message_handler(state=NewItemStates.art)
async def proceed_to_art(message: types.Message, state: FSMContext):
    art = message.text
    await state.update_data(art=art)

    await NewItemStates.size.set()
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_size'])


## Handling size insertion
@dp.message_handler(state=NewItemStates.size)
async def proceed_to_art(message: types.Message, state: FSMContext):
    size = message.text
    await state.update_data(size=size)

    await NewItemStates.ikpu.set()
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_ikpu'])


# Handling IKPU insertion
@dp.message_handler(state=NewItemStates.ikpu)
async def proceed_to_units_code(message: types.Message, state: FSMContext):
    ikpu = message.text
    await state.update_data(ikpu=ikpu)

    await NewItemStates.units_code.set()
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_units'])


# Handling units code insertion
@dp.message_handler(state=NewItemStates.units_code)
async def proceed_to_package_code(message: types.Message, state: FSMContext):
    units_code = message.text
    await state.update_data(units_code=units_code)

    await NewItemStates.package_code.set()
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_package'])


@dp.message_handler(state=NewItemStates.package_code)
async def proceed_to_price(message: types.Message, state: FSMContext):
    package_code = message.text
    await state.update_data(package_code=package_code)

    await NewItemStates.price.set()
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_price'])


def is_float(s):
    return bool(re.match(r"^\d+\.\d+$", s))


# Handling price
@dp.message_handler(state=NewItemStates.price)
async def proceed_to_first_photo(message: types.Message, state: FSMContext):
    passed = is_float(message.text)

    print(f'PASSED: {passed}')

    if passed:

        if message.text.find("."):
            temp = message.text.split(".")

            string = ""

            for item in temp:
                string += item

            price = int(string)

        else:
            price = int(message.text)

        await state.update_data(price=price)
        await NewItemStates.first.set()
        await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['insert_photo'])


    else:
        await bot.send_message(chat_id=message.chat.id, text="Введите корректную цену")


## Handling photo
@dp.message_handler(content_types=types.ContentType.PHOTO, state=NewItemStates.first)
async def proceed_to_second_photo(message: types.Message, state: FSMContext):
    file = BytesIO()
    await message.photo[-1].download(destination_file=file)
    photo_data = BytesIO(file.read())

    await state.update_data(first_photo=photo_data.read())
    data = await state.get_data()
    await items.create_new_item(data=data)

    await state.finish()
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['item_added'],
                           reply_markup=create_admin_settings(language=core.language_global))
