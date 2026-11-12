
import asyncio
from sqlalchemy import select

from app.database.session import SessionLocal
from app.database.models.data.data_import import DataImport
from app.database.models.data.data_profile import DataProfile
from app.database.models.data.data_quality_alert import DataQualityAlert


async def main():
    import_id = "66e4edf5-5025-4bd3-8e2a-1974738482c2"

    async with SessionLocal() as session:
        data_import = await session.get(DataImport, import_id)

        if data_import is None:
            print("Import not found in the configured database.")
            return

        result = await session.execute(
            select(DataProfile)
            .where(DataProfile.data_import_id == data_import.id)
            .order_by(
                DataProfile.created_at.desc(),
                DataProfile.id.desc(),
            )
            .limit(1)
        )
        profile = result.scalar_one_or_none()

        if profile is None:
            print("No profile found for this import.")
            return

        alert = DataQualityAlert(
            data_import_id=data_import.id,
            data_profile_id=profile.id,
            severity="WARNING",
            alert_type="AUDIT_TEST",
            message="Temporary alert for testing status transition audit history.",
            details={"temporary_test": True},
            status="OPEN",
        )

        session.add(alert)
        await session.commit()
        await session.refresh(alert)

        print("Test alert created.")
        print("Alert ID:", alert.id)
        print("Status:", alert.status)


if __name__ == "__main__":
    asyncio.run(main())
