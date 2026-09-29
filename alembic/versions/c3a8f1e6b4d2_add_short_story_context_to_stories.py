"""add short_story_context to stories

Revision ID: c3a8f1e6b4d2
Revises: b7e1a4c9d2f0
Create Date: 2026-09-29 09:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c3a8f1e6b4d2"
down_revision: Union[str, Sequence[str], None] = "b7e1a4c9d2f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "stories",
        sa.Column("short_story_context", sa.String(), nullable=False, server_default=""),
    )
    op.alter_column("stories", "short_story_context", server_default=None)


def downgrade() -> None:
    op.drop_column("stories", "short_story_context")
