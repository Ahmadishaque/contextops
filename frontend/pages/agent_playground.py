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


def extract_value(
    data: dict[str, Any],
    *keys: str,
    default: Any = None,
) -> Any:
    for key in keys:
        if data.get(key) is not None:
            return data[key]

    return default


def render_sources(data: dict[str, Any]) -> None:
    sources = extract_value(
        data,
        "sources",
        "evidence",
        "retrieved_chunks",
        default=[],
    )

    if not isinstance(sources, list) or not sources:
        st.info("No structured source list was returned.")
        return

    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            continue

        title = (
            source.get("title")
            or source.get("document_title")
            or source.get("source")
            or f"Source {index}"
        )

        text = (
            source.get("text")
            or source.get("content")
            or source.get("chunk_text")
            or "No source text returned."
        )

        with st.container(border=True):
            st.markdown(f"#### {index}. {title}")
            st.write(text)

            with st.expander("Source metadata"):
                st.json(source)


def render() -> None:
    render_page_header(
        eyebrow="Grounded Execution",
        title="Agent Playground",
        description=(
            "Run a grounded agent query and inspect the answer, evidence, "
            "execution trace, provider metadata, and latency."
        ),
    )

    example_columns = st.columns(3)

    examples = [
        "What information is required for enterprise refund requests?",
        "Summarize the indexed refund policy.",
        "What evidence supports the current refund process?",
    ]

    for index, example in enumerate(examples):
        with example_columns[index]:
            if st.button(
                example,
                use_container_width=True,
                key=f"agent_example_{index}",
            ):
                st.session_state.agent_query = example

    query = st.text_area(
        "Question",
        key="agent_query",
        height=120,
        placeholder="Ask a question grounded in indexed knowledge...",
    )

    control_one, control_two, control_three = st.columns(3)

    with control_one:
        limit = st.slider(
            "Retrieval limit",
            min_value=1,
            max_value=20,
            value=5,
        )

    with control_two:
        max_context_chars = st.slider(
            "Context budget",
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
        "Run grounded agent",
        type="primary",
        use_container_width=True,
    )

    if not submitted:
        st.info(
            "The agent retrieves evidence, assembles bounded context, "
            "invokes the configured provider, and persists a trace."
        )
        return

    if not query.strip():
        st.error("A question is required.")
        return

    payload = {
        "query": query.strip(),
        "limit": limit,
        "access_level": access_level,
        "max_context_chars": max_context_chars,
        "owner_email": owner_email.strip(),
    }

    config = get_frontend_config()
    client = ContextOpsAPIClient(
        base_url=config.api_base_url,
        api_key=config.api_key,
        timeout_seconds=120.0,
    )

    with st.spinner("Running ContextOps agent pipeline..."):
        try:
            response = client.query_agent(payload)
        except ContextOpsAPIError as exc:
            render_api_error(exc)
            return

    store_response_metadata(response)
    render_response_metadata(response)

    if not isinstance(response.data, dict):
        st.json(response.data)
        return

    data = response.data

    answer = extract_value(
        data,
        "answer",
        "response",
        "output",
        default="No answer returned.",
    )

    trace_id = extract_value(
        data,
        "trace_id",
        "traceId",
        default="Unavailable",
    )

    provider = extract_value(
        data,
        "provider",
        "llm_provider",
        default="Unavailable",
    )

    metrics = st.columns(4)

    with metrics[0]:
        st.metric("Trace ID", str(trace_id)[:16])

    with metrics[1]:
        st.metric("Provider", provider)

    with metrics[2]:
        st.metric(
            "Retrieved sources",
            len(data.get("sources", []))
            if isinstance(data.get("sources"), list)
            else "Unavailable",
        )

    with metrics[3]:
        st.metric(
            "Context characters",
            data.get("context_char_count", "Unavailable"),
        )

    st.subheader("Grounded answer")
    st.markdown(str(answer))

    st.download_button(
        "Download answer",
        data=str(answer),
        file_name="contextops-answer.txt",
        mime="text/plain",
    )

    st.subheader("Supporting evidence")
    render_sources(data)

    with st.expander("Execution stages"):
        st.markdown(
            """
            1. Query received
            2. Evidence retrieved
            3. Context assembled
            4. Provider invoked
            5. Execution trace persisted
            """
        )

    with st.expander("Raw agent response"):
        st.json(data)

    if trace_id != "Unavailable":
        st.session_state.latest_trace_id = str(trace_id)
        st.success(
            "Trace saved. Open Trace Explorer and use the stored trace ID."
        )
