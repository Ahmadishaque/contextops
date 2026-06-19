from typing import Any

import streamlit as st

from frontend.components.api_feedback import (
    render_api_error,
    render_response_metadata,
    store_response_metadata,
)
from frontend.components.page_header import render_page_header
from frontend.config import get_frontend_config
from frontend.services.api_client import (
    ContextOpsAPIClient,
    ContextOpsAPIError,
)


def normalize_results(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [
            item
            for item in data
            if isinstance(item, dict)
        ]

    if not isinstance(data, dict):
        return []

    for key in ("results", "chunks", "matches", "items"):
        value = data.get(key)

        if isinstance(value, list):
            return [
                item
                for item in value
                if isinstance(item, dict)
            ]

    return []


def first_value(
    item: dict[str, Any],
    *keys: str,
    default: Any = None,
) -> Any:
    for key in keys:
        value = item.get(key)

        if value is not None:
            return value

    payload = item.get("payload")

    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)

            if value is not None:
                return value

    return default


def render_result(
    result: dict[str, Any],
    rank: int,
) -> None:
    score = first_value(
        result,
        "score",
        "similarity_score",
        "similarity",
        default=0.0,
    )

    try:
        numeric_score = float(score)
    except (TypeError, ValueError):
        numeric_score = 0.0

    text = str(
        first_value(
            result,
            "text",
            "content",
            "chunk_text",
            default="No chunk text returned.",
        )
    )

    title = str(
        first_value(
            result,
            "title",
            "document_title",
            "source",
            default=f"Result {rank}",
        )
    )

    document_id = first_value(
        result,
        "document_id",
        "doc_id",
        default="Unavailable",
    )

    access_level = first_value(
        result,
        "access_level",
        default="Unavailable",
    )

    with st.container(border=True):
        header_column, score_column = st.columns([4, 1])

        with header_column:
            st.markdown(f"### {rank}. {title}")

        with score_column:
            st.metric("Score", f"{numeric_score:.4f}")

        st.progress(
            min(max(numeric_score, 0.0), 1.0),
            text="Semantic similarity",
        )

        st.write(text)

        metadata_one, metadata_two = st.columns(2)

        with metadata_one:
            st.caption(f"Document ID: `{document_id}`")

        with metadata_two:
            st.caption(f"Access level: `{access_level}`")

        with st.expander("Result metadata"):
            st.json(result)


def render() -> None:
    render_page_header(
        eyebrow="Evidence Discovery",
        title="Semantic Retrieval",
        description=(
            "Search indexed knowledge and inspect the exact evidence, "
            "similarity scores, source metadata, and access attributes "
            "returned by ContextOps."
        ),
    )

    query = st.text_input(
        "Search query",
        placeholder=(
            "What information must enterprise customers provide "
            "for refund requests?"
        ),
    )

    control_one, control_two, control_three = st.columns(3)

    with control_one:
        limit = st.slider(
            "Maximum results",
            min_value=1,
            max_value=20,
            value=5,
        )

    with control_two:
        access_level = st.selectbox(
            "Access level",
            options=["private", "internal", "public"],
        )

    with control_three:
        owner_email = st.text_input(
            "Owner email",
            value="demo@contextops.dev",
        )

    submitted = st.button(
        "Search indexed knowledge",
        type="primary",
        use_container_width=True,
    )

    if not submitted:
        st.info(
            "Enter a natural-language query to inspect semantic retrieval."
        )
        return

    if not query.strip():
        st.error("Search query is required.")
        return

    payload = {
        "query": query.strip(),
        "limit": limit,
        "access_level": access_level,
        "owner_email": owner_email.strip(),
    }

    config = get_frontend_config()
    client = ContextOpsAPIClient(
        base_url=config.api_base_url,
        api_key=config.api_key,
    )

    with st.spinner("Searching Qdrant..."):
        try:
            response = client.search_documents(payload)
        except ContextOpsAPIError as exc:
            render_api_error(exc)
            return

    store_response_metadata(response)
    render_response_metadata(response)

    results = normalize_results(response.data)

    if not results:
        st.warning(
            "The API returned no retrieval results for this query."
        )

        with st.expander("Raw API response"):
            st.json(response.data)

        return

    st.success(f"Retrieved {len(results)} evidence chunks.")

    for rank, result in enumerate(results, start=1):
        render_result(result, rank)

    with st.expander("Raw API response"):
        st.json(response.data)

    st.caption(
        "ContextOps currently uses dense semantic retrieval. Hybrid search "
        "and reranking are planned extensions."
    )
