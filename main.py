import requests
from bot.config import BotConfig
from bot.loader import db, bot


async def on_startup(dp):
    requests.post('http://127.0.0.1:8000/connect_to_db', data={
        'password': 'my_passworD',
    })
    await db.create_connect()
    await db.create_start_tables()
    for admin in BotConfig.admins:
        await bot.send_message(admin, 'бот запущен')

if __name__ == '__main__':
    from aiogram import executor
    from bot.handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)