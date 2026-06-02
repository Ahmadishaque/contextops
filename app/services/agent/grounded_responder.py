from app.schemas.context import ContextPackage


class GroundedResponder:
    def generate_answer(self, context_package: ContextPackage) -> str:
        if not context_package.context_text.strip() or not context_package.sources:
            return (
                "I could not find relevant context to answer this question. "
                "Please ingest relevant documents or broaden the search filters."
            )

        source_titles = ", ".join(
            source.title for source in context_package.sources[:3]
        )

        return (
            "Based on the retrieved context, the relevant information is:\n\n"
            f"{self._extract_relevant_text(context_package.context_text)}\n\n"
            f"Sources used: {source_titles}."
        )

    @staticmethod
    def _extract_relevant_text(context_text: str, max_chars: int = 1200) -> str:
        cleaned_text = context_text.strip()

        if len(cleaned_text) <= max_chars:
            return cleaned_text

        return cleaned_text[:max_chars].rstrip() + "..."
