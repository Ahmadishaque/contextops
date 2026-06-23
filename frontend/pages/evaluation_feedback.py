
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


def get_client() -> ContextOpsAPIClient:
    config = get_frontend_config()

    return ContextOpsAPIClient(
        base_url=config.api_base_url,
        api_key=config.api_key,
    )


def render_evaluation() -> None:
    st.subheader("Evaluate a response")

    query = st.text_area(
        "Original question",
        height=90,
    )

    answer = st.text_area(
        "Agent answer",
        height=180,
    )

    context = st.text_area(
        "Supporting context or evidence",
        height=220,
    )

    if not st.button(
        "Run evaluation",
        type="primary",
        use_container_width=True,
    ):
        return

    if not answer.strip():
        st.error("An answer is required.")
        return

    payload = {
        "query": query.strip(),
        "answer": answer.strip(),
        "context": context.strip(),
    }

    with st.spinner("Evaluating response quality..."):
        try:
            response = get_client().evaluate_response(payload)
        except ContextOpsAPIError as exc:
            render_api_error(exc)
            st.info(
                "If HTTP 422 is returned, inspect Swagger and adjust the "
                "evaluation payload fields to match the backend schema."
            )
            return

    store_response_metadata(response)
    render_response_metadata(response)

    st.success("Evaluation completed.")

    if isinstance(response.data, dict):
        checks = (
            response.data.get("checks")
            or response.data.get("results")
        )

        if isinstance(checks, list):
            for check in checks:
                if isinstance(check, dict):
                    name = check.get("name", "Evaluation check")
                    passed = check.get("passed")
                    detail = check.get("detail", "")

                    icon = "✅" if passed else "⚠️"
                    st.markdown(f"### {icon} {name}")
                    st.write(detail)

    with st.expander("Raw evaluation response"):
        st.json(response.data)


def render_feedback_submission() -> None:
    st.subheader("Submit trace feedback")

    trace_id = st.text_input(
        "Trace ID",
        value=str(st.session_state.get("latest_trace_id", "")),
        key="feedback_trace_id",
    )

    owner_email = st.text_input(
        "Owner email",
        value="demo@contextops.dev",
        key="feedback_owner",
    )

    rating = st.slider(
        "Rating",
        min_value=1,
        max_value=5,
        value=5,
    )

    label = st.selectbox(
        "Feedback label",
        options=[
            "helpful",
            "incorrect",
            "incomplete",
            "unsupported-claim",
            "wrong-source",
            "tool-error",
        ],
    )

    comment = st.text_area(
        "Comment",
        height=120,
    )

    if not st.button(
        "Submit feedback",
        type="primary",
        use_container_width=True,
    ):
        return

    if not trace_id.strip():
        st.error("Trace ID is required.")
        return

    payload = {
        "trace_id": trace_id.strip(),
        "owner_email": owner_email.strip(),
        "rating": rating,
        "label": label,
        "comment": comment.strip() or None,
    }

    with st.spinner("Saving feedback..."):
        try:
            response = get_client().create_feedback(payload)
        except ContextOpsAPIError as exc:
            render_api_error(exc)
            return

    store_response_metadata(response)
    render_response_metadata(response)

    st.success("Feedback saved.")

    if isinstance(response.data, dict):
        feedback_id = response.data.get("id")

        if feedback_id:
            st.session_state.latest_feedback_id = feedback_id

    st.json(response.data)


def render_feedback_lookup() -> None:
    st.subheader("Retrieve feedback")

    feedback_id = st.text_input(
        "Feedback ID",
        value=str(
            st.session_state.get("latest_feedback_id", "")
        ),
        key="feedback_lookup_id",
    )

    if not st.button(
        "Load feedback",
        use_container_width=True,
    ):
        return

    if not feedback_id.strip():
        st.error("Feedback ID is required.")
        return

    try:
        response = get_client().get_feedback(feedback_id.strip())
    except ContextOpsAPIError as exc:
        render_api_error(exc)
        return

    store_response_metadata(response)
    render_response_metadata(response)
    st.json(response.data)


def render() -> None:
    render_page_header(
        eyebrow="Quality Improvement",
        title="Evaluation & Feedback",
        description=(
            "Combine deterministic quality checks with human feedback linked "
            "to execution traces."
        ),
    )

    evaluation_tab, feedback_tab, lookup_tab = st.tabs(
        ["Evaluate", "Submit feedback", "Retrieve feedback"]
    )

    with evaluation_tab:
        render_evaluation()

    with feedback_tab:
        render_feedback_submission()

    with lookup_tab:
        render_feedback_lookup()

    st.info(
        "Evaluation and human feedback create signals for regression tests, "
        "prompt improvement, failure analysis, and future retraining workflows."
    )
