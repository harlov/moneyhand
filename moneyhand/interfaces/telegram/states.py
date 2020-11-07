from aiogram.dispatcher.filters.state import StatesGroup, State


class AddCategory(StatesGroup):
    name = State()


class SetIncome(StatesGroup):
    part_num = State()
    amount = State()


class SetSpend(StatesGroup):
    category = State()
    part_num = State()
    amount = State()
