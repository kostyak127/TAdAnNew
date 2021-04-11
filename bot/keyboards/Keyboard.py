from aiogram import types


class Keyboard:
    def __init__(self, buttons: list = None):
        self._buttons = buttons
        self._keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False)

    def create_keyboard(self) -> types.ReplyKeyboardMarkup:
        keyboard = types.ReplyKeyboardMarkup()
        for button in self._buttons:
            keyboard.row(button)

        return keyboard

    @property
    def admin_keyboard(self):
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.row('Узнать количество пользователей')
        keyboard.row('Узнать количество каналов в базе')
        keyboard.row('Отправить рекламное сообщение')
        return keyboard


class DownloadMessagesInlineKeyboard:
    def __init__(self, table_name: str, button_text: str, table_type: str):
        self._keyboard = types.InlineKeyboardMarkup()
        self.table_name = table_name
        self.button_text = button_text
        self.table_type = table_type
        self.button = types.InlineKeyboardButton(text=self.button_text,
                                                 callback_data=f'{table_name}/{table_type}',
                                                 url=f'http://127.0.0.1:8000/{table_type}/'
                                                     f'{table_name.replace(".", "_dot_")}')

    @property
    def keyboard(self) -> types.InlineKeyboardMarkup:
        return self._keyboard.add(self.button)