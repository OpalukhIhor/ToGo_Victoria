from aiogram.types import Message

from keyboards.default.start import start_keyboard
from loader import dp


@dp.message_handler(commands='start')
async def start_command(message: Message):
    await message.answer(f"Привіт, <b>{message.from_user.first_name}</b>!\n"
                         f"Вас вітає ресторан <i><b>ВІКТОРІЯ</b></i>.\n"
                         f"У нас Ви зможете замовити смачні страви на різний смак",
                         reply_markup=start_keyboard)
