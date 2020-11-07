from aiogram.dispatcher import FSMContext
from aiogram import types

from moneyhand.app import create_service
from moneyhand.core.service import Service

from moneyhand.interfaces.telegram.app import dp
from moneyhand.interfaces.telegram import renders
from moneyhand.interfaces.telegram import helpers
from moneyhand.interfaces.telegram import states


service: Service


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        text="Please select action",
        reply_markup=helpers.keyboard(
            [
                ["/get_categories", "/add_category"],
                ["/get_income", "/set_income"],
                ["/get_spending_plan", "/set_spend"],
                ["/get_balance_report"],
            ]
        ),
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
    await message.answer(renders.spending_plan(plan=plan, categories=categories))


@dp.message_handler(commands=["get_balance_report"])
async def get_balance_report(message: types.Message):
    report = await service.get_balance_report()
    await message.answer(renders.balance_report(report=report))


# ADD CATEGORY


@dp.message_handler(commands="add_category")
async def add_category_start(message: types.Message):
    await states.AddCategory.name.set()
    await message.reply("Enter name for a new category:")


@dp.message_handler(state=states.AddCategory.name)
async def add_category_finish(message: types.Message, state: FSMContext):
    category = await service.create_category(message.text.strip())
    await message.reply(f"New category {category.name} has created")
    await state.finish()


# SET INCOME


@dp.message_handler(commands="set_income")
async def set_income_start(message: types.Message):
    await states.SetIncome.part_num.set()
    await message.reply(
        text="Select part of period", reply_markup=helpers.keyboard([["1", "2"]])
    )


@dp.message_handler(state=states.SetIncome.part_num)
async def set_income_part_num(message: types.Message, state: FSMContext):
    await state.update_data(part_num=int(message.text))
    await states.SetIncome.next()
    await message.reply("Enter amount:")


@dp.message_handler(state=states.SetIncome.amount)
async def set_income_finish(message: types.Message, state: FSMContext):
    state_date = await state.get_data()
    income = await service.set_income(state_date["part_num"], float(message.text))
    await message.reply(renders.income(income))
    await state.finish()


# SET SPEND FOR CATEGORY
@dp.message_handler(commands="set_spend")
async def set_spend_start(message: types.Message, state: FSMContext):
    await states.SetSpend.category.set()
    categories = await service.get_categories()

    await message.reply(
        text="Select category: ",
        reply_markup=helpers.keyboard([[category.name] for category in categories]),
    )


@dp.message_handler(state=states.SetSpend.category)
async def set_spend_category(message: types.Message, state: FSMContext):
    category = await service.find_category(message.text)
    await state.update_data(category_id=category.id)
    await states.SetSpend.next()
    await message.reply(
        "Select part of period:", reply_markup=helpers.keyboard([["1", "2"]])
    )


@dp.message_handler(state=states.SetSpend.part_num)
async def set_spend_part(message: types.Message, state: FSMContext):
    await state.update_data(part_num=int(message.text))
    await states.SetSpend.next()
    await message.reply("Enter amount:")


@dp.message_handler(state=states.SetSpend.amount)
async def set_spend_finish(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    await service.set_spend_for_category(
        category_id=state_data["category_id"],
        part=state_data["part_num"],
        amount=float(message.text),
    )
    await state.finish()


async def setup():
    global service
    service = await create_service()
