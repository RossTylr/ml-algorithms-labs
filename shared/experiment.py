"""shared.experiment — run-and-tabulate helpers for parameter sweeps and model comparisons."""
from __future__ import annotations

import time

import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import cross_val_score


def parameter_sweep(model_fn, name, values, Xtr, ytr, Xte, yte, scoring="accuracy", cv=5) -> pd.DataFrame:
    rows = []
    for v in values:
        m = model_fn(v); t0 = time.time(); m.fit(Xtr, ytr); dt = time.time() - t0
        cvs = cross_val_score(m, Xtr, ytr, cv=cv, scoring=scoring)
        rows.append(dict(value=v, train=m.score(Xtr, ytr), test=m.score(Xte, yte), cv_mean=cvs.mean(), cv_std=cvs.std(), seconds=dt))
    df = pd.DataFrame(rows); df.index.name = name
    return df


def compare_models(models: dict, Xtr, ytr, Xte, yte, scoring="accuracy", cv=5) -> pd.DataFrame:
    rows = []
    for name, m in models.items():
        t0 = time.time(); m.fit(Xtr, ytr); dt = time.time() - t0
        cvs = cross_val_score(m, Xtr, ytr, cv=cv, scoring=scoring)
        rows.append(dict(model=name, train=m.score(Xtr, ytr), test=m.score(Xte, yte), cv_mean=cvs.mean(), cv_std=cvs.std(), seconds=dt))
    return pd.DataFrame(rows).set_index("model")


def data_variation(model, variants: dict, score_fn) -> pd.DataFrame:
    rows = []
    for name, (Xtr, ytr, Xte, yte) in variants.items():
        m = clone(model); m.fit(Xtr, ytr)
        rows.append(dict(variant=name, train=score_fn(ytr, m.predict(Xtr)), test=score_fn(yte, m.predict(Xte))))
    return pd.DataFrame(rows).set_index("variant")
