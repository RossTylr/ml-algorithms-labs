"""shared.evaluation — clinical-first evaluation visuals: sensitivity/specificity, PPV at prevalence, calibration."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.calibration import calibration_curve
from sklearn.metrics import (auc, average_precision_score, confusion_matrix, mean_absolute_error,
                             mean_squared_error, precision_recall_curve, r2_score, roc_curve,
                             silhouette_samples, silhouette_score)

from .plotting import PALETTE


def diagnostic_report(y_true, y_proba, threshold=0.5, prevalence=None, title="Diagnostic performance"):
    """Confusion matrix + ROC + PR + sensitivity/specificity/PPV/NPV at the threshold.
    If prevalence given, PPV/NPV are re-expressed at that population prevalence."""
    y_pred = (y_proba >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    sens, spec = tp / (tp + fn), tn / (tn + fp)
    prev = prevalence if prevalence is not None else y_true.mean()
    ppv = sens * prev / (sens * prev + (1 - spec) * (1 - prev))
    npv = spec * (1 - prev) / (spec * (1 - prev) + (1 - sens) * prev)

    fig, ax = plt.subplots(1, 3, figsize=(20, 6))
    sns.heatmap([[tn, fp], [fn, tp]], annot=True, fmt="d", cmap="Blues", ax=ax[0],
                xticklabels=["pred −", "pred +"], yticklabels=["true −", "true +"])
    ax[0].set_title(f"Confusion @ threshold {threshold:.2f}")
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    ax[1].plot(fpr, tpr, lw=2, label=f"AUC {auc(fpr, tpr):.3f}"); ax[1].plot([0, 1], [0, 1], "k--", alpha=0.3)
    ax[1].scatter([1 - spec], [sens], s=120, zorder=5, color=PALETTE[1], label="operating point")
    ax[1].set(xlabel="1 − specificity", ylabel="sensitivity", title="ROC"); ax[1].legend()
    p, r, _ = precision_recall_curve(y_true, y_proba)
    ax[2].plot(r, p, lw=2, color=PALETTE[1], label=f"AP {average_precision_score(y_true, y_proba):.3f}")
    ax[2].axhline(prev, ls="--", color="grey", label=f"prevalence {prev:.2%}")
    ax[2].set(xlabel="sensitivity (recall)", ylabel="PPV (precision)", title="Precision–Recall"); ax[2].legend()
    fig.suptitle(f"{title}\nSens {sens:.2f} · Spec {spec:.2f} · PPV {ppv:.2f} · NPV {npv:.2f} @ prevalence {prev:.1%}", fontweight="bold")
    plt.tight_layout()
    return fig, dict(sensitivity=sens, specificity=spec, ppv=ppv, npv=npv, prevalence=prev)


def calibration_report(y_true, y_proba, n_bins=10, title="Calibration"):
    frac, mean_pred = calibration_curve(y_true, y_proba, n_bins=n_bins)
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    ax[0].plot(mean_pred, frac, "o-", lw=2, label="model"); ax[0].plot([0, 1], [0, 1], "k--", label="perfect")
    ax[0].set(xlabel="predicted risk", ylabel="observed frequency", title="Reliability diagram"); ax[0].legend()
    ax[1].hist(y_proba, bins=30, color=PALETTE[0], alpha=0.8); ax[1].set(xlabel="predicted risk", ylabel="count", title="Risk distribution")
    fig.suptitle(title, fontweight="bold"); plt.tight_layout()
    return fig


def regression_report(y_true, y_pred, title="Regression diagnostics"):
    from scipy import stats
    res = np.asarray(y_true) - np.asarray(y_pred)
    fig, ax = plt.subplots(2, 2, figsize=(14, 10))
    ax[0, 0].scatter(y_pred, y_true, alpha=0.5, edgecolors="k", lw=0.3)
    lim = [min(np.min(y_pred), np.min(y_true)), max(np.max(y_pred), np.max(y_true))]
    ax[0, 0].plot(lim, lim, "k--", alpha=0.5); ax[0, 0].set(xlabel="predicted", ylabel="actual", title="Predicted vs actual")
    ax[0, 1].hist(res, bins=30, color=PALETTE[1], edgecolor="k", alpha=0.7); ax[0, 1].axvline(0, color="k", ls="--"); ax[0, 1].set(title="Residuals")
    ax[1, 0].scatter(y_pred, res, alpha=0.5, color=PALETTE[2], edgecolors="k", lw=0.3); ax[1, 0].axhline(0, color="k", ls="--"); ax[1, 0].set(xlabel="fitted", ylabel="residual", title="Residuals vs fitted")
    stats.probplot(res, dist="norm", plot=ax[1, 1]); ax[1, 1].set_title("Normal Q–Q")
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    fig.suptitle(f"{title}\nRMSE {rmse:.3f} · MAE {mean_absolute_error(y_true, y_pred):.3f} · R² {r2_score(y_true, y_pred):.3f}", fontweight="bold")
    plt.tight_layout()
    return fig


def clustering_report(X, labels, title="Clustering evaluation"):
    k = len(set(labels)) - (1 if -1 in labels else 0)
    fig, ax = plt.subplots(figsize=(10, 6))
    if k > 1:
        sv = silhouette_samples(X, labels); lo = 10
        for i in range(k):
            v = np.sort(sv[labels == i]); hi = lo + len(v)
            ax.fill_betweenx(np.arange(lo, hi), 0, v, color=PALETTE[i % 10], alpha=0.8); ax.text(-0.05, lo + len(v) / 2, str(i)); lo = hi + 10
        ax.axvline(silhouette_score(X, labels), color="red", ls="--", label=f"mean {silhouette_score(X, labels):.3f}")
        ax.legend()
    ax.set(xlabel="silhouette coefficient", ylabel="cluster", title=f"{title} (k={k})")
    return fig
