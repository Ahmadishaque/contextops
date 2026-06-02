from openai import OpenAI

from app.core.config import settings
from app.services.agent.llm_provider import LLMProvider, LLMResponse


class OpenAILLMProvider(LLMProvider):
    def __init__(
        self,
        api_key: str = settings.openai_api_key,
        model: str = settings.openai_model,
    ) -> None:
        if not api_key or api_key == "replace_me":
            raise ValueError("OPENAI_API_KEY must be set when LLM_PROVIDER=openai")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=user_prompt,
        )

        return LLMResponse(
            text=response.output_text,
            provider="openai",
            model=self.model,
        )
