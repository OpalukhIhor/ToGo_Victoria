# from asyncio import sleep
# from datetime import datetime
#
# from aiogram.dispatcher import FSMContext
# from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
# from aiogram.utils.callback_data import CallbackData
#
# from keyboards.inline.order_button import order_buttons
# from loader import dp
# from states.test_order import TestOrder
# from utils.db_api.commands import DBCommands
# from utils.db_api.schemas.items import Item
# from utils.db_api.schemas.test_order import BuyingOrder
#
# db = DBCommands()
#
# order_item = CallbackData('order', 'name')
#
#
# @dp.callback_query_handler(text='pizza')
# async def show_pizza(call: CallbackQuery):
#     pizza_list = await db.show_pizza()
#     for item in pizza_list:
#         text = f"<b>{item.type} {item.name}:</b>\n" \
#                f"<b>Склад:</b> {item.description}\n" \
#                f"<b>Ціна:</b> {item.price} грн."
#         order_button = InlineKeyboardMarkup(inline_keyboard=[
#             [InlineKeyboardButton(text="Замовити", callback_data=order_item.new(name=item.name))]
#         ])
#         await call.message.answer_photo(photo=item.photo,
#                                         caption=text.format(type=item.type,
#                                                             name=item.name,
#                                                             description=item.description,
#                                                             price=item.price), reply_markup=order_button)
#         await sleep(0.3)
#
#
# @dp.callback_query_handler(text='sushi')
# async def show_sushi(call: CallbackQuery):
#     sushi_list = await db.show_sushi()
#     for item in sushi_list:
#         text = f"<b>{item.type} {item.name}:</b>\n" \
#                f"<b>Склад:</b> {item.description}\n" \
#                f"<b>Ціна:</b> {item.price} грн."
#         order_button = InlineKeyboardMarkup(inline_keyboard=[
#             [InlineKeyboardButton(text="Замовити", callback_data=order_item.new(name=item.name))]
#         ])
#         await call.message.answer_photo(photo=item.photo,
#                                         caption=text.format(type=item.type,
#                                                             name=item.name,
#                                                             description=item.description,
#                                                             price=item.price), reply_markup=order_button)
#         await sleep(0.3)
#
#
# @dp.callback_query_handler(text='burgers')
# async def order_burgers(call: CallbackQuery):
#     burgers_list = await db.show_burgers()
#     for item in burgers_list:
#         text = f"<b>{item.type} {item.name}:</b>\n" \
#                f"<b>Склад:</b> {item.description}\n" \
#                f"<b>Ціна:</b> {item.price} грн."
#         order_button = InlineKeyboardMarkup(inline_keyboard=[
#             [InlineKeyboardButton(text="Замовити", callback_data=order_item.new(name=item.name))]
#         ])
#         await call.message.answer_photo(photo=item.photo,
#                                         caption=text.format(type=item.type,
#                                                             name=item.name,
#                                                             description=item.description,
#                                                             price=item.price), reply_markup=order_button)
#         await sleep(0.3)
#
#
# @dp.callback_query_handler(order_item.filter())
# async def order_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
#     name = callback_data.get('name')
#     await call.message.edit_reply_markup()
#     item = await Item.get(name)
#     if not item:
#         await call.message.answer("Такої страви немає")
#         return
#     text = f"Ви хочете замовити:\n" \
#            f"<b>{item.type} {item.name}</b>\n" \
#            f"<b>Ціна: </b> {item.price} грн.\n" \
#            f"<u>Введіть кількість</u>:"
#     await call.message.answer(text)
#     await TestOrder.quantity.set()
#     await state.update_data(item=item, order=BuyingOrder(name=name,
#                                                          order_time=datetime.datetime.now()))
#
#
# @dp.message_handler(regexp=r"^(\d+)$", state=TestOrder.quantity)
# async def test_order_quantity(message: Message, state: FSMContext):
#     quantity = int(message.text)
#     async with state.proxy() as data:
#         data['order'].quantity = quantity
#         item = data['item']
#         amount = int(item.price) * int(quantity)
#         data['order'].amount = amount
#         await message.answer(f"<b>Ваше замовлення:</b> {item.type} {item.name} <b><u>{quantity}шт</u></b>.\n"
#                              f"<b>До оплати:</b> {amount} грн.", reply_markup=order_buttons)
#         await TestOrder.status.set()
#
#         @dp.message_handler(state=TestOrder.quantity)
#         async def wrong_quantity(message: Message):
#             await message.answer(f"Ви ввели не число")
#
#         @dp.callback_query_handler(text='cancel', state=TestOrder)
#         async def cancel_order(call: CallbackQuery, state: FSMContext):
#             await call.message.edit_reply_markup()
#             await call.message.answer("Замовлення відмінено")
#             await state.reset_state()
#
#         @dp.callback_query_handler(text_contains='change', state=TestOrder.status)
#         async def change_order(call: CallbackQuery, state: FSMContext):
#             await call.message.edit_reply_markup()
#             await call.message.answer("Ще раз введіть кількість")
#             await TestOrder.quantity.set()
#
#         @dp.callback_query_handler(text_contains='add', state=TestOrder)
#         async def add_more_items(call: CallbackQuery, state: FSMContext):
#             await call.message.edit_reply_markup()
#             await call.message.answer("Доповнити замовлення")
#             await TestOrder.quantity.set()
#
#         @dp.callback_query_handler(text_contains='agree', state=TestOrder.status)
#         async def agree_order(call: CallbackQuery, state: FSMContext):
#             await call.message.edit_reply_markup()
#             data = await state.get_data()
#             order = data.get('order')
#             item = data.get('item')
#
#             await order.create()
#             await call.message.answer("Замовлення прийнято.")
