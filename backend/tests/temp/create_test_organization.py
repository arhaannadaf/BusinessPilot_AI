import asyncio
import os

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.database.models.identity.organization import Organization


async def main():
    url = make_url(os.environ["DATABASE_URL"])

    if url.database != "businesspilot_test_db" or url.port != 5433:
        raise RuntimeError(
            "Safety check failed: expected businesspilot_test_db on port 5433"
        )

    engine = create_async_engine(url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with session_factory() as session:
            organization = Organization(
                name="BusinessPilot API Test",
                domain="businesspilot-api-test.local",
                is_active=True,
            )
            session.add(organization)
            await session.commit()
            await session.refresh(organization)

            print("Organization created successfully.")
            print("Organization ID:", organization.id)
            print("Organization name:", organization.name)
    finally:
        await engine.dispose()


asyncio.run(main())
