from aiogram.dispatcher.filters.state import StatesGroup, State


class Main(StatesGroup):
    menu = State()
    admin_menu = State()


class Search(StatesGroup):
    ask_what_search = State()
    ask_domain = State()
    ask_channel = State()


class AdminTools(StatesGroup):
    ask_adv_text = State()
    Sending = State()
    add_media = State()


class AddChannel(StatesGroup):
    ask_channel = State()
    ask_link = State()
