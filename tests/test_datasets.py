import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import pandas as pd
from datasets import (load_screening, load_admissions, load_trial, load_vitals, load_prescribing,
                      load_cohort, load_notes, load_referrals, load_imaging, load_evac, synthetic)


def test_screening_truth():
    df, truth = load_screening(n=500, return_truth=True)
    assert df.shape == (500, 15) and set(truth["strong"]) <= set(df.columns)
    pd.testing.assert_frame_equal(load_screening(n=100), load_screening(n=100))

def test_admissions_mechanism():
    df = load_admissions(n=2000)
    assert {"los_days", "readmit_30d", "died", "discharge_destination"} <= set(df.columns)
    assert df.loc[df.died == 1, "readmit_30d"].sum() == 0  # dead patients aren't readmitted
    assert df["patient_id"].duplicated().any()               # repeat patients for group splits

def test_trial_effect_sign():
    df, truth = load_trial(n=4000, return_truth=True)
    d = df.groupby("arm")["outcome_12w"].mean()
    assert d["treatment"] < d["control"] and truth["true_effect_sd"] < 0

def test_vitals_shape_and_labels():
    df = load_vitals(n_patients=6, hours=48)
    assert len(df) == 6 * 48 and set(df.deteriorating.unique()) <= {0, 1}

def test_prescribing_both_forms():
    b = load_prescribing(n_patients=50); f = load_prescribing(n_patients=50, as_frame=True)
    assert len(b) == 50 and {"item", "adverse_event"} <= set(f.columns)

def test_cohort_segments():
    df = load_cohort(n=200)
    assert df["segment"].nunique() == 5

def test_notes_text():
    df = load_notes(n=50)
    assert df["note"].str.len().min() > 10 and set(df.urgent.unique()) <= {0, 1}

def test_referrals_graph():
    nodes, edges = load_referrals(n_nodes=80)
    assert len(nodes) == 80 and {"source", "target", "n_referrals"} <= set(edges.columns)

def test_imaging_masks():
    X, y, M = load_imaging(n=40, return_masks=True)
    assert X.shape == (40, 16, 16) and M[y == 1].sum() > 0 and M[y == 0].sum() == 0

def test_evac_spec():
    s = load_evac()
    assert s["terrain"].shape == (6, 6) and s["start"] != s["goal"]

def test_synthetic_variants():
    assert len(synthetic.classification_variants(n=100)) == 8
    assert "spirals" in synthetic.clustering_variants(n=120)
    assert len(synthetic.bandit_arms()) == 5

def test_ledger_reads_the_build_record():
    from datasets import load_ledger
    df, digest = load_ledger()
    assert {"id", "attempt", "verdict"} <= set(df.columns) and isinstance(digest, str)
