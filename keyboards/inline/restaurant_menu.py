from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("๐๐ ะกะผะฐัะฝะฐ ะฟััะฐ ๐๐", callback_data="pizza")],
        [InlineKeyboardButton("๐ฃ๐ฃ ะกะฟัะฐะฒะถะฝั ัััั ๐ฃ๐ฃ", callback_data="sushi")],
        [InlineKeyboardButton("๐๐ ะกะธัะฝั ะฑััะณะตัะธ ๐๐", callback_data="burgers")]
    ]
)
