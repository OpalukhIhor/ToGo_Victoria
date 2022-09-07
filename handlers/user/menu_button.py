from aiogram.types import Message

from keyboards.inline.restaurant_menu import menu
from loader import dp


@dp.message_handler(text="📋 Меню расторану 📋")
async def menu_button(message: Message):
    await message.answer(f"<b>{message.from_user.first_name}</b>, у нас Ви точно знайдете щось на свій смак!\n",
                         reply_markup=menu)

