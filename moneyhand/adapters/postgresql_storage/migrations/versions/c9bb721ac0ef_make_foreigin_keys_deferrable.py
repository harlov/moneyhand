"""make foreigin keys deferrable

Revision ID: c9bb721ac0ef
Revises: c12a0e9b0f18
Create Date: 2020-11-08 21:05:00.322817

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = "c9bb721ac0ef"
down_revision = "c12a0e9b0f18"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "income_items",
        sa.Column("income_id", pg.UUID, sa.ForeignKey("incomes.id", deferrable=True)),
    )

    op.alter_column(
        "spending_plan_items",
        sa.Column(pg.UUID(), sa.ForeignKey("spending_plans.id", deferrable=True)),
    )


def downgrade():
    pass
