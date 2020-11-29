from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from passlib.context import CryptContext

from .base import new_id, Model, PrivateAttr


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Tenant(Model):
    id: UUID


class UserTelegramLink(Model):
    id: UUID
    telegram_user_id: str
    telegram_user_name: str


class User(Model):
    id: UUID
    name: str
    email: str
    disabled: bool

    telegram_link: Optional[UserTelegramLink] = None

    _tenant_id: UUID = PrivateAttr()
    _password_hash: str = PrivateAttr()

    @property
    def tenant_id(self):
        return self._tenant_id

    def link_to_tenant(self, tenant_id: UUID) -> None:
        self._tenant_id = tenant_id

    def set_password(self, password: str) -> None:
        self._password_hash = pwd_context.hash(password)

    def check_password(self, password) -> bool:
        return pwd_context.verify(password, self._password_hash)

    def link_to_telegram(self, telegram_user_id: str, telegram_user_name: str) -> None:
        if self.telegram_link is None:
            self.telegram_link = UserTelegramLink(
                id=new_id(),
                telegram_user_id=telegram_user_id,
                telegram_user_name=telegram_user_name,
            )
        else:
            self.telegram_link.telegram_user_id = telegram_user_id
            self.telegram_link.telegram_user_name = telegram_user_name

    @classmethod
    def new(cls, name: str, email: str, password: str) -> User:
        u = User(id=new_id(), name=name, email=email, disabled=False)
        u.set_password(password)
        return u


class UserToken(Model):
    user_id: UUID
    expires_at: datetime
