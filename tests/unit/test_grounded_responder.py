from app.schemas.context import ContextPackage, ContextSource
from app.services.agent.grounded_responder import GroundedResponder


def make_context_package(context_text: str) -> ContextPackage:
    return ContextPackage(
        query="What is the refund policy?",
        context_text=context_text,
        sources=[
            ContextSource(
                chunk_id="chunk_1",
                document_id="doc_1",
                title="Refund Policy",
                score=0.9,
                chunk_index=0,
                source_type="raw_text",
                source_uri=None,
                access_level="private",
            )
        ],
        source_count=1,
        total_context_chars=len(context_text),
        truncated=False,
    )


def test_grounded_responder_returns_fallback_when_no_context() -> None:
    responder = GroundedResponder()

    context_package = ContextPackage(
        query="Unknown question",
        context_text="",
        sources=[],
        source_count=0,
        total_context_chars=0,
        truncated=False,
    )

    answer = responder.generate_answer(context_package)

    assert "could not find relevant context" in answer
    assert "ingest relevant documents" in answer


def test_grounded_responder_uses_context_when_available() -> None:
    responder = GroundedResponder()
    context_package = make_context_package(
        "Enterprise customers must contact account support for refund requests."
    )

    answer = responder.generate_answer(context_package)

    assert "Based on the retrieved context" in answer
    assert "Enterprise customers must contact account support" in answer
    assert "Refund Policy" in answer
