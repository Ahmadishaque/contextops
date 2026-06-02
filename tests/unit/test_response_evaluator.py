from app.schemas.context import ContextSource
from app.schemas.evaluation import ResponseEvaluationRequest
from app.services.evaluation.response_evaluator import ResponseEvaluator


def make_source() -> ContextSource:
    return ContextSource(
        chunk_id="chunk_1",
        document_id="doc_1",
        title="Refund Policy",
        score=0.9,
        chunk_index=0,
        source_type="raw_text",
        source_uri=None,
        access_level="private",
    )


def test_response_evaluator_passes_grounded_response_with_sources() -> None:
    evaluator = ResponseEvaluator()
    request = ResponseEvaluationRequest(
        query="What should customers provide?",
        answer="Customers should provide account ID and invoice number.",
        grounded=True,
        sources=[make_source()],
    )

    result = evaluator.evaluate(request)

    assert result.passed is True
    assert result.has_sources is True
    assert result.source_count == 1
    assert result.warnings == []


def test_response_evaluator_warns_when_grounded_without_sources() -> None:
    evaluator = ResponseEvaluator()
    request = ResponseEvaluationRequest(
        query="What should customers provide?",
        answer="Customers should provide account ID and invoice number.",
        grounded=True,
        sources=[],
    )

    result = evaluator.evaluate(request)

    assert result.passed is False
    assert "Response is marked grounded but has no sources." in result.warnings


def test_response_evaluator_warns_on_no_context_fallback_when_grounded() -> None:
    evaluator = ResponseEvaluator()
    request = ResponseEvaluationRequest(
        query="What is the policy?",
        answer="I could not find relevant context to answer this question.",
        grounded=True,
        sources=[make_source()],
    )

    result = evaluator.evaluate(request)

    assert result.passed is False
    assert result.has_no_context_fallback is True
