"""Add structured decision learning fields

Revision ID: 1bbe2c99b05c
Revises: 4c5ddbf076d2
Create Date: 2026-10-05 00:02:05.642670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bbe2c99b05c'
down_revision: Union[str, Sequence[str], None] = '4c5ddbf076d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "decision_learning",
        sa.Column(
            "decision_option_id",
            sa.UUID(),
            nullable=True,
        ),
    )

    op.create_index(
        op.f("ix_decision_learning_decision_option_id"),
        "decision_learning",
        ["decision_option_id"],
        unique=False,
    )

    op.create_foreign_key(
        None,
        "decision_learning",
        "decision_options",
        ["decision_option_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.add_column(
        "decision_learning",
        sa.Column(
            "metric_name",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "decision_learning",
        sa.Column(
            "performance",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "decision_learning",
        sa.Column(
            "variance_percentage",
            sa.Float(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "decision_learning",
        "variance_percentage",
    )

    op.drop_column(
        "decision_learning",
        "performance",
    )

    op.drop_column(
        "decision_learning",
        "metric_name",
    )

    op.drop_constraint(
        None,
        "decision_learning",
        type_="foreignkey",
    )

    op.drop_index(
        op.f("ix_decision_learning_decision_option_id"),
        table_name="decision_learning",
    )

    op.drop_column(
        "decision_learning",
        "decision_option_id",
    )
