import logging
from io import BytesIO

from aiogram.dispatcher.filters import Text, StateFilter
from aiogram import types
from aiogram.types import CallbackQuery, InputMediaPhoto
from loader import *
from lang.localization import *

import data.core as core

## States
from states.categories import *

## Keyboards
from keyboards.choose_category import create_categories, create_sex_choice
from keyboards.menu_keyboard import create_menu
from keyboards.item_keyboard import create_item_keyboard
from keyboards.back_from_categs import create_back_from_cats

## Database handlers
from db.user import user_handler as user
from db.items import items_handler as items
from db.items import order_handler as order
from db.items import category_handler as cats


@dp.message_handler(Text('test'))
async def test(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=f"{core.language_global} - {lcl[core.language_global]['catalogue']}")


## Handling catalog request
@dp.message_handler(text=[lcl['ru']['catalogue'], lcl['uz']['catalogue']])
async def process_catalogue(message: types.Message):
    lang = await user.get_user_lang(id=message.chat.id)

    print(lang)

    categories = await cats.get_all_categories()

    await ChooseCategories.choosing_category.set()

    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['choose_category'],
                           reply_markup=create_categories(language=core.language_global, categories=categories,
                                                          is_admin=False))


## Handling back to main menu button
@dp.message_handler(Text(equals=[lcl['ru']['back_to_main_menu'], lcl['uz']['back_to_main_menu']]),
                    state=[ChooseCategories.choosing_category, ChooseCategories.choosing_item])
async def proceed_to_main_menu(message: types.Message, state: FSMContext):
    user_result = user.does_user_exist(message.from_id)
    is_admin = user_result[3] in config.ADMINS

    await state.finish()

    await bot.send_message(chat_id=message.chat.id,
                           text=f"{lcl[user_result[1]]['menu_message_1']}{user_result[0]}!\n{lcl[user_result[1]]['menu_message_2']}",
                           reply_markup=create_menu(language=user_result[1], is_admin=is_admin))


## Handling back to category choice button
@dp.message_handler(text=[lcl['ru']['back_to_category'], lcl['uz']['back_to_category']],
                    state=[ChooseCategories.choosing_sex, ChooseCategories.choosing_item,
                           ChooseCategories.choosing_category])
async def proceed_to_categories(message: types.Message):
    categs = await cats.get_all_categories()
    await ChooseCategories.choosing_category.set()

    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['choose_category'],
                           reply_markup=create_categories(core.language_global, categories=categs, is_admin=False))


@dp.message_handler(state=[ChooseCategories.choosing_sex, ChooseCategories.choosing_item])
async def handle_sex_choice(message: types.Message, state: FSMContext):
    sex = message.text

    if sex == lcl[core.language_global]['men'] or sex == lcl[core.language_global]['women']:

        sex_values = list(core.sex_dict.values())

        for index in range(0, len(sex_values)):
            localz = list(sex_values[index].values())

            if sex in localz:
                if index == 0:
                    sex = 'm'
                    break

                elif index == 1:
                    sex = 'w'
                    break

        data = await state.get_data()

        print(data)
        print(sex)
        print(data['category'][0])

        goods = await items.get_all_items_by_category_sex(sex=sex, category_id=data['category'][0])

        if len(goods) == 0:
            await ChooseCategories.choosing_category.set()
            await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['empty_category'],
                                   reply_markup=create_back_from_cats(language=core.language_global))

        else:
            await ChooseCategories.choosing_item.set()

            cur_index = 0
            cur_amount = 1

            item_id = goods[cur_index][0]
            photo = BytesIO(goods[cur_index][9])
            label = goods[cur_index][3]
            color = goods[cur_index][5]
            sex = goods[cur_index][4]
            size = goods[cur_index][7]
            price = core.price_to_string(price=goods[cur_index][8])

            await bot.send_photo(chat_id=message.chat.id, photo=photo,
                                 caption=f"*{label}*\n\n{lcl[core.language_global]['color_label']}{color}\n{lcl[core.language_global]['size_label']}{size}\n\n{lcl[core.language_global]['price_label']}{price}",
                                 parse_mode="Markdown",
                                 reply_markup=create_item_keyboard(language=core.language_global, cur_index=cur_index,
                                                                   length=len(goods), sex=sex, item_id=item_id,
                                                                   category=data['category'][3],
                                                                   cur_amount=cur_amount))

            await bot.send_message(chat_id=message.chat.id,
                                   text='Чтобы вернуться обратно в меню, воспользуйтесь клавиатурой бота',
                                   reply_markup=create_back_from_cats(language=core.language_global))


