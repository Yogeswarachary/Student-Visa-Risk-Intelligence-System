import pandas as pd
import streamlit as st

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.config import FEATURE_COLUMNS, SEED
from src.preprocessing import build_preprocessor


@st.cache_resource(show_spinner=False)
def train_models(df: pd.DataFrame) -> dict:
    X = df[FEATURE_COLUMNS]
    y_class = df["visa_status"]
    y_reg = df["visa_processing_days"]

    X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
        X, y_class, y_reg, test_size=0.2, random_state=SEED, stratify=y_class
    )

    classifier = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=240,
                    max_depth=12,
                    min_samples_split=4,
                    min_samples_leaf=2,
                    random_state=SEED,
                    n_jobs=-1,
                    class_weight="balanced_subsample",
                ),
            ),
        ]
    )

    regressor = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "model",
                RandomForestRegressor(
                    n_estimators=260,
                    max_depth=14,
                    min_samples_split=4,
                    min_samples_leaf=2,
                    random_state=SEED,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    classifier.fit(X_train, y_class_train)
    regressor.fit(X_train, y_reg_train)

    class_pred = classifier.predict(X_test)
    reg_pred = regressor.predict(X_test)

    accuracy = accuracy_score(y_class_test, class_pred)
    mae = mean_absolute_error(y_reg_test, reg_pred)
    r2 = r2_score(y_reg_test, reg_pred)

    transformed_X = classifier.named_steps["preprocessor"].transform(X)
    feature_names = classifier.named_steps["preprocessor"].get_feature_names_out()

    rf_classifier = classifier.named_steps["model"]
    global_feature_importance = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": rf_classifier.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    perm = permutation_importance(
        classifier,
        X_test,
        y_class_test,
        n_repeats=5,
        random_state=SEED,
        n_jobs=-1,
    )
    permutation_df = pd.DataFrame(
        {
            "feature": X_test.columns,
            "importance": perm.importances_mean,
        }
    ).sort_values("importance", ascending=False)

    return {
        "classifier": classifier,
        "regressor": regressor,
        "accuracy": accuracy,
        "mae": mae,
        "r2": r2,
        "global_feature_importance": global_feature_importance,
        "permutation_importance": permutation_df,
        "transformed_shape": transformed_X.shape,
    }