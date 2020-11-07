from typing import List, Dict
from uuid import UUID

from moneyhand.core import entities
from aiogram.utils import markdown

EMPTY = ""
NL = "\n"


def bold(s):
    return markdown.bold(s)


def categories_list(categories: List[entities.Category]) -> str:
    lines = [
        bold("Categories"),
        EMPTY,
    ] + [markdown.escape_md(f" - {category.name}") for category in categories]
    return NL.join(lines)


def income(_income: entities.Income) -> str:
    lines = [
        bold("Income"),
        EMPTY,
        f"Part 1: {bold(_income.part_1.amount)} {_income.currency}",
        f"Part 2: {bold(_income.part_2.amount)} {_income.currency}",
        EMPTY,
        f"Total: {bold(_income.total)} {_income.currency}",
    ]
    return NL.join(lines)


def normalize_length_to(s: str, length: int, fill_symb=" ") -> str:
    need_to_add = length - len(s)
    return s + fill_symb * need_to_add


def spending_plan(
    plan: entities.SpendingPlan, categories: List[entities.Category]
) -> str:

    category_map: Dict[UUID, entities.Category] = {
        category.id: category for category in categories
    }

    lines = [
        bold("Spending plan"),
        EMPTY,
    ]
    for item in plan.items:
        category = category_map[item.category_id]
        lines.append(
            f"{normalize_length_to(category.name, 20)}\t{bold(item.part_1.amount)}\t"
            f"{bold(item.part_2.amount)}"
        )

    return NL.join(lines)


def balance_report(report: entities.BalanceReport) -> str:
    lines = [
        bold("Balance report"),
        EMPTY,
        f"Part 1: {bold(report.part_1)}",
        f"Part 2: {bold(report.part_2)}",
    ]
    return NL.join(lines)
