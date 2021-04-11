import csv
from typing import List

from asyncpg import Record

from bot.loader import db


class LinkShower:
    def __init__(self, link: str):
        self.link = link.replace('.', '_dot_')

    async def show_link_mention_data(self) -> str:
        all_links = [link['link_name'] for link in await db.get_all_links()]
        if self.link.replace('_dot_', '.') in all_links:
            data = self.set_link_mention_data_format(await db.get_mention_link_data(self.link))
            if len(data) > 30:
                with open(f'{self.link}_data.csv', 'w', newline="", encoding='cp1251') as outfile:
                    columns = ['Канал', 'Количество упоминаний']
                    writer = csv.writer(outfile, delimiter=';')
                    writer.writerow(columns)
                    writer.writerows(data)
                    result = f'@{self.link}_data.csv'
            elif len(data) != 0:
                result = f'Домен <b>{self.link.replace("_dot_", ".")}</b> упоминался каналами:\n'
                for key in data:
                    result += f'<b>{key[0]} {key[1]}</b> {self.get_number_format(key[1])}\n'
            else:
                result = f'Нет данных об упоминаниях {self.link.replace("_dot_", ".")}'
        else:
            result = f'Нет данных об упоминаниях {self.link.replace("_dot_", ".")}'

        return result

    @staticmethod
    def set_link_mention_data_format(data: List[Record]) -> list:
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

    async def show_link_message_data(self):
        html = """<head>
    <meta charset="utf-8">

    <link href="//telegram.org/css/widget-frame.css?45" rel="stylesheet" media="screen">
    <link href="//telegram.org/css/telegram-web.css?18" rel="stylesheet" media="screen">
    <script>TBaseUrl='/';</script>
  </head>
"""
        for message in await db.get_link_message_data(self.link):
            data = message[0]
            html += f"""<div class="tgme_widget_message_bubble"><div class="tgme_widget_message_author 
                accent_color"><a><span dir="auto">{message[1]}</span></a></div><i 
                class="tgme_widget_message_bubble_tail"> 
      <svg class="bubble_icon" width="9px" height="20px" viewBox="0 0 9 20">
        <g fill="none">
          <path class="background" fill="#ffffff" d="M8,1 L9,1 L9,20 L8,20 L8,18 C7.807,15.161 7.124,12.233 5.950,9.218 C5.046,6.893 3.504,4.733 1.325,2.738 L1.325,2.738 C0.917,2.365 0.89,1.732 1.263,1.325 C1.452,1.118 1.72,1 2,1 L8,1 Z"></path>
          <path class="border_1x" fill="#d7e3ec" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0 L9,0 L9,20 L7,20 L7,20 L7.002,18.068 C6.816,15.333 6.156,12.504 5.018,9.58 C4.172,7.406 2.72,5.371 0.649,3.475 C-0.165,2.729 -0.221,1.464 0.525,0.649 C0.904,0.236 1.439,0 2,0 Z"></path>
          <path class="border_2x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.5 L9,0.5 L9,20 L7.5,20 L7.5,20 L7.501,18.034 C7.312,15.247 6.64,12.369 5.484,9.399 C4.609,7.15 3.112,5.052 0.987,3.106 C0.376,2.547 0.334,1.598 0.894,0.987 C1.178,0.677 1.579,0.5 2,0.5 Z"></path>
          <path class="border_3x" d="M9,1 L2,1 C1.72,1 1.452,1.118 1.263,1.325 C0.89,1.732 0.917,2.365 1.325,2.738 C3.504,4.733 5.046,6.893 5.95,9.218 C7.124,12.233 7.807,15.161 8,18 L8,20 L9,20 L9,1 Z M2,0.667 L9,0.667 L9,20 L7.667,20 L7.667,20 L7.668,18.023 C7.477,15.218 6.802,12.324 5.64,9.338 C4.755,7.064 3.243,4.946 1.1,2.983 C0.557,2.486 0.52,1.643 1.017,1.1 C1.269,0.824 1.626,0.667 2,0.667 Z"></path>
        </g>
      </svg>
    </i> 
                <div class="tgme_widget_message_text js-message_text before_footer" dir="auto">{data['text_message']}
                </div>

<div class="tgme_widget_message_footer compact js-message_footer">

  <div class="tgme_widget_message_info short js-message_info">
    <span class="tgme_widget_message_views">{data['views']}</span><span class="copyonly"> views</span><span class="tgme_widget_message_meta"></span>
  </div>
</div>
  </div>"""
        return html