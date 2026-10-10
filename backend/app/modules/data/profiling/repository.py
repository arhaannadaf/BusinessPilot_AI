
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.data.data_profile import DataProfile


class DataProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        data_import_id: UUID,
        report: dict,
    ) -> DataProfile:
        profile = DataProfile(
            data_import_id=data_import_id,
            row_count=report["row_count"],
            column_count=report["column_count"],
            column_profiles=report["columns"],
            duplicate_rows=report["duplicate_rows"],
        )

        self.session.add(profile)
        await self.session.flush()
        await self.session.refresh(profile)

        return profile

    async def get_by_id(
        self,
        profile_id: UUID,
    ) -> DataProfile | None:
        result = await self.session.execute(
            select(DataProfile).where(
                DataProfile.id == profile_id
            )
        )
        return result.scalar_one_or_none()

    async def list_by_import(
        self,
        data_import_id: UUID,
    ) -> list[DataProfile]:
        result = await self.session.execute(
            select(DataProfile)
            .where(
                DataProfile.data_import_id == data_import_id
            )
            .order_by(
                DataProfile.created_at.desc(),
                DataProfile.id.desc(),
            )
        )
        return list(result.scalars().all())
