from app.schemas.retrieval import RetrievalSearchResult
from app.services.context.budget import ContextBudgetManager


def make_result(text: str, score: float = 0.9) -> RetrievalSearchResult:
    return RetrievalSearchResult(
        chunk_id="chunk_1",
        document_id="doc_1",
        title="Test Document",
        text=text,
        score=score,
        chunk_index=0,
        source_type="raw_text",
        source_uri=None,
        access_level="private",
    )


def test_context_budget_selects_results_within_budget() -> None:
    manager = ContextBudgetManager(max_chars=100)
    results = [
        make_result("short text"),
        make_result("another short text"),
    ]

    selected, truncated = manager.select_results(results)

    assert len(selected) == 2
    assert truncated is False


def test_context_budget_truncates_when_budget_exceeded() -> None:
    manager = ContextBudgetManager(max_chars=20)
    results = [
        make_result("short text"),
        make_result("this text is definitely too long"),
    ]

    selected, truncated = manager.select_results(results)

    assert len(selected) == 1
    assert truncated is True
