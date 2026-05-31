from app.schemas.retrieval import RetrievalSearchResult


class ContextBudgetManager:
    def __init__(self, max_chars: int) -> None:
        if max_chars <= 0:
            raise ValueError("max_chars must be positive")

        self.max_chars = max_chars

    def select_results(
        self,
        results: list[RetrievalSearchResult],
    ) -> tuple[list[RetrievalSearchResult], bool]:
        selected_results: list[RetrievalSearchResult] = []
        current_chars = 0
        truncated = False

        for result in results:
            result_chars = len(result.text)

            if current_chars + result_chars > self.max_chars:
                truncated = True
                break

            selected_results.append(result)
            current_chars += result_chars

        return selected_results, truncated
