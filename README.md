# Student Visa Risk Intelligence System

A modular, portfolio-ready Streamlit application for **student visa risk analysis**, built using synthetic data, machine learning, rule-based screening, and interactive dashboarding.

This project demonstrates how to build an end-to-end applied data science solution using only:

- Streamlit
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn

---

## Project Overview

The **Student Visa Risk Intelligence System** simulates how applicant profiles can be analyzed for:

- Visa approval probability
- Estimated visa processing time
- Structural profile anomalies
- Document validation quality
- Risk segmentation and executive-level monitoring

The application is designed as a lightweight but well-structured GitHub portfolio project, with business logic split into reusable modules under the `src/` folder. The project entry point is `app.py`, which loads the dashboard and predictive evaluator modules. [file:78][file:74][file:71]

---

## Features

### Executive Analytics Dashboard
- Approval and rejection rate cards
- Average processing time and anomaly monitoring
- Approval trends by country
- Intake-wise visa outcome analysis
- Rejection driver visualization
- Model feature importance analysis
- Applicant segmentation summary
- OCR-style document validation simulation

### Predictive Smart Evaluator
- Manual applicant profile testing
- Approval probability prediction
- Predicted visa outcome
- Processing days estimation
- Risk band classification
- Rule-based risk warnings
- Structural anomaly detection
- Benchmark comparison with portfolio median

### ML Pipeline
- Synthetic dataset generation with exactly **2000 rows**
- `RandomForestClassifier` for `visa_status`
- `RandomForestRegressor` for `visa_processing_days`
- `ColumnTransformer` with:
  - `StandardScaler` for numeric features
  - `OneHotEncoder` for categorical features
- Cached training and data generation for performance

---

## Project Structure

```text
student_visa_risk_system/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── src/
    ├── __init__.py
    ├── config.py
    ├── utils.py
    ├── data_generation.py
    ├── preprocessing.py
    ├── model_training.py
    ├── risk_rules.py
    ├── dashboard.py
    └── evaluator.py
```

The app starts from `app.py`, which loads data generation, model training, dashboard rendering, and evaluator rendering through the `src` modules. [file:78]

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/student-visa-risk-intelligence-system.git
cd student-visa-risk-intelligence-system
```

### 2. Create a virtual environment

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the App

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will usually open in your browser at:

```text
http://localhost:8501
```

Since `app.py` is the project entry point, this is the only command needed to launch the full dashboard and evaluator experience. [file:78]

---

## Core Modules

### `app.py`
Main entry point of the application. It sets up the Streamlit page, loads styling, generates data, trains the models, and routes users between the dashboard and evaluator views. [file:78]

### `src/data_generation.py`
Generates the synthetic applicant dataset with:
- academic indicators
- finance-related variables
- profile anomalies
- visa status target
- processing time target

### `src/preprocessing.py`
Builds the preprocessing layer using `ColumnTransformer`, `StandardScaler`, and `OneHotEncoder`.

### `src/model_training.py`
Trains and evaluates:
- `RandomForestClassifier`
- `RandomForestRegressor`

Also computes feature importance and model metrics.

### `src/risk_rules.py`
Contains rule-based logic for:
- anomaly detection
- risk warnings
- risk band assignment

### `src/dashboard.py`
Renders the executive dashboard charts, summary cards, applicant segmentation, and OCR simulation module. [file:74]

### `src/evaluator.py`
Renders the predictive evaluator form, prediction outputs, risk diagnostics, and benchmarking view. [file:71]

### `src/utils.py`
Contains shared utilities such as custom CSS injection and UI styling helpers.

---

## Synthetic Data Logic

The dataset is fully synthetic but designed to mimic realistic student visa screening behavior.

### Input Features
- `ielts_score`
- `backlogs`
- `financial_history_usd`
- `university_ranking`
- `gap_years`
- `sop_score`
- `previous_rejections`
- `country`
- `intake`
- `loan_status`

### Targets
- `visa_status`
- `visa_processing_days`
- `anomaly_flag`

### Business Logic
Visa approval risk is influenced by:
- low IELTS score
- high backlog count
- weak financial history
- multiple previous rejections
- long academic gap
- poor SOP quality

A small noise factor is also added to make the target more realistic.

---

## Why This Project Is Good for a Portfolio

This project is useful for showcasing:

- applied machine learning
- business-rule engineering
- synthetic data modeling
- Streamlit dashboard development
- modular Python project structure
- explainability and decision-support design

It is especially strong for candidates targeting:
- Data Analyst
- Data Scientist
- ML Engineer
- AI Engineer
- Risk Analytics roles

---

## Deployment

This project can be deployed easily on **Streamlit Community Cloud**.

### Deployment entry point
```text
app.py
```

### Recommended repository contents
- `app.py`
- `requirements.txt`
- `README.md`
- `.gitignore`
- `src/`

Because `app.py` imports all business modules from `src`, make sure the entire `src` folder is pushed to GitHub. [file:78]

---

## Requirements

Use the exact versions listed in `requirements.txt`.

Expected Python version:

```text
Python 3.12
```

---

## Future Enhancements

Possible improvements for future versions:

- Downloadable CSV prediction reports
- Confusion matrix and regression diagnostics
- SHAP-like explainability alternatives
- Authentication layer
- Real OCR API integration
- Database-backed persistence
- Cloud deployment pipeline

---

## Author

**Yogeswarachary Modepalli**

This project is designed as a clean, recruiter-friendly portfolio artifact to demonstrate practical data science, machine learning, and interactive analytics engineering.