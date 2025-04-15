from termios import VLNEXT
from aiogram import Dispatcher
from tg_bot.config import ADMINS

class AdminMiddleware:
    async def on_pre_process_message(self, message, data):
        if message.text.startswith('/admin'):
            if str(message.from_user.id) not in ADMINS:
                await message.answer("Доступ запрещен!")
                # raise CancelHandler()
                raise ValueError("ERR!")
            
# TODO: Сделать это позже (реализовать фильтра админов)