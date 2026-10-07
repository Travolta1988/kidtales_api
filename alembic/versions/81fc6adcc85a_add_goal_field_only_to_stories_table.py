"""Add goal field only to stories table

Revision ID: 81fc6adcc85a
Revises: 799fc96c7f46
Create Date: 2026-10-07 15:45:24.340073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81fc6adcc85a'
down_revision: Union[str, Sequence[str], None] = '799fc96c7f46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column("stories", sa.Column("goal", sa.String(), nullable=True))
    op.execute("UPDATE stories SET goal = NULL")


def downgrade() -> None:
    op.drop_column("stories", "goal")