from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_model(
    session: AsyncSession,
    model: type,
    data: list[dict[str, Any]],
    unique_field: str = "code",
) -> None:
    """
    Seed a SQLAlchemy model while preventing duplicate records.

    Args:
        session: Active SQLAlchemy session.
        model: SQLAlchemy model class.
        data: List of dictionaries to insert.
        unique_field: Field used to detect existing records.
    """

    for item in data:
        result = await session.scalar(
            select(model).where(
                getattr(model, unique_field) == item[unique_field]
            )
        )

        if result:
            continue

        session.add(model(**item))