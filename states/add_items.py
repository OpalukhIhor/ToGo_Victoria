from aiogram.dispatcher.filters.state import StatesGroup, State


class AddItem(StatesGroup):
    type = State()
    name = State()
    photo = State()
    description = State()
    price = State()
