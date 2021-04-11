import asyncio
import sys

from telethon import events

from bot.loader import db
from data.clients.all_clients import all_clients
from data.messages.download.messages import MessageDownloader

client = all_clients[0]


async def start_client(client_):
    await db.create_connect()

    await client_.connect()
    list_channels = await db.get_channels_to_subscribe(client_number=0)
    list_channels = list(map(lambda x: x['channel_name'], list_channels))

    @client_.on(events.NewMessage(list_channels))
    async def handle_message(event):
        message = event.message.to_dict()
        # a = await event.message.download_media()

        handler = MessageDownloader(client=client_, channel_link=f't.me/{event.chat.username}')
        data = handler.handle_searched_data(message)
        await data.add_links_from_message_to_db(event.chat.username)
        await data.add_channels_from_message_to_db(event.chat.username)

    await asyncio.sleep(24*3600)
    sys.exit()

with client:
    client.loop.run_until_complete(start_client(client))