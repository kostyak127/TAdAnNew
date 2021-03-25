import csv
from typing import List

from asyncpg import Record

from bot.loader import db
from web.config import WebConfig


class ChannelShower:
    def __init__(self, channel_name):
        self.channel_name = channel_name

    async def show_channel_mention_data(self) -> str:
        data = self.set_channel_mention_data_format(await db.get_mention_channel_data(self.channel_name))
        if len(data) > 30:
            with open(f'{self.channel_name}_data.csv', 'w', newline="", encoding='cp1251') as outfile:
                columns = ['Имя канала/Сылка', 'Количество упоминаний']
                writer = csv.writer(outfile, delimiter=';')
                writer.writerow(columns)
                writer.writerows(data)
                result = f'{self.channel_name}_data.csv'
        elif len(data) != 0:
            result = f'В канале <b>@{self.channel_name}</b> упоминались:\n'
            for key in data:
                result += f'<b>{key[0]} {key[1]}</b> {self.get_number_format(key[1])}\n'
        else:
            result = f'Нет данных об упоминаниях {self.channel_name}'

        return result

    @staticmethod
    def set_channel_mention_data_format(data: List[Record]) -> list:
        correct_data = list()
        for item in data:
            if '.' in item['mention']:
                correct_data.append([item['mention'], item['mention_time']])
            else:
                correct_data.append(['@' + item['mention'], item['mention_time']])

        return correct_data

    @staticmethod
    def get_number_format(number: int) -> str:
        if 10 <= number <= 19 or number % 10 == 1 or number % 10 >= 5 or number % 10 == 0:
            word = 'раз'
        else:
            word = 'раза'
        return word

    async def show_channel_messages_data(self) -> str:
        data_to_csv = [[item['message_id'], item['date_published'], item['mention'],
                        item['text_message'], item['views'], item['forwards'],
                        rf'{WebConfig.ip}:{WebConfig.port}/{self.channel_name}/{item["message_id"]}']
                       for item in await db.get_messages_data(self.channel_name)]
        with open(f'{self.channel_name}_messages_data.csv', 'w', newline="", encoding='cp1251') as outfile:
            columns = ['ID сообщения', 'Дата публикации', 'Имя канала/Ссылка', 'Текст сообщения',
                       'Количество просмотров', 'Количество репостов', 'Получить сообщение']
            writer = csv.writer(outfile, delimiter=';')
            writer.writerow(columns)
            for data in data_to_csv:
                try:
                    writer.writerow(data)
                except Exception as e:
                    print(e)
        return f'{self.channel_name}_messages_data.csv'

