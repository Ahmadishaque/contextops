import streamlit as st

from frontend.components.sidebar import render_sidebar_configuration
from frontend.components.styles import apply_global_styles
from frontend.config import initialize_session_state
from frontend.pages import (
    agent_playground,
    context_inspector,
    evaluation_feedback,
    ingestion,
    overview,
    retrieval,
    tools,
    trace_explorer,
)

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
            ingestion.render,
            title="Ingestion",
            icon=":material/upload_file:",
            url_path="ingestion",
        ),
        st.Page(
            retrieval.render,
            title="Retrieval",
            icon=":material/search:",
            url_path="retrieval",
        ),
        st.Page(
            context_inspector.render,
            title="Context Inspector",
            icon=":material/account_tree:",
            url_path="context-inspector",
        ),
    ],
    "Execution": [
        st.Page(
            agent_playground.render,
            title="Agent Playground",
            icon=":material/smart_toy:",
            url_path="agent-playground",
        ),
        st.Page(
            trace_explorer.render,
            title="Trace Explorer",
            icon=":material/timeline:",
            url_path="trace-explorer",
        ),
        st.Page(
            evaluation_feedback.render,
            title="Evaluation & Feedback",
            icon=":material/rate_review:",
            url_path="evaluation-feedback",
        ),
        st.Page(
            tools.render,
            title="Tools",
            icon=":material/construction:",
            url_path="tools",
        ),
    ],
}

navigation = st.navigation(pages)
navigation.run()
