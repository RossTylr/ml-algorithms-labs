"""
datasets.baselines — rule-based clinician proxies for the error-analysis experiment (Ng, *ML Yearning*, ch. 33–35).

Each returns a score or label the way a clinician using a published-style rule would, with NO access to the
generating mechanism. They are deliberately simple: the point is a human-level yardstick, not a strong model.
Every notebook that runs "error analysis: 20 worst cases vs clinician baseline" compares against one of these.

    from datasets.baselines import clinician_baseline
    score = clinician_baseline("screening", df)          # returns np.ndarray of risk scores in [0, 1]
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _news2_like(df: pd.DataFrame) -> np.ndarray:
    """NEWS2-style aggregate early-warning score from hourly vitals. 0–20, higher = sicker."""
    s = np.zeros(len(df))
    rr = df["rr"].fillna(16).values
    s += np.select([rr <= 8, rr <= 11, rr <= 20, rr <= 24], [3, 1, 0, 2], 3)
    spo2 = df["spo2"].fillna(96).values
    s += np.select([spo2 <= 91, spo2 <= 93, spo2 <= 95], [3, 2, 1], 0)
    sbp = df["sbp"].fillna(120).values
    s += np.select([sbp <= 90, sbp <= 100, sbp <= 110, sbp <= 219], [3, 2, 1, 0], 3)
    hr = df["hr"].fillna(75).values
    s += np.select([hr <= 40, hr <= 50, hr <= 90, hr <= 110, hr <= 130], [3, 1, 0, 1, 2], 3)
    t = df["temp"].fillna(36.8).values
    s += np.select([t <= 35.0, t <= 36.0, t <= 38.0, t <= 39.0], [3, 1, 0, 1], 2)
    return s


def _two_marker_rule(df: pd.DataFrame) -> np.ndarray:
    """A clinician's two-test rule on the screening panel: positive if either strong marker is > 1 SD, weighted by age."""
    z1 = df["bm_01"].values; z2 = df["bm_02"].values
    age = df["age"].values
    raw = 0.5 * (z1 > 1.0) + 0.5 * (z2 > 1.0) + 0.1 * (age > 65)
    return np.clip(raw, 0, 1)


def _charlson_like(df: pd.DataFrame) -> np.ndarray:
    """Comorbidity-and-age index for readmission/mortality: Charlson-style points, scaled to [0, 1]."""
    pts = df["comorbidity_count"].values.astype(float)
    pts += np.select([df["age"].values >= 80, df["age"].values >= 70, df["age"].values >= 60, df["age"].values >= 50], [4, 3, 2, 1], 0)
    pts += (df["admission_type"].values == "emergency") * 1.0
    pts += np.minimum(df["prior_admissions"].values, 3)
    return pts / 15.0


def _triage_rule(df: pd.DataFrame) -> np.ndarray:
    """Urgency from a note: any red-flag symptom → urgent."""
    red = ["chest pain", "radiating", "weakness one side", "slurred", "confusion", "shortness of breath"]
    return np.array([float(any(r in n for r in red)) for n in df["note"].values])


def _cohort_rule(df: pd.DataFrame) -> np.ndarray:
    """Frailty-style index: age, ED visits, medication count."""
    return np.clip(0.01 * df["age"].values + 0.1 * df["ed_visits"].values + 0.03 * df["meds"].values, 0, 1)


_RULES = {"vitals": _news2_like, "screening": _two_marker_rule, "admissions": _charlson_like, "notes": _triage_rule, "cohort": _cohort_rule}


def clinician_baseline(dataset: str, df: pd.DataFrame) -> np.ndarray:
    """Rule-based risk score for `dataset`. Raises KeyError for datasets with no baseline (imaging, trial, etc.)."""
    return _RULES[dataset](df)


def available() -> list[str]:
    return sorted(_RULES)
