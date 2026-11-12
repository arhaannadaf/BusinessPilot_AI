"""Add duplicate status to data profiles

Revision ID: 93a3745d9e86
Revises: 7b42d06f4287
Create Date: 2026-10-11 12:42:13.475028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93a3745d9e86'
down_revision: Union[str, Sequence[str], None] = '7b42d06f4287'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "data_profiles",
        sa.Column(
            "duplicate_status",
            sa.String(length=30),
            server_default="NO_DUPLICATES",
            nullable=False,
        ),
    )

    # Backfill existing profiles using their actual duplicate counts.
    op.execute(
        """
        UPDATE data_profiles
        SET duplicate_status = CASE
            WHEN duplicate_rows > 0 THEN 'DUPLICATES_FOUND'
            ELSE 'NO_DUPLICATES'
        END
        """
    )

    # Keep the default in the SQLAlchemy model, not as a permanent DB default.
    op.alter_column(
        "data_profiles",
        "duplicate_status",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("data_profiles", "duplicate_status")

