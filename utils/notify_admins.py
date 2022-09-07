import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            text = "Бот он-лайн"
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as error:
            logging.exception(error)
