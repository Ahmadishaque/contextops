from fastapi import APIRouter

from app.schemas.retrieval import RetrievalSearchRequest, RetrievalSearchResponse
from app.services.retrieval.retriever import SemanticRetriever

router = APIRouter(prefix="/retrieval", tags=["retrieval"])


@router.post("/search", response_model=RetrievalSearchResponse)
def search_chunks(request: RetrievalSearchRequest) -> RetrievalSearchResponse:
    retriever = SemanticRetriever()
    results = retriever.search(request)

    return RetrievalSearchResponse(
        query=request.query,
        result_count=len(results),
        results=results,
    )
