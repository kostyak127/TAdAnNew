from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from bot.config import BotConfig
from bot.loader import db


class IsUser(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return len(await db.check_user(message.from_user.id)) > 0


class FirstTime(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        print(await db.check_user(message.from_user.id))
        return len(await db.check_user(message.from_user.id)) == 0


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in BotConfig().admins