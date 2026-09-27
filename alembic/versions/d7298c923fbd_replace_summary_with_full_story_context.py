"""replace summary with full_story_context

Revision ID: d7298c923fbd
Revises: 9716b1262cf6
Create Date: 2026-09-14 21:15:21.304742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7298c923fbd'
down_revision: Union[str, Sequence[str], None] = '9716b1262cf6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "stories",
        "summary",
        new_column_name="full_story_context",
    )


def downgrade() -> None:
    op.alter_column(
        "stories",
        "full_story_context",
        new_column_name="summary",
    )

