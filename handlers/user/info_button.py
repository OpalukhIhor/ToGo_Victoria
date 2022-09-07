from aiogram.types import Message

from keyboards.default.start import start_keyboard
from loader import dp


@dp.message_handler(text="ℹ️ Інформація про нас ℹ️")
async def info_button(message: Message):
    await message.answer(f"<b>{message.from_user.first_name}</b>, ми працюємо для Вас\n"
                         f"<b>щодня з 10:00 до 22:00</b>\n"
                         f"за адресою <b>вул.Умовна, 1</b>",
                         reply_markup=start_keyboard)
