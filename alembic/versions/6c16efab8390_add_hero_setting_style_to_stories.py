"""add hero setting style to stories

Revision ID: 6c16efab8390
Revises: 1137faad3fbd
Create Date: 2026-09-14 15:28:50.486255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c16efab8390'
down_revision: Union[str, Sequence[str], None] = '1137faad3fbd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('stories', sa.Column('hero', sa.String(), nullable=False))
    op.add_column('stories', sa.Column('setting', sa.String(), nullable=False))
    op.add_column('stories', sa.Column('style', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('stories', 'style')
    op.drop_column('stories', 'setting')
    op.drop_column('stories', 'hero')
    
