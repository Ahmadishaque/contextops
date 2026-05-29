from app.services.ingestion.chunker import SimpleTextChunker


def test_chunker_returns_single_chunk_for_short_text() -> None:
    chunker = SimpleTextChunker(chunk_size=100, chunk_overlap=20)

    chunks = chunker.chunk("This is a short document.")

    assert len(chunks) == 1
    assert chunks[0].chunk_index == 0
    assert chunks[0].text == "This is a short document."


def test_chunker_returns_multiple_chunks_for_long_text() -> None:
    chunker = SimpleTextChunker(chunk_size=20, chunk_overlap=5)

    chunks = chunker.chunk("abcdefghijklmnopqrstuvwxyz")

    assert len(chunks) > 1
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1


def test_chunker_removes_empty_lines() -> None:
    chunker = SimpleTextChunker(chunk_size=100, chunk_overlap=10)

    chunks = chunker.chunk("Line one\n\n\nLine two")

    assert len(chunks) == 1
    assert chunks[0].text == "Line one\nLine two"
