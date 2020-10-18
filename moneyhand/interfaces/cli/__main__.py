import asyncio
from typing import Awaitable, Callable, Any
from uuid import UUID

import click
from functools import wraps
import nest_asyncio

from moneyhand.app import create_service
from moneyhand.core.service import Service
from . import renders

service: Service

loop = asyncio.get_event_loop()
nest_asyncio.apply(loop)


def command(f: Callable[..., Awaitable]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args, **kwargs):
        return loop.run_until_complete(f(*args, **kwargs))

    return wrapper


@click.group()
def cli() -> None:
    pass


@cli.group()
def categories() -> None:
    pass


@cli.group()
def income() -> None:
    pass


@cli.group(name="plan")
def spending_plan() -> None:
    pass


@categories.command(name="list")
@command
async def list_categories() -> None:
    click.echo("categories: ")
    click.echo(renders.categories_list(await service.get_categories()))


@categories.command(name="add")
@command
@click.option("--name", prompt="Category name", help="The name of a category.")
async def add_category(name: str) -> None:
    category = await service.create_category(name=name)
    click.echo(f"New category {name} was created. ID = {category.id}")


@income.command(name="get")
@command
async def get_incomes() -> None:
    click.echo("Income:")
    i = await service.get_income()
    click.echo(renders.income(i))


@income.command(name="set")
@click.option("--part", prompt="Part sequence number", type=int)
@click.option("--amount", prompt="Amount", type=float)
@command
async def set_income(part: int, amount: float) -> None:
    i = await service.set_income(part=part, amount=amount)
    click.echo("Current income state:")
    click.echo(renders.income(i))


@spending_plan.command(name="set_for_category")
@command
async def set_spending_plan_for_category() -> None:
    categories_ = await service.get_categories()
    click.echo(renders.categories_list(categories_))
    category_id = UUID(click.prompt("Enter ID of category: ").strip())
    part = int(click.prompt("Part sequence number"))
    amount = int(click.prompt("Amount: ").strip())
    spending_plan_ = await service.set_spend_for_category(category_id, part, amount)
    click.echo(renders.spending_plan(spending_plan_, categories=categories_))


@spending_plan.command(name="get")
@command
async def get_spending_plan() -> None:
    click.echo(
        renders.spending_plan(
            await service.get_spending_plan(),
            categories=await service.get_categories(),
        )
    )


async def main():
    global service
    service = await create_service()
    cli()


if __name__ == "__main__":
    loop.run_until_complete(main())
