from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from moneyhand import config
from .auth import AuthMiddleware

bot = Bot(token=config.TELEGRAM_API_TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(AuthMiddleware())


async def on_start():
    await bot.set_my_commands(
        [
            types.BotCommand("/get_categories", "Send list of all spending categories"),
            types.BotCommand("/get_income", "Send current income"),
            types.BotCommand("/get_spending_plan", "Show current spending plan"),
            types.BotCommand(
                "/get_balance_report", "Show income/spending balance report"
            ),
            types.BotCommand("/add_category", "Create new spending category"),
            types.BotCommand("/change_category", "Change category attributes"),
            types.BotCommand("/set_income", "Set income"),
            types.BotCommand("/set_spend", "Set spending plan for category"),
            types.BotCommand("/cancel", "Cancel any scenario"),
        ]
    )
