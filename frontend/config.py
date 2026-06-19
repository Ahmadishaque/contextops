from dataclasses import dataclass

import streamlit as st

DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_API_KEY = "dev-contextops-key"


@dataclass(frozen=True)
class FrontendConfig:
    api_base_url: str
    api_key: str


def initialize_session_state() -> None:
    defaults = {
        "api_base_url": DEFAULT_API_BASE_URL,
        "api_key": DEFAULT_API_KEY,
        "last_request_id": None,
        "last_latency_ms": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_frontend_config() -> FrontendConfig:
    return FrontendConfig(
        api_base_url=str(st.session_state.api_base_url).rstrip("/"),
        api_key=str(st.session_state.api_key),
    )
