"""add image_url to stories

Revision ID: a7c4e2b91d08
Revises: e8b2c4a91f07
Create Date: 2026-10-04 17:33:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a7c4e2b91d08"
down_revision: Union[str, Sequence[str], None] = "e8b2c4a91f07"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("stories", sa.Column("image_url", sa.String(), nullable=True))
    op.execute("UPDATE stories SET image_url = NULL")


def downgrade() -> None:
    op.drop_column("stories", "image_url")
