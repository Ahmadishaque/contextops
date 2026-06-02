from app.core.config import settings
from app.services.agent.llm_provider import LLMProvider
from app.services.agent.mock_provider import MockLLMProvider
from app.services.agent.openai_provider import OpenAILLMProvider


def get_llm_provider() -> LLMProvider:
    provider_name = settings.llm_provider.lower().strip()

    if provider_name == "mock":
        return MockLLMProvider()

    if provider_name == "openai":
        return OpenAILLMProvider()

    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")
