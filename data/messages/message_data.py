from typing import List

from bot.loader import db


class MessageData:
    def __init__(self, message_id: int, links: List[str], channels: List[str], message_text: str,
                 date_published: str, views: int, forwards: int, media: dict = None):
        self.message_id = message_id
        self.date_published = date_published
        self.links = links
        self.views = views if views else 0
        self.forwards = forwards if forwards else 0
        self.channels = channels
        self.message_text = message_text or ' '
        self.media = media or ' '

    async def add_channels_from_message_to_db(self, channel_name):
        for channel in self.channels:
            try:
                await db.add_to_channel_table(
                    table_name=channel_name,
                    mention=channel,
                    message_id=self.message_id,
                    date=self.date_published,
                    mentioning_type='channel',
                    text=self.message_text,
                    views=self.views,
                    forwards=self.forwards,
                    media=self.media
                )
            except Exception as e:
                print(e.__class__)
                print(channel)

    async def add_links_from_message_to_db(self, channel_name):
        all_links = [item['link_name'] for item in await db.get_all_links()]

        for link in self.links:
            try:
                print(link)
                if link not in all_links:
                    await db.create_link_table(link.replace('.', '_dot_'))
                    await db.add_to_links(link)
                    all_links.append(link)

                await db.add_to_link_table(link.replace('.', '_dot_'), channel_name, self.message_id)
                await db.add_to_channel_table(table_name=channel_name,
                                              mention=link,
                                              message_id=self.message_id,
                                              date=self.date_published,
                                              mentioning_type='link',
                                              text=self.message_text,
                                              views=self.views,
                                              forwards=self.forwards,
                                              media=self.media)
            except Exception as e:
                print(e.__class__)
                print(link)
