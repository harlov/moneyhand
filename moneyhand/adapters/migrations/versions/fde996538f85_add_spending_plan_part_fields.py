"""add spending plan part fields

Revision ID: fde996538f85
Revises: baed8664d687
Create Date: 2020-10-19 18:44:41.805879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fde996538f85"
down_revision = "baed8664d687"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "spending_plan_items",
        sa.Column("seq_num", sa.Integer, nullable=False, server_default="1"),
    )


def downgrade():
    pass
