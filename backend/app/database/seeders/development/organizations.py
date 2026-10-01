from app.database.models.identity.organization import Organization

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def seed_organizations(session: AsyncSession) -> None:

    existing = await session.scalar(
        select(Organization).where(
            Organization.domain == "businesspilot.ai"
        )
    )

    if existing:
        print("BusinessPilot Organization already exists.")
        return

    session.add(
        Organization(
            name="BusinessPilot",
            domain="businesspilot.ai",
            is_active=True,
        )
    )

    print("BusinessPilot Organization created")