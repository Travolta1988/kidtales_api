"""Add next_options array with id and text (str) to story_chapters

Revision ID: 40948f1c9887
Revises: 4ea5ebc2d1ce
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "40948f1c9887"
down_revision: Union[str, Sequence[str], None] = "4ea5ebc2d1ce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "story_chapters",
        sa.Column(
            "next_options",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )


def downgrade() -> None:
    op.drop_column("story_chapters", "next_options")