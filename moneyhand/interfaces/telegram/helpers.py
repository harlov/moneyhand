from typing import List

from aiogram import types


def keyboard(items_matrix: List[List[str]]) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [types.KeyboardButton(text=item) for item in row] for row in items_matrix
        ],
    )


def unset_keyboard():
    return types.ReplyKeyboardRemove()
