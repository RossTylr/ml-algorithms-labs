"""Each clinician baseline must beat chance and lose to a tuned model on its own dataset — otherwise it is not a yardstick."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import pytest
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_predict
from datasets import load_screening, load_admissions, load_vitals, load_notes, load_cohort
from datasets.baselines import clinician_baseline, available


def _check(name, df, y, X, model=None):
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    model = model or GradientBoostingClassifier(random_state=0)
    base = roc_auc_score(y, clinician_baseline(name, df))
    model = roc_auc_score(y, cross_val_predict(model, X, y, cv=3, method="predict_proba")[:, 1])
    assert base > 0.55, f"{name}: baseline AUC {base:.2f} is chance"
    assert model > base, f"{name}: model {model:.2f} ≤ baseline {base:.2f}"
    return base, model


def test_screening():
    df = load_screening(n=1500); _check("screening", df, df.disease.values, df.filter(like="bm_").values)

def test_admissions():
    df = load_admissions(n=3000); X = df[["age", "severity", "comorbidity_count", "prior_admissions"]].values
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    _check("admissions", df, df.readmit_30d.values, X, make_pipeline(StandardScaler(), LogisticRegression()))

def test_vitals():
    df = load_vitals(n_patients=40, hours=72); df = df.dropna()
    y = ((df.deteriorating == 1) & (df.hour >= df.onset_hour.fillna(1e9))).astype(int).values
    _check("vitals", df, y, df[["hr", "rr", "spo2", "sbp", "temp"]].values)

def test_notes():
    df = load_notes(n=1500)
    base = roc_auc_score(df.urgent, clinician_baseline("notes", df)); assert base > 0.6

def test_cohort():
    df = load_cohort(n=2000); y = (df.segment.isin(["complex", "frail"])).astype(int).values
    base = roc_auc_score(y, clinician_baseline("cohort", df)); assert base > 0.7

def test_available():
    assert set(available()) == {"vitals", "screening", "admissions", "notes", "cohort"}
