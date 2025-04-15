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




def register_posthunter_handlers(dp: Dispatcher):
    ...