"""add users

Revision ID: 6a7d08ff2003
Revises: c9bb721ac0ef
Create Date: 2020-11-29 08:52:54.356059

"""
from uuid import uuid4

from alembic import op
from alembic import context

import sqlalchemy as sa

import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = "6a7d08ff2003"
down_revision = "c9bb721ac0ef"
branch_labels = None
depends_on = None


def only_structure():
    return context.config.get_main_option("only_structure", "0") == "1"


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", pg.UUID, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("password_hash", sa.String, nullable=False),
        sa.Column("disabled", sa.Boolean, nullable=False, server_default="0"),
    )

    op.create_table(
        "tenants",
        sa.Column("id", pg.UUID, primary_key=True),
    )

    op.create_table(
        "tenant_users",
        sa.Column("id", pg.UUID, primary_key=True),
        sa.Column(
            "tenant_id",
            pg.UUID,
            sa.ForeignKey("tenants.id", deferrable=True),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            pg.UUID,
            sa.ForeignKey("users.id", deferrable=True),
            nullable=False,
        ),
    )

    op.create_table(
        "user_telegram_account",
        sa.Column("id", pg.UUID, primary_key=True),
        sa.Column(
            "user_id",
            pg.UUID,
            sa.ForeignKey("users.id", deferrable=True),
            nullable=False,
        ),
        sa.Column("telegram_user_id", sa.String, nullable=False),
        sa.Column("telegram_user_name", sa.String, nullable=False),
    )


def downgrade():
    pass
