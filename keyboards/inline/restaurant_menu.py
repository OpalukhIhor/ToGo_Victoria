from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🍕🍕 Смачна піца 🍕🍕", callback_data="pizza")],
        [InlineKeyboardButton("🍣🍣 Справжні суші 🍣🍣", callback_data="sushi")],
        [InlineKeyboardButton("🍔🍔 Ситні бургери 🍔🍔", callback_data="burgers")]
    ]
)
