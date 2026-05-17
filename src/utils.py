import streamlit as st


def apply_custom_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #020617 0%, #071122 100%);
        }

        .main .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6 {
            color: #f8fafc !important;
        }

        .stApp p,
        .stApp li,
        .stApp label,
        .stApp span {
            color: #e2e8f0;
        }

        .section-card {
            background: #ffffff;
            border-radius: 18px;
            padding: 1.1rem 1.25rem;
            box-shadow: 0 6px 22px rgba(15, 23, 42, 0.12);
            border: 1px solid rgba(15, 23, 42, 0.10);
            margin-bottom: 1rem;
        }

        .section-card h1,
        .section-card h2,
        .section-card h3,
        .section-card h4,
        .section-card h5,
        .section-card h6 {
            color: #0f172a !important;
            font-weight: 800 !important;
            margin-bottom: 0.55rem !important;
        }

        .section-card p,
        .section-card li,
        .section-card span,
        .section-card strong {
            color: #334155 !important;
            font-weight: 500 !important;
            line-height: 1.65 !important;
        }

        .small-note {
            font-size: 0.97rem !important;
            color: #334155 !important;
            font-weight: 500 !important;
            line-height: 1.7 !important;
        }

        .risk-high {
            background: #fff1f2;
            border: 1px solid #fecdd3;
            padding: 0.8rem 1rem;
            border-radius: 12px;
            color: #7f1d1d !important;
            margin-top: 0.8rem;
            font-weight: 700;
        }

        .risk-medium {
            background: #fff7ed;
            border: 1px solid #fed7aa;
            padding: 0.8rem 1rem;
            border-radius: 12px;
            color: #9a3412 !important;
            margin-top: 0.8rem;
            font-weight: 700;
        }

        .risk-low {
            background: #ecfdf5;
            border: 1px solid #bbf7d0;
            padding: 0.8rem 1rem;
            border-radius: 12px;
            color: #166534 !important;
            margin-top: 0.8rem;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            background: #ffffff !important;
            border: 1px solid rgba(15, 23, 42, 0.10) !important;
            padding: 18px 20px !important;
            border-radius: 18px !important;
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.08) !important;
            min-height: 110px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #475569 !important;
            opacity: 1 !important;
            font-weight: 800 !important;
            font-size: 1rem !important;
            line-height: 1.3 !important;
        }

        div[data-testid="stMetricLabel"] * {
            color: #475569 !important;
            fill: #475569 !important;
            stroke: #475569 !important;
            opacity: 1 !important;
            visibility: visible !important;
        }

        div[data-testid="stMetricValue"] {
            color: #0f172a !important;
            opacity: 1 !important;
            font-weight: 900 !important;
            font-size: 1.7rem !important;
            line-height: 1.2 !important;
        }

        div[data-testid="stMetricValue"] * {
            color: #0f172a !important;
            fill: #0f172a !important;
            stroke: #0f172a !important;
            opacity: 1 !important;
            visibility: visible !important;
        }

        div[data-testid="stMetricDelta"] {
            color: #64748b !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }

        div[data-testid="stMetricDelta"] * {
            color: #64748b !important;
            fill: #64748b !important;
            stroke: #64748b !important;
            opacity: 1 !important;
            visibility: visible !important;
        }

        div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stMarkdownContainer"] h4 {
            color: #f8fafc !important;
        }

        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li {
            color: #e2e8f0 !important;
        }

        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }

        .stAlert {
            border-radius: 12px;
        }

        section[data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )