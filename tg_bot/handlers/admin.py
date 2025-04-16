# aiogram import
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

# import public modules
import re

# import local modules
from tg_bot.states import AdminActions

# import database module
from tg_bot.models import Account, sessionmaker, engine


Session = sessionmaker(bind=engine)

async def add_accounts(message: types.Message):
    await AdminActions.waiting_for_tokens.set()
    await message.answer("Отправьте токены аккаунтов:")

async def process_tokens(message: types.Message, state: FSMContext):
    session = Session()
    tokens = message.text.split()
    print(tokens)
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

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(add_accounts, text='Добавить аккаунты')
    dp.register_message_handler(process_tokens, state=AdminActions.waiting_for_tokens)
    dp.register_message_handler(remove_banned, text='Удаление забаненных аккаунтов')