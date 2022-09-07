from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.db_api.schemas.items import Item
from states.add_items import AddItem
from data.config import ADMINS
from keyboards.inline.cancel_button import cancel_button
from loader import dp


@dp.callback_query_handler(user_id=ADMINS, text='cancel', state=AddItem)
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer("Ви вийшли з меню модератора")
    await state.reset_state()


@dp.message_handler(user_id=ADMINS, commands='add_item')
async def add_item(message: Message):
    await message.answer(f"Привіт, <b>{message.from_user.first_name}</b>!\n"
                         f"Ви зайшли як модератор. Можете додати страву.\n"
                         f"Введіть <b>ТИП</b> (наприклад, піца, суші...).\n"
                         f"Або натисніть <b>Відмінити</b>, щоб війти з режиму модератора", reply_markup=cancel_button)
    await AddItem.type.set()


@dp.message_handler(user_id=ADMINS, state=AddItem.type)
async def add_type(message: Message, state: FSMContext):
    type = message.text
    item = Item()
    item.type = type
    await message.answer(f"Введіть <b>НАЗВУ</b> страви.\n"
                         f"Або натисніть <b>Відмінити</b>, щоб війти з режиму модератора", reply_markup=cancel_button)
    await AddItem.name.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=ADMINS, state=AddItem.name)
async def add_name(message: Message, state: FSMContext):
    name = message.text
    data = await state.get_data()
    item: Item = data.get('item')
    item.name = name
    await message.answer(f"Завантажте <b>ФОТО</b> страви.\n"
                         f"Або натисніть <b>Відмінити</b>, щоб війти з режиму модератора", reply_markup=cancel_button)
    await AddItem.photo.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=ADMINS, content_types=types.ContentType.PHOTO, state=AddItem.photo)
async def add_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    item: Item = data.get('item')
    item.photo = photo
    await message.answer(f"Опишіть <b>СКЛАД</b> страви.\n"
                         f"Або натисніть <b>Відмінити</b>, щоб війти з режиму модератора", reply_markup=cancel_button)
    await AddItem.description.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=ADMINS, state=AddItem.description)
async def add_description(message: Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    item: Item = data.get('item')
    item.description = description
    await message.answer(f"Додайте <b>ЦІНУ</b> страви (лише число, наприклад, 100 або 100.50).\n"
                         f"Натисніть <b>Відмінити</b>, щоб війти з режиму модератора", reply_markup=cancel_button)
    await AddItem.price.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=ADMINS, state=AddItem.price)
async def add_price(message: Message, state: FSMContext):
    price = message.text
    data = await state.get_data()
    item: Item = data.get('item')
    item.price = price
    await message.answer_photo(photo=item.photo, caption=f"<b>Ви успішно додали страву в меню!</b>\n"
                                                         f"<b>{item.type} {item.name}:</b>\n"
                                                         f"{item.description}\n"
                                                         f"<b>Ціна:</b> {item.price} грн.")
    await message.answer(f"Та вийшли з режиму модератора.\n"
                         f"Щоб додати ще нативніть /add_item")
    await state.update_data(item=item)
    await item.create()
    await state.reset_state()
