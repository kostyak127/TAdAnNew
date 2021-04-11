from random import randint
from typing import List

from telethon import TelegramClient
from telethon.errors import FloodWaitError

from bot.loader import db, bot
from data.messages.save.message import ChannelSaver
from data.show.channel_data import ChannelShower


class Channel:
    def __init__(self, channel_name: str, clients: List[TelegramClient]):
        self.channel_name = channel_name
        self.parse_link = f't.me/s/{self.channel_name}'
        self.link = f't.me/{self.channel_name}'
        self.client = clients[randint(0, len(clients) - 1)]
        self.saver = ChannelSaver(self.client, self.channel_name)
        self.shower = ChannelShower(self.channel_name)

    async def get_channel_data(self, user_id: int) -> str:
        try:
            await self.client.connect()

            channels = [item['channel_name'] for item in await db.get_all_channels()]
            if self.channel_name not in channels:
                await bot.send_message(user_id, 'Запрос отправлен. Ожидайте результат в течении нескольких секунд')
                await db.create_channel_table(self.channel_name)

                # this method save all messages and return last_message_id
                last_message_id = await self.saver.save_downloaded_channels()
                await db.add_to_channels(channel_name=self.channel_name,
                                         parse_link=self.parse_link,
                                         channel_link=self.link,
                                         last_message_id=last_message_id)

            await self.client.disconnect()

            return await self.shower.show_channel_mention_data()
        except FloodWaitError:
            await self.client.disconnect()
            await bot.send_message(f'suka zabanili {self.client.get_me()}', -1001263798812)
            raise FloodWaitError