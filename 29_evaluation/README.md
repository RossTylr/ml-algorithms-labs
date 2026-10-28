# Module 29 — Evaluation & Metrics

**Tier** 1 · **Notebooks** 10 · **Prerequisites** 04, 05, 06

> Measuring honestly — because the cost of a false negative is a person.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Sensitivity, Specificity, PPV, NPV, ROC & PR](01_classification_metrics/01_sensitivity_specificity_ppv_npv_roc_pr.ipynb) | P1 | predict | `screening` |  | A screening test — accuracy lies at 1% prevalence |
| 01.02 | [Confusion Matrix, MCC & Kappa](01_classification_metrics/02_confusion_matrix_mcc_kappa.ipynb) | P1 | predict | `screening` |  | Beyond accuracy; inter-rater agreement |
| 02.01 | [MSE, RMSE, MAE, MAPE & R²](02_regression_metrics/01_mse_rmse_mae_mape_r².ipynb) | P2 | decide | `admissions` |  | LOS residuals |
| 03.01 | [Silhouette, ARI, NMI, NDCG & MAP](03_clustering_ranking/01_silhouette_ari_nmi_ndcg_map.ipynb) | P1 | predict | `cohort` |  | Phenotypes; guideline retrieval lists |
| 04.01 | [Cross-Validation & Nested CV](04_validation/01_cross_validation_nested_cv.ipynb) | P2 | decide | `admissions` |  | Readmission — K-fold, stratified, temporal, patient-grouped |
| 04.02 | [Statistical Model Comparison](04_validation/02_statistical_model_comparison.ipynb) | P2 | decide | `admissions` |  | Two models, same folds |
| 05.01 | [Calibration — Reliability, Platt, Isotonic](05_calibration_bias/01_calibration_reliability_platt_isotonic.ipynb) | P1 | predict | `screening` | `TRIPOD calibration reporting` | Does 70% risk mean 70%? |
| 05.02 | [Bias–Variance Decomposition](05_calibration_bias/02_biasvariance_decomposition.ipynb) | P2 | decide | `admissions` |  | LOS — bias² + variance + noise |
| 06.01 | [Science About This Repo — the Ledger and the Digest as Data](06_meta/01_science_about_this_repo_the_ledger_and_the_digest_as_data.ipynb) | P4 | explain | `ledger` |  | After every other notebook is built: where did a strong model get it wrong first time, which registers slipped, where did Clinical Readings overclaim — the jagged frontier across ML, measured |
| 07.01 | [Demographic Parity, Equalised Odds & Calibration Across Groups](07_fairness/01_demographic_parity_equalised_odds_calibration_across_groups.ipynb) | P1 | explain | `cohort` | `Obermeyer et al. 2019 algorithmic bias in care management` | A risk model audited by sex, age band and deprivation |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 29_evaluation` gates the module.
