
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.modules.data.profiling.alert_repository import (
    DataQualityAlertRepository,
)
from app.database.models.data.data_quality_alert import DataQualityAlert
from app.database.models.data.data_quality_alert_audit import (
    DataQualityAlertAudit,
)

@pytest.mark.asyncio
async def test_create_alert():
    session = MagicMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    async def mock_refresh(instance, *args, **kwargs):
        if hasattr(instance, "status") and instance.status is None:
            instance.status = "OPEN"
        return

    session.refresh = AsyncMock(side_effect=mock_refresh)

    repository = DataQualityAlertRepository(session)

    data_import_id = uuid4()
    data_profile_id = uuid4()

    alert = await repository.create(
        data_import_id=data_import_id,
        data_profile_id=data_profile_id,
        severity="WARNING",
        alert_type="COMPLETENESS_DROP",
        message="Data completeness dropped by 5 percentage points.",
        details={
            "completeness_drop": 5.0,
            "duplicate_rows_increase": 0,
            "reasons": ["COMPLETENESS_DROP"],
        },
    )

    assert alert.data_import_id == data_import_id
    assert alert.data_profile_id == data_profile_id
    assert alert.severity == "WARNING"
    assert alert.alert_type == "COMPLETENESS_DROP"
    assert alert.status == "OPEN"

    session.add.assert_called_once_with(alert)
    session.flush.assert_awaited_once()
    session.refresh.assert_awaited_once_with(alert)

@pytest.mark.asyncio
async def test_update_status_creates_audit_record():
    session = MagicMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()

    repository = DataQualityAlertRepository(session)

    alert = MagicMock()
    alert.id = uuid4()
    alert.status = "OPEN"

    updated_alert = await repository.update_status(
        alert,
        "ACKNOWLEDGED",
    )

    assert updated_alert.status == "ACKNOWLEDGED"

    # One audit object should have been added to the session.
    session.add.assert_called_once()
    audit = session.add.call_args.args[0]

    assert isinstance(audit, DataQualityAlertAudit)
    assert audit.data_quality_alert_id == alert.id
    assert audit.previous_status == "OPEN"
    assert audit.new_status == "ACKNOWLEDGED"
    assert audit.changed_by is None
    assert audit.change_reason is None

    session.flush.assert_awaited_once()
    session.refresh.assert_awaited_once_with(alert)


@pytest.mark.asyncio
async def test_update_status_same_status_does_not_create_audit():
    session = MagicMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()

    repository = DataQualityAlertRepository(session)

    alert = MagicMock()
    alert.id = uuid4()
    alert.status = "ACKNOWLEDGED"

    updated_alert = await repository.update_status(
        alert,
        "ACKNOWLEDGED",
    )

    assert updated_alert.status == "ACKNOWLEDGED"
    session.add.assert_not_called()
    session.flush.assert_not_awaited()
    session.refresh.assert_not_awaited()

@pytest.mark.asyncio
async def test_list_audit_history_orders_oldest_first():
    session = MagicMock()
    session.execute = AsyncMock()

    first_audit = MagicMock(spec=DataQualityAlertAudit)
    second_audit = MagicMock(spec=DataQualityAlertAudit)

    result = MagicMock()
    result.scalars.return_value.all.return_value = [
        first_audit,
        second_audit,
    ]
    session.execute.return_value = result

    repository = DataQualityAlertRepository(session)

    alert_id = uuid4()
    history = await repository.list_audit_history(alert_id)

    assert history == [first_audit, second_audit]
    session.execute.assert_awaited_once()

    query = session.execute.await_args.args[0]
    order_by_clauses = query._order_by_clauses

    assert len(order_by_clauses) == 2
    assert order_by_clauses[0].element.name == "created_at"
    assert order_by_clauses[0].modifier.__name__ == "asc_op"
    assert order_by_clauses[1].element.name == "id"
    assert order_by_clauses[1].modifier.__name__ == "asc_op"
