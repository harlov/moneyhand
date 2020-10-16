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
down_revision = "b7f6a29e722c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "incomes",
        sa.Column("id", pg.UUID, primary_key=True),
        sa.Column("seq_num", sa.Integer, nullable=False),
        sa.Column("amount", sa.Float, nullable=False),
    )


def downgrade():
    pass
