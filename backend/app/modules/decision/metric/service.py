from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.decision.decision import Decision
from app.database.models.decision.option import DecisionOption
from app.database.models.decision.metric import DecisionMetric

from app.modules.decision.metric.repository import DecisionMetricRepository

from app.modules.decision.metric.schemas import (
    DecisionMetricCreate,
    DecisionMetricUpdate,
)

class DecisionMetricService:
    def __init__(
            self,
            repository: DecisionMetricRepository,
            session: AsyncSession
    ) : 
        self.repository = repository
        self.session = session

    async def create_metric(
            self,
            data: DecisionMetricCreate,
            organization_id: UUID,
    ) -> DecisionMetric:

        result = await self.session.execute(
            select(DecisionOption)
            .join(
                Decision,
                Decision.id == DecisionOption.decision_id
            )
            .where(
                DecisionOption.id == data.decision_option_id,
                Decision.organization_id == organization_id
            )
        )

        option = result.scalar_one_or_none()

        if option is None:
            raise ValueError(
                "Decision option not found for this organization."
            )

        metric = DecisionMetric(
            decision_option_id=data.decision_option_id,
            metric_name=data.metric_name,
            value=data.value,
            unit=data.unit,
            direction=data.direction,
            source=data.source,
            meta_data=data.meta_data,
        )

        return await self.repository.create(metric)

    async def get_metric(
            self,
            metric_id: UUID,
            decision_option_id: UUID,
            organization_id: UUID,
    ) -> DecisionMetric | None:

        result = await self.session.execute(
            select(DecisionOption)
            .join(
                Decision,
                Decision.id == DecisionOption.decision_id,
            )
            .where(
                DecisionOption.id == decision_option_id,
                Decision.organization_id == organization_id,
            )
        )

        option = result.scalar_one_or_none()

        if option is None:
            return None

        return await self.repository.get_by_id(
            metric_id=metric_id,
            decision_option_id=decision_option_id,
        )

    async def list_metrics(
            self,
            decision_option_id:UUID,
            organization_id:UUID,
            skip: int = 0,
            limit: int =100,

    ) -> list[DecisionMetric]:

        result = await self.session.execute(
            select(DecisionOption)
            .join(
                Decision,
                Decision.id ==DecisionOption.decision_id,
            )
            .where(
                DecisionOption.id == decision_option_id,
                Decision.organization_id == organization_id,
            )
        )

        option = result.scalar_one_or_none()

        if option is None:
            return []

        return await self.repository.list_by_option(
            decision_option_id=decision_option_id,
            skip=skip,
            limit=limit,
        )

    async def update_metric(
            self,
            metric_id:UUID,
            decision_option_id: UUID,
            data: DecisionMetricUpdate,
            organization_id:UUID,
    ) -> DecisionMetric | None:

        metric = await self.get_metric(
            metric_id=metric_id,
            decision_option_id=decision_option_id,
            organization_id=organization_id,
        )

        if metric is None:
            return None

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(metric, field,value)

        return await self.repository.update(metric)

    async def delete_metric(
            self,
            metric_id: UUID,
            decision_option_id: UUID,
            organization_id:UUID,
    ) -> bool:

        metric = await self.get_metric(
            metric_id=metric_id,
            decision_option_id=decision_option_id,
            organization_id=organization_id
        )

        if metric is None:
            return False

        await self.repository.delete(metric)

        return True