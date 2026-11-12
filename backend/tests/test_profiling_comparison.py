
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.modules.data.profiling.service import DataProfilingService


@pytest.mark.asyncio
async def test_compare_latest_profiles_detects_changes():
    import_id = "c6d54424-bba6-414e-9084-08ae64ee03a0"

    previous = SimpleNamespace(
        id="profile-old",
        row_count=505,
        column_count=3,
        completeness_percentage=100.0,
        duplicate_rows=0,
        duplicate_status="NO_DUPLICATES",
        overall_quality_status="COMPLETE",
        column_profiles=[
            {
                "column_name": "Name",
                "inferred_type": "text",
                "missing_count": 0,
                "missing_percentage": 0.0,
                "quality_status": "COMPLETE",
                "distinct_count": 505,
            }
        ],
    )

    latest = SimpleNamespace(
        id="profile-new",
        row_count=500,
        column_count=4,
        completeness_percentage=98.0,
        duplicate_rows=2,
        duplicate_status="DUPLICATES_FOUND",
        overall_quality_status="MINOR_ISSUES",
        column_profiles=[
            {
                "column_name": "Name",
                "inferred_type": "text",
                "missing_count": 10,
                "missing_percentage": 2.0,
                "quality_status": "MINOR_ISSUES",
                "distinct_count": 490,
            },
            {
                "column_name": "Revenue",
                "inferred_type": "decimal",
                "missing_count": 0,
                "missing_percentage": 0.0,
                "quality_status": "COMPLETE",
                "distinct_count": 500,
            },
        ],
    )

    import_repo = SimpleNamespace(
        get_by_id=AsyncMock(
            return_value=SimpleNamespace(
                id=import_id,
                data_source_id="source-1",
                file_name="sales.csv",
            )
        )
    )

    staging_repo = SimpleNamespace()
    profile_repo = SimpleNamespace(
        list_by_import=AsyncMock(return_value=[latest, previous])
    )

    service = DataProfilingService(
        import_repo,
        staging_repo,
        profile_repo,
    )

    result = await service.compare_latest_profiles(import_id)

    assert result["previous_profile_id"] == "profile-old"
    assert result["current_profile_id"] == "profile-new"

    changes = result["changes"]

    assert changes["row_count"]["delta"] == -5
    assert changes["column_count"]["delta"] == 1
    assert changes["completeness_percentage"]["delta"] == -2.0
    assert changes["duplicate_rows"]["delta"] == 2
    assert changes["duplicate_status"]["current"] == "DUPLICATES_FOUND"
    assert changes["overall_quality_status"]["current"] == "MINOR_ISSUES"

    column_changes = {
        item["column_name"]: item
        for item in changes["columns"]
    }

    assert column_changes["Name"]["change"] == "MODIFIED"
    assert column_changes["Revenue"]["change"] == "ADDED"

    assert "missing_count" in column_changes["Name"]["changed_fields"]

    profile_repo.list_by_import.assert_awaited_once()


@pytest.mark.asyncio
async def test_compare_latest_profiles_detects_removed_column():
    import_id = "test-import"

    previous = SimpleNamespace(
        id="profile-old",
        row_count=10,
        column_count=2,
        completeness_percentage=100.0,
        duplicate_rows=0,
        duplicate_status="NO_DUPLICATES",
        overall_quality_status="COMPLETE",
        column_profiles=[
            {
                "column_name": "Name",
                "inferred_type": "text",
                "missing_count": 0,
                "missing_percentage": 0.0,
                "quality_status": "COMPLETE",
                "distinct_count": 10,
            },
            {
                "column_name": "Revenue",
                "inferred_type": "decimal",
                "missing_count": 0,
                "missing_percentage": 0.0,
                "quality_status": "COMPLETE",
                "distinct_count": 10,
            },
        ],
    )

    latest = SimpleNamespace(
        id="profile-new",
        row_count=10,
        column_count=1,
        completeness_percentage=100.0,
        duplicate_rows=0,
        duplicate_status="NO_DUPLICATES",
        overall_quality_status="COMPLETE",
        column_profiles=[
            {
                "column_name": "Name",
                "inferred_type": "text",
                "missing_count": 0,
                "missing_percentage": 0.0,
                "quality_status": "COMPLETE",
                "distinct_count": 10,
            },
        ],
    )

    import_repo = SimpleNamespace(
        get_by_id=AsyncMock(
            return_value=SimpleNamespace(
                id=import_id,
                data_source_id="source-1",
                file_name="test.csv",
            )
        )
    )

    profile_repo = SimpleNamespace(
        list_by_import=AsyncMock(return_value=[latest, previous])
    )

    service = DataProfilingService(
        import_repo,
        SimpleNamespace(),
        profile_repo,
    )

    result = await service.compare_latest_profiles(import_id)

    assert result["changes"]["column_count"]["delta"] == -1

    column_changes = result["changes"]["columns"]

    assert len(column_changes) == 1
    assert column_changes[0]["column_name"] == "Revenue"
    assert column_changes[0]["change"] == "REMOVED"
    assert column_changes[0]["current"] is None


