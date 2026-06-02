from app.schemas.agent import AgentQueryRequest, AgentQueryResponse
from app.schemas.context import ContextAssembleRequest
from app.services.agent.prompts import AgentPromptBuilder
from app.services.agent.provider_factory import get_llm_provider
from app.services.context.assembler import ContextAssembler


class AgentRuntime:
    def __init__(self) -> None:
        self.context_assembler = ContextAssembler()
        self.prompt_builder = AgentPromptBuilder()
        self.llm_provider = get_llm_provider()

    def answer(self, request: AgentQueryRequest) -> AgentQueryResponse:
        context_request = ContextAssembleRequest(
            query=request.query,
            limit=request.limit,
            access_level=request.access_level,
            max_context_chars=request.max_context_chars,
        )

        context_package = self.context_assembler.assemble(context_request)

        if context_package.source_count == 0:
            return AgentQueryResponse(
                query=request.query,
                answer=(
                    "I could not find relevant context to answer this question. "
                    "Please ingest relevant documents or broaden the search filters."
                ),
                grounded=False,
                source_count=0,
                sources=[],
                provider="none",
                model="none",
            )

        system_prompt = self.prompt_builder.build_system_prompt()
        user_prompt = self.prompt_builder.build_user_prompt(context_package)
        llm_response = self.llm_provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return AgentQueryResponse(
            query=request.query,
            answer=llm_response.text,
            grounded=True,
            source_count=context_package.source_count,
            sources=context_package.sources,
            provider=llm_response.provider,
            model=llm_response.model,
        )
