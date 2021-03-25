from telethon import TelegramClient

from data.messages.download.messages import MessageDownloader


class ChannelSaver:
    def __init__(self, client: TelegramClient, channel_name: str):
        self.client = client
        self.channel_name = channel_name
        self.channel_link = f't.me/{self.channel_name}'
        self.downloader = MessageDownloader(self.client, self.channel_link)

    async def get_messages(self):
        return await self.downloader.download_messages()

    @staticmethod
    def get_last_message_id(messages: list):
        return messages[0].get('id')

    async def save_downloaded_channels(self) -> int:
        messages = await self.get_messages()
        last_message_id = self.get_last_message_id(messages)
        for message in messages:
            message_data = self.downloader.handle_searched_data(message)
            await message_data.add_channels_from_message_to_db(self.channel_name)
            await message_data.add_links_from_message_to_db(self.channel_name)

        return last_message_id