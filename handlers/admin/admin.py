from aiogram import types
from loader import *

## Localization
from lang.localization import *
from app import send_welcome
import data.core as core

## States
from states.adding_admin import *

## Keyboards
from keyboards.admin.admin_settings import create_admin_settings
from keyboards.admin.new_admin import create_new_adm

## Handlers
from db.user import user_handler as us


## Handling admin button
@dp.message_handler(text=[lcl['ru']['settings'], lcl['uz']['settings']])
async def proceed_to_admin_settings(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['menu_message_2'],
    reply_markup=create_admin_settings(core.language_global))

## Handling back admin menu button
@dp.message_handler(text=[lcl['ru']["back_admin"], lcl['uz']["back_admin"]])
async def back_admin(message: types.Message):
    await send_welcome(message=message)

@dp.message_handler(text=[lcl['ru']['add_admin'], lcl['uz']['add_admin']])
async def add_admin(message: types.Message):
    await AddingAdmin.fwd_message.set()
    await bot.send_message(chat_id=message.chat.id, text=lcl[core.language_global]['resend_mes'],
                           parse_mode='Markdown')

@dp.message_handler(state=AddingAdmin.fwd_message)
async def proceed_fwd_message(message: types.Message, state: FSMContext):

    if message.forward_from is not None:
        is_alrd_user = us.does_user_exist(id=message.forward_from.id)

        if is_alrd_user:
            res = us.make_user_admin(id=message.forward_from.id)
            if res:
                await state.finish()
                await bot.send_message(chat_id=message.chat.id, text='Пользователь успешно стал админом!')
            else:
                await state.finish()
                await bot.send_message(chat_id=message.chat.id, text='Произошла непредвиденная ошибка, попробуйте позже.')
        else:
            await bot.send_message(chat_id=message.chat.id, text='Попросите пользователя зарегистрироваться и попробуйте снова')
            await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id, text='Пожалуйста, попробуйте переотправить сообщение заново')

