from typing import Any

import streamlit as st

from frontend.services.api_client import APIResponse, ContextOpsAPIError


def store_response_metadata(response: APIResponse) -> None:
    st.session_state.last_request_id = response.request_id
    st.session_state.last_latency_ms = response.latency_ms


def render_response_metadata(response: APIResponse) -> None:
    latency_column, request_column, status_column = st.columns(3)

    with latency_column:
        st.metric("Latency", f"{response.latency_ms:.2f} ms")

    with request_column:
        request_id = response.request_id or "Unavailable"
        st.metric("Request ID", request_id[:16])

    with status_column:
        st.metric("HTTP status", response.status_code)


def render_api_error(error: ContextOpsAPIError) -> None:
    st.error(str(error))

    if error.status_code == 401:
        st.info(
            "Check the API key in the sidebar configuration."
        )

    if error.status_code == 404:
        st.info(
            "Confirm the endpoint path in frontend/services/endpoints.py."
        )

    if error.response_body is not None:
        with st.expander("API error response"):
            render_json_or_text(error.response_body)


def render_json_or_text(value: Any) -> None:
    if isinstance(value, (dict, list)):
        st.json(value)
    else:
        st.code(str(value), language=None)
