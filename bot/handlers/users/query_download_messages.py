import os

from bot.loader import dp, bot
from aiogram import types

from data.show.channel_data import ChannelShower
from data.show.link_data import LinkShower


@dp.callback_query_handler()
async def callback(query: types.CallbackQuery):
    print(query.data)
    await query.answer('')
    await query.message.delete()
    table_name, table_type = query.data.split('/')
    if table_type == 'channel':
        res = await ChannelShower(table_name).show_channel_messages_data()
        with open(res, 'rb') as file:
            await bot.send_document(query.from_user.id, file)
            os.remove(res)
    else:
        await LinkShower(table_name).show_link_message_data()
