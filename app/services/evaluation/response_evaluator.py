from app.schemas.evaluation import (
    ResponseEvaluationRequest,
    ResponseEvaluationResult,
)


class ResponseEvaluator:
    NO_CONTEXT_PHRASES = [
        "could not find relevant context",
        "do not have enough context",
        "insufficient context",
        "please ingest relevant documents",
    ]

    def evaluate(self, request: ResponseEvaluationRequest) -> ResponseEvaluationResult:
        warnings: list[str] = []

        answer = request.answer.strip()
        answer_lower = answer.lower()

        has_empty_answer = len(answer) == 0
        has_sources = len(request.sources) > 0
        has_no_context_fallback = any(
            phrase in answer_lower for phrase in self.NO_CONTEXT_PHRASES
        )

        if has_empty_answer:
            warnings.append("Answer is empty.")

        if request.grounded and not has_sources:
            warnings.append("Response is marked grounded but has no sources.")

        if request.grounded and has_no_context_fallback:
            warnings.append(
                "Response is marked grounded but contains a no-context fallback."
            )

        if not request.grounded and has_sources:
            warnings.append("Response is marked ungrounded but includes sources.")

        if len(answer) < 20:
            warnings.append("Answer is very short and may be incomplete.")

        passed = len(warnings) == 0

        return ResponseEvaluationResult(
            passed=passed,
            grounded=request.grounded,
            source_count=len(request.sources),
            answer_length=len(answer),
            has_sources=has_sources,
            has_empty_answer=has_empty_answer,
            has_no_context_fallback=has_no_context_fallback,
            warnings=warnings,
        )
