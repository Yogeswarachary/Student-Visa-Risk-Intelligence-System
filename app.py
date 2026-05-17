import streamlit as st

from src.data_generation import generate_synthetic_data
from src.model_training import train_models
from src.dashboard import render_dashboard
from src.evaluator import render_predictive_evaluator
from src.utils import apply_custom_css


st.set_page_config(
    page_title="Student Visa Risk Intelligence System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    apply_custom_css()
    df = generate_synthetic_data()
    artifacts = train_models(df)

    with st.sidebar:
        st.title("Navigation")
        page = st.radio(
            "Go to module",
            ["Executive Analytics Dashboard", "Predictive Smart Evaluator"],
            index=0,
        )
        st.markdown("---")
        st.markdown("### System Scope")
        st.write("- Synthetic portfolio generation")
        st.write("- Classification and regression pipelines")
        st.write("- Risk diagnostics and anomaly screening")
        st.write("- Executive charts and evaluator workflow")
        st.markdown("---")
        st.markdown(f"**Dataset size:** {len(df)} rows")
        st.markdown(f"**Encoded feature space:** {artifacts['transformed_shape'][1]} columns")

    if page == "Executive Analytics Dashboard":
        render_dashboard(df, artifacts)
    else:
        render_predictive_evaluator(df, artifacts)


if __name__ == "__main__":
    main()