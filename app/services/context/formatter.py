from app.schemas.retrieval import RetrievalSearchResult


class ContextFormatter:
    @staticmethod
    def format_results(results: list[RetrievalSearchResult]) -> str:
        formatted_blocks: list[str] = []

        for idx, result in enumerate(results, start=1):
            block = (
                f"[Source {idx}]\n"
                f"Title: {result.title}\n"
                f"Document ID: {result.document_id}\n"
                f"Chunk ID: {result.chunk_id}\n"
                f"Chunk Index: {result.chunk_index}\n"
                f"Access Level: {result.access_level}\n"
                f"Score: {result.score:.4f}\n"
                f"Text:\n{result.text}"
            )
            formatted_blocks.append(block)

        return "\n\n---\n\n".join(formatted_blocks)
