from typing import List
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from moneyhand import config
from moneyhand.core import errors
from .service import service
from . import schemas
from . import security


app = FastAPI(
    debug=config.API_DEBUG,
    title="MoneyHand REST API",
    root_path=config.API_ROOT_PATH,
    on_startup=[service.on_startup],
)

app.router.route_class = security.AuthenticatedAPIRoute


@app.exception_handler(errors.EntityNotFound)
def not_found_exception_handler(request: Request, exc: errors.EntityNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": "not_found", "entity": exc.entity_name, "pk": str(exc.pk)},
    )


@app.get(
    "/",
)
async def read_root():
    return {}


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
async def get_user_info():
    return security.current_user.get()


@app.get("/categories", response_model=List[schemas.DumpCategory])
async def get_categories():
    return await service.get_categories()


@app.post("/categories", response_model=schemas.DumpCategory)
async def create_category(
    category_data: schemas.CreateCategoryData,
):
    return await service.create_category(
        category_data.name,
        category_data.type,
    )


@app.patch("/categories/{pk}", response_model=schemas.DumpCategory)
async def update_category(
    pk: UUID,
    category_data: schemas.UpdateCategoryData,
):
    return await service.update_category(
        pk=pk, name=category_data.name, type_=category_data.type
    )


@app.get("/income", response_model=schemas.DumpIncome)
async def get_income():
    res = await service.get_income()
    return res or {}


@app.patch("/income", response_model=schemas.DumpIncome)
async def update_income(
    income_data: schemas.UpdateIncomeData,
):
    return await service.set_income(
        part_1=income_data.part_1, part_2=income_data.part_2
    )

