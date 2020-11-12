from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from moneyhand.interfaces.telegram.errors import UnauthorizedUser
from moneyhand import config


class AuthMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        if not self._is_admin_user(message.from_user):
            raise UnauthorizedUser

    @staticmethod
    def _is_admin_user(user: types.User) -> bool:
        if config.TELEGRAM_GOD_USER.isdigit():
            return config.TELEGRAM_GOD_USER == user.id
        else:
            return config.TELEGRAM_GOD_USER == user.username
