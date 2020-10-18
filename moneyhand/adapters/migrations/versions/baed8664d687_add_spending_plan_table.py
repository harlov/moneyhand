"""add spending plan table

Revision ID: baed8664d687
Revises: 278954a025c6
Create Date: 2020-10-19 08:47:10.701807

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = "baed8664d687"
down_revision = "278954a025c6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "spending_plan_items",
        sa.Column("id", pg.UUID, primary_key=True),
        sa.Column("category_id", pg.UUID, nullable=False),
        sa.Column("amount", sa.Float, nullable=False),
    )


def downgrade():
    pass
