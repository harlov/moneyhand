from typing import List, Dict
from uuid import UUID

from aiogram.utils import markdown

from moneyhand.core import entities
from moneyhand.adapters import graph_render

EMPTY = ""
NL = "\n"


def bold(s: str) -> str:
    return markdown.bold(s)


def italic(s: str) -> str:
    return markdown.italic(s)


def es(s) -> str:
    return markdown.escape_md(s)


def categories_list(
    categories: List[entities.Category],
) -> str:
    lines = [bold("Categories"), EMPTY, italic("Goals: "), EMPTY]
    for category in filter(
        lambda c: c.type == entities.CategoryType.GOAL,
        categories,
    ):
        lines.append(es(f" - {category.name}"))

    lines.append(EMPTY)
    lines.append(italic("Necessary: "))
    lines.append(EMPTY)
    for category in filter(
        lambda c: c.type == entities.CategoryType.NECESSARY,
        categories,
    ):
        lines.append(es(f" - {category.name}"))

    return f"{NL.join(lines)}"


def income(_income: entities.Income) -> str:
    lines = [
        bold("Income"),
        EMPTY,
        f"Part 1: {bold(_income.part_1)} {_income.currency}",
        f"Part 2: {bold(_income.part_2)} {_income.currency}",
        EMPTY,
        f"Total: {bold(_income.total)} {_income.currency}",
    ]
    return NL.join(lines)


def normalize_length_to(s: str, length: int, fill_symb=" ") -> str:
    need_to_add = length - len(s)
    return s + fill_symb * need_to_add


def spending_plan_img(
    plan: entities.SpendingPlan,
    categories: List[entities.Category],
):
    category_map: Dict[UUID, entities.Category] = {
        category.id: category for category in categories
    }

    return graph_render.render_table(
        ["Category", "Part 1 amount", "Part 2 amount"],
        [
            [category_map[item.category_id].name, item.part_1, item.part_2]
            for item in plan.items
        ],
    )


def balance_report(report: entities.BalanceReport) -> str:
    lines = [
        bold("Balance report"),
        EMPTY,
        f"Part 1: {bold(report.part_1)} {report.currency}",
        f"Part 2: {bold(report.part_2)} {report.currency}",
    ]
    return NL.join(lines)
