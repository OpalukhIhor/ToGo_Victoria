from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ℹ️ Інформація про нас ℹ️")
        ],
        [
            KeyboardButton(text="📋 Меню расторану 📋")
        ]
    ], resize_keyboard=True
)
