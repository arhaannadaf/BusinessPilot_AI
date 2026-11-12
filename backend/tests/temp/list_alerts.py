import asyncio
import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from app.database.models.data.data_quality_alert import DataQualityAlert


async def main():
    engine = create_async_engine(os.environ["DATABASE_URL"])

    try:
        async with engine.connect() as conn:
            query = (
                select(
                    DataQualityAlert.id,
                    DataQualityAlert.severity,
                    DataQualityAlert.alert_type,
                    DataQualityAlert.data_import_id,
                )
                .order_by(DataQualityAlert.created_at.desc())
                .limit(10)
            )

            result = await conn.execute(query)
            rows = result.all()

            if not rows:
                print("No alerts found in this database.")
            else:
                for row in rows:
                    print(row)
    finally:
        await engine.dispose()


asyncio.run(main())
