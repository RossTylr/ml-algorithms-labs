# Module 29 — Evaluation & Metrics

**Tier** 1 · **Notebooks** 9 · **Prerequisites** 04, 05, 06

> Measuring honestly — because the cost of a false negative is a person.

## Notebooks

| # | Notebook | Band | Dataset | Clinical problem |
|---|----------|------|---------|------------------|
| 01.01 | [Sensitivity, Specificity, PPV, NPV, ROC & PR](01_classification_metrics/01_sensitivity_specificity_ppv_npv_roc_pr.ipynb) | P1 | `screening` | A screening test — accuracy lies at 1% prevalence |
| 01.02 | [Confusion Matrix, MCC & Kappa](01_classification_metrics/02_confusion_matrix_mcc_kappa.ipynb) | P1 | `screening` | Beyond accuracy; inter-rater agreement |
| 02.01 | [MSE, RMSE, MAE, MAPE & R²](02_regression_metrics/01_mse_rmse_mae_mape_r².ipynb) | P2 | `admissions` | LOS residuals |
| 03.01 | [Silhouette, ARI, NMI, NDCG & MAP](03_clustering_ranking/01_silhouette_ari_nmi_ndcg_map.ipynb) | P1 | `cohort` | Phenotypes; guideline retrieval lists |
| 04.01 | [Cross-Validation & Nested CV](04_validation/01_cross_validation_nested_cv.ipynb) | P2 | `admissions` | Readmission — K-fold, stratified, temporal, patient-grouped |
| 04.02 | [Statistical Model Comparison](04_validation/02_statistical_model_comparison.ipynb) | P2 | `admissions` | Two models, same folds |
| 05.01 | [Calibration — Reliability, Platt, Isotonic](05_calibration_bias/01_calibration_reliability_platt_isotonic.ipynb) | P1 | `screening` | Does 70% risk mean 70%? |
| 05.02 | [Bias–Variance Decomposition](05_calibration_bias/02_biasvariance_decomposition.ipynb) | P2 | `admissions` | LOS — bias² + variance + noise |
| 06.01 | [Demographic Parity, Equalised Odds & Calibration Across Groups](06_fairness/01_demographic_parity_equalised_odds_calibration_across_groups.ipynb) | P1 | `cohort` | A risk model audited by sex, age band and deprivation |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 29_evaluation` checks all of it.
