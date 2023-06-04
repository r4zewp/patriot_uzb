from aiogram import types
from loader import *
from aiogram.types import CallbackQuery, InputMediaPhoto
from io import BytesIO

## Localization
from lang.localization import *
import data.core as core

## Keyboards
from keyboards.cart_keyboard import create_cart_keyboard
from keyboards.menu_keyboard import create_menu

## Database handlers
from db.items import order_handler as order
from db.items import category_handler as cats


## Handling cart
@dp.message_handler(text=[lcl['ru']['cart'], lcl['uz']['cart']])
async def display_cart(message: types.Message):
    cur_index = 0
    goods = await order.get_items_from_cart_by_user(user_id=message.chat.id)
    length = len(goods)



    if length != 0:
        cur_item = goods[cur_index]

        amount = cur_item[2]
        item_id = cur_item[0]
        photo = cur_item[13]
        name = cur_item[7]

        category_obj = await cats.get_category_by_id(id=cur_item[5])

        print(goods)

        category = ''

        if core.language_global == 'ru':
            category = category_obj[1]
        else:
            category = category_obj[2]

        color = cur_item[9]
        size = cur_item[11]
        price = core.price_to_string(cur_item[12])

        await bot.send_message(chat_id=message.chat.id,
                               parse_mode='Markdown',
                               text='*Your current items in cart*')

        await bot.send_photo(chat_id=message.chat.id,
                             parse_mode='Markdown',
                             photo=photo,
                             reply_markup=create_cart_keyboard(language=core.language_global, cur_index=0,
                                                               length=length, item_id=item_id, user_id=message.chat.id,
                                                               amount=amount),
                             caption=f"*{name}*\n\n{lcl[core.language_global]['category_label']}{category}\n{lcl[core.language_global]['color_label']}{color}\n{lcl[core.language_global]['size_label']}{size}\n\n{lcl[core.language_global]['price_label']}{price}"
                                     f"\nКоличество: {amount}")
    else:
        await bot.send_message(text=lcl[core.language_global]['empty_category'], chat_id=message.chat.id)


@dp.callback_query_handler(lambda c: c.data.startswith('item_cart_'))
async def handle_cart_kb(c: CallbackQuery):
    data_splitted = c.data.split('_')

    print(data_splitted)

    direction = data_splitted[2]
    cur_index = int(data_splitted[3])
    cur_amount = int(data_splitted[4])

    goods = await order.get_items_from_cart_by_user(user_id=c.message.chat.id)
    items_count = len(goods)

    if items_count != 0:
        new_index = cur_index

        if direction == 'prev':
            if cur_index == 0:
                new_index = items_count - 1
                cur_item = goods[new_index]
            else:
                new_index = cur_index - 1
                cur_item = goods[new_index]
        if direction == 'next':
            if cur_index == items_count - 1:
                new_index = 0
                cur_item = goods[0]
            else:
                new_index = cur_index + 1
                cur_item = goods[new_index]

        item_id = cur_item[0]
        photo = BytesIO(cur_item[13])
        name = cur_item[7]
        category = cur_item[5]
        color = cur_item[9]
        size = cur_item[11]
        price = cur_item[12]
        cur_amount = cur_item[2]

        media = InputMediaPhoto(photo)

        await bot.edit_message_media(media=media, message_id=c.message.message_id, chat_id=c.message.chat.id)
        await bot.edit_message_caption(message_id=c.message.message_id, chat_id=c.message.chat.id,
                                       parse_mode='Markdown',
                                       reply_markup=create_cart_keyboard(language=core.language_global,
                                                                         cur_index=new_index, length=items_count,
                                                                         item_id=item_id, user_id=c.message.chat.id,
                                                                         amount=cur_amount),
                                       caption=f"*{name}*\n\n{lcl[core.language_global]['category_label']}{category}\n{lcl[core.language_global]['color_label']}{color}\n{lcl[core.language_global]['size_label']}{size}\n\n{lcl[core.language_global]['price_label']}{price}"
                                               f"\n*Количество: *{cur_amount}", )
    else:
        await bot.send_message(text=lcl[core.language_global]['empty_category'], chat_id=c.message.chat.id)


## HANDLING DELETE ITEM FROM CART QUERY
@dp.callback_query_handler(lambda c: c.data.startswith('delete_item'))
async def handle_delete(c: CallbackQuery):
    data_splitted = c.data.split('_')
    item_to_delete = data_splitted[2]
    item_am = data_splitted[3]

    await order.delete_item_from_cart(user_id=c.message.chat.id, item_id=item_to_delete)
    await bot.delete_message(message_id=c.message.message_id, chat_id=c.message.chat.id)
    await bot.delete_message(message_id=c.message.message_id - 1, chat_id=c.message.chat.id)

    items_left = await order.get_items_from_cart_by_user(user_id=c.message.chat.id)
    length = len(items_left)

    await bot.answer_callback_query(callback_query_id=c.id, text=lcl[core.language_global]['item_deleted_cart'])

    if length != 0:
        cur_item = items_left[0]

        item_id = cur_item[0]
        photo = cur_item[13]
        name = cur_item[7]
        category = cur_item[5]
        color = cur_item[9]
        size = cur_item[11]
        price = core.price_to_string(cur_item[12])

        await bot.send_message(chat_id=c.message.chat.id,
                               parse_mode='Markdown',
                               text='*Your current items in cart*')

        await bot.send_photo(chat_id=c.message.chat.id,
                             parse_mode='Markdown',
                             photo=photo,
                             reply_markup=create_cart_keyboard(language=core.language_global, cur_index=0,
                                                               length=length, item_id=item_id,
                                                               user_id=c.message.chat.id,
                                                               amount=item_am),
                             caption=f"*{name}*\n\n{lcl[core.language_global]['category_label']}{category}\n{lcl[core.language_global]['color_label']}{color}\n{lcl[core.language_global]['size_label']}{size}\n\n{lcl[core.language_global]['price_label']}{price}")
    else:
        await bot.send_message(text=lcl[core.language_global]['empty_category'], chat_id=c.message.chat.id,
                               reply_markup=create_menu(language=core.language_global,
                                                        is_admin=c.message.chat.id in config.ADMINS))
