from fastapi import APIRouter

from app.schemas.evaluation import (
    ResponseEvaluationRequest,
    ResponseEvaluationResponse,
)
from app.services.evaluation.response_evaluator import ResponseEvaluator

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.post("/response", response_model=ResponseEvaluationResponse)
def evaluate_response(
    request: ResponseEvaluationRequest,
) -> ResponseEvaluationResponse:
    evaluator = ResponseEvaluator()
    evaluation = evaluator.evaluate(request)

    return ResponseEvaluationResponse(
        query=request.query,
        evaluation=evaluation,
    )
