import asyncio
import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from app.database.models.data.data_import import DataImport


async def main():
    engine = create_async_engine(os.environ["DATABASE_URL"])

    try:
        async with engine.connect() as conn:
            result = await conn.execute(
                select(
                    DataImport.id,
                    DataImport.file_name,
                    DataImport.status,
                    DataImport.data_source_id,
                ).order_by(DataImport.created_at.desc()).limit(10)
            )

            rows = result.all()

            if not rows:
                print("No data imports found in this database.")
            else:
                for row in rows:
                    print(row)
    finally:
        await engine.dispose()


asyncio.run(main())