@dp.message_handler(state=[ChooseCategories.choosing_category, ChooseCategories.choosing_item])
async def handle_categories(message: types.Message, state: FSMContext):
    name = message.text

    categs = await cats.get_all_categories()
    cur_cat = 0
    flag = 0

    for cat in enumerate(categs):

        if name in cat[1][1] or name in cat[1][2]:
            cur_cat = cat
            flag = 1

            break

    if flag == 0:
        await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['wrong_input'])

    else:

        goods = await items.get_all_items_by_category_id(category_id=cur_cat[1][0])

        if len(goods) == 0:
            await ChooseCategories.choosing_category.set()
            print(core.language_global)
            await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['empty_category'],
                                   reply_markup=create_back_from_cats(language=core.language_global))

        else:
            if cur_cat[1][4]:
                await state.update_data(category=cur_cat[1])
                await ChooseCategories.choosing_sex.set()

                await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['choose_undercat'],
                                       reply_markup=create_sex_choice(language=core.language_global))

            else:
                await ChooseCategories.choosing_item.set()

                cur_index = 0
                cur_amount = 1

                item_id = goods[cur_index][0]
                photo = BytesIO(goods[cur_index][9])
                label = goods[cur_index][3]
                color = goods[cur_index][5]
                sex = goods[cur_index][4]
                size = goods[cur_index][7]
                price = core.price_to_string(price=goods[cur_index][8])

                await bot.send_photo(chat_id=message.chat.id, photo=photo,
                                     caption=f"*{label}*\n\n{lcl[core.language_global]['color_label']}{color}\n{lcl[core.language_global]['size_label']}{size}\n\n{lcl[core.language_global]['price_label']}{price}",
                                     parse_mode="Markdown",
                                     reply_markup=create_item_keyboard(language=core.language_global,
                                                                       cur_index=cur_index,
                                                                       length=len(goods), sex=sex, item_id=item_id,
                                                                       category=cur_cat[1][3],
                                                                       cur_amount=cur_amount))

                await bot.send_message(chat_id=message.chat.id,
                                       text='Чтобы вернуться обратно в меню, воспользуйтесь клавиатурой бота',
                                       reply_markup=create_back_from_cats(language=core.language_global))


@dp.callback_query_handler(lambda callback: callback.data.startswith('item_cat_'), state=ChooseCategories.choosing_item)
async def handle_next_prev(callback: CallbackQuery):
    data_split = callback.data.split("_")

    direction = data_split[3]
    cur_index = int(data_split[4])
    cur_sex = data_split[5]
    cur_category = data_split[2]
    cur_amount = data_split[6]

    category = await cats.get_category_by_name(name=cur_category)

    if category[4]:
        goods = await items.get_all_items_by_category_sex(category_id=category[0], sex=cur_sex)
    else:
        goods = await items.get_all_items_by_category_id(category_id=category[0])

    cur_item = goods[cur_index]

    length = len(goods)

    new_index = cur_index

    if direction == "prev":
        if cur_index == 0:
            cur_item = goods[length - 1]
            new_index = length - 1
        else:
            cur_item = goods[cur_index - 1]
            new_index = cur_index - 1

    if direction == "next":
        print(cur_index)
        if cur_index == length - 1:
            cur_item = goods[0]
            new_index = 0
        else:
            cur_item = goods[cur_index + 1]
            new_index = cur_index + 1

    photo = BytesIO(cur_item[9])
    name = cur_item[3]

    color = cur_item[5]
    size = cur_item[7]
    price = core.price_to_string(cur_item[8])
    item_id = cur_item[0]

    media = InputMediaPhoto(photo)

    await bot.edit_message_media(media=media, chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.edit_message_caption(chat_id=callback.message.chat.id,
                                   message_id=callback.message.message_id,
                                   parse_mode="Markdown",
                                   caption=f"*{name}*\n\n{lcl[core.language_global]['color_label']}{color}\n{lcl[core.language_global]['size_label']}{size}\n\n{lcl[core.language_global]['price_label']}{price}",
                                   reply_markup=create_item_keyboard(language=core.language_global, length=length,
                                                                     cur_index=new_index, sex=cur_sex, item_id=item_id,
                                                                     category=cur_category,
                                                                     cur_amount=cur_amount
                                                                     )
                                   )


## Handling add to cart button
@dp.callback_query_handler(lambda callback: callback.data.startswith('add_to_cart_'),
                           state=ChooseCategories.choosing_item)
async def add_to_cart(callback: CallbackQuery):
    data = callback.data.split('_')
    item_id = data[3]
    cur_amount = data[4]

    print(data)
    await order.item_to_cart(item_id=item_id, user_id=callback.message.chat.id, amount=cur_amount)
    await bot.answer_callback_query(callback_query_id=callback.id, text=lcl[core.language_global]['item_added'])


## Handling cur amount
@dp.callback_query_handler(lambda c: c.data.startswith('item_am'), state=ChooseCategories.choosing_item)
async def handle_cur_amount(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')

    cur_amount = int(data[5])
    direction = data[3]
    cur_index = int(data[4])
    cur_sex = data[6]
    cur_category = data[2]

    category = await cats.get_category_by_name(name=cur_category)

    if category[4]:
        goods = await items.get_all_items_by_category_sex(category_id=category[0], sex=cur_sex)
    else:
        goods = await items.get_all_items_by_category_id(category_id=category[0])

    cur_item = goods[cur_index]
    length = len(goods)
    new_amount = cur_amount

    item_id = cur_item[0]

    if direction == 'plus':
        new_amount = cur_amount + 1

    elif direction == 'minus':
        if cur_amount == 1:
            pass
        else:
            new_amount = cur_amount - 1

    if new_amount != cur_amount:
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            reply_markup=create_item_keyboard(language=core.language_global,
                                                                              length=length, cur_index=cur_index,
                                                                              sex=cur_sex, item_id=item_id,
                                                                              category=cur_category,
                                                                              cur_amount=new_amount)
                                            )
    else:
        pass
