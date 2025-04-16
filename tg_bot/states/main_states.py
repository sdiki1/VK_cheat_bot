from aiogram.dispatcher.filters.state import State, StatesGroup

class PostActions(StatesGroup):
    waiting_for_links = State()
    waiting_for_quantity = State()

class AdminActions(StatesGroup):
    waiting_for_tokens = State()
    waiting_for_remove_accounts = State()

class PostHunterStates(StatesGroup):
    waiting_group_link = State()
    waiting_likes_count = State()
    waiting_comments_count = State()
    waiting_reposts_count = State()
    waiting_interval = State()
    managing_requests = State()