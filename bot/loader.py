import asyncio

from aiogram import Bot, Dispatcher, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config import BotConfig
from database.database import Database

bot = Bot(token='1099799716:AAH34aWXLIBiUNZPVP24WOT4cVxHHgqeAgc', parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()