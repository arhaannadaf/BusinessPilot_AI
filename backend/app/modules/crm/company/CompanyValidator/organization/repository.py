from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.identity.organization import Organization

class OrganizationRepository:
    """
    Repository for Organization database operation.
    """

    def __init__(
            self,
            db:AsyncSession,
    ):
        self.db = db

    async def get_by_id(
            self,
            organization_id: UUID,

    ) -> Organization | None:

        result = await self.db.execute(
            select(Organization).where(
                Organization.id == organization_id
            )
        )

        return result.scalar_one_or_none()

    async def exists(
            self,
            organization_id:UUID,

    ) -> bool:
        return(
            await self.get_by_id(organization_id)
        ) is not None