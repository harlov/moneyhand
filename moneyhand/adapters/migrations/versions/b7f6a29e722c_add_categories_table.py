"""add categories table

Revision ID: b7f6a29e722c
Revises: 
Create Date: 2020-10-14 20:48:51.920648

"""
from alembic import op
import sqlalchemy as sa

import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = 'b7f6a29e722c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "categories",
        sa.Column('id', pg.UUID, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
    )


def downgrade():
    op.drop_table("categories")
