"""
datasets.synthetic — controlled generators with known ground truth, clinically framed.

    from datasets import synthetic
    data = synthetic.regression_variants()   # dict name -> (X, y, truth)
"""
from __future__ import annotations

import numpy as np
from sklearn.datasets import make_blobs, make_circles, make_classification, make_moons, make_s_curve, make_swiss_roll

SEED = 42


def dose_response(n=300, seed=SEED, noise=0.15):
    """Quadratic dose–response with therapeutic window. Returns dose, response, truth-fn."""
    r = np.random.RandomState(seed)
    dose = np.sort(r.uniform(0, 10, n))
    f = lambda d: -0.08 * (d - 6) ** 2 + 3.0
    return dose, f(dose) + r.normal(0, noise, n), f


def regression_variants(n=500, seed=SEED):
    """Clean / heteroscedastic / outlier / collinear / non-linear versions of a LOS-like target."""
    r = np.random.RandomState(seed)
    X = r.normal(0, 1, (n, 3))
    y_clean = 3 * X[:, 0] + 1.5 * X[:, 1] - 2 * X[:, 2] + 5 + r.normal(0, 0.5, n)
    y_het = 3 * X[:, 0] + r.normal(0, 1 + 2 * np.abs(X[:, 0]), n)
    y_out = y_clean.copy(); idx = r.choice(n, n // 10, replace=False); y_out[idx] += r.normal(0, 20, len(idx))
    Xc = np.column_stack([X, X[:, 0] + r.normal(0, 0.05, n)])
    y_nl = np.sin(2 * X[:, 0]) + X[:, 1] ** 2 + r.normal(0, 0.3, n)
    return {
        "clean_linear": (X, y_clean, dict(coef=[3, 1.5, -2], intercept=5)),
        "heteroscedastic": (X, y_het, dict(coef=[3, 0, 0])),
        "with_outliers": (X, y_out, dict(outlier_idx=idx)),
        "multicollinear": (Xc, 3 * X[:, 0] + 1.5 * X[:, 1] + r.normal(0, 1, n), dict(collinear=(0, 3))),
        "nonlinear": (X, y_nl, dict(form="sin(2x0)+x1^2")),
    }


def classification_variants(n=1000, seed=SEED):
    """Diagnostic boundary shapes. 'triage' is a 4-class imbalanced set (T1 2%, T2 13%, T3 35%, T4 50%)."""
    out = {
        "separable": make_classification(n_samples=n, n_features=2, n_redundant=0, n_informative=2, n_clusters_per_class=1, class_sep=2.0, random_state=seed),
        "overlapping": make_classification(n_samples=n, n_features=2, n_redundant=0, n_informative=2, n_clusters_per_class=1, class_sep=0.5, random_state=seed),
        "moons": make_moons(n_samples=n, noise=0.2, random_state=seed),
        "rings": make_circles(n_samples=n, noise=0.1, factor=0.5, random_state=seed),
        "xor": _xor(n, seed),
        "rare_positive": make_classification(n_samples=n, n_features=2, n_redundant=0, n_informative=2, weights=[0.98, 0.02], random_state=seed),
        "high_dimensional": make_classification(n_samples=n, n_features=50, n_informative=5, n_redundant=10, random_state=seed),
        "triage": make_classification(n_samples=n, n_features=6, n_informative=4, n_classes=4, weights=[0.02, 0.13, 0.35, 0.50], random_state=seed),
    }
    return out


def _xor(n, seed):
    r = np.random.RandomState(seed)
    X = r.uniform(-1, 1, (n, 2))
    y = ((X[:, 0] > 0) ^ (X[:, 1] > 0)).astype(int)
    return X + r.normal(0, 0.1, X.shape), y


def clustering_variants(n=1000, seed=SEED):
    """Phenotype shapes: blobs, moons, rings, variable density, with noise, anisotropic, spirals."""
    r = np.random.RandomState(seed)
    Xb, yb = make_blobs(n_samples=n, centers=5, cluster_std=1.0, random_state=seed)
    Xv = np.vstack([r.normal(c, s, (n // 3, 2)) for c, s in zip([(-5, 0), (0, 0), (5, 0)], [0.5, 2.0, 0.8])])
    Xn = np.vstack([Xb, r.uniform(-15, 15, (n // 5, 2))]); yn = np.concatenate([yb, -np.ones(n // 5, int)])
    t = np.linspace(0, 3 * np.pi, n // 2)
    s1 = np.column_stack([t * np.cos(t), t * np.sin(t)]); s2 = -s1
    Xs = np.vstack([s1, s2]) + r.normal(0, 0.3, (n // 2 * 2, 2))
    return {
        "blobs": (Xb, yb), "moons": make_moons(n_samples=n, noise=0.1, random_state=seed),
        "rings": make_circles(n_samples=n, noise=0.05, factor=0.5, random_state=seed),
        "variable_density": (Xv, np.repeat([0, 1, 2], n // 3)), "with_noise": (Xn, yn),
        "anisotropic": (Xb @ np.array([[0.6, -0.6], [-0.4, 0.8]]), yb),
        "spirals": (Xs, np.repeat([0, 1], n // 2)),
    }


def time_series_variants(n=1095, seed=SEED):
    """Daily attendance-like series: trend, weekly season, winter surge, changepoint, outliers, random walk."""
    r = np.random.RandomState(seed)
    t = np.arange(n)
    trend = 0.02 * t
    weekly = 8 * np.sin(2 * np.pi * t / 7)
    winter = 15 * np.maximum(0, np.cos(2 * np.pi * (t - 15) / 365))
    noise = r.normal(0, 4, n)
    base = 120 + trend + weekly + winter
    return {
        "trend_only": 120 + trend + noise,
        "weekly_only": 120 + weekly + noise,
        "full": base + noise,
        "with_changepoint": base + noise + 25 * (t > n // 2),
        "with_outliers": base + noise + (r.random(n) > 0.985) * r.normal(0, 50, n),
        "random_walk": 120 + np.cumsum(r.normal(0, 2, n)),
    }


def manifold_variants(n=1000, seed=SEED):
    Xs, ts = make_swiss_roll(n_samples=n, noise=0.5, random_state=seed)
    Xc, tc = make_s_curve(n_samples=n, noise=0.1, random_state=seed)
    return {"swiss_roll": (Xs, ts), "s_curve": (Xc, tc)}


def bandit_arms(k=5, seed=SEED):
    """k treatment arms with hidden Bernoulli response rates."""
    r = np.random.RandomState(seed)
    return r.uniform(0.15, 0.55, k)
