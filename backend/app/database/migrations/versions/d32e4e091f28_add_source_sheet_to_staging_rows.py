"""Keep worksheet provenance for staged Excel rows.

Revision ID: d32e4e091f28
Revises: c4a67b9f1d20
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d32e4e091f28"
down_revision: str | Sequence[str] | None = "c4a67b9f1d20"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "staging_rows",
        sa.Column("source_sheet_name", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "staging_rows",
        sa.Column("source_row_number", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("staging_rows", "source_row_number")
    op.drop_column("staging_rows", "source_sheet_name")
