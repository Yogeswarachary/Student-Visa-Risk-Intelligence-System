import pandas as pd
import streamlit as st

from src.config import COUNTRIES, INTAKES, LOAN_STATUSES
from src.risk_rules import detect_structural_anomaly, generate_risk_warnings, assess_risk_band


def render_predictive_evaluator(df: pd.DataFrame, artifacts: dict) -> None:
    st.title("🧠 Predictive Smart Evaluator")
    st.caption("Manual applicant profile testing with approval scoring, delay estimation, anomaly checks, and risk diagnostics.")

    classifier = artifacts["classifier"]
    regressor = artifacts["regressor"]

    with st.form("predictive_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            ielts_score = st.slider("IELTS Score", 5.0, 9.0, 6.5, 0.1)
            backlogs = st.slider("Backlogs", 0, 15, 2, 1)
            financial_history_usd = st.slider("Financial History (USD)", 10000, 80000, 35000, 1000)
            university_ranking = st.slider("University Ranking", 1, 500, 180, 1)

        with col2:
            gap_years = st.slider("Gap Years", 0, 8, 1, 1)
            sop_score = st.slider("SOP Score", 1.0, 5.0, 3.5, 0.1)
            previous_rejections = st.slider("Previous Rejections", 0, 3, 0, 1)
            country = st.selectbox("Destination Country", COUNTRIES)

        with col3:
            intake = st.selectbox("Intake", INTAKES)
            loan_status = st.selectbox("Loan Status", LOAN_STATUSES)
            profile_template = st.selectbox(
                "Quick Scenario Template",
                [
                    "Manual Input",
                    "Strong Profile",
                    "Borderline Profile",
                    "High-Risk Profile",
                    "Anomalous Profile",
                ],
                index=0,
            )

        submitted = st.form_submit_button("Run Risk Intelligence Evaluation", use_container_width=True)

    scenario = build_scenario(
        profile_template=profile_template,
        ielts_score=ielts_score,
        backlogs=backlogs,
        financial_history_usd=financial_history_usd,
        university_ranking=university_ranking,
        gap_years=gap_years,
        sop_score=sop_score,
        previous_rejections=previous_rejections,
        country=country,
        intake=intake,
        loan_status=loan_status,
    )

    if submitted:
        input_df = pd.DataFrame([scenario])
        probability = float(classifier.predict_proba(input_df)[0][1])
        predicted_status = int(classifier.predict(input_df)[0])
        predicted_days = float(regressor.predict(input_df)[0])

        anomaly_detected, anomaly_reasons = detect_structural_anomaly(input_df)
        warnings_list = generate_risk_warnings(input_df)
        risk_band, risk_class = assess_risk_band(probability, predicted_days, anomaly_detected)

        m1, m2, m3, m4 = st.columns(4)
        
        # Column 1: Approval Probability
        m1.caption("**Approval Probability**")
        m1.subheader(f"{probability * 100:.1f}%")

        # Column 2: Predicted Outcome
        m2.caption("**Predicted Outcome**")
        m2.subheader("Approved" if predicted_status == 1 else "Rejected")

        # Column 3: Expected Processing Days
        m3.caption("**Expected Processing Days**")
        m3.subheader(f"{predicted_days:.0f} Days")

        # Column 4: Risk Band
        m4.caption("**Risk Band**")
        m4.subheader(risk_band)

        st.markdown(
            f"<div class='{risk_class}'><strong>Profile Risk Summary:</strong> {risk_band} applicant profile based on current synthetic model signals.</div>",
            unsafe_allow_html=True,
        )

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.markdown("### Evaluation Breakdown")
            st.write(f"- Destination country: {scenario['country']}")
            st.write(f"- Intake season: {scenario['intake']}")
            st.write(f"- Loan status: {scenario['loan_status']}")
            st.write(f"- Academic continuity gap: {scenario['gap_years']} years")
            st.write(f"- Past visa rejection count: {scenario['previous_rejections']}")

            gauge_df = pd.DataFrame(
                {
                    "metric": ["Approval Probability", "Delay Exposure"],
                    "value": [round(probability * 100, 2), round(min(predicted_days / 60 * 100, 100), 2)],
                }
            ).set_index("metric")
            st.bar_chart(gauge_df)

        with result_col2:
            st.markdown("### Diagnostic Alerts")
            if warnings_list:
                for warning in warnings_list:
                    st.warning(warning)
            else:
                st.success("No major risk warnings were triggered by the rule-based screening layer.")

            if anomaly_detected:
                st.error("Structural anomaly flag detected.")
                for reason in anomaly_reasons:
                    st.write(f"- {reason}")
            else:
                st.success("No structural anomalies detected in the submitted profile.")

        st.markdown("### Submitted Applicant Snapshot")
        st.dataframe(input_df, use_container_width=True, hide_index=True)

        st.markdown("### Benchmark vs Portfolio Median")
        numeric_cols = [
            "ielts_score",
            "backlogs",
            "financial_history_usd",
            "university_ranking",
            "gap_years",
            "sop_score",
            "previous_rejections",
        ]
        benchmark = pd.DataFrame(
            {
                "Applicant": input_df[numeric_cols].iloc[0],
                "Portfolio Median": df[numeric_cols].median(),
            }
        )
        st.dataframe(benchmark, use_container_width=True)
    else:
        st.info("Submit the evaluator form to generate an approval score, delay estimate, anomaly review, and warning diagnostics.")


def build_scenario(
    profile_template: str,
    ielts_score: float,
    backlogs: int,
    financial_history_usd: int,
    university_ranking: int,
    gap_years: int,
    sop_score: float,
    previous_rejections: int,
    country: str,
    intake: str,
    loan_status: str,
) -> dict:
    templates = {
        "Strong Profile": {
            "ielts_score": 8.0,
            "backlogs": 1,
            "financial_history_usd": 62000,
            "university_ranking": 110,
            "gap_years": 0,
            "sop_score": 4.4,
            "previous_rejections": 0,
            "country": "Canada",
            "intake": "Fall",
            "loan_status": "Approved",
        },
        "Borderline Profile": {
            "ielts_score": 6.3,
            "backlogs": 4,
            "financial_history_usd": 26000,
            "university_ranking": 290,
            "gap_years": 2,
            "sop_score": 3.0,
            "previous_rejections": 1,
            "country": "UK",
            "intake": "Spring",
            "loan_status": "Not Applied",
        },
        "High-Risk Profile": {
            "ielts_score": 5.5,
            "backlogs": 8,
            "financial_history_usd": 18000,
            "university_ranking": 420,
            "gap_years": 5,
            "sop_score": 2.0,
            "previous_rejections": 2,
            "country": "USA",
            "intake": "Summer",
            "loan_status": "Rejected",
        },
        "Anomalous Profile": {
            "ielts_score": 8.6,
            "backlogs": 0,
            "financial_history_usd": 70000,
            "university_ranking": 90,
            "gap_years": 6,
            "sop_score": 1.4,
            "previous_rejections": 0,
            "country": "Australia",
            "intake": "Fall",
            "loan_status": "Approved",
        },
    }

    if profile_template != "Manual Input":
        return templates[profile_template]

    return {
        "ielts_score": ielts_score,
        "backlogs": backlogs,
        "financial_history_usd": financial_history_usd,
        "university_ranking": university_ranking,
        "gap_years": gap_years,
        "sop_score": sop_score,
        "previous_rejections": previous_rejections,
        "country": country,
        "intake": intake,
        "loan_status": loan_status,
    }