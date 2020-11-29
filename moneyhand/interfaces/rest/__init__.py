from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from moneyhand import config
from moneyhand.app import create_service
from moneyhand.core import entities
from moneyhand.core import errors
from moneyhand.core.service import Service
from . import schemas

service: Service


async def setup():
    global service
    service = await create_service()


app = FastAPI(
    debug=config.API_DEBUG,
    title="MoneyHand REST API",
    root_path=config.API_ROOT_PATH,
    on_startup=[setup],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


@app.get("/")
async def read_root():
    return {}


async def decode_token(token) -> entities.User:
    try:
        return await service.tenant.get_user_by_token(token)
    except errors.AuthCredentialsInvalidError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return await decode_token(token)


@app.post("/user/token")
async def create_user_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token = await service.tenant.create_access_token(
            form_data.username, form_data.password
        )
        return {"access_token": token, "token_type": "bearer"}
    except errors.AuthCredentialsInvalidError:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


@app.get("/user")
async def get_user_info(current_user: entities.User = Depends(get_current_user)):
    return current_user


@app.get("/categories")
async def get_categories(current_user: entities.User = Depends(get_current_user)):
    return await service.get_categories()


@app.post("/categories")
async def create_category(
    create_category_data: schemas.CreateCategoryData,
    current_user: entities.User = Depends(get_current_user),
):
    return await service.create_category(
        create_category_data.name,
        create_category_data.type,
    )
