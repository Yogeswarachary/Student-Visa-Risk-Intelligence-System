COUNTRIES = ["USA", "UK", "Canada", "Australia", "Germany"]
INTAKES = ["Fall", "Spring", "Summer"]
LOAN_STATUSES = ["Approved", "Rejected", "Not Applied"]

SEED = 42
N_ROWS = 2000

NUMERIC_FEATURES = [
    "ielts_score",
    "backlogs",
    "financial_history_usd",
    "university_ranking",
    "gap_years",
    "sop_score",
    "previous_rejections",
]

CATEGORICAL_FEATURES = [
    "country",
    "intake",
    "loan_status",
]

FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES