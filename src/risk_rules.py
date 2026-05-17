import pandas as pd


def detect_structural_anomaly(record: pd.DataFrame) -> tuple[bool, list[str]]:
    row = record.iloc[0]
    reasons = []

    if row["ielts_score"] >= 8.5 and row["sop_score"] <= 1.5:
        reasons.append("High IELTS paired with extremely weak SOP score.")
    if row["financial_history_usd"] >= 65000 and row["loan_status"] == "Rejected":
        reasons.append("Strong financial profile but rejected education loan outcome.")
    if row["backlogs"] <= 1 and row["previous_rejections"] >= 3 and row["sop_score"] >= 4.2:
        reasons.append("Strong academic indicators conflict with repeated past rejections.")
    if row["ielts_score"] <= 5.5 and row["sop_score"] >= 4.7:
        reasons.append("Very low IELTS but unusually strong SOP score pattern.")
    if row["gap_years"] >= 6 and row["ielts_score"] >= 8.0 and row["sop_score"] <= 2.0:
        reasons.append("Large study gap with inconsistent communication strength indicators.")

    return len(reasons) > 0, reasons


def generate_risk_warnings(input_df: pd.DataFrame) -> list[str]:
    row = input_df.iloc[0]
    warnings_list = []

    if row["ielts_score"] < 6.0:
        warnings_list.append("IELTS score is below a common safety threshold.")
    if row["backlogs"] >= 6:
        warnings_list.append("Backlog count is materially high for many universities and visa teams.")
    if row["financial_history_usd"] < 22000:
        warnings_list.append("Financial history appears weak against tuition and living cost expectations.")
    if row["gap_years"] >= 4:
        warnings_list.append("Extended study gap increases scrutiny during academic continuity checks.")
    if row["previous_rejections"] >= 1:
        warnings_list.append("Previous rejection history can trigger deeper manual review.")
    if row["sop_score"] < 2.5:
        warnings_list.append("SOP quality appears weak and may hurt narrative credibility.")
    if row["loan_status"] == "Rejected":
        warnings_list.append("Loan rejection may raise funding consistency concerns.")
    if row["university_ranking"] > 350:
        warnings_list.append("Lower-ranked institution selection may reduce profile competitiveness in some cases.")

    return warnings_list


def assess_risk_band(probability: float, predicted_days: float, anomaly_detected: bool) -> tuple[str, str]:
    if anomaly_detected or probability < 0.4 or predicted_days >= 36:
        return "High Risk", "risk-high"
    if probability < 0.7 or predicted_days >= 24:
        return "Medium Risk", "risk-medium"
    return "Low Risk", "risk-low"