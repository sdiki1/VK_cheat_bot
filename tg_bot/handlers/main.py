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


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_admin, commands=['admin'])


