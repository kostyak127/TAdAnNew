import asyncio
import datetime
from typing import Optional, NoReturn, List

import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool


def get_date():
    now = datetime.datetime.now()
    return str(now.year) + '-' + str(now.month) + '-' + str(now.day)


class Database:
    def __init__(self):
        """Создается база данных без подключения в loader"""

        self.pool: Optional[Pool] = None

    async def create_connect(self):
        """В этой функции создается подключение к базе"""

        pool = await asyncpg.create_pool(
            user='postgres',
            password='2KosTyA14',
            host='localhost',
            database='TAdAn',
            port=5090
        )
        self.pool = pool

    async def test_connection(self):
        try:
            await self.pool.execute('SELECT 1')
        except Exception as e:
            print(e.__class__)

    async def create_start_tables(self) -> NoReturn:
        query = """CREATE TABLE IF NOT EXISTS channel(
                    channel_id SERIAL PRIMARY KEY,
                    channel_name VARCHAR(50),
                    channel_link VARCHAR(50),
                    parse_link VARCHAR (53),
                    date_start VARCHAR(10),
                    last_message_id INT);
        
                    CREATE TABLE IF NOT EXISTS link(
                    link_id SERIAL PRIMARY KEY,
                    link_name VARCHAR (255));
                    
                    CREATE TABLE IF NOT EXISTS users(
                    user_id SERIAL PRIMARY KEY,
                    user_name VARCHAR(255),
                    user_chat_id INT,
                    user_date_start VARCHAR(10))"""
        await self.pool.execute(query)

    async def create_channel_table(self, table_name: str):
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name}(
        id SERIAL PRIMARY KEY,
        mention VARCHAR(50),
        text_message VARCHAR(2000),
        message_id INT,
        date_published VARCHAR(30),
        views INT,
        forwards INT,
        mentioning_type VARCHAR (10),
        media VARCHAR (500))
        """
        await self.pool.execute(query)

    async def add_to_channel_table(self, table_name: str, mention: str, message_id: int, date: str, mentioning_type: str,
                                   text: str = '', views: int = 0, forwards: int = 0, media: str = ''):

        query = f"""
        INSERT INTO {table_name} (mention, text_message, message_id, date_published, views, forwards, mentioning_type, media)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """
        await self.pool.execute(query, mention, text, message_id, date, views, forwards, mentioning_type, media)

    async def create_link_table(self, table_name: str):
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name}(
        id SERIAL PRIMARY KEY,
        mentioned_by VARCHAR(50),
        message_id INT)"""
        await self.pool.execute(query)

    async def add_to_links(self, link_name):
        query = 'INSERT INTO link (link_name) VALUES ($1)'
        await self.pool.execute(query, link_name)

    async def add_to_link_table(self, table_name: str, mentioned_by: str, message_id: int):
        query = f"""
        INSERT INTO {table_name} (mentioned_by, message_id)
        VALUES ($1, $2)
        """
        await self.pool.execute(query, mentioned_by, message_id)

    async def get_all_links(self) -> List[Record]:
        query = 'SELECT link_name FROM link'
        return await self.pool.fetch(query)

    async def get_all_channels(self) -> List[Record]:
        query = 'SELECT channel_name FROM channel'
        return await self.pool.fetch(query)

    async def get_mention_channel_data(self, table_name: str) -> List[Record]:
        query = f'SELECT mention, count(mention) as mention_time FROM {table_name}' \
                f' GROUP BY mention ORDER BY mention_time DESC'
        return await self.pool.fetch(query)

    async def get_mention_link_data(self, table_name: str) -> List[Record]:
        query = f'SELECT mentioned_by AS mention, count(mentioned_by) AS mention_time FROM {table_name}' \
                f' GROUP BY mention ORDER BY mention_time DESC'
        return await self.pool.fetch(query)

    async def get_channel_messages_data(self, table_name) -> List[Record]:
        query = f'SELECT text_message AS text, message_id, views, replies FROM {table_name}'
        return await self.pool.fetch(query)

    async def count_rows(self, table_name):
        sql = f'SELECT count(*) FROM {table_name}'

        return await self.pool.fetchval(sql)

    async def get_all_users(self):
        sql = 'SELECT user_chat_id FROM users'

        return await self.pool.fetch(sql)

    async def check_user(self, chat_id):
        sql = 'SELECT user_name FROM users WHERE user_chat_id=$1'

        return await self.pool.fetch(sql, chat_id)

    async def add_user(self, name: str, chat_id: int):
        sql = 'INSERT INTO users (user_chat_id, user_name, user_date_start) VALUES($1, $2, $3)'

        await self.pool.execute(sql, chat_id, name, get_date())

    async def add_to_channels(self, channel_name: str, parse_link: str, channel_link: str, last_message_id: int = 0):
        query = 'INSERT INTO channel (channel_name, parse_link, channel_link, last_message_id, date_start) VALUES ' \
                '($1, $2, $3, $4, $5)'
        await self.pool.execute(query, channel_name, parse_link, channel_link, last_message_id, get_date())

    async def get_messages_data(self, channel_name: str) -> List[Record]:
        query = f'SELECT message_id, date_published, mention, text_message, views, forwards' \
                f' FROM {channel_name} ORDER BY message_id DESC'

        return await self.pool.fetch(query)

    async def get_link_message_data(self, link_name: str):
        query = f'SELECT mentioned_by AS mention FROM {link_name.replace(".", "_dot_")}'
        all_mentions = list()
        channels = list(set([link['mention'] for link in await self.pool.fetch(query)]))
        for channel in channels:
            channel_data = list()
            query = f"""SELECT message_id, date_published, mention, text_message, views, forwards
             FROM {channel} WHERE mention = '{link_name.replace('_dot_', '.')}'"""
            
            for mention in await self.pool.fetch(query):
                channel_data.append([mention, '@' + channel])

            await asyncio.sleep(1)
            all_mentions.extend(channel_data)
            all_mentions.sort(key=lambda x: x[0]['message_id'], reverse=True)
        return all_mentions

    async def get_channels_to_subscribe(self, client_number):
        query = f'SELECT channel_name FROM channel WHERE channel_id BETWEEN {client_number*500 + 1} AND {(client_number +1) *500}'
        return await self.pool.fetch(query)