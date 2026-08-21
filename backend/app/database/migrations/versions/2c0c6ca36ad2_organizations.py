"""organizations

Revision ID: 2c0c6ca36ad2
Revises: 9e8d46aabb36
Create Date: 2026-07-30 21:14:05.328304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c0c6ca36ad2'
down_revision: Union[str, Sequence[str], None] = '9e8d46aabb36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
