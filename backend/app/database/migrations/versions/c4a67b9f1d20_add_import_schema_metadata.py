"""Add discovered schema metadata to data imports.

Revision ID: c4a67b9f1d20
Revises: 0a64dc90ea18
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "c4a67b9f1d20"
down_revision: Union[str, Sequence[str], None] = "0a64dc90ea18"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "data_imports",
        sa.Column(
            "schema_metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("data_imports", "schema_metadata")
