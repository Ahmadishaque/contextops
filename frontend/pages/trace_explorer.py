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


def display_value(
    data: dict[str, Any],
    *keys: str,
    default: Any = "Unavailable",
) -> Any:
    for key in keys:
        value = data.get(key)

        if value is not None:
            return value

    return default


def render() -> None:
    render_page_header(
        eyebrow="Execution Observability",
        title="Trace Explorer",
        description=(
            "Inspect agent execution metadata, request inputs, retrieved "
            "evidence, generated output, timestamps, and latency."
        ),
    )

    default_trace_id = str(
        st.session_state.get("latest_trace_id", "")
    )

    trace_id = st.text_input(
        "Trace ID",
        value=default_trace_id,
        placeholder="Paste an agent trace ID...",
    )

    submitted = st.button(
        "Load trace",
        type="primary",
        use_container_width=True,
    )

    if not submitted:
        st.info(
            "Run an agent query first or paste an existing trace ID."
        )
        return

    if not trace_id.strip():
        st.error("Trace ID is required.")
        return

    config = get_frontend_config()
    client = ContextOpsAPIClient(
        base_url=config.api_base_url,
        api_key=config.api_key,
    )

    with st.spinner("Loading execution trace..."):
        try:
            response = client.get_trace(trace_id.strip())
        except ContextOpsAPIError as exc:
            render_api_error(exc)
            return

    store_response_metadata(response)
    render_response_metadata(response)

    if not isinstance(response.data, dict):
        st.json(response.data)
        return

    data = response.data

    metric_columns = st.columns(4)

    with metric_columns[0]:
        st.metric(
            "Status",
            display_value(data, "status", default="Completed"),
        )

    with metric_columns[1]:
        st.metric(
            "Provider",
            display_value(data, "provider", "llm_provider"),
        )

    with metric_columns[2]:
        st.metric(
            "Latency",
            display_value(
                data,
                "latency_ms",
                "duration_ms",
            ),
        )

    with metric_columns[3]:
        st.metric(
            "Created",
            str(
                display_value(
                    data,
                    "created_at",
                    "timestamp",
                )
            )[:19],
        )

    st.subheader("Execution timeline")

    stages = [
        ("Request received", "Input validated and authenticated."),
        ("Retrieval", "Relevant evidence searched and filtered."),
        ("Context assembly", "Evidence selected within the context budget."),
        ("Model execution", "Configured provider generated the answer."),
        ("Trace persistence", "Execution metadata stored in PostgreSQL."),
    ]

    for index, (stage, description) in enumerate(stages, start=1):
        with st.container(border=True):
            st.markdown(f"### {index}. {stage}")
            st.caption(description)

    query = display_value(
        data,
        "query",
        "user_query",
        "input",
    )

    answer = display_value(
        data,
        "answer",
        "response",
        "output",
    )

    left, right = st.columns(2)

    with left:
        st.subheader("User query")
        st.write(query)

    with right:
        st.subheader("Agent response")
        st.write(answer)

    evidence = display_value(
        data,
        "sources",
        "retrieved_chunks",
        "evidence",
        default=[],
    )

    st.subheader("Retrieved evidence")

    if isinstance(evidence, list) and evidence:
        for index, item in enumerate(evidence, start=1):
            with st.expander(f"Evidence {index}"):
                st.json(item)
    else:
        st.info("No structured evidence list was returned.")

    with st.expander("Raw trace JSON"):
        st.json(data)

    st.download_button(
        "Download trace JSON",
        data=str(data),
        file_name=f"contextops-trace-{trace_id}.txt",
        mime="text/plain",
    )
