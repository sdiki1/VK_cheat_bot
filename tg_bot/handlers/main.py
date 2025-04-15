# aiogram import
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

# import public modules
import random
import re

# import local modules
from tg_bot.states import PostActions, AdminActions
from tg_bot.keyboards import get_main_kb, get_admin_kb
from tg_bot.models import TaskManager


# import database module
from tg_bot.models import Account, sessionmaker, engine


Session = sessionmaker(bind=engine)

async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=get_main_kb())


async def cmd_admin(message: types.Message):
    await message.answer("Админ-панель:", reply_markup=get_admin_kb())

# 
# 
# POSTS
# 
# 
async def process_post_action(message: types.Message, state: FSMContext):
    await PostActions.waiting_for_links.set()
    async with state.proxy() as data:
        data["type"] = message.text
    await message.answer("Отправьте ссылки на посты (через пробел или с новой строки):")


async def process_links(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment_text'] = message.text
    
    await PostActions.next()
    await message.answer("Введите количество действий:")

async def process_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
    except:
        return await message.answer("❌ Введите число!")
    async with state.proxy() as data:
        task_type = {
            'Накрутить лайки на пост': 'like',
            'Накрутить репосты на пост': 'repost',
            'Написать коммент': 'comment'
        }[data['type']]
        intervals = {
            'like': random.randint(20, 30),
            'comment': random.randint(60, 70),
            'repost': random.randint(120, 180)
        }

        for url in data['urls']:
            for _ in range(quantity):
                TaskManager.create_task(
                    task_type=task_type,
                    url=url,
                    params={'comment_text': data.get('comment_text', '')},
                    interval=intervals[task_type]
                )

    await message.answer(f"✅ Добавлено {quantity * len(data['urls'])} задач в очередь!")
    await state.finish()


async def add_accounts(message: types.Message):
    await AdminActions.waiting_for_tokens.set()
    await message.answer("Отправьте токены аккаунтов:")

async def process_tokens(message: types.Message, state: FSMContext):
    session = Session()
    tokens = re.findall(r'[a-zA-Z0-9]{85}', message.text)
    
    added = 0
    for token in tokens:
        try:
            account = Account(token=token)
            session.add(account)
            session.commit()
            added += 1
        except Exception as E:
            session.rollback()
            continue
            
    await message.answer(f"Успешно добавлено {added} аккаунтов!\n"
                         f"Дубликатов: {len(tokens) - added}")
    await state.finish()

async def remove_banned(message: types.Message):
    session = Session()
    result = session.query(Account).filter(Account.is_banned == True).delete()
    session.commit()
    await message.answer(f"Удалено {result} забаненных аккаунтов!")

def register_all_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_admin, commands=['admin'])

    dp.register_message_handler(process_post_action, lambda message: message.text in ['Накрутить лайки на пост', 'Накрутить репосты на пост', 'Написать коммент'])
    dp.register_message_handler(process_links, state=PostActions.waiting_for_links)
    dp.register_message_handler(process_quantity, state=PostActions.waiting_for_quantity)

    # admin
    dp.register_message_handler(add_accounts, text='Добавить аккаунты')
    dp.register_message_handler(process_tokens, state=AdminActions.waiting_for_tokens)
    dp.register_message_handler(remove_banned, text='Удаление забаненных аккаунтов')