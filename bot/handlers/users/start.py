from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from bot.config import BotConfig
from bot.filters.IsUser import FirstTime
from bot.keyboards.Keyboard import Keyboard
from bot.loader import dp, db, bot


@dp.message_handler(CommandStart(), FirstTime())
async def bot_start(message: types.Message):
    admin_keyboard = Keyboard().admin_keyboard if message.from_user.id in BotConfig().admins else None
    await message.answer('Узнай, что и где рекламируется в Telegram:\n\n'
                         '- Отправь адрес канала <b>@channel</b> и получи список доменов и каналов,'
                         ' на которые ссылался канал.\n\n'
                         '- Отправь адрес домена и получи список каналов, которые ссылались на этот домен.'
                         , reply_markup=admin_keyboard)

    await db.add_user(name=message.from_user.username, chat_id=message.from_user.id)
    await bot.send_message(-1001263798812,
                           f'добавлен пользователь {message.from_user.username or message.from_user.id}')
