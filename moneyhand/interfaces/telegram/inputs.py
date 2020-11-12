from typing import Type, Optional, TypeVar

from aiogram.types import Message

from . import renders

EnumTypeVar = TypeVar("EnumTypeVar")


async def read_int(message: Message) -> Optional[int]:
    try:
        return int(message.text)
    except ValueError:
        await message.answer(
            renders.es(f'"{message.text}" is not a number. Try again?')
        )


async def read_type(
    type_cls: Type[EnumTypeVar], message: Message
) -> Optional[EnumTypeVar]:
    try:
        return type_cls[message.text]
    except KeyError:
        await message.answer(renders.es(f'Unknown type "{message.text}". Try again?'))
