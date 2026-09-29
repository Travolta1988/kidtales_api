"""drop author and emoji from stories

Revision ID: b7e1a4c9d2f0
Revises: 0c924ced524d
Create Date: 2026-09-29 09:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7e1a4c9d2f0"
down_revision: Union[str, Sequence[str], None] = "0c924ced524d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("stories", "author")
    op.drop_column("stories", "emoji")


def downgrade() -> None:
    op.add_column("stories", sa.Column("author", sa.String(), nullable=False, server_default=""))
    op.add_column("stories", sa.Column("emoji", sa.String(), nullable=False, server_default=""))
    op.alter_column("stories", "author", server_default=None)
    op.alter_column("stories", "emoji", server_default=None)
