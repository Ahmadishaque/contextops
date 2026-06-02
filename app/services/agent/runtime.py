from app.schemas.agent import AgentQueryRequest, AgentQueryResponse
from app.schemas.context import ContextAssembleRequest
from app.services.agent.grounded_responder import GroundedResponder
from app.services.context.assembler import ContextAssembler


class AgentRuntime:
    def __init__(self) -> None:
        self.context_assembler = ContextAssembler()
        self.responder = GroundedResponder()

    def answer(self, request: AgentQueryRequest) -> AgentQueryResponse:
        context_request = ContextAssembleRequest(
            query=request.query,
            limit=request.limit,
            access_level=request.access_level,
            max_context_chars=request.max_context_chars,
        )

        context_package = self.context_assembler.assemble(context_request)
        answer = self.responder.generate_answer(context_package)

        return AgentQueryResponse(
            query=request.query,
            answer=answer,
            grounded=context_package.source_count > 0,
            source_count=context_package.source_count,
            sources=context_package.sources,
        )