@pytest.mark.asyncio
async def test_compare_latest_profiles_detects_quality_degradation():
    import_id = "test-import"

    previous = SimpleNamespace(
        id="profile-old",
        row_count=100,
        column_count=1,
        completeness_percentage=100.0,
        duplicate_rows=0,
        duplicate_status="NO_DUPLICATES",
        overall_quality_status="COMPLETE",
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
    )

    latest = SimpleNamespace(
        id="profile-new",
        row_count=100,
        column_count=1,
        completeness_percentage=95.0,
        duplicate_rows=0,
        duplicate_status="NO_DUPLICATES",
        overall_quality_status="MINOR_ISSUES",
        column_profiles=[
            {
                "column_name": "Name",
                "inferred_type": "text",
                "missing_count": 5,
                "missing_percentage": 5.0,
                "quality_status": "MINOR_ISSUES",
                "distinct_count": 95,
            }
        ],
    )

    import_repo = SimpleNamespace(
        get_by_id=AsyncMock(
            return_value=SimpleNamespace(
                id=import_id,
                data_source_id="source-1",
                file_name="test.csv",
            )
        )
    )

    profile_repo = SimpleNamespace(
        list_by_import=AsyncMock(return_value=[latest, previous])
    )

    service = DataProfilingService(
        import_repo,
        SimpleNamespace(),
        profile_repo,
    )

    result = await service.compare_latest_profiles(import_id)

    changes = result["changes"]

    assert changes["completeness_percentage"]["delta"] == -5.0
    assert result["quality_regression"]["severity"] == "WARNING"
    assert result["quality_regression"]["completeness_drop"] == 5.0
    assert result["quality_regression"]["duplicate_rows_increase"] == 0
    assert "COMPLETENESS_DROP" in result["quality_regression"]["reasons"]

    assert changes["overall_quality_status"]["previous"] == "COMPLETE"
    assert changes["overall_quality_status"]["current"] == "MINOR_ISSUES"

    column_changes = {
        item["column_name"]: item
        for item in changes["columns"]
    }

    assert column_changes["Name"]["change"] == "MODIFIED"
    assert "missing_count" in column_changes["Name"]["changed_fields"]
    assert "quality_status" in column_changes["Name"]["changed_fields"]

@pytest.mark.asyncio
async def test_profile_import_first_run_has_no_comparison():
    import_id = "test-import"

    saved_profile = SimpleNamespace(
        id="profile-first",
        created_at=__import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ),
    )

    import_repo = SimpleNamespace(
        get_by_id=AsyncMock(
            return_value=SimpleNamespace(
                id=import_id,
                data_source_id="source-1",
                file_name="test.csv",
            )
        )
    )

    staging_repo = SimpleNamespace(
        list_by_import=AsyncMock(return_value=[])
    )

    profile_repo = SimpleNamespace(
        create=AsyncMock(return_value=saved_profile),
        list_by_import=AsyncMock(return_value=[saved_profile]),
    )

    service = DataProfilingService(
        import_repo,
        staging_repo,
        profile_repo,
    )

    result = await service.profile_import(import_id)

    assert result["profile_id"] == "profile-first"
    assert result["comparison"] is None

    profile_repo.create.assert_awaited_once()
    profile_repo.list_by_import.assert_awaited_once()
    

@pytest.mark.asyncio
async def test_row_count_change_without_quality_degradation():
    import_id = "test-import"

    previous_profile = SimpleNamespace(
        id="profile-previous",
        row_count=505,
        column_count=3,
        completeness_percentage=100.0,
        duplicate_rows=0,
        overall_quality_status="COMPLETE",
        duplicate_status="NO_DUPLICATES",
        column_profiles=[
            {
                "column_name": "Name",
                "inferred_type": "text",
                "missing_count": 0,
                "missing_percentage": 0.0,
                "quality_status": "COMPLETE",
                "distinct_count": 505,
            },
        ],
    )

    current_profile = SimpleNamespace(
        id="profile-current",
        row_count=500,
        column_count=3,
        completeness_percentage=100.0,
        duplicate_rows=0,
        overall_quality_status="COMPLETE",
        duplicate_status="NO_DUPLICATES",
        column_profiles=[
            {
                "column_name": "Name",
                "inferred_type": "text",
                "missing_count": 0,
                "missing_percentage": 0.0,
                "quality_status": "COMPLETE",
                "distinct_count": 500,
            },
        ],
    )

    import_repo = SimpleNamespace(
        get_by_id=AsyncMock(
            return_value=SimpleNamespace(id=import_id)
        )
    )

    profile_repo = SimpleNamespace(
        list_by_import=AsyncMock(
            return_value=[current_profile, previous_profile]
        )
    )

    service = DataProfilingService(
    import_repo,
    None,
    profile_repo,
)

    result = await service.compare_latest_profiles(import_id)

    assert result["changes"]["row_count"]["previous"] == 505
    assert result["changes"]["row_count"]["current"] == 500
    assert result["changes"]["row_count"]["delta"] == -5

    assert result["quality_regression"]["severity"] == "NO_REGRESSION"
    assert result["quality_regression"]["completeness_drop"] == 0.0
    assert result["quality_regression"]["duplicate_rows_increase"] == 0
    assert result["quality_regression"]["reasons"] == []


