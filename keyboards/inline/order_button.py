from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

order_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✔ Підтвердити ✔", callback_data='agree')],
        [InlineKeyboardButton(text="❌ Відмінити замовлення ❌", callback_data='cancel')],
        [InlineKeyboardButton(text="🔁 Ввести кількість ще раз 🔁", callback_data='change')],
    ])
