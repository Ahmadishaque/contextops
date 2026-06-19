import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --contextops-cyan: #22d3ee;
            --contextops-violet: #8b5cf6;
            --contextops-surface: rgba(15, 23, 42, 0.72);
            --contextops-border: rgba(148, 163, 184, 0.18);
        }

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 10%,
                    rgba(34, 211, 238, 0.08),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 20%,
                    rgba(139, 92, 246, 0.08),
                    transparent 32%
                );
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid var(--contextops-border);
        }

        .contextops-hero {
            padding: 2.4rem;
            border: 1px solid var(--contextops-border);
            border-radius: 1.4rem;
            background:
                linear-gradient(
                    135deg,
                    rgba(15, 23, 42, 0.94),
                    rgba(30, 41, 59, 0.76)
                );
            box-shadow: 0 24px 80px rgba(2, 6, 23, 0.28);
            margin-bottom: 1.5rem;
        }

        .contextops-eyebrow {
            color: var(--contextops-cyan);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin-bottom: 0.8rem;
        }

        .contextops-title {
            font-size: clamp(2.4rem, 6vw, 4.7rem);
            line-height: 1;
            font-weight: 800;
            letter-spacing: -0.05em;
            margin-bottom: 1rem;
        }

        .contextops-gradient-text {
            background: linear-gradient(
                90deg,
                #f8fafc,
                var(--contextops-cyan),
                #c4b5fd
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .contextops-subtitle {
            color: #cbd5e1;
            max-width: 760px;
            font-size: 1.08rem;
            line-height: 1.7;
            margin-bottom: 1.5rem;
        }

        .contextops-tagline {
            color: #94a3b8;
            font-family: monospace;
            font-size: 0.9rem;
        }

        .contextops-card {
            min-height: 170px;
            padding: 1.25rem;
            border: 1px solid var(--contextops-border);
            border-radius: 1rem;
            background: var(--contextops-surface);
            margin-bottom: 1rem;
        }

        .contextops-card-title {
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.55rem;
        }

        .contextops-card-copy {
            color: #94a3b8;
            line-height: 1.55;
            font-size: 0.92rem;
        }

        .contextops-pipeline-step {
            padding: 1rem;
            border: 1px solid var(--contextops-border);
            border-radius: 0.9rem;
            background: rgba(15, 23, 42, 0.58);
            text-align: center;
            font-weight: 650;
            min-height: 76px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .contextops-status-online {
            color: #4ade80;
            font-weight: 700;
        }

        .contextops-status-offline {
            color: #fb7185;
            font-weight: 700;
        }

        .contextops-section-copy {
            color: #94a3b8;
            max-width: 840px;
            line-height: 1.65;
            margin-bottom: 1.2rem;
        }

        .block-container {
            max-width: 1440px;
            padding-top: 1.6rem;
            padding-bottom: 4rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
