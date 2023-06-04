from aiogram.types import *
from loader import *

## Localization
from lang.localization import *
import data.core as core

## Keyboards
from keyboards.shipment_keyboard import create_order_type_keyboard
from keyboards.request_loc import create_request_loc

## Database handlers
from db.items import order_handler as orders
from db.user import user_handler as userh

## States
from states.order_confirmation import *


async def create_invoice(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    prices = []
    items_provider = []

    ordered_items = await orders.get_items_from_cart_by_user(user_id=user_id)
    for item in ordered_items:
        detail = {}
        final_price = item[12]

        detail['check_type'] = '1'
        detail['price'] = item[12] * 100
        detail['count'] = item[2]  ## TODO
        detail['code'] = item[6]
        detail['units'] = item[14]
        detail['vat_percent'] = item[16]
        detail['package_code'] = str(item[15])
        detail['label'] = f"{item[7]} {item[9]} {item[8]} {item[11]} {detail['count']}шт."

        items_provider.append(detail)
        prices.append(LabeledPrice(detail['label'], final_price * 100))

    await state.update_data(details=items_provider, prices=prices, status='not paid', items_obj=ordered_items)

    await bot.send_invoice(
        chat_id=message.chat.id,
        title=lcl[core.language_global]['order_payment_label'],
        description=lcl[core.language_global]['order_payment_desc'],
        provider_token=config.MERCHANT_TOKEN_LIVE,
        currency='UZS',
        prices=prices,
        start_parameter='payment_test',
        payload='test',
        provider_data=items_provider
    )


# Handling confirm order query
@dp.callback_query_handler(lambda c: c.data.startswith('confirm_order'))
async def handle_order(c: CallbackQuery):
    await orders.cache.clear()

    await OrderConfirm.type.set()

    user_id = c.message.chat.id
    await bot.send_message(chat_id=user_id, text=lcl[core.language_global]['shipment_type'],
                           reply_markup=create_order_type_keyboard(language=core.language_global))


# Handling takeaway type of shipment \\ confirm order afterchoice
@dp.message_handler(state=OrderConfirm.type)
async def handle_takeaway(message: types.Message, state: FSMContext):
    if message.text == lcl[core.language_global]['takeaway']:
        await state.update_data(type='takeaway', location='null')
        await create_invoice(message=message, state=state)
        user = userh.does_user_exist(id=message.chat.id)

        user_name = user[0]
        user_phone = user[2]

        await OrderConfirm.payment.set()
        data = await state.get_data()

        product_string = ""
        total_price = 0
        if len(data['prices']) != 0:
            for good in data['prices']:
                product_string += good.label + "\n"
                total_price = total_price + good.amount

        total_price = core.price_to_string(total_price / 100)

        # Clearing cart
        items_obj = await state.get_data()
        await orders.delete_order_after_success(user_id=message.chat.id, items=items_obj['items_obj'])

        await bot.send_message(chat_id=message.chat.id, text='Адрес, где можно забрать заказ',
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=config.GROUP_CHAT_ID,
                               text=f"*Тип заказа: *{lcl[core.language_global]['takeaway']}\n\n"
                                    f"*Товары:*\n{product_string}\n*Сумма:* {total_price} сум\n"
                                    f"*Имя заказчика:* {user_name}\n*Телефон:* +{user_phone}\n"
                                    f"*Статус:* {data['status']}",
                               parse_mode="Markdown")

    elif message.text == lcl[core.language_global]['ship']:
        await state.update_data(type='ship')

        await OrderConfirm.location.set()

        await bot.send_message(chat_id=message.chat.id,
                               text=lcl[core.language_global]['loc_req'],
                               reply_markup=create_request_loc(language=core.language_global))


@dp.message_handler(state=OrderConfirm.location, content_types=ContentType.LOCATION)
async def handle_location(message: types.Message, state: FSMContext):
    if message.location:
        await state.update_data(location=message.location)

        await OrderConfirm.payment.set()
        await create_invoice(message=message, state=state)
        user = userh.does_user_exist(id=message.chat.id)

        user_name = user[0]
        user_phone = user[2]

        await OrderConfirm.payment.set()
        data = await state.get_data()

        product_string = ""
        total_price = 0
        if len(data['prices']) != 0:
            for good in data['prices']:
                product_string += good.label + "\n"
                total_price = total_price + good.amount

        total_price = core.price_to_string(total_price / 100)

        # Clearing cart
        items_obj = await state.get_data()
        await orders.delete_order_after_success(user_id=message.chat.id, items=items_obj['items_obj'])

        await bot.send_message(chat_id=message.chat.id, text='Адрес, где можно забрать заказ',
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=config.GROUP_CHAT_ID,
                               text=f"*Тип заказа: *{lcl[core.language_global]['ship']}\n\n"
                                    f"*Товары:*\n{product_string}\n*Сумма:* {total_price} сум\n"
                                    f"*Имя заказчика:* {user_name}\n*Телефон:* +{user_phone}\n"
                                    f"*Статус:* {data['status']}",
                               parse_mode="Markdown")
        await bot.send_location(chat_id=config.GROUP_CHAT_ID,
                                longitude=message.location.longitude,
                                latitude=message.location.latitude,
                                )
    else:
        await bot.send_message(chat_id=message.chat.id, text='Пожалуйста, отправьте локацию по кнопке')


@dp.message_handler(state=OrderConfirm.payment)
# move it to successful payment, just for test for now
async def send_order_to_group(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=f"Тип доставки: {data['type']}\n")
    await bot.send_location(chat_id=config.GROUP_CHAT_ID, longitude=data['location'].longitude,
                            latitude=data['location'].latitude)


# Define the payment handler
@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")
    data = await state.get_data()
    await bot.send_message(chat_id=config.GROUP_CHAT_ID, text=data)


# Define the payment success handler
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state=OrderConfirm.payment)
async def process_successful_payment(message: SuccessfulPayment, state: FSMContext):
    await state.update_data(status='success')
    data = await state.get_data()

    await state.finish()

    invoice_payload = message.successful_payment.invoice_payload
    provider_payment_charge_id = message.successful_payment.provider_payment_charge_id
