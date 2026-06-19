import streamlit as st

PAGE_DESCRIPTIONS = {
    "Ingestion": (
        "Upload or paste knowledge, create chunks, generate embeddings, "
        "and index content."
    ),
    "Retrieval": (
        "Inspect semantic search results, similarity scores, sources, "
        "and access metadata."
    ),
    "Context Inspector": (
        "See how retrieved evidence is selected and assembled within a "
        "context budget."
    ),
    "Agent Playground": (
        "Run grounded questions through the ContextOps agent runtime."
    ),
    "Trace Explorer": (
        "Inspect execution metadata, retrieved evidence, response data, "
        "and latency."
    ),
    "Evaluation & Feedback": (
        "Evaluate model responses and capture human feedback linked to traces."
    ),
    "Tools": (
        "Discover and execute registered ContextOps tools."
    ),
}


def render_placeholder(title: str) -> None:
    st.title(title)
    st.caption(PAGE_DESCRIPTIONS[title])

    st.info(
        "This page shell is connected to the shared ContextOps frontend. "
        "Its complete workflow will be implemented in the next frontend "
        "milestone."
    )

    st.markdown("### Planned capabilities")
    st.markdown(
        """
        - authenticated FastAPI integration
        - loading and error states
        - request ID and latency display
        - raw response inspection
        - production-oriented empty states
        """
    )
