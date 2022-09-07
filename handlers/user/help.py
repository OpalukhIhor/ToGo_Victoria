from aiogram.types import Message

from loader import dp


@dp.message_handler(commands='help')
async def help_command(message: Message):
    await message.answer(f"<b>{message.from_user.first_name}</b>, виникли запитання чи є цікава пропозиція?\n"
                         f"Ви можете зателефонувати нам за номером <i>0676767676</i>")
