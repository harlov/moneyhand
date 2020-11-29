import logging

from aiogram.dispatcher import FSMContext
from aiogram import types


from moneyhand.app import create_service
from moneyhand.core.errors import EntityValidationError
from moneyhand.core import entities
from moneyhand.core.service import Service

from moneyhand.interfaces.telegram.app import dp
from moneyhand.interfaces.telegram import renders, inputs
from moneyhand.interfaces.telegram import helpers
from moneyhand.interfaces.telegram import states
from moneyhand.interfaces.telegram.errors import UnauthorizedUser

log = logging.getLogger(__name__)

service: Service


@dp.errors_handler(exception=UnauthorizedUser)
async def unauthorized(update: types.Update, e):
    log.error(
        f"user @{update.message.from_user.username}({update.message.from_user.id}): unauthorized"
    )
    await update.message.answer(renders.es("The owls are not what they seem"))


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        text="Please send command", reply_markup=helpers.unset_keyboard()
    )


@dp.message_handler(state="*", commands="cancel")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    # And remove keyboard (just in case)
    await message.answer(
        "Cancelled, please send new command", reply_markup=helpers.unset_keyboard()
    )


@dp.message_handler(commands=["get_categories"])
async def get_categories(message: types.Message):
    categories = await service.get_categories()
    await message.answer(
        text=renders.categories_list(categories),
    )


@dp.message_handler(commands=["get_income"])
async def get_income(message: types.Message):
    income = await service.get_income()
    await message.answer(renders.income(income))


@dp.message_handler(commands=["get_spending_plan"])
async def get_spending_plan(message: types.Message):
    plan = await service.get_spending_plan()
    categories = await service.get_categories()
    await message.answer_photo(
        renders.spending_plan_img(plan=plan, categories=categories)
    )


@dp.message_handler(commands=["get_balance_report"])
async def get_balance_report(message: types.Message):
    report = await service.get_balance_report()
    await message.answer(renders.balance_report(report=report))


# ADD CATEGORY


@dp.message_handler(commands="add_category")
async def add_category_start(message: types.Message):
    await states.AddCategory.name.set()
    await message.answer(
        "Enter name for a new category:", reply_markup=helpers.unset_keyboard()
    )


@dp.message_handler(state=states.AddCategory.name)
async def add_category_name(message: types.Message, state: FSMContext):
    await states.AddCategory.next()
    await state.update_data(name=message.text)
    await message.answer(
        "Select type for a new category:",
        reply_markup=helpers.keyboard([[i.name for i in entities.CategoryType]]),
    )


@dp.message_handler(state=states.AddCategory.type)
async def add_category_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    type_ = await inputs.read_type(entities.CategoryType, message)
    if type_ is None:
        return

    category = await service.create_category(name=data["name"], type_=type_)

    await message.answer(
        f"New category {category.name} has created",
        reply_markup=helpers.unset_keyboard(),
    )
    await state.finish()


# SET INCOME


@dp.message_handler(commands="set_income")
async def set_income_start(message: types.Message):
    await states.SetIncome.part_num.set()
    await message.answer(
        text="Select part of period", reply_markup=helpers.keyboard([["1", "2"]])
    )


@dp.message_handler(state=states.SetIncome.part_num)
async def set_income_part_num(message: types.Message, state: FSMContext):
    part_num = await inputs.read_int(message)
    if part_num is None:
        return

    await state.update_data(part_num=part_num)
    await states.SetIncome.next()
    await message.answer("Enter amount:")


@dp.message_handler(state=states.SetIncome.amount)
async def set_income_finish(message: types.Message, state: FSMContext):
    state_date = await state.get_data()
    try:
        income = await service.set_income(state_date["part_num"], float(message.text))
    except EntityValidationError as e:
        await message.answer(renders.es(f"{e.field}: {e.error}"))
        return

    await message.answer(renders.income(income))
    await state.finish()


# SET SPEND FOR CATEGORY
@dp.message_handler(commands="set_spend")
async def set_spend_start(message: types.Message, state: FSMContext):
    await states.SetSpend.category.set()
    categories = await service.get_categories()

    await message.answer(
        text="Select category: ",
        reply_markup=helpers.keyboard([[category.name] for category in categories]),
    )


@dp.message_handler(state=states.SetSpend.category)
async def set_spend_category(message: types.Message, state: FSMContext):
    category = await service.find_category(message.text)
    await state.update_data(category_id=category.id)
    await states.SetSpend.next()
    await message.answer(
        "Select part of period:", reply_markup=helpers.keyboard([["1", "2"]])
    )


@dp.message_handler(state=states.SetSpend.part_num)
async def set_spend_part(message: types.Message, state: FSMContext):
    part_num = await inputs.read_int(message)
    if part_num is None:
        return

    await state.update_data(part_num=part_num)
    await states.SetSpend.next()
    await message.answer("Enter amount:")


@dp.message_handler(state=states.SetSpend.amount)
async def set_spend_finish(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    await service.set_spend_for_category(
        category_id=state_data["category_id"],
        part=state_data["part_num"],
        amount=float(message.text),
    )
    await state.finish()


# MODIFY CATEGORY


@dp.message_handler(commands="change_category")
async def change_category_start(message: types.Message, state: FSMContext):
    await states.ChangeCategory.category.set()
    categories = await service.get_categories()

    await message.answer(
        text="Select category: ",
        reply_markup=helpers.keyboard([[category.name] for category in categories]),
    )


@dp.message_handler(state=states.ChangeCategory.category)
async def change_category_category(message: types.Message, state: FSMContext):
    category = await service.find_category(message.text)
    await state.update_data(category_id=category.id)
    await states.ChangeCategory.next()
    await message.answer(
        text="Select changing attribute: ",
        reply_markup=helpers.keyboard([["name", "type"]]),
    )


@dp.message_handler(state=states.ChangeCategory.attr_name)
async def change_category_attr_name(message: types.Message, state: FSMContext):
    attr_name = message.text
    await state.update_data(attr_name=attr_name)
    await states.ChangeCategory.next()
    await message.answer(
        text=f"Send new value for {attr_name} attribute: ",
        reply_markup=helpers.unset_keyboard(),
    )


@dp.message_handler(state=states.ChangeCategory.attr_value)
async def change_category_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()

    kwargs = {"pk": data["category_id"], data["attr_name"]: message.text}

    await service.update_category(**kwargs)
    await state.finish()
    await message.answer(
        text="Please send command", reply_markup=helpers.unset_keyboard()
    )


async def setup():
    global service
    service = await create_service()
