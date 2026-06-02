from app.services.agent.mock_provider import MockLLMProvider
from app.services.agent.prompts import AgentPromptBuilder


def test_mock_provider_returns_grounded_prompt_preview() -> None:
    provider = MockLLMProvider()

    response = provider.generate(
        system_prompt="Answer only from context.",
        user_prompt="Retrieved context: enterprise customers must contact support.",
    )

    assert response.provider == "mock"
    assert response.model == "mock-grounded-model"
    assert "enterprise customers must contact support" in response.text


def test_prompt_builder_includes_context_and_question() -> None:
    from app.schemas.context import ContextPackage, ContextSource

    context_package = ContextPackage(
        query="What should customers provide?",
        context_text="Customers should provide account ID and invoice number.",
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
        total_context_chars=55,
        truncated=False,
    )

    user_prompt = AgentPromptBuilder.build_user_prompt(context_package)

    assert "What should customers provide?" in user_prompt
    assert "Customers should provide account ID" in user_prompt
    assert "Do not use outside knowledge" in user_prompt
