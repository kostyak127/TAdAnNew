import asyncio

from telethon import events

from bot.config import BotConfig
from bot.loader import db, bot
from data.clients.all_clients import all_clients


async def on_startup(dp):
    await db.create_connect()
    await db.create_start_tables()
    for admin in BotConfig.admins:
        await bot.send_message(admin, 'бот запущен')

    client = all_clients[0]

    @client.on(events.NewMessage(chats=('@novostyrus')))
    async def normal_handler(event):
        #    print(event.message)
        print(event.message.to_dict()['message'])

if __name__ == '__main__':
    from aiogram import executor
    from bot.handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)