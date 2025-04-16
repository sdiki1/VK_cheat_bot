# aiogram import
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hcode
# import public modules
import random
import re

# import local modules
from tg_bot.states import PostActions, AdminActions, PostHunterStates
from tg_bot.keyboards import get_requests_kb, get_main_kb, get_request_actions_kb, get_posthunter_kb


# import database module
from tg_bot.models import sessionmaker, engine, PostHunterRequest


Session = sessionmaker(bind=engine)



async def handle_posthunter(message: types.Message):
    await message.answer(
        "🕵️‍♂️ Режим PostHunter - управление автоматическим продвижением постов",
        reply_markup=get_posthunter_kb()
    )

async def start_posthunter(message: types.Message):
    await PostHunterStates.waiting_group_link.set()
    await message.answer("Введите ссылку на группу ВК:", reply_markup=types.ReplyKeyboardRemove())

# making request process

async def process_group_link(message: types.Message, state: FSMContext):
    if 'vk.com' not in message.text:
        await message.answer("Некорректная ссылка! Попробуйте еще раз:")
        return
    
    async with state.proxy() as data:
        data['group_url'] = message.text
    
    await PostHunterStates.next()
    await message.answer("Введите необходимое количество лайков:")


async def process_likes(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число!")
        return
    
    async with state.proxy() as data:
        data['likes'] = int(message.text)
    
    await PostHunterStates.next()
    await message.answer("Введите необходимое количество комментариев:")

async def process_comments(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число!")
        return
    
    async with state.proxy() as data:
        data['comments'] = int(message.text)
    
    await PostHunterStates.next()
    await message.answer("Введите необходимое количество репостов:")



async def process_reposts(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число!")
        return
    
    async with state.proxy() as data:
        data['reposts'] = int(message.text)
    
    await PostHunterStates.next()
    await message.answer("Введите необходимый интервал:")





async def process_interval(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        session = Session()
        new_request = PostHunterRequest(
            group_url=data['group_url'],
            likes=data['likes'],
            comments=data['comments'],
            reposts=data['reposts'],
            interval=int(message.text),
            owner_id=message.from_user.id
        )
        session.add(new_request)
        session.commit()
    
    await state.finish()
    await message.answer("✅ Заявка создана!", reply_markup=get_main_kb())


# requests info and delete

async def show_requests(message: types.Message):
    session = Session()
    requests = session.query(PostHunterRequest).filter_by(
        owner_id=message.from_user.id,
        is_active=True
    ).all()
    
    if not requests:
        await message.answer("У вас нет активных заявок")
        return
    
    await message.answer("Ваши активные заявки:", reply_markup=get_requests_kb(requests))

async def show_request_details(callback: types.CallbackQuery):
    request_id = int(callback.data.split('_')[1])
    session = Session()
    request = session.query(PostHunterRequest).get(request_id)
    
    if not request or request.owner_id != callback.from_user.id:
        await callback.answer("Заявка не найдена!")
        return
    
    text = (
        f"{hbold('Детали заявки')} #{request.id}\n\n"
        f"🔗 Группа: {hcode(request.group_url)}\n"
        f"❤️ Лайки: {request.likes}\n"
        f"💬 Комментарии: {request.comments}\n"
        f"↩️ Репосты: {request.reposts}\n"
        f"⏱ Интервал: {request.interval} cекунд\n"
        f"🔄 Статус: {'Активна' if request.is_active else 'Неактивна'}"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_request_actions_kb(request.id)
    )
    await callback.answer()



async def delete_request(callback: types.CallbackQuery):
    request_id = int(callback.data.split('_')[1])
    session = Session()
    request = session.query(PostHunterRequest).get(request_id)
    
    if request and request.owner_id == callback.from_user.id:
        request.is_active = False
        session.commit()
        await callback.message.edit_text("Заявка удалена!")
    else:
        await callback.answer("Ошибка удаления!")



def register_posthunter_handlers(dp: Dispatcher):
    dp.register_message_handler(process_interval, state=PostHunterStates.waiting_interval)
    dp.register_message_handler(show_requests, text='Мои заявки')
    dp.register_callback_query_handler(delete_request, lambda c: c.data.startswith('delete_'))
    dp.register_message_handler(process_likes, state=PostHunterStates.waiting_likes_count)
    dp.register_message_handler(process_comments, state=PostHunterStates.waiting_comments_count)
    dp.register_message_handler(process_reposts, state=PostHunterStates.waiting_reposts_count)
    dp.register_message_handler(process_group_link, state=PostHunterStates.waiting_group_link)
    dp.register_message_handler(handle_posthunter, text='Постхантер')
    dp.register_message_handler(start_posthunter, text='Создать заявку')
    dp.register_callback_query_handler(show_request_details, lambda c: c.data.startswith('req_'))
