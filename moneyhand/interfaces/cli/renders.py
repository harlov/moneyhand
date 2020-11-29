from typing import List

from moneyhand.core import entities


def category(e: entities.Category) -> str:
    return f"{e.name}        (ID / {e.id})"


def categories_list(
    categories: List[entities.Category],
) -> str:
    return "\n".join((f" -   {category(c)}" for c in categories))


def income(e: entities.Income) -> str:
    return "\n".join(
        [
            f"  part 1: {e.part_1.amount} {e.currency}",
            f"  part 2: {e.part_2.amount} {e.currency}",
            "---",
            f"Total: {e.total} {e.currency}.",
        ]
    )


def spending_plan(
    e: entities.SpendingPlan,
    categories: List[entities.Category],
) -> str:

    categories_map = {c.id: c for c in categories}

    res = "Spending plan\n"
    res += "\n".join(
        f"  -   {category(categories_map[item.category_id])}                 {item.part_1.amount}     {item.part_2.amount}"
        for item in e.items
    )

    return res
