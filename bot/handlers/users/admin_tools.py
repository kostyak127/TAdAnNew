import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, MediaGroup

from bot.filters.IsUser import IsAdmin
from bot.keyboards.Keyboard import Keyboard
from bot.loader import dp, db, bot
from bot.states.statesgroup import AdminTools


@dp.message_handler(IsAdmin(), text=['Узнать количество пользователей',
                                     'Узнать количество каналов в базе',
                                     'Отправить рекламное сообщение'])
async def do_admin_command(message: types.Message):
    if message.text == 'Узнать количество пользователей':
        await message.answer(f'Количество пользователей бота TAdAn - <b>{await db.count_rows("users")}</b>')
    elif message.text == 'Узнать количество каналов в базе':
        await message.answer(f'Количество каналов в базе - <b>{await db.count_rows("channels")}</b>')
    elif message.text == 'Отправить рекламное сообщение':
        await message.answer('Введите текст рекламы')
        await AdminTools.ask_adv_text.set()


@dp.message_handler(state=AdminTools.add_media, text=['Отправить', 'Назад'])
async def SendMedia(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Отправить':
        users = await db.get_all_users()
        for user in users:
            try:
                await bot.send_media_group(user['chat_id'], data.get('media'))
                await asyncio.sleep(0.34)
            except Exception:
                pass
        await message.answer('Отправлено', reply_markup=Keyboard().admin_keyboard)
    elif message.text == 'Назад':
        await message.answer('Я вернул вас!', reply_markup=Keyboard().admin_keyboard)

    await state.finish()


@dp.message_handler(state=AdminTools.ask_adv_text)
async def get_adv_text(message: types.Message, state: FSMContext):
    await message.answer('Отправляю? Если нужно приложить фото/видео, '
                         'то прикладывайте их по одному, потом нажмите Отправить.',
                         reply_markup=Keyboard(buttons=['Отправить', 'Назад']).create_keyboard())
    await state.update_data(
        {'text': message.text}
    )
    await AdminTools.Sending.set()


@dp.message_handler(state=AdminTools.Sending, text=['Отправить', 'Назад'])
async def Sending(message: types.Message, state: FSMContext):
    if message.text == 'Отправить':
        data = await state.get_data()
        users = await db.get_all_users()
        for user in users:
            try:
                await bot.send_message(user['chat_id'], data.get('text'))
                await asyncio.sleep(0.34)
            except:
                pass
        await message.answer('Отправлено', reply_markup=Keyboard().admin_keyboard)
    elif message.text == 'Назад':
        await message.answer('Я вернул вас!', reply_markup=Keyboard().admin_keyboard)

    await state.finish()


@dp.message_handler(state=[AdminTools.Sending, AdminTools.add_media], content_types=ContentType.PHOTO)
async def AddMedia(message: types.Message, state: FSMContext):
    await AdminTools.add_media.set()
    data = await state.get_data()

    if data.get('media'):
        data['media'].attach_photo(message.photo[-1].file_id)
    else:
        data['media'] = MediaGroup()
        data['media'].attach_photo(message.photo[-1].file_id, caption=data.get('text'))

    await state.update_data(data)
    await message.answer('Я добавил фото')


@dp.message_handler(state=[AdminTools.Sending, AdminTools.add_media], content_types=ContentType.VIDEO)
async def AddMedia(message: types.Message, state: FSMContext):
    await AdminTools.add_media.set()
    data = await state.get_data()
    if data.get('media'):
        data['media'].attach_video(message.video.file_id)
    else:
        data['media'] = MediaGroup()
        data['media'].attach_video(message.video.file_id, caption=data.get('text'))
    await message.answer('Я добавил видео')
