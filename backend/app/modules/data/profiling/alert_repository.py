
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.data.data_quality_alert import DataQualityAlert
from app.database.models.data.data_quality_alert_audit import (
    DataQualityAlertAudit,
      DataQualityAlertAudit,)  

class DataQualityAlertRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        data_import_id: UUID,
        data_profile_id: UUID,
        severity: str,
        alert_type: str,
        message: str,
        details: dict,
    ) -> DataQualityAlert:
        alert = DataQualityAlert(
            data_import_id=data_import_id,
            data_profile_id=data_profile_id,
            severity=severity,
            alert_type=alert_type,
            message=message,
            details=details,
        )

        self.session.add(alert)
        await self.session.flush()
        await self.session.refresh(alert)

        return alert

    async def get_by_id(
        self,
        alert_id: UUID,
    ) -> DataQualityAlert | None:
        result = await self.session.execute(
            select(DataQualityAlert).where(
                DataQualityAlert.id == alert_id
            )
        )
        return result.scalar_one_or_none()

    async def list_by_import(
        self,
        data_import_id: UUID,
    ) -> list[DataQualityAlert]:
        result = await self.session.execute(
            select(DataQualityAlert)
            .where(DataQualityAlert.data_import_id == data_import_id)
            .order_by(
                DataQualityAlert.created_at.desc(),
                DataQualityAlert.id.desc(),
            )
        )
        return list(result.scalars().all())

    
    
    async def update_status(
        self,
        alert: DataQualityAlert,
        status: str,
        *,
        changed_by: UUID | None = None,
        change_reason: str | None = None,
    ) -> DataQualityAlert:
        previous_status = alert.status

        # Do not create audit records for unchanged status.
        if previous_status == status:
            return alert

        # Update the alert.
        alert.status = status

        # Record the transition in the same database session.
        audit = DataQualityAlertAudit(
            data_quality_alert_id=alert.id,
            previous_status=previous_status,
            new_status=status,
            changed_by=changed_by,
            change_reason=change_reason,
        )

        self.session.add(audit)

        # Flush both changes within the current transaction.
        await self.session.flush()
        await self.session.refresh(alert)

        return alert

    
    async def list_audit_history(
        self,
        alert_id: UUID,
    ) -> list[DataQualityAlertAudit]:
        result = await self.session.execute(
            select(DataQualityAlertAudit)
            .where(
                DataQualityAlertAudit.data_quality_alert_id
                == alert_id
            )
            .order_by(
                DataQualityAlertAudit.created_at.asc(),
                DataQualityAlertAudit.id.asc(),
            )
        )

        return list(result.scalars().all())


