from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt


from moneyhand import config
from moneyhand.core.unit_of_work import AbstractUnitOfWork
from moneyhand.core import entities
from moneyhand.core import errors

ALGORITHM = "HS256"


class TenantService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def create_access_token(self, name: str, password: str) -> str:
        user = await self._login_user(name, password)

        if not user:
            raise errors.AuthCredentialsInvalidError

        return self._dump_token(
            entities.UserToken(
                user_id=user.id,
                expires_at=datetime.utcnow()
                + timedelta(seconds=config.USER_TOKEN_LIFETIME_SEC),
            )
        )

    async def _login_user(self, name: str, password: str) -> Optional[entities.User]:
        async with self.uow:
            user = await self.uow.user.find(name)
            if not user:
                return None

            if not user.check_password(password):
                return None

            return user

    @staticmethod
    def _dump_token(data: entities.UserToken) -> str:
        return jwt.encode(
            {
                "sub": str(data.user_id),
                "exp": data.expires_at,
            },
            config.HASH_SECRET_KEY,
            algorithm=ALGORITHM,
        )

    def _load_token(self, token: str) -> entities.UserToken:
        try:
            payload = jwt.decode(token, config.HASH_SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise errors.AuthCredentialsInvalidError

            return entities.UserToken(
                user_id=UUID(user_id), expires_at=payload.get("exp")
            )
        except JWTError:
            raise errors.AuthCredentialsInvalidError

    async def get_user_by_token(self, token: str) -> Optional[entities.User]:
        user_token: entities.UserToken = self._load_token(token)
        async with self.uow:
            return await self.uow.user.get(user_token.user_id)

    async def get_user(self, pk: UUID) -> Optional[entities.User]:
        async with self.uow:
            return await self.uow.user.get(pk=pk)

    async def ensure_default(self):
        async with self.uow:
            tenant = await self.uow.tenant.get(config.DEFAULT_TENANT_UUID)
            if tenant is None:
                tenant = entities.Tenant(id=config.DEFAULT_TENANT_UUID)
                user = entities.User.new(
                    name=config.DEFAULT_TENANT_USER,
                    email=config.DEFAULT_TENANT_EMAIL,
                    password=config.DEFAULT_TENANT_PASSWORD,
                )
                user.link_to_tenant(tenant.id)
                await self.uow.tenant.save(tenant)
                await self.uow.user.save(user)
