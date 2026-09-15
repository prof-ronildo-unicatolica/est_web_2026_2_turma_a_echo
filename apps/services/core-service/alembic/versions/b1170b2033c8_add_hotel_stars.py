"""add hotel stars

Revision ID: b1170b2033c8
Revises: 6602e651ea28
Create Date: 2026-09-15 16:27:23.114809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b1170b2033c8"
down_revision: Union[str, None] = "6602e651ea28"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("hoteis", sa.Column("estrelas", sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column("hoteis", "estrelas")
