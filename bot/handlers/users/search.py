import os
import re

from aiogram import types
from telethon.errors import FloodWaitError

from bot.filters.IsUser import IsUser
from bot.keyboards.Keyboard import DownloadMessagesInlineKeyboard
from bot.loader import dp, bot
from data.channel.channel import Channel
from data.clients.all_clients import all_clients
from data.show.link_data import LinkShower


@dp.message_handler(IsUser())
async def send_data(message: types.Message):
    try:
        answer = message.text
        if answer == '@channel' or answer == '@link':
            await message.answer('Невозможно получить данные канала')

        elif answer.startswith('@'):
            res = await Channel(answer[1:], all_clients).get_channel_data(message.from_user.id)  # [1:] is without @

            if res.endswith('.csv'):
                await message.answer(f'Канал {answer} упоминал:')
                with open(res, 'rb') as file:
                    await bot.send_document(message.from_user.id, file,
                                            reply_markup=DownloadMessagesInlineKeyboard(table_name=answer[1:],
                                                                                        table_type='channel',
                                                                                        button_text=f'Получить сообщения с канала {answer}').keyboard)
                os.remove(res)
            elif res == f'Нет данных об упоминаниях {answer[1:]}':
                await message.answer(res)
            else:
                await message.answer(res,
                                     reply_markup=DownloadMessagesInlineKeyboard(table_name=answer[1:],
                                                                                 table_type='channel',
                                                                                 button_text=f'Получить сообщения с канала {answer}').keyboard)
        elif answer.startswith('www.') or '.' in answer:
            answer = answer[4:] if answer.startswith('www.') else answer
            link = re.findall('[a-zA-z0-9_]+[.][a-z]+', answer)[0]
            res = await LinkShower(link).show_link_mention_data()

            if res.endswith('.csv'):
                await message.answer(f'Домен {link} упоминался:')
                with open(res, 'rb') as file:
                    await bot.send_document(message.from_user.id, file,
                                            reply_markup=DownloadMessagesInlineKeyboard(table_name=link,
                                                                                        table_type='link',
                                                                                        button_text=f'Получить сообщения упоминавшие {link}').keyboard)
                os.remove(res)
            elif res == f'Нет данных об упоминаниях {link}':
                await message.answer(res)
            else:
                await message.answer(res, reply_markup=DownloadMessagesInlineKeyboard(table_name=link,
                                                                                      table_type='link',
                                                                                      button_text=f'Получить сообщения упоминавшие'
                                                                                                  f' {link.replace("_dot_", ".")}').keyboard)
        else:
            await message.answer('Неверный формат данных')
    except FloodWaitError:
        await message.answer('Ошибка в получении данных о канале, пожалуйста повторите попытку позже')
    except ValueError:
        await message.answer('Данного канала не сущетсвует')
    except:
        await message.answer('Неизвестная ошибка')