import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")


def compute_dashboard_metrics(df: pd.DataFrame) -> dict:
    approval_rate = df["visa_status"].mean() * 100
    avg_processing = df["visa_processing_days"].mean()
    anomaly_rate = df["anomaly_flag"].mean() * 100
    rejection_rate = 100 - approval_rate

    high_risk_profiles = (
        (df["ielts_score"] < 6.0)
        | (df["backlogs"] >= 6)
        | (df["gap_years"] >= 4)
        | (df["previous_rejections"] >= 2)
        | (df["financial_history_usd"] < 22000)
    )

    return {
        "approval_rate": approval_rate,
        "rejection_rate": rejection_rate,
        "avg_processing": avg_processing,
        "anomaly_rate": anomaly_rate,
        "high_risk_count": int(high_risk_profiles.sum()),
    }


def create_country_approval_chart(df: pd.DataFrame):
    country_summary = (
        df.groupby("country", as_index=False)["visa_status"]
        .mean()
        .assign(approval_rate=lambda x: x["visa_status"] * 100)
        .sort_values("approval_rate", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(data=country_summary, x="country", y="approval_rate", palette="Blues_d", ax=ax)
    ax.set_title("Approval Rate by Destination Country", fontsize=13, weight="bold")
    ax.set_xlabel("Country")
    ax.set_ylabel("Approval Rate (%)")
    ax.set_ylim(0, 100)

    for idx, value in enumerate(country_summary["approval_rate"]):
        ax.text(idx, value + 1, f"{value:.1f}%", ha="center", fontsize=9)

    plt.tight_layout()
    return fig


def create_intake_distribution_chart(df: pd.DataFrame):
    intake_summary = df.groupby(["intake", "visa_status"]).size().reset_index(name="count")
    intake_summary["visa_result"] = intake_summary["visa_status"].map({1: "Approved", 0: "Rejected"})

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(
        data=intake_summary,
        x="intake",
        y="count",
        hue="visa_result",
        palette={"Approved": "#16a34a", "Rejected": "#dc2626"},
        ax=ax,
    )
    ax.set_title("Intake-wise Decision Distribution", fontsize=13, weight="bold")
    ax.set_xlabel("Intake")
    ax.set_ylabel("Applicant Count")
    ax.legend(title="Decision")
    plt.tight_layout()
    return fig


def create_rejection_driver_chart(df: pd.DataFrame):
    rejected = df[df["visa_status"] == 0].copy()
    cause_counts = {
        "Low IELTS": int((rejected["ielts_score"] < 6.0).sum()),
        "High Backlogs": int((rejected["backlogs"] >= 6).sum()),
        "Low Finances": int((rejected["financial_history_usd"] < 22000).sum()),
        "Gap Years": int((rejected["gap_years"] >= 4).sum()),
        "Past Rejections": int((rejected["previous_rejections"] >= 1).sum()),
        "Weak SOP": int((rejected["sop_score"] < 2.5).sum()),
    }
    cause_df = pd.DataFrame(
        {"cause": list(cause_counts.keys()), "count": list(cause_counts.values())}
    ).sort_values("count", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    sns.barplot(data=cause_df, x="count", y="cause", palette="Reds", ax=ax)
    ax.set_title("Primary Rejection Drivers", fontsize=13, weight="bold")
    ax.set_xlabel("Affected Rejected Profiles")
    ax.set_ylabel("")
    plt.tight_layout()
    return fig


def create_feature_importance_chart(feature_importance_df: pd.DataFrame):
    top_df = feature_importance_df.head(12).sort_values("importance", ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5.2))
    sns.barplot(data=top_df, x="importance", y="feature", palette="viridis", ax=ax)
    ax.set_title("Model Feature Importance", fontsize=13, weight="bold")
    ax.set_xlabel("Importance Score")
    ax.set_ylabel("")
    plt.tight_layout()
    return fig


def create_segmentation_summary(df: pd.DataFrame) -> pd.DataFrame:
    conditions = [
        (df["visa_status"] == 1) & (df["visa_processing_days"] <= 20) & (df["anomaly_flag"] == 0),
        (df["visa_status"] == 1) & (df["visa_processing_days"] > 20),
        (df["visa_status"] == 0) & (df["anomaly_flag"] == 0),
        (df["anomaly_flag"] == 1),
    ]
    labels = [
        "Low Risk Fast-Track",
        "Approved but Slow-Moving",
        "High-Risk Rejected",
        "Profile Anomaly Watchlist",
    ]

    segment = pd.Series("Balanced Review Pool", index=df.index)
    for condition, label in zip(conditions, labels):
        segment = segment.mask(condition, label)

    segment_df = pd.DataFrame({"segment": segment})
    summary = segment_df.value_counts().reset_index(name="count")
    summary["share_pct"] = (summary["count"] / len(df) * 100).round(2)
    return summary


def render_dashboard(df: pd.DataFrame, artifacts: dict) -> None:
    metrics = compute_dashboard_metrics(df)

    st.title("🎓 Student Visa Risk Intelligence System")
    st.caption("Executive analytics for synthetic student visa portfolio intelligence and risk monitoring.")


    c1, c2, c3, c4, c5 = st.columns(5)
    # Adding native borders forces high-contrast typography styling automatically
    # Column 1
    c1.caption("**Approval Rate**")
    c1.subheader(f"{metrics['approval_rate']:.1f}%")

    # Column 2
    c2.caption("**Rejection Rate**")
    c2.subheader(f"{metrics['rejection_rate']:.1f}%")

    # Column 3
    c3.caption("**Avg Processing Days**")
    c3.subheader(f"{metrics['avg_processing']:.1f}")

    # Column 4
    c4.caption("**Anomaly Rate**")
    c4.subheader(f"{metrics['anomaly_rate']:.1f}%")

    # Column 5
    c5.caption("**High-Risk Profiles**")
    c5.subheader(f"{metrics['high_risk_count']}")

    left, right = st.columns(2)
    with left:
        st.pyplot(create_country_approval_chart(df), use_container_width=True)
    with right:
        st.pyplot(create_intake_distribution_chart(df), use_container_width=True)

    left2, right2 = st.columns(2)
    with left2:
        st.pyplot(create_rejection_driver_chart(df), use_container_width=True)
    with right2:
        st.pyplot(create_feature_importance_chart(artifacts["global_feature_importance"]), use_container_width=True)

    st.markdown("### Portfolio Intelligence Snapshot")
    seg_summary = create_segmentation_summary(df)
    seg_col1, seg_col2 = st.columns([1.2, 1.8])

    with seg_col1:
        st.dataframe(seg_summary, use_container_width=True, hide_index=True)

    with seg_col2:
        st.markdown(
            """
            <div class="section-card">
                <h4>Applicant Segmentation Summary</h4>
                <p class="small-note">
                    <strong>The portfolio is grouped into fast-track approvals, slow-moving approved cases,
                    balanced review pools, anomaly watchlists, and high-risk rejected profiles.</strong>
                </p>
                <p class="small-note">
                    <strong>This helps analysts prioritize interventions, document reviews, and counselor follow-up actions.</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
    )

        mc1, mc2, mc3 = st.columns(3)

        # Column 1
        mc1.caption("**Classifier Accuracy**")
        mc1.subheader(f"{artifacts['accuracy']:.3f}")

        # Column 2
        mc2.caption("**Regressor MAE**")
        mc2.subheader(f"{artifacts['mae']:.2f} days")

        # Column 3
        mc3.caption("**Regressor R²**")
        mc3.subheader(f"{artifacts['r2']:.3f}")

    st.markdown("### OCR-based Document Validation Simulation")
    doc_col1, doc_col2 = st.columns([1, 1])

    with doc_col1:
        st.markdown(
            """
            <div class="section-card">
                <p><strong>Simulated Validation Controls</strong></p>
                <p class="small-note">
                    <strong>This simulation mimics an OCR review lane for student visa document validation.</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        transcript_ok = st.checkbox("Transcript formatting is consistent", value=True)
        bank_ok = st.checkbox("Bank statement matches declared funds", value=True)
        passport_ok = st.checkbox("Passport data fields are readable", value=True)
        sop_ok = st.checkbox("SOP contains clear academic intent", value=True)
        name_match = st.checkbox("All documents show matching candidate name", value=True)

    with doc_col2:
        validation_flags = [transcript_ok, bank_ok, passport_ok, sop_ok, name_match]
        validation_score = int(sum(validation_flags) / len(validation_flags) * 100)
        match_confidence = min(98, validation_score)

        o1, o2 = st.columns(2)

        # Column 1
        o1.caption("**Match Confidence**")
        o1.subheader(f"{match_confidence}%")

        # Column 2
        o2.caption("**Document Validation Score**")
        o2.subheader(f"{validation_score}%")

        if validation_score == 100:
            st.success("OCR Simulation Outcome: Validated")
        elif validation_score >= 60:
            st.warning("OCR Simulation Outcome: Needs Manual Review")
        else:
            st.error("OCR Simulation Outcome: Critical Mismatch")

        failed_checks = [
            label
            for label, passed in {
                "Transcript consistency": transcript_ok,
                "Financial document coherence": bank_ok,
                "Passport readability": passport_ok,
                "SOP clarity": sop_ok,
                "Cross-document name match": name_match,
            }.items()
            if not passed
        ]

        st.write("Review flags:")
        if failed_checks:
            for item in failed_checks:
                st.write(f"- {item}")
        else:
            st.write("- No validation mismatches detected.")

    st.markdown("### Synthetic Dataset Preview")
    st.dataframe(df.head(25), use_container_width=True, hide_index=True)