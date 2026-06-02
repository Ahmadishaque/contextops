from typing import Any

from app.schemas.retrieval import RetrievalSearchRequest
from app.services.retrieval.retriever import SemanticRetriever
from app.services.tools.base import BaseTool


class DocumentSearchTool(BaseTool):
    name = "document_search"
    description = "Searches indexed document chunks using semantic retrieval."
    input_schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query for indexed documents.",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of results.",
                "default": 5,
            },
            "access_level": {
                "type": "string",
                "description": "Access level filter.",
                "default": "private",
            },
        },
        "required": ["query"],
    }

    def __init__(self) -> None:
        self.retriever = SemanticRetriever()

    def run(self, arguments: dict[str, Any]) -> dict[str, Any]:
        query = arguments.get("query")

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Document search tool requires a non-empty query")

        limit = int(arguments.get("limit", 5))
        access_level = str(arguments.get("access_level", "private"))

        request = RetrievalSearchRequest(
            query=query,
            limit=limit,
            access_level=access_level,
        )

        results = self.retriever.search(request)

        return {
            "query": query,
            "result_count": len(results),
            "results": [result.model_dump() for result in results],
        }
