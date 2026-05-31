from app.schemas.context import (
    ContextAssembleRequest,
    ContextPackage,
    ContextSource,
)
from app.schemas.retrieval import RetrievalSearchRequest
from app.services.context.budget import ContextBudgetManager
from app.services.context.formatter import ContextFormatter
from app.services.retrieval.retriever import SemanticRetriever


class ContextAssembler:
    def __init__(self) -> None:
        self.retriever = SemanticRetriever()
        self.formatter = ContextFormatter()

    def assemble(self, request: ContextAssembleRequest) -> ContextPackage:
        retrieval_request = RetrievalSearchRequest(
            query=request.query,
            limit=request.limit,
            access_level=request.access_level,
        )

        retrieval_results = self.retriever.search(retrieval_request)

        budget_manager = ContextBudgetManager(max_chars=request.max_context_chars)
        selected_results, truncated = budget_manager.select_results(retrieval_results)

        context_text = self.formatter.format_results(selected_results)

        sources = [
            ContextSource(
                chunk_id=result.chunk_id,
                document_id=result.document_id,
                title=result.title,
                score=result.score,
                chunk_index=result.chunk_index,
                source_type=result.source_type,
                source_uri=result.source_uri,
                access_level=result.access_level,
            )
            for result in selected_results
        ]

        return ContextPackage(
            query=request.query,
            context_text=context_text,
            sources=sources,
            source_count=len(sources),
            total_context_chars=len(context_text),
            truncated=truncated,
        )
