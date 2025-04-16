# aiogram import
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

# import public modules
import random

# import local modules
from tg_bot.states import PostActions
from tg_bot.models import TaskManager


async def process_post_action(message: types.Message, state: FSMContext):
    await PostActions.waiting_for_links.set()
    async with state.proxy() as data:
        data["type"] = message.text
    await message.answer("Отправьте ссылки на посты (через пробел или с новой строки):")


async def process_links(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = message.text
    
    await PostActions.next()
    await message.answer("Введите количество действий:")

async def process_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
        print(quantity)
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

        urls = data['url'].split()
        for url in urls:
            for i in range(quantity):
                interval = intervals[task_type]*i
                TaskManager.create_task(
                    task_type=task_type,
                    url=url,
                    params={'comment_text': data.get('comment_text', '')},
                    interval=interval
                )

    await message.answer(f"✅ Добавлено {quantity} задач в очередь!")
    await state.finish()


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(process_post_action, lambda message: message.text in ['Накрутить лайки на пост', 'Накрутить репосты на пост', 'Написать коммент'])
    dp.register_message_handler(process_links, state=PostActions.waiting_for_links)
    dp.register_message_handler(process_quantity, state=PostActions.waiting_for_quantity)