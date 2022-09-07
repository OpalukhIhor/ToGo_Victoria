async def on_startup(dp):
    from utils.notify_admins import on_startup_notify

    await on_startup_notify(dp)

    print('Bot is on-line')

    from utils.set_bot_commands import set_default_commands

    await set_default_commands(dp)

    from utils.db_api.database import create_db

    await create_db()

    print('Connected to database')


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
