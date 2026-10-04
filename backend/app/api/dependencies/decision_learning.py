from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

from app.modules.decision.feedback.repository import (
    DecisionFeedbackRepository,
)
from app.modules.decision.learning.repository import (
    DecisionLearningRepository,
)
from app.modules.decision.learning.service import (
    DecisionLearningService,
)
from app.modules.decision.outcome.analysis.service import (
    OutcomeAnalysisService,
)
from app.modules.decision.outcome.repository import (
    OutcomeRepository,
)
from app.modules.decision.outcome.outcome_metric.repository import (
    OutcomeMetricRepository,
)
from app.modules.decision.execution.repository import (
    ExecutionRepository,
)
from app.modules.decision.recommendation.repository import (
    RecommendationRepository,
)

async def get_decision_learning_service(
    session: AsyncSession = Depends(get_db),
) -> DecisionLearningService:

    learning_repository = DecisionLearningRepository(
        session
    )

    feedback_repository = DecisionFeedbackRepository(
        session
    )

    outcome_repository = OutcomeRepository(
        session
    )

    outcome_metric_repository = OutcomeMetricRepository(
        session
    )

    outcome_analysis_service = OutcomeAnalysisService(
        outcome_repository=outcome_repository,
        outcome_metric_repository=outcome_metric_repository,
    )
    execution_repository = ExecutionRepository(session)

    recommendation_repository = RecommendationRepository(session)

    return DecisionLearningService(
    learning_repository=learning_repository,
    feedback_repository=feedback_repository,
    outcome_repository=outcome_repository,
    outcome_analysis_service=outcome_analysis_service,
    execution_repository=execution_repository,
    recommendation_repository=recommendation_repository,
)