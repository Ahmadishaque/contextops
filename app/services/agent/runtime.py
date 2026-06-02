from sqlalchemy.orm import Session

from app.schemas.agent import AgentQueryRequest, AgentQueryResponse
from app.schemas.context import ContextAssembleRequest
from app.services.agent.prompts import AgentPromptBuilder
from app.services.agent.provider_factory import get_llm_provider
from app.services.context.assembler import ContextAssembler
from app.services.tracing.trace_logger import AgentTraceLogger
from app.services.tracing.user_resolver import UserResolver


class AgentRuntime:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.context_assembler = ContextAssembler()
        self.prompt_builder = AgentPromptBuilder()
        self.llm_provider = get_llm_provider()
        self.user_resolver = UserResolver(db=db)

    def answer(self, request: AgentQueryRequest) -> AgentQueryResponse:
        user = self.user_resolver.get_or_create_user(email=request.owner_email)

        with AgentTraceLogger(db=self.db, user=user, query=request.query) as trace_logger:
            context_request = ContextAssembleRequest(
                query=request.query,
                limit=request.limit,
                access_level=request.access_level,
                max_context_chars=request.max_context_chars,
            )

            context_package = self.context_assembler.assemble(context_request)

            if context_package.source_count == 0:
                answer = (
                    "I could not find relevant context to answer this question. "
                    "Please ingest relevant documents or broaden the search filters."
                )
                trace = trace_logger.mark_success(response=answer)

                return AgentQueryResponse(
                    query=request.query,
                    answer=answer,
                    grounded=False,
                    source_count=0,
                    sources=[],
                    provider="none",
                    model="none",
                    trace_id=trace.id,
                    latency_ms=trace.latency_ms,
                )

            system_prompt = self.prompt_builder.build_system_prompt()
            user_prompt = self.prompt_builder.build_user_prompt(context_package)
            llm_response = self.llm_provider.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )

            trace = trace_logger.mark_success(
                response=llm_response.text,
                prompt_tokens=len(user_prompt.split()),
                completion_tokens=len(llm_response.text.split()),
            )

            return AgentQueryResponse(
                query=request.query,
                answer=llm_response.text,
                grounded=True,
                source_count=context_package.source_count,
                sources=context_package.sources,
                provider=llm_response.provider,
                model=llm_response.model,
                trace_id=trace.id,
                latency_ms=trace.latency_ms,
            )
