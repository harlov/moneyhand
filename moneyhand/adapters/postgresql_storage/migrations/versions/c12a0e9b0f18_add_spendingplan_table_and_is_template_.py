"""add SpendingPlan table and is_template flags

Revision ID: c12a0e9b0f18
Revises: 278954a025c6
Create Date: 2020-11-07 22:16:20.832081

"""
from uuid import uuid4

from alembic import op
from alembic import context

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = "c12a0e9b0f18"
down_revision = "278954a025c6"
branch_labels = None
depends_on = None


def only_structure():
    return context.config.get_main_option("only_structure", "0") == "1"


def upgrade():
    spending_plan_tbl = op.create_table(
        "spending_plans",
        sa.Column("id", pg.UUID, primary_key=True),
        sa.Column("is_template", sa.Boolean, nullable=False),
    )

    template_plan_id = str(uuid4())

    if not only_structure():
        op.bulk_insert(
            spending_plan_tbl, [{"id": template_plan_id, "is_template": True}]
        )

    op.add_column(
        "spending_plan_items",
        sa.Column(
            "spending_plan_id",
            pg.UUID(),
            sa.ForeignKey("spending_plans.id"),
            nullable=True,
        ),
    )

    if not only_structure():
        op.execute(
            f"UPDATE spending_plan_items SET spending_plan_id = '{template_plan_id}';"
        )

    op.alter_column(
        "spending_plan_items",
        sa.Column("spending_plan_id", pg.UUID(), sa.ForeignKey("spending_plan.id")),
    )

    op.add_column("incomes", sa.Column("is_template", sa.Boolean, nullable=True))

    op.execute("UPDATE incomes SET is_template=true;")

    op.alter_column("incomes", sa.Column("is_template", sa.Boolean))


def downgrade():
    pass
