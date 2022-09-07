from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderItems(StatesGroup):
    quantity = State()
    amount = State()
    status = State()
