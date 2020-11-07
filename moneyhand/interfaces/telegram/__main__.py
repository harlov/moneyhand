import logging
import asyncio

from aiogram import executor

from moneyhand import config

from . import handlers
from .app import dp


logging.basicConfig(level=config.LOG_LEVEL)
loop = asyncio.get_event_loop()


if __name__ == "__main__":
    log = logging.getLogger("aiogram")
    loop.run_until_complete(handlers.setup())
    executor.start_polling(dp)
