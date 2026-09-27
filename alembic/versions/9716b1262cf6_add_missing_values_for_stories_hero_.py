"""Add missing values for stories hero/style/settings fields

Revision ID: 9716b1262cf6
Revises: 6c16efab8390
Create Date: 2026-09-14 17:02:48.224432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9716b1262cf6'
down_revision: Union[str, Sequence[str], None] = '6c16efab8390'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE stories
        SET
            hero = COALESCE(hero, 'Unknown'),
            setting = COALESCE(setting, 'Unknown'),
            style = COALESCE(style, 'Unknown')
        WHERE hero IS NULL
           OR setting IS NULL
           OR style IS NULL
        """
    )
    op.alter_column("stories", "hero", existing_type=sa.String(), nullable=False)
    op.alter_column("stories", "setting", existing_type=sa.String(), nullable=False)
    op.alter_column("stories", "style", existing_type=sa.String(), nullable=False)



def downgrade() -> None:
    op.alter_column("stories", "style", existing_type=sa.String(), nullable=True)
    op.alter_column("stories", "setting", existing_type=sa.String(), nullable=True)
    op.alter_column("stories", "hero", existing_type=sa.String(), nullable=True)
