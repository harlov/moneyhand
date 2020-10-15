import asyncio
import click
from functools import wraps
import nest_asyncio

from moneyhand.app import create_service
from moneyhand.core.service import Service

service: Service

loop = asyncio.get_event_loop()
nest_asyncio.apply(loop)


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return loop.run_until_complete(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@cli.group()
def categories():
    pass


@categories.command(name="list")
@coro
async def list_categories():
    click.echo("categories: ")
    categories_list = await service.get_categories()

    for category in categories_list:
        click.echo(f" - {category.name}")


@categories.command(name="add")
@click.option('--name', prompt='Category name',
              help='The name of a category.')
@coro
async def add_category(name: str):
    category = await service.create_category(name)
    print(f"New category {name} was created. ID = {category.id}")


async def main():
    global service
    service = await create_service()
    cli()

if __name__ == '__main__':
    loop.run_until_complete(main())
