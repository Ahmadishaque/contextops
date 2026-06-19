import streamlit as st

from frontend.config import get_frontend_config
from frontend.services.api_client import (
    ContextOpsAPIClient,
    ContextOpsAPIError,
)


def render_sidebar_configuration() -> None:
    st.sidebar.markdown("## ContextOps")
    st.sidebar.caption("Context and reliability infrastructure")

    with st.sidebar.expander("API configuration", expanded=False):
        st.text_input(
            "API base URL",
            key="api_base_url",
            help="FastAPI service address.",
        )

        st.text_input(
            "API key",
            key="api_key",
            type="password",
            help="Sent using the X-API-Key header.",
        )

        if st.button(
            "Test API connection",
            use_container_width=True,
            key="sidebar_health_check",
        ):
            config = get_frontend_config()
            client = ContextOpsAPIClient(
                base_url=config.api_base_url,
                api_key=config.api_key,
            )

            try:
                response = client.get_health()
            except ContextOpsAPIError as exc:
                st.session_state.last_latency_ms = None
                st.session_state.last_request_id = None
                st.error(str(exc))
            else:
                st.session_state.last_latency_ms = response.latency_ms
                st.session_state.last_request_id = response.request_id
                st.success(
                    f"API healthy · {response.latency_ms:.2f} ms"
                )

    st.sidebar.divider()

    config = get_frontend_config()
    st.sidebar.caption("Connected API")
    st.sidebar.code(config.api_base_url, language=None)

    if st.session_state.last_request_id:
        st.sidebar.caption("Latest request ID")
        st.sidebar.code(
            str(st.session_state.last_request_id),
            language=None,
        )
