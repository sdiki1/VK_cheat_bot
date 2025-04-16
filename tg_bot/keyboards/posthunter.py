from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_posthunter_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton('Создать заявку'),
        KeyboardButton('Мои заявки')
    ).row(
        KeyboardButton('Главное меню')
    )

def get_requests_kb(requests):
    kb = InlineKeyboardMarkup()
    for req in requests:
        kb.add(InlineKeyboardButton(
            f"Заявка #{req.id}", 
            callback_data=f"req_{req.id}"
        ))
    return kb

def get_request_actions_kb(request_id):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton('Удалить', callback_data=f"delete_{request_id}"),
        InlineKeyboardButton('Назад', callback_data='back_to_requests')
    )