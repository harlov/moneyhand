from aiogram.dispatcher.filters.state import StatesGroup, State


class AddCategory(StatesGroup):
    name = State()
    type = State()


class SetIncome(StatesGroup):
    part_num = State()
    amount = State()


class SetSpend(StatesGroup):
    category = State()
    part_num = State()
    amount = State()


class ChangeCategory(StatesGroup):
    category = State()
    attr_name = State()
    attr_value = State()
