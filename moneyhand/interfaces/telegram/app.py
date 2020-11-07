from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from moneyhand import config

bot = Bot(token=config.TELEGRAM_API_TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
