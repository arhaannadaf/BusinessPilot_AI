from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class ReferenceRepository:
    """
    Generic repository for all reference tables.
    """

    def __init__(
            self,
            db: AsyncSession,
    ): 
        self.db = db

    async def get_by_id(
            self,
            model: type,
            id: UUID,
    ):
        result = await self.db.execute(
            select(model).where(
                model.id == id
            )
        )

        return result.scalar_one_or_none()

    async def exists(
            self,
            model: type,
            id: UUID,
    ) -> bool:

        return(
            await self.get_by_id(model, id)
        ) is not None
        