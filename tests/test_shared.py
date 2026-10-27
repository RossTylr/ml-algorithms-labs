import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib; matplotlib.use("Agg")
from shared.plotting import set_style, PALETTE, grid, decision_boundary
from shared.evaluation import diagnostic_report
from shared.rl import EvacGrid
from datasets import load_evac, load_screening


def test_style_and_palette():
    set_style(); assert len(PALETTE) == 10 and all(c.startswith("#") for c in PALETTE)

def test_grid_hides_unused():
    fig, axes = grid(4, ncols=3); assert len(axes) == 4

def test_diagnostic_report_metrics():
    rng = np.random.RandomState(0); y = rng.binomial(1, 0.2, 500); p = np.clip(y * 0.6 + rng.normal(0.3, 0.2, 500), 0, 1)
    _, m = diagnostic_report(y, p, prevalence=0.01)
    assert 0 <= m["ppv"] <= 1 and m["prevalence"] == 0.01

def test_evac_env_runs():
    env = EvacGrid(load_evac()); s = env.reset(); done = False; steps = 0
    while not done and steps < 100:
        s, r, done, _ = env.step(np.random.randint(4)); steps += 1
    assert steps > 0

def test_decision_boundary_draws():
    from sklearn.linear_model import LogisticRegression
    df = load_screening(n=200); X = df[["bm_01", "bm_02"]].values; y = df["disease"].values
    decision_boundary(LogisticRegression().fit(X, y), X, y)
