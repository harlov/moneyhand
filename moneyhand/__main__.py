import asyncio

from moneyhand import app


async def main():
    await app.run()

asyncio.run(main())
