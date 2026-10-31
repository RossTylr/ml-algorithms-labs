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


# ── hand-derived truths: each expected value comes from the mechanism on paper, not from the generator's output ──

def test_screening_prevalence_hand_truth():
    """disease ~ Bernoulli(p) iid, so the sample rate lies within 3·√(p(1−p)/n) of the configured p."""
    p, n = 0.08, 10000
    df, _ = load_screening(n=n, prevalence=p, return_truth=True)
    assert abs(df["disease"].mean() - p) < 3 * np.sqrt(p * (1 - p) / n)

def test_trial_true_effect_hand_truth():
    """Effect = true_effect·(1 + 0.4·baseline)·adherence with E[baseline] = 0 and E[adherence | treated] = 5/6.5 (Beta(5, 1.5)), so arm-mean difference ÷ (5/6.5) recovers true_effect within one SE."""
    true_effect, dilution = -0.35, 5 / 6.5
    df, _ = load_trial(n=20000, true_effect=true_effect, return_truth=True)
    g = df.groupby("arm")["outcome_12w"]; m, v, c = g.mean(), g.var(ddof=1), g.count()
    diff = m["treatment"] - m["control"]; se = np.sqrt(v["treatment"] / c["treatment"] + v["control"] / c["control"])
    assert abs(diff / dilution - true_effect) < se / dilution

def test_admissions_leak_hand_truth():
    """discharge_destination is 'mortuary' if and only if died = 1, so the leak indicator separates died perfectly: AUC = 1 > 0.95."""
    from sklearn.metrics import roc_auc_score
    df = load_admissions(n=2000)
    assert roc_auc_score(df["died"], (df["discharge_destination"] == "mortuary").astype(int)) > 0.95

def test_vitals_onsets_hand_truth():
    """Each patient deteriorates iff U(0,1) < rate, so rate 1 labels every one of n patients with one onset in [⌊0.3·hours⌋, ⌊0.8·hours⌋], and rate 0 labels none."""
    n, hours = 12, 48
    onsets = load_vitals(n_patients=n, hours=hours, deterioration_rate=1.0).groupby("patient_id")["onset_hour"].first()
    assert onsets.notna().sum() == n and onsets.between(int(0.3 * hours), int(0.8 * hours)).all()
    assert load_vitals(n_patients=n, hours=hours, deterioration_rate=0.0)["onset_hour"].notna().sum() == 0

def test_cohort_segments_hand_truth():
    """The mechanism fixes five segments of 3500/2500/2000/1200/800 patients, so exactly five appear, at exactly those sizes."""
    counts = load_cohort()["segment"].value_counts().to_dict()
    assert counts == {"healthy": 3500, "rising_risk": 2500, "chronic_stable": 2000, "complex": 1200, "frail": 800}

def test_areas_adjacency_hand_truth():
    """A 7×7 queen grid has 4 corners × 3 + 20 edge cells × 5 + 25 interior cells × 8 = 312 neighbour links."""
    from datasets import load_areas
    _, adj, _ = load_areas(n_side=7, return_truth=True)
    assert sum(len(v) for v in adj.values()) == 312
