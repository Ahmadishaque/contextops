import streamlit as st


def render_page_header(
    eyebrow: str,
    title: str,
    description: str,
) -> None:
    st.markdown(
        f"""
        <div class="contextops-eyebrow">{eyebrow}</div>
        """,
        unsafe_allow_html=True,
    )

    st.title(title)
    st.markdown(
        f"""
        <div class="contextops-section-copy">
            {description}
        </div>
        """,
        unsafe_allow_html=True,
    )
