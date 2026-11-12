
import os
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from uuid import UUID
import pytest
from sqlalchemy import select
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.database.models.data.data_import import DataImport
from app.database.models.data.data_profile import DataProfile
from app.database.models.data.data_quality_alert import DataQualityAlert
from app.database.models.data.staging_row import StagingRow
from app.modules.data.imports.repository import DataImportRepository
from app.modules.data.imports.staging_repository import StagingRowRepository
from app.modules.data.profiling.alert_repository import DataQualityAlertRepository
from app.modules.data.profiling.repository import DataProfileRepository
from app.modules.data.profiling.service import DataProfilingService
from app.database.models.data.data_source import DataSource

@pytest.mark.asyncio
async def test_profile_import_persists_quality_alert():
    database_url = os.environ["DATABASE_URL"]

    # Prevent accidental writes to the development database.
    assert make_url(database_url).database == "businesspilot_test_db"

    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    try:
        async with session_factory() as session:
            try:
                import_id = uuid4()
                data_source_id = uuid4()

                data_source = DataSource(
                    id=data_source_id,
                    organization_id=uuid4(),
                    name="Integration Test Source",
                    source_type="CSV",
                    connection_config={},
                    is_active=True,
                )
                session.add(data_source)
                await session.flush()

                data_import = DataImport(
                    id=import_id,
                    data_source_id=data_source_id,
                    file_name="integration-quality.csv",
                    status="COMPLETED",
                    total_rows=100,
                    successful_rows=100,
                    failed_rows=0,
                    file_size_bytes=0,
                )
                session.add(data_import)

                previous_profile = DataProfile(
                    data_import_id=import_id,
                    row_count=100,
                    column_count=1,
                    column_profiles=[
                        {
                            "column_name": "Name",
                            "inferred_type": "text",
                            "missing_count": 0,
                            "missing_percentage": 0.0,
                            "quality_status": "COMPLETE",
                            "distinct_count": 100,
                        }
                    ],
                    duplicate_rows=0,
                    total_cells=100,
                    completeness_percentage=100.0,
                    overall_quality_status="COMPLETE",
                    duplicate_status="NO_DUPLICATES",
                    created_at=datetime.now(timezone.utc)
                    - timedelta(days=1),
                )
                session.add(previous_profile)

                # Five missing values out of 100 rows produce
                # 95% completeness and a 5-point regression.
                session.add_all(
                    [
                        StagingRow(
                            data_import_id=import_id,
                            data_source_id=data_source_id,
                            row_number=row_number,
                            row_data={
    "Name": "" if row_number <= 5 else f"Example-{row_number}"
}
                        )
                        for row_number in range(1, 101)
                    ]
                )

                await session.flush()

                service = DataProfilingService(
                    data_import_repository=DataImportRepository(session),
                    staging_repository=StagingRowRepository(session),
                    profile_repository=DataProfileRepository(session),
                    alert_repository=DataQualityAlertRepository(session),
                )

                result = await service.profile_import(import_id)

                # Verify the service detected the regression.
                assert result["comparison"]["quality_regression"]["severity"] == (
                    "WARNING"
                )
                assert result["alert"] is not None
                assert result["alert"]["severity"] == "WARNING"

                # Verify the alert exists in PostgreSQL.
                query = select(DataQualityAlert).where(
                    DataQualityAlert.data_import_id == import_id
                )
                db_result = await session.execute(query)
                alert = db_result.scalar_one()

                assert alert.data_profile_id == UUID(str(result["profile_id"]))
                assert alert.data_import_id == import_id
                assert alert.severity == "WARNING"
                assert alert.alert_type == "COMPLETENESS_DROP"
                assert alert.status == "OPEN"
                assert alert.details["completeness_drop"] == 5.0

            finally:
                # Roll back all test records.
                await session.rollback()
    finally:
        await engine.dispose()
