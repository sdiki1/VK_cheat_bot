from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

action_cb = CallbackData('post_action', 'action_type')

def get_main_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton('Накрутить лайки на пост'),
        KeyboardButton('Накрутить репосты на пост')
    ).row(
        KeyboardButton('Написать коммент'),
    )

def get_admin_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Добавить аккаунты'),
        KeyboardButton('Удаление забаненных аккаунтов')
    )

def get_action_kb():
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton('Лайки', callback_data=action_cb.new(action_type='like')),
        InlineKeyboardButton('Репосты', callback_data=action_cb.new(action_type='repost')),
        InlineKeyboardButton('Комменты', callback_data=action_cb.new(action_type='comment'))
    )
