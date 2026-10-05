"""add generated_chapters_count to stories

Revision ID: d5e8a1c74b20
Revises: a7c4e2b91d08
Create Date: 2026-10-05 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d5e8a1c74b20"
down_revision: Union[str, Sequence[str], None] = "a7c4e2b91d08"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "stories",
        sa.Column("generated_chapters_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.execute(
        """
        UPDATE stories
        SET generated_chapters_count = (
            SELECT COUNT(*)
            FROM story_chapters
            WHERE story_chapters.story_id = stories.id
        )
        """
    )
    op.alter_column("stories", "generated_chapters_count", server_default=None)


def downgrade() -> None:
    op.drop_column("stories", "generated_chapters_count")
