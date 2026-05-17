import numpy as np
import pandas as pd
import streamlit as st

from src.config import COUNTRIES, INTAKES, LOAN_STATUSES, N_ROWS, SEED


@st.cache_data(show_spinner=False)
def generate_synthetic_data(n_rows: int = N_ROWS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    country = rng.choice(COUNTRIES, size=n_rows, p=[0.28, 0.18, 0.22, 0.18, 0.14])
    intake = rng.choice(INTAKES, size=n_rows, p=[0.56, 0.29, 0.15])
    loan_status = rng.choice(LOAN_STATUSES, size=n_rows, p=[0.52, 0.16, 0.32])

    ielts_score = np.clip(rng.normal(6.9, 0.9, n_rows), 5.0, 9.0).round(1)
    backlogs = np.clip(rng.poisson(2.2, n_rows), 0, 15).astype(int)
    financial_history_usd = np.clip(rng.normal(38000, 14000, n_rows), 10000, 80000).astype(int)
    university_ranking = rng.integers(1, 501, size=n_rows)
    gap_years = np.clip(rng.poisson(1.5, n_rows), 0, 8).astype(int)
    sop_score = np.clip(rng.normal(3.4, 0.8, n_rows), 1.0, 5.0).round(1)
    previous_rejections = rng.choice([0, 1, 2, 3], size=n_rows, p=[0.68, 0.2, 0.09, 0.03])

    country_risk_map = {"USA": 0.35, "UK": 0.15, "Canada": 0.2, "Australia": 0.25, "Germany": -0.15}
    intake_risk_map = {"Fall": -0.1, "Spring": 0.12, "Summer": 0.22}
    loan_risk_map = {"Approved": -0.35, "Rejected": 0.55, "Not Applied": 0.12}

    financial_safety = (financial_history_usd - 10000) / 70000
    ranking_pressure = np.clip((university_ranking - 1) / 499, 0, 1)

    rejection_score = (
        np.where(ielts_score < 6.0, 2.1, 0)
        + np.where(ielts_score < 6.5, 1.1, 0)
        + np.where(backlogs >= 8, 2.0, 0)
        + np.where(backlogs >= 4, 0.8, 0)
        + np.where(gap_years >= 4, 1.8, 0)
        + np.where(gap_years >= 2, 0.7, 0)
        + np.where(financial_history_usd < 22000, 1.8, 0)
        + np.where(financial_history_usd < 32000, 0.7, 0)
        + np.where(previous_rejections >= 2, 1.8, 0)
        + np.where(previous_rejections == 1, 0.7, 0)
        + np.where(sop_score < 2.5, 1.5, 0)
        + np.where(university_ranking > 350, 0.45, 0)
        + np.vectorize(country_risk_map.get)(country)
        + np.vectorize(intake_risk_map.get)(intake)
        + np.vectorize(loan_risk_map.get)(loan_status)
        + rng.normal(0, 0.18, n_rows)
    )

    approval_boundary = 3.2
    visa_status = (rejection_score < approval_boundary).astype(int)

    noise_count = max(1, int(0.05 * n_rows))
    noise_idx = rng.choice(n_rows, size=noise_count, replace=False)
    visa_status[noise_idx] = 1 - visa_status[noise_idx]

    base_processing_days = (
        12
        + (1 - financial_safety) * 9
        + ranking_pressure * 4
        + np.maximum(0, 7.0 - ielts_score) * 3.6
        + backlogs * 1.6
        + gap_years * 3.0
        + previous_rejections * 4.0
        + np.where(loan_status == "Rejected", 6, 0)
        + np.where(loan_status == "Not Applied", 2, 0)
        + np.where(visa_status == 0, 7, 0)
        + np.where(intake == "Summer", 3, 0)
        + rng.normal(0, 2.5, n_rows)
    )
    visa_processing_days = np.clip(np.round(base_processing_days), 7, 90).astype(int)

    mismatch_conditions = (
        ((ielts_score >= 8.5) & (sop_score <= 1.5))
        | ((financial_history_usd >= 65000) & (loan_status == "Rejected"))
        | ((backlogs <= 1) & (previous_rejections >= 3) & (sop_score >= 4.2))
        | ((ielts_score <= 5.5) & (sop_score >= 4.7))
        | ((gap_years >= 6) & (ielts_score >= 8.0) & (sop_score <= 2.0))
    )
    anomaly_flag = mismatch_conditions.astype(int)

    return pd.DataFrame(
        {
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
            "visa_status": visa_status,
            "visa_processing_days": visa_processing_days,
            "anomaly_flag": anomaly_flag,
        }
    )