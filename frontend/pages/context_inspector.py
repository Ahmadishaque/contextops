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


def extract_context(data: Any) -> str:
    if not isinstance(data, dict):
        return str(data)

    for key in (
        "context",
        "assembled_context",
        "formatted_context",
        "content",
    ):
        value = data.get(key)

        if isinstance(value, str):
            return value

    return ""


def extract_sources(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, dict):
        return []

    for key in (
        "sources",
        "selected_chunks",
        "chunks",
        "evidence",
    ):
        value = data.get(key)

        if isinstance(value, list):
            return [
                item
                for item in value
                if isinstance(item, dict)
            ]

    return []


def render_source(
    source: dict[str, Any],
    index: int,
) -> None:
    title = (
        source.get("title")
        or source.get("document_title")
        or source.get("source")
        or f"Evidence {index}"
    )

    text = (
        source.get("text")
        or source.get("content")
        or source.get("chunk_text")
        or "No evidence text returned."
    )

    score = (
        source.get("score")
        or source.get("similarity_score")
        or source.get("similarity")
    )

    with st.container(border=True):
        st.markdown(f"#### {index}. {title}")
        st.write(text)

        if score is not None:
            try:
                st.caption(
                    f"Similarity score: {float(score):.4f}"
                )
            except (TypeError, ValueError):
                st.caption(f"Similarity score: {score}")

        with st.expander("Evidence metadata"):
            st.json(source)


def render() -> None:
    render_page_header(
        eyebrow="Context Engineering",
        title="Context Inspector",
        description=(
            "Inspect how retrieved evidence is selected, ordered, and "
            "assembled within an explicit context budget before model "
            "execution."
        ),
    )

    query = st.text_area(
        "User question",
        height=110,
        placeholder=(
            "What should enterprise customers include when requesting "
            "a refund?"
        ),
    )

    control_one, control_two, control_three = st.columns(3)

    with control_one:
        retrieval_limit = st.slider(
            "Retrieval limit",
            min_value=1,
            max_value=20,
            value=5,
        )

    with control_two:
        max_context_chars = st.slider(
            "Context character budget",
            min_value=500,
            max_value=12000,
            value=4000,
            step=500,
        )

    with control_three:
        access_level = st.selectbox(
            "Access level",
            options=["private", "internal", "public"],
        )

    owner_email = st.text_input(
        "Owner email",
        value="demo@contextops.dev",
    )

    submitted = st.button(
        "Assemble inspectable context",
        type="primary",
        use_container_width=True,
    )

    if not submitted:
        st.info(
            "Run context assembly to compare retrieved evidence with the "
            "final context package."
        )
        return

    if not query.strip():
        st.error("A user question is required.")
        return

    payload = {
        "query": query.strip(),
        "limit": retrieval_limit,
        "access_level": access_level,
        "max_context_chars": max_context_chars,
        "owner_email": owner_email.strip(),
    }

    config = get_frontend_config()
    client = ContextOpsAPIClient(
        base_url=config.api_base_url,
        api_key=config.api_key,
    )

    with st.spinner(
        "Retrieving, filtering, budgeting, and assembling context..."
    ):
        try:
            response = client.assemble_context(payload)
        except ContextOpsAPIError as exc:
            render_api_error(exc)
            return

    store_response_metadata(response)
    render_response_metadata(response)

    assembled_context = extract_context(response.data)
    sources = extract_sources(response.data)

    used_characters = len(assembled_context)
    budget_utilization = min(
        used_characters / max_context_chars,
        1.0,
    )

    metric_one, metric_two, metric_three = st.columns(3)

    with metric_one:
        st.metric(
            "Context characters",
            f"{used_characters:,}",
        )

    with metric_two:
        st.metric(
            "Selected evidence",
            len(sources),
        )

    with metric_three:
        estimated_tokens = round(used_characters / 4)
        st.metric(
            "Estimated tokens",
            f"{estimated_tokens:,}",
        )

    st.progress(
        budget_utilization,
        text=(
            f"Budget utilization: "
            f"{budget_utilization * 100:.1f}%"
        ),
    )

    st.markdown("### Context construction stages")

    stage_columns = st.columns(4)
    stages = [
        "Retrieved",
        "Access filtered",
        "Budgeted",
        "Assembled",
    ]

    for column, stage in zip(
        stage_columns,
        stages,
        strict=True,
    ):
        with column:
            st.markdown(
                f"""
                <div class="contextops-pipeline-step">
                    {stage}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    evidence_column, context_column = st.columns(2)

    with evidence_column:
        st.subheader("Selected evidence")

        if not sources:
            st.warning(
                "No structured source list was returned by the API."
            )
        else:
            for index, source in enumerate(sources, start=1):
                render_source(source, index)

    with context_column:
        st.subheader("Final model context")

        if assembled_context:
            st.code(
                assembled_context,
                language="text",
                wrap_lines=True,
            )

            st.download_button(
                "Download context",
                data=assembled_context,
                file_name="contextops-context.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.warning(
                "The API response did not include an assembled context string."
            )

    with st.expander("Raw context assembly response"):
        st.json(response.data)

    st.info(
        "The context package is inspectable and bounded before it reaches "
        "the language model. ContextOps therefore treats context as managed "
        "infrastructure rather than untracked prompt concatenation."
    )
