import asyncio
import os

from sqlalchemy import select
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from app.database.models.data.data_source import DataSource


async def main():
    url = make_url(os.environ["DATABASE_URL"])

    if url.database != "businesspilot_test_db" or url.port != 5433:
        raise RuntimeError(
            "Safety check failed: expected businesspilot_test_db on port 5433"
        )

    engine = create_async_engine(url)

    try:
        async with engine.connect() as conn:
            result = await conn.execute(
                select(DataSource.id, DataSource.name).limit(10)
            )
            rows = result.all()

            if rows:
                for row in rows:
                    print(row)
            else:
                print("No data sources found.")
    finally:
        await engine.dispose()


asyncio.run(main())
