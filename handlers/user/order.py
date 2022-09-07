from asyncio import sleep

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.callback_data import CallbackData

from keyboards.default.phone_number import phone_number
from keyboards.inline.order_button import order_buttons
from keyboards.inline.restaurant_menu import menu
from loader import dp
from states.order_items import OrderItems
from utils.db_api.commands import DBCommands
from utils.db_api.schemas.items import Item
from utils.db_api.schemas.orders import Order

db = DBCommands()

order_item = CallbackData('order', 'name')


@dp.callback_query_handler(text='pizza')
async def order_pizza(call: CallbackQuery):
    pizza_list = await db.show_pizza()
    for item in pizza_list:
        text = f"<b>{item.type} {item.name}:</b>\n" \
               f"<b>Склад:</b> {item.description}\n" \
               f"<b>Ціна:</b> {item.price} грн."
        order_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Замовити",
                                         callback_data=order_item.new(name=item.name))
                ]
            ]
        )
        await call.message.answer_photo(photo=item.photo,
                                        caption=text.format(type=item.type,
                                                            name=item.name,
                                                            description=item.description,
                                                            price=item.price), reply_markup=order_button)
        await sleep(0.3)


@dp.callback_query_handler(text='sushi')
async def order_pizza(call: CallbackQuery):
    sushi_list = await db.show_sushi()
    for item in sushi_list:
        text = f"<b>{item.type} {item.name}:</b>\n" \
               f"<b>Склад:</b> {item.description}\n" \
               f"<b>Ціна:</b> {item.price} грн."
        order_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Замовити",
                                         callback_data=order_item.new(name=item.name))
                ]
            ]
        )
        await call.message.answer_photo(photo=item.photo,
                                        caption=text.format(type=item.type,
                                                            name=item.name,
                                                            description=item.description,
                                                            price=item.price), reply_markup=order_button)
        await sleep(0.3)


@dp.callback_query_handler(text='burgers')
async def order_burgers(call: CallbackQuery):
    burgers_list = await db.show_burgers()
    for item in burgers_list:
        text = f"<b>{item.type} {item.name}:</b>\n" \
               f"<b>Склад:</b> {item.description}\n" \
               f"<b>Ціна:</b> {item.price} грн."
        order_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Замовити",
                                         callback_data=order_item.new(name=item.name))
                ]
            ]
        )
        await call.message.answer_photo(photo=item.photo,
                                        caption=text.format(type=item.type,
                                                            name=item.name,
                                                            description=item.description,
                                                            price=item.price), reply_markup=order_button)
        await sleep(0.3)


@dp.callback_query_handler(order_item.filter())
async def ordering_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
    name = callback_data.get('name')
    await call.message.edit_reply_markup()
    item = await Item.get(name)
    if not item:
        await call.message.answer("Такої страви немає")
        return
    text = f"Ви хочете замовити:\n" \
           f"<b>{item.type} {item.name}</b>\n" \
           f"<b>Ціна: </b> {item.price} грн.\n" \
           f"Введіть кількість:"
    await call.message.answer(text)
    await OrderItems.quantity.set()
    await state.update_data(item=item, order=Order(name=name))


@dp.message_handler(regexp=r"^(\d+)$", state=OrderItems.quantity)
async def order_quantity(message: Message, state: FSMContext):
    quantity = int(message.text)
    async with state.proxy() as data:
        data['order'].user_id = message.from_user.id
        data['order'].user_name = message.from_user.full_name
        data['order'].quantity = quantity
        item = data['item']
        amount = int(item.price) * int(quantity)
        data['order'].amount = amount
        await message.answer(f"<b>Ваше замовлення:</b> {item.type} {item.name} <b><u>{quantity}шт</u></b>.\n"
                             f"<b>До оплати:</b> {amount} грн.", reply_markup=order_buttons)
        await OrderItems.status.set()

    @dp.message_handler(state=OrderItems.quantity)
    async def wrong_quantity(message: Message):
        await message.answer("Ви ввели не число. Введіть ціле число")

    @dp.callback_query_handler(text_contains='cancel', state=OrderItems)
    async def cancel_order(call: CallbackQuery, state: FSMContext):
        await call.message.edit_reply_markup()
        await call.message.answer("Замовлення відмінено")
        await state.reset_state()

    @dp.callback_query_handler(text_contains='change', state=OrderItems.status)
    async def change_order(call: CallbackQuery, state: FSMContext):
        await call.message.edit_reply_markup()
        await call.message.answer("Ще раз введіть кількість")
        await OrderItems.quantity.set()

    @dp.callback_query_handler(text_contains='agree', state=OrderItems.status)
    async def agree_order(call: CallbackQuery, state: FSMContext):
        await call.message.edit_reply_markup()
        data = await state.get_data()
        order = data.get('order')
        item = data.get('item')
        user_id = data.get('user_id')
        user_name = data.get('user_name')
        await order.create()
        await call.message.answer(f"Підтверджено! Бажаєте замовити ще щось смачненьке?", reply_markup=menu)
        await call.message.answer("Завершили замовлення?\n"
                                  "Тоді залиште, будь-ласка, свій номер телефону, щоб ми могли Вам зателефонувати, "
                                  "коли все буде готове.\n"
                                  "<b>Смачного!</b>   І до зустрічі!", reply_markup=phone_number)
        await state.reset_state()


