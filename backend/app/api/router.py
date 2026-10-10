from fastapi import APIRouter

from app.api.v1.router import router as v1_router

from app.modules.crm.company.router import router as company_router
from app.modules.reference.industry.router import router as industry_router
from app.modules.reference.company_size.router import router as company_size_router
from app.modules.reference.company_status.router import router as company_status_router
from app.modules.reference.country.router import router as country_router
from app.modules.reference.currency.router import router as currency_router
from app.modules.decision.scenario.router import router as scenario_router
from app.modules.decision.decision.router import router as decision_router
from app.modules.decision.option.router import router as decision_option_router
from app.modules.decision.metric.router import router as decision_metric_router
from app.modules.decision.recommendation.router import router as recommendation_router
from app.modules.decision.execution.router import router as execution_router
from app.modules.decision.outcome.router import router as outcome_router
from app.modules.decision.outcome.outcome_metric.router import router as outcome_metric_router
from app.modules.decision.outcome.analysis.router import router as outcome_analysis_router
from app.modules.decision.feedback.router import router as feedback_router
from app.modules.decision.learning.router import router as decision_learning_router
from app.modules.data.source.router import router as data_source_router
from app.modules.data.imports.router import router as data_import_router
from app.modules.data.profiling.router import router as data_profiling_router

router = APIRouter()

router.include_router(
    v1_router,
    prefix="/v1",
    tags=["API v1"],
)

router.include_router(company_router)

router.include_router(industry_router)

router.include_router(company_size_router)

router.include_router(company_status_router)

router.include_router(country_router)

router.include_router(currency_router)

router.include_router(scenario_router)

router.include_router(decision_router)

router.include_router(decision_option_router)

router.include_router(decision_metric_router)

router.include_router(recommendation_router)

router.include_router(execution_router)

router.include_router(outcome_router)

router.include_router(outcome_metric_router)

router.include_router(outcome_analysis_router)

router.include_router(feedback_router)

router.include_router(decision_learning_router)

router.include_router(data_source_router)

router.include_router(data_import_router)

router.include_router(data_profiling_router)