"""add income table

Revision ID: 278954a025c6
Revises: b7f6a29e722c
Create Date: 2020-10-16 09:11:54.608041

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = "278954a025c6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "incomes",
        sa.Column("id", pg.UUID, primary_key=True),
    )

    op.create_table(
        "income_items",
        sa.Column("id", pg.UUID, primary_key=True),
        sa.Column("income_id", pg.UUID, sa.ForeignKey("incomes.id", deferrable=True)),
        sa.Column("seq", sa.Integer, nullable=False),
        sa.Column("amount", sa.Float, nullable=False),
    )
    op.create_table(
        "categories",
        sa.Column("id", pg.UUID, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("type", sa.Integer, nullable=False, server_default="1"),
    )
    op.create_table(
        "spending_plan_items",
        sa.Column("id", pg.UUID, primary_key=True),
        sa.Column(
            "category_id", pg.UUID, sa.ForeignKey("categories.id"), nullable=False
        ),
        sa.Column("amount", sa.Float, nullable=False),
        sa.Column("seq_num", sa.Integer, nullable=False, server_default="1"),
    )


def downgrade():
    pass
