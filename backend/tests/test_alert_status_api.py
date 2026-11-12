
from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.data.profiling.dependencies import (
    get_data_profiling_service,
)



class FakeAlertRepository:
    def __init__(self):
        self.alerts = {}
        self.audit_history = {}

    async def get_by_id(self, alert_id):
        return self.alerts.get(alert_id)

    async def update_status(self, alert, status):
        previous_status = alert.status

        if previous_status == status:
            return alert

        now = datetime.now(timezone.utc)

        audit = SimpleNamespace(
            id=uuid4(),
            data_quality_alert_id=alert.id,
            previous_status=previous_status,
            new_status=status,
            changed_by=None,
            change_reason=None,
            created_at=now,
            updated_at=now,
        )

        self.audit_history.setdefault(alert.id, []).append(audit)

        alert.status = status
        alert.updated_at = now
        return alert

    async def list_audit_history(self, alert_id):
        return self.audit_history.get(alert_id, [])


@pytest.fixture
def alert_api():
    alert_id = uuid4()
    now = datetime.now(timezone.utc)

    alert = SimpleNamespace(
        id=alert_id,
        data_import_id=uuid4(),
        data_profile_id=uuid4(),
        severity="WARNING",
        alert_type="COMPLETENESS_DROP",
        message="Data quality regression detected.",
        details={"completeness_drop": 5.0},
        status="OPEN",
        created_at=now,
        updated_at=now,
    )

    repository = FakeAlertRepository()
    repository.alerts[alert_id] = alert

    service = SimpleNamespace(alert_repository=repository)

    def override_service():
        return service

    app.dependency_overrides[
        get_data_profiling_service
    ] = override_service

    with TestClient(app) as client:
        yield client, alert_id, repository

    app.dependency_overrides.pop(
        get_data_profiling_service, None
    )


def test_open_to_acknowledged(alert_api):
    client, alert_id, _ = alert_api

    response = client.patch(
        f"/api/data-profiling/alerts/{alert_id}/status",
        json={"status": "ACKNOWLEDGED"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ACKNOWLEDGED"


def test_acknowledged_to_resolved(alert_api):
    client, alert_id, repository = alert_api
    repository.alerts[alert_id].status = "ACKNOWLEDGED"

    response = client.patch(
        f"/api/data-profiling/alerts/{alert_id}/status",
        json={"status": "RESOLVED"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "RESOLVED"


def test_resolved_to_open_is_rejected(alert_api):
    client, alert_id, repository = alert_api
    repository.alerts[alert_id].status = "RESOLVED"

    response = client.patch(
        f"/api/data-profiling/alerts/{alert_id}/status",
        json={"status": "OPEN"},
    )

    assert response.status_code == 409
    assert "Cannot transition alert" in response.json()["detail"]
    assert repository.alerts[alert_id].status == "RESOLVED"


def test_invalid_status_is_rejected(alert_api):
    client, alert_id, _ = alert_api

    response = client.patch(
        f"/api/data-profiling/alerts/{alert_id}/status",
        json={"status": "INVALID"},
    )

    assert response.status_code == 422


def test_missing_alert_returns_404(alert_api):
    client, _, _ = alert_api

    response = client.patch(
        f"/api/data-profiling/alerts/{uuid4()}/status",
        json={"status": "ACKNOWLEDGED"},
    )

    assert response.status_code == 404


def test_repeating_current_status_is_idempotent(alert_api):
    client, alert_id, _ = alert_api

    response = client.patch(
        f"/api/data-profiling/alerts/{alert_id}/status",
        json={"status": "OPEN"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "OPEN"

def test_get_alert_history_returns_status_transitions(alert_api):
    client, alert_id, repository = alert_api

    # Create a transition through the fake repository.
    alert = repository.alerts[alert_id]

    import asyncio
    asyncio.run(repository.update_status(alert, "ACKNOWLEDGED"))

    response = client.get(
        f"/api/data-profiling/alerts/{alert_id}/history"
    )

    assert response.status_code == 200

    history = response.json()
    assert len(history) == 1
    assert history[0]["previous_status"] == "OPEN"
    assert history[0]["new_status"] == "ACKNOWLEDGED"
    assert history[0]["data_quality_alert_id"] == str(alert_id)


def test_get_alert_history_returns_404_for_missing_alert(alert_api):
    client, _, _ = alert_api

    response = client.get(
        f"/api/data-profiling/alerts/{uuid4()}/history"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Data quality alert not found."
