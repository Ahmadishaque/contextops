import streamlit as st

from frontend.components.sidebar import render_sidebar_configuration
from frontend.components.styles import apply_global_styles
from frontend.config import initialize_session_state
from frontend.pages import overview
from frontend.pages.placeholders import render_placeholder


def render_ingestion() -> None:
    render_placeholder("Ingestion")


def render_retrieval() -> None:
    render_placeholder("Retrieval")


def render_context_inspector() -> None:
    render_placeholder("Context Inspector")


def render_agent_playground() -> None:
    render_placeholder("Agent Playground")


def render_trace_explorer() -> None:
    render_placeholder("Trace Explorer")


def render_evaluation_feedback() -> None:
    render_placeholder("Evaluation & Feedback")


def render_tools() -> None:
    render_placeholder("Tools")


st.set_page_config(
    page_title="ContextOps",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_session_state()
apply_global_styles()
render_sidebar_configuration()

pages = {
    "Platform": [
        st.Page(
            overview.render,
            title="Overview",
            icon=":material/dashboard:",
            url_path="overview",
            default=True,
        ),
        st.Page(
            render_ingestion,
            title="Ingestion",
            icon=":material/upload_file:",
            url_path="ingestion",
        ),
        st.Page(
            render_retrieval,
            title="Retrieval",
            icon=":material/search:",
            url_path="retrieval",
        ),
        st.Page(
            render_context_inspector,
            title="Context Inspector",
            icon=":material/account_tree:",
            url_path="context-inspector",
        ),
    ],
    "Execution": [
        st.Page(
            render_agent_playground,
            title="Agent Playground",
            icon=":material/smart_toy:",
            url_path="agent-playground",
        ),
        st.Page(
            render_trace_explorer,
            title="Trace Explorer",
            icon=":material/timeline:",
            url_path="trace-explorer",
        ),
        st.Page(
            render_evaluation_feedback,
            title="Evaluation & Feedback",
            icon=":material/rate_review:",
            url_path="evaluation-feedback",
        ),
        st.Page(
            render_tools,
            title="Tools",
            icon=":material/construction:",
            url_path="tools",
        ),
    ],
}

navigation = st.navigation(pages)
navigation.run()
