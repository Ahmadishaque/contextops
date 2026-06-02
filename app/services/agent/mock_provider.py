from app.services.agent.llm_provider import LLMProvider, LLMResponse


class MockLLMProvider(LLMProvider):
    def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        del system_prompt

        return LLMResponse(
            text=(
                "Mock LLM response generated from the grounded prompt.\n\n"
                f"{user_prompt[:1200]}"
            ),
            provider="mock",
            model="mock-grounded-model",
        )
