"""Add language field only to stories table

Revision ID: 799fc96c7f46
Revises: d5e8a1c74b20
Create Date: 2026-10-06 12:43:54.453788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '799fc96c7f46'
down_revision: Union[str, Sequence[str], None] = 'd5e8a1c74b20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("stories", sa.Column("language", sa.String(), default="en"))
    op.execute("UPDATE stories SET language = 'en'")


def downgrade() -> None:
    op.drop_column("stories", "language")
