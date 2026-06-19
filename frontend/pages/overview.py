import streamlit as st

from frontend.config import get_frontend_config
from frontend.services.api_client import (
    ContextOpsAPIClient,
    ContextOpsAPIError,
)


def render_pipeline() -> None:
    steps = [
        "Documents",
        "Chunking & Embeddings",
        "Permission-Aware Retrieval",
        "Context Assembly",
        "Agent Response",
        "Trace, Evaluation & Feedback",
    ]

    columns = st.columns(3)

    for index, step in enumerate(steps):
        with columns[index % 3]:
            st.markdown(
                f"""
                <div class="contextops-pipeline-step">
                    {index + 1}. {step}
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_architecture_cards() -> None:
    cards = [
        (
            "FastAPI",
            "Versioned APIs, validation, authentication, and orchestration.",
        ),
        (
            "PostgreSQL",
            "Persistent metadata for users, documents, traces, and feedback.",
        ),
        (
            "Qdrant",
            "Vector indexing and semantic retrieval over document chunks.",
        ),
        (
            "Redis",
            "Infrastructure foundation for caching and coordination.",
        ),
        (
            "LLM Provider Layer",
            "Provider abstraction supporting mock and OpenAI-backed responses.",
        ),
        (
            "Observability",
            "Request IDs, structured logs, latency, traces, and evaluations.",
        ),
    ]

    columns = st.columns(3)

    for index, (title, description) in enumerate(cards):
        with columns[index % 3]:
            st.markdown(
                f"""
                <div class="contextops-card">
                    <div class="contextops-card-title">{title}</div>
                    <div class="contextops-card-copy">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_health_panel() -> None:
    config = get_frontend_config()
    client = ContextOpsAPIClient(
        base_url=config.api_base_url,
        api_key=config.api_key,
    )

    status_column, latency_column, request_column = st.columns(3)

    try:
        response = client.get_health()
    except ContextOpsAPIError as exc:
        with status_column:
            st.metric("API status", "Offline")

        with latency_column:
            st.metric("Latency", "Unavailable")

        with request_column:
            st.metric("Request ID", "Unavailable")

        st.warning(
            "The backend is not currently reachable. "
            "Start FastAPI locally or update the API configuration."
        )

        with st.expander("Connection details"):
            st.code(str(exc), language=None)

        return

    st.session_state.last_latency_ms = response.latency_ms
    st.session_state.last_request_id = response.request_id

    with status_column:
        st.metric("API status", "Healthy")

    with latency_column:
        st.metric("Health latency", f"{response.latency_ms:.2f} ms")

    with request_column:
        short_request_id = (
            response.request_id[:12]
            if response.request_id
            else "Unavailable"
        )
        st.metric("Request ID", short_request_id)


def render() -> None:
    st.markdown(
        """
        <div class="contextops-hero">
            <div class="contextops-eyebrow">
                Production AI Infrastructure
            </div>
            <div class="contextops-title contextops-gradient-text">
                ContextOps
            </div>
            <div class="contextops-subtitle">
                The context and reliability layer behind grounded AI systems.
                ContextOps manages how evidence is ingested, retrieved,
                filtered, assembled, traced, evaluated, and improved.
            </div>
            <div class="contextops-tagline">
                Ingest. Retrieve. Assemble. Trace. Evaluate. Improve.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(4)

    metrics = [
        ("Pipeline stages", "6"),
        ("Storage systems", "3"),
        ("Registered tools", "2"),
        ("API version", "v1"),
    ]

    for column, (label, value) in zip(
        metric_columns,
        metrics,
        strict=True,
    ):
        with column:
            st.metric(label, value)

    st.divider()

    st.subheader("System status")
    st.markdown(
        """
        <div class="contextops-section-copy">
            ContextOps separates the presentation layer from the FastAPI
            service. This dashboard communicates with the same API that an
            external production client would use.
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_health_panel()

    st.divider()

    st.subheader("How ContextOps works")
    st.markdown(
        """
        <div class="contextops-section-copy">
            Context is treated as managed infrastructure rather than a single
            prompt-construction step. Every stage can be inspected,
            constrained, traced, and evaluated.
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_pipeline()

    st.divider()

    st.subheader("Architecture")
    render_architecture_cards()

    st.divider()

    st.subheader("Why ContextOps?")
    left, right = st.columns(2)

    with left:
        st.markdown("#### Generic AI application")
        st.markdown(
            """
            - Retrieve some text
            - Insert it into a prompt
            - Return a model response
            - Limited visibility into what happened
            """
        )

    with right:
        st.markdown("#### ContextOps")
        st.markdown(
            """
            - Persist and index governed knowledge
            - Apply access-aware retrieval
            - Assemble context within explicit budgets
            - Trace execution and source usage
            - Evaluate responses
            - Capture feedback for improvement
            """
        )

    st.divider()

    st.subheader("Current implementation scope")
    st.info(
        "ContextOps currently provides service-level API-key authentication, "
        "metadata-based access filtering, registered tools, response tracing, "
        "evaluation, and feedback capture. Autonomous arbitrary tool planning "
        "and full multi-tenant RBAC are future extensions."
    )
