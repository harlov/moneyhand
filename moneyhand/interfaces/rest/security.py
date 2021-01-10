from contextvars import ContextVar
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRoute
from fastapi import status, Depends
from fastapi.security import OAuth2PasswordBearer


from moneyhand.core import entities
from moneyhand.core import errors

from .service import service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


current_user = ContextVar("current_user")


UNAUTHORISED_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(token: str) -> entities.User:
    try:
        user = await service.tenant.get_user_by_token(token)
        if user is None:
            raise UNAUTHORISED_ERROR
        return user
    except errors.AuthCredentialsInvalidError:
        raise UNAUTHORISED_ERROR


async def set_current_user(token: str = Depends(oauth2_scheme)) -> None:
    user = await get_current_user(token)
    current_user.set(user)


exclude_auth_routes = ["/user/token"]


class AuthenticatedAPIRoute(APIRoute):
    def __init__(self, path, endpoint, **kwargs):
        if path not in exclude_auth_routes:
            if getattr(kwargs, "dependencies", None) is None:
                kwargs["dependencies"] = []

            kwargs["dependencies"].append(Depends(set_current_user))

        super(AuthenticatedAPIRoute, self).__init__(path, endpoint, **kwargs)