@pytest.mark.asyncio
async def test_warning_regression_creates_alert():
    alert_repository = SimpleNamespace(
        create=AsyncMock(
            return_value=SimpleNamespace(
                id="alert-123",
                severity="WARNING",
                alert_type="COMPLETENESS_DROP",
                message="Data quality regression detected: WARNING.",
                status="OPEN",
            )
        )
    )

    service = DataProfilingService(
        None,
        None,
        None,
        alert_repository,
    )

    regression = {
        "severity": "WARNING",
        "completeness_drop": 5.0,
        "duplicate_rows_increase": 0,
        "reasons": ["COMPLETENESS_DROP"],
    }

    result = await service._create_quality_alert_if_needed(
        import_id="test-import",
        profile_id="profile-current",
        regression=regression,
    )

    assert result["alert_id"] == "alert-123"
    assert result["severity"] == "WARNING"
    assert result["alert_type"] == "COMPLETENESS_DROP"
    assert result["status"] == "OPEN"

    alert_repository.create.assert_awaited_once_with(
        data_import_id="test-import",
        data_profile_id="profile-current",
        severity="WARNING",
        alert_type="COMPLETENESS_DROP",
        message="Data quality regression detected: WARNING. "
        "Reasons: COMPLETENESS_DROP.",
        details=regression,
    )


@pytest.mark.asyncio
async def test_no_regression_does_not_create_alert():
    alert_repository = SimpleNamespace(
        create=AsyncMock()
    )

    service = DataProfilingService(
        None,
        None,
        None,
        alert_repository,
    )

    regression = {
        "severity": "NO_REGRESSION",
        "completeness_drop": 0.0,
        "duplicate_rows_increase": 0,
        "reasons": [],
    }

    result = await service._create_quality_alert_if_needed(
        import_id="test-import",
        profile_id="profile-current",
        regression=regression,
    )

    assert result is None
    alert_repository.create.assert_not_awaited()

@pytest.mark.asyncio
async def test_profile_import_creates_alert_on_quality_regression():
    from datetime import datetime, timezone

    import_id = "test-import"
    now = datetime.now(timezone.utc)

    previous_profile = SimpleNamespace(
        id="profile-previous",
        created_at=now,
        row_count=100,
        column_count=1,
        completeness_percentage=100.0,
        duplicate_rows=0,
        duplicate_status="NO_DUPLICATES",
        overall_quality_status="COMPLETE",
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
    )

    current_profile = SimpleNamespace(
        id="profile-current",
        created_at=now,
        row_count=100,
        column_count=1,
        completeness_percentage=95.0,
        duplicate_rows=0,
        duplicate_status="NO_DUPLICATES",
        overall_quality_status="MINOR_ISSUES",
        column_profiles=[
            {
                "column_name": "Name",
                "inferred_type": "text",
                "missing_count": 5,
                "missing_percentage": 5.0,
                "quality_status": "MINOR_ISSUES",
                "distinct_count": 95,
            }
        ],
    )

    data_import = SimpleNamespace(
        id=import_id,
        data_source_id="source-1",
        file_name="sales.csv",
    )

    import_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=data_import)
    )

    staging_repo = SimpleNamespace(
        list_by_import=AsyncMock(
            return_value=[
                SimpleNamespace(row_data={"Name": "Example"})
            ]
        )
    )

    profile_repo = SimpleNamespace(
        create=AsyncMock(return_value=current_profile),
        list_by_import=AsyncMock(
            return_value=[current_profile, previous_profile]
        ),
    )

    saved_alert = SimpleNamespace(
        id="alert-123",
        severity="WARNING",
        alert_type="COMPLETENESS_DROP",
        message="Data quality regression detected: WARNING. "
        "Reasons: COMPLETENESS_DROP.",
        status="OPEN",
    )

    alert_repo = SimpleNamespace(
        create=AsyncMock(return_value=saved_alert)
    )

    service = DataProfilingService(
        import_repo,
        staging_repo,
        profile_repo,
        alert_repo,
    )

    service.processor.profile = lambda rows: {
        "row_count": 100,
        "column_count": 1,
        "columns": current_profile.column_profiles,
        "duplicate_rows": 0,
        "duplicate_status": "NO_DUPLICATES",
        "total_cells": 100,
        "completeness_percentage": 95.0,
        "overall_quality_status": "MINOR_ISSUES",
    }

    result = await service.profile_import(import_id)

    assert result["profile_id"] == "profile-current"
    assert result["comparison"]["quality_regression"]["severity"] == "WARNING"
    assert result["alert"]["alert_id"] == "alert-123"
    assert result["alert"]["severity"] == "WARNING"
    assert result["alert"]["status"] == "OPEN"

    profile_repo.create.assert_awaited_once()
    alert_repo.create.assert_awaited_once()
