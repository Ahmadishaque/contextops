from pathlib import Path
from typing import Any

import streamlit as st

from frontend.components.api_feedback import (
    render_api_error,
    render_json_or_text,
    render_response_metadata,
    store_response_metadata,
)
from frontend.components.page_header import render_page_header
from frontend.config import get_frontend_config
from frontend.services.api_client import (
    ContextOpsAPIClient,
    ContextOpsAPIError,
)


def parse_metadata(metadata_text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}

    for line in metadata_text.splitlines():
        stripped_line = line.strip()

        if not stripped_line:
            continue

        if "=" not in stripped_line:
            raise ValueError(
                f"Metadata entry must use key=value format: {stripped_line}"
            )

        key, value = stripped_line.split("=", maxsplit=1)
        metadata[key.strip()] = value.strip()

    return metadata


def read_uploaded_text(uploaded_file: Any) -> str:
    file_bytes = uploaded_file.getvalue()

    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "The uploaded file must use UTF-8 text encoding."
        ) from exc


def render_result(data: Any) -> None:
    if not isinstance(data, dict):
        render_json_or_text(data)
        return

    document_id = (
        data.get("document_id")
        or data.get("id")
        or data.get("document", {}).get("id")
        or "Unavailable"
    )

    chunk_count = (
        data.get("chunk_count")
        or data.get("chunks_created")
        or data.get("num_chunks")
        or "Unavailable"
    )

    status_value = (
        data.get("status")
        or data.get("indexing_status")
        or "Completed"
    )

    column_one, column_two, column_three = st.columns(3)

    with column_one:
        st.metric("Document ID", str(document_id)[:18])

    with column_two:
        st.metric("Chunks created", chunk_count)

    with column_three:
        st.metric("Status", status_value)

    with st.expander("Full ingestion response"):
        st.json(data)


def render() -> None:
    render_page_header(
        eyebrow="Knowledge Pipeline",
        title="Document Ingestion",
        description=(
            "Add governed knowledge to ContextOps. The backend persists "
            "document metadata, creates chunks, generates embeddings, and "
            "indexes vectors in Qdrant."
        ),
    )

    input_tab, workflow_tab = st.tabs(
        ["Ingest document", "How ingestion works"]
    )

    with input_tab:
        source_mode = st.radio(
            "Document source",
            options=["Paste text", "Upload file"],
            horizontal=True,
        )

        uploaded_file = None
        content = ""

        if source_mode == "Paste text":
            content = st.text_area(
                "Document content",
                height=280,
                placeholder=(
                    "Paste documentation, policies, technical notes, "
                    "or other knowledge here..."
                ),
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload a UTF-8 text document",
                type=["txt", "md", "markdown"],
            )

            if uploaded_file is not None:
                try:
                    content = read_uploaded_text(uploaded_file)
                except ValueError as exc:
                    st.error(str(exc))
                    content = ""

                if content:
                    st.text_area(
                        "Uploaded content preview",
                        value=content,
                        height=220,
                        disabled=True,
                    )

        title_default = ""

        if uploaded_file is not None:
            title_default = Path(uploaded_file.name).stem

        title = st.text_input(
            "Document title",
            value=title_default,
            placeholder="Enterprise refund policy",
        )

        left_column, right_column = st.columns(2)

        with left_column:
            owner_email = st.text_input(
                "Owner email",
                value="demo@contextops.dev",
            )

        with right_column:
            access_level = st.selectbox(
                "Access level",
                options=["private", "internal", "public"],
            )

        source_name = st.text_input(
            "Source name",
            placeholder="operations-handbook",
        )

        metadata_text = st.text_area(
            "Optional metadata",
            placeholder=(
                "department=operations\n"
                "region=global\n"
                "version=2026-01"
            ),
            help="Enter one key=value pair per line.",
        )

        character_count = len(content)
        approximate_chunks = max(
            1,
            round(character_count / 1000),
        ) if content else 0

        metric_one, metric_two = st.columns(2)

        with metric_one:
            st.metric("Characters", f"{character_count:,}")

        with metric_two:
            st.metric(
                "Approximate chunks",
                approximate_chunks,
                help=(
                    "This is only a frontend estimate. The backend controls "
                    "the actual chunking strategy."
                ),
            )

        submitted = st.button(
            "Ingest and index document",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if not title.strip():
                st.error("Document title is required.")
                return

            if not content.strip():
                st.error("Document content is required.")
                return

            try:
                metadata = parse_metadata(metadata_text)
            except ValueError as exc:
                st.error(str(exc))
                return

            if source_name.strip():
                metadata["source"] = source_name.strip()

            payload = {
                "title": title.strip(),
                "text": content.strip(),
                "owner_email": owner_email.strip(),
                "access_level": access_level,
                "metadata": metadata,
            }

            config = get_frontend_config()
            client = ContextOpsAPIClient(
                base_url=config.api_base_url,
                api_key=config.api_key,
                timeout_seconds=120.0,
            )

            with st.spinner(
                "Chunking, embedding, and indexing document..."
            ):
                try:
                    response = client.ingest_document(payload)
                except ContextOpsAPIError as exc:
                    render_api_error(exc)
                    return

            store_response_metadata(response)
            st.success("Document ingested successfully.")
            render_response_metadata(response)
            render_result(response.data)

    with workflow_tab:
        st.subheader("Ingestion pipeline")

        pipeline_columns = st.columns(5)
        stages = [
            "Validate",
            "Persist metadata",
            "Create chunks",
            "Generate embeddings",
            "Index in Qdrant",
        ]

        for column, stage in zip(
            pipeline_columns,
            stages,
            strict=True,
        ):
            with column:
                st.markdown(
                    f"""
                    <div class="contextops-pipeline-step">
                        {stage}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.info(
            "The Streamlit frontend submits text to FastAPI. It does not "
            "connect directly to PostgreSQL or Qdrant."
        )

