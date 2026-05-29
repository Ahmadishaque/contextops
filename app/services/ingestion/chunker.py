from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    chunk_index: int
    text: str


class SimpleTextChunker:
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 120) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> list[TextChunk]:
        cleaned_text = self._normalize_text(text)

        if not cleaned_text:
            return []

        chunks: list[TextChunk] = []
        start = 0
        chunk_index = 0

        while start < len(cleaned_text):
            end = start + self.chunk_size
            chunk_text = cleaned_text[start:end].strip()

            if chunk_text:
                chunks.append(TextChunk(chunk_index=chunk_index, text=chunk_text))
                chunk_index += 1

            if end >= len(cleaned_text):
                break

            start = end - self.chunk_overlap

        return chunks

    @staticmethod
    def _normalize_text(text: str) -> str:
        lines = [line.strip() for line in text.splitlines()]
        non_empty_lines = [line for line in lines if line]
        return "\n".join(non_empty_lines)