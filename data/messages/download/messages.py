import re
from itertools import groupby
from typing import List, Optional

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from data.messages.message_data import MessageData

LINK_FINDER = ['w{0,3}[.]?[w]{0,2}[a-zA-Z0-9_]+[.][a-z]+']
CHANNEL_FINDER = ['t[.]me+[/][a-zA-Z0-9_]+[/]?[\w]*', '@[a-zA-Z0-9_]+']


class MessageDownloader:
    def __init__(self, client: TelegramClient, channel_link: str):
        self.client = client
        self.channel_link = channel_link

    @property
    async def channel(self):
        return await self.client.get_entity(self.channel_link)

    async def download_messages(self) -> list:
        offset_msg = 0
        limit_msg = 500
        all_messages = []
        while True:
            total_count_limit = 5000
            history = await self.client(GetHistoryRequest(
                peer=await self.channel,
                offset_id=offset_msg,
                offset_date=None, add_offset=0,
                limit=limit_msg, max_id=0, min_id=0,
                hash=0))
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                all_messages.append(message.to_dict())
            offset_msg = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
        return all_messages

    def handle_searched_data(self, message):
        try:
            message_text = message.get('message')
            message_entities = message.get('entities')

            links = self.find_links_from_message_text(message_text)
            if links:
                print(links)
            channels = self.find_channels_from_message_text(message_text)

            # here find links, messages and maybe media in message_entities
            if message_entities:
                for entity in message_entities:
                    if entity['_'] == 'MessageEntityTextUrl':
                        channel = self.find_channel_from_entity(entity['url'])
                        link = self.find_link_from_entity(entity['url'])
                        if link and not link.startswith('t.me'):
                            links.append(link)
                        elif channel:
                            channels.append(channel)
            links = [el for el, _ in groupby(links)]
            channels = self.set_channels_right_format([el for el, _ in groupby(channels)])
            date_published = str(message.get('date'))[:10]

            views = message.get('views')
            forwards = message.get('forwards')


        # TODO media
            return MessageData(message_id=message['id'],
                           links=links,
                           channels=channels,
                           message_text=message_text,
                           date_published=date_published,
                           views=views,
                           forwards=forwards,
                           media=None)  # add media to init

        except Exception as e:
            print(e)

    @staticmethod
    # re find all links from messages than check that not t.me because t.me is a channel, not link
    def find_links_from_message_text(message_text: str) -> List[str]:
        try:
            links = [link for link in re.findall(LINK_FINDER[0], message_text) if link != 't.me']
            links = list(map(lambda item: item[4:] if item.startswith('www.') else item, links))
        except TypeError:
            return []
        return links

    @staticmethod
    def find_channels_from_message_text(message_text: str) -> List[str]:
        try:
            # here re find all channel links and channels like @channel_name or t.me/channel_name
            channels = [channel for channel in re.findall(CHANNEL_FINDER[0], message_text)]
            channels.extend([channel[1:] for channel in re.findall(CHANNEL_FINDER[1], message_text)])
            return channels
        except TypeError:
            return []

    @staticmethod
    def set_channels_right_format(channels: List[str]) -> List[str]:
        # write to db and work with channel without @ and with channels t.me/joinchat/AAA44
        # REMOVE t.me from channels like t.me/channel_name
        for i, channel in enumerate(channels):
            if channel.startswith('t.me/joinchat'):
                pass
            elif channel.startswith('t.me/'):
                channels[i] = channel.split('/')[1]
            elif channel.startswith('www.'):
                channel[i] = channel[i][4:]
        return channels

    @staticmethod
    def find_channel_from_entity(string: str) -> Optional[str]:
        res = re.findall(CHANNEL_FINDER[0], string)
        return res[0] if res else None

    @staticmethod
    def find_link_from_entity(string: str) -> Optional[str]:
        res = re.findall(LINK_FINDER[0], string)
        if res and res[0].startswith('www.'):
            res[0] = res[0][4:]
        return res[0] if res else None