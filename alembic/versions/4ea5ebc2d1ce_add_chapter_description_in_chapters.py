"""add chapter_description in chapters

Revision ID: 4ea5ebc2d1ce
Revises: d7298c923fbd
Create Date: 2026-09-15 13:04:13.988315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ea5ebc2d1ce'
down_revision: Union[str, Sequence[str], None] = 'd7298c923fbd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column(
        "story",
        sa.Column("accent_color", sa.Text(), nullable=False, server_default=""),
    )
    op.alter_column("story", "accent_color", server_default=None)

def downgrade() -> None:
    op.drop_column("story", "accent_color")
