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


def get_client() -> ContextOpsAPIClient:
    config = get_frontend_config()

    return ContextOpsAPIClient(
        base_url=config.api_base_url,
        api_key=config.api_key,
    )


def normalize_tools(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]

    if isinstance(data, dict):
        tools = data.get("tools")

        if isinstance(tools, list):
            return [
                item for item in tools
                if isinstance(item, dict)
            ]

    return []


def render_registry() -> None:
    st.subheader("Registered tools")

    try:
        response = get_client().list_tools()
    except ContextOpsAPIError as exc:
        render_api_error(exc)
        return

    store_response_metadata(response)
    render_response_metadata(response)

    tools = normalize_tools(response.data)

    if not tools:
        st.warning("No registered tools were returned.")
        st.json(response.data)
        return

    columns = st.columns(2)

    for index, tool in enumerate(tools):
        with columns[index % 2]:
            with st.container(border=True):
                st.markdown(
                    f"### {tool.get('name', 'Unnamed tool')}"
                )
                st.write(
                    tool.get(
                        "description",
                        "No description returned.",
                    )
                )

                with st.expander("Tool schema"):
                    st.json(tool)


def render_calculator() -> None:
    st.subheader("Calculator")

    expression = st.text_input(
        "Expression",
        value="12 * 4 + 2",
    )

    if not st.button(
        "Run calculator",
        type="primary",
        use_container_width=True,
    ):
        return

    payload = {
        "tool_name": "calculator",
        "arguments": {
            "expression": expression,
        },
    }

    try:
        response = get_client().run_tool(payload)
    except ContextOpsAPIError as exc:
        render_api_error(exc)
        return

    store_response_metadata(response)
    render_response_metadata(response)

    st.success("Tool execution completed.")
    st.json(response.data)


def render_document_search() -> None:
    st.subheader("Document Search Tool")

    query = st.text_input(
        "Search query",
        key="tool_search_query",
    )

    limit = st.slider(
        "Result limit",
        min_value=1,
        max_value=10,
        value=5,
        key="tool_search_limit",
    )

    access_level = st.selectbox(
        "Access level",
        options=["private", "internal", "public"],
        key="tool_search_access",
    )

    if not st.button(
        "Run document search",
        type="primary",
        use_container_width=True,
    ):
        return

    payload = {
        "tool_name": "document_search",
        "arguments": {
            "query": query.strip(),
            "limit": limit,
            "access_level": access_level,
        },
    }

    try:
        response = get_client().run_tool(payload)
    except ContextOpsAPIError as exc:
        render_api_error(exc)
        return

    store_response_metadata(response)
    render_response_metadata(response)
    st.json(response.data)


def render() -> None:
    render_page_header(
        eyebrow="Controlled Capabilities",
        title="Tool Registry",
        description=(
            "Inspect and execute registered tools through the same protected "
            "FastAPI interface used by external clients."
        ),
    )

    registry_tab, calculator_tab, search_tab = st.tabs(
        ["Registry", "Calculator", "Document search"]
    )

    with registry_tab:
        render_registry()

    with calculator_tab:
        render_calculator()

    with search_tab:
        render_document_search()

    st.warning(
        "Registered tools are available for controlled execution. "
        "Autonomous arbitrary tool planning is not yet implemented."
    )
