# Module 06 — Ensemble Methods

**Tier** 1 · **Notebooks** 15 · **Prerequisites** 05

> Why most deployed clinical risk models are gradient-boosted trees.

## Notebooks

| # | Notebook | Band | Dataset | Clinical problem |
|---|----------|------|---------|------------------|
| 01.01 | [Bootstrap Aggregating](01_bagging/01_bootstrap_aggregating.ipynb) | P2 | `admissions` | One tree vs 100 for LOS |
| 02.01 | [Feature Subsampling & OOB](02_random_forest/01_feature_subsampling_oob.ipynb) | P2 | `admissions` | Readmission from 15 features — correlated, noisy, irrelevant |
| 02.02 | [Tuning & Interpretation](02_random_forest/02_tuning_interpretation.ipynb) | P2 | `admissions` | Full hyperparameter space; PDP on age and severity |
| 03.01 | [Extreme Randomisation](03_extra_trees/01_extreme_randomisation.ipynb) | P2 | `admissions` | RF vs ET |
| 04.01 | [Adaptive Boosting](04_adaboost/01_adaptive_boosting.ipynb) | P1 | `screening` | Diagnosis — the hard cases get reweighted |
| 05.01 | [Gradient Descent in Function Space](05_gradient_boosting/01_gradient_descent_in_function_space.ipynb) | P2 | `admissions` | LOS — fitting residuals |
| 05.02 | [Regularisation & Early Stopping](05_gradient_boosting/02_regularisation_early_stopping.ipynb) | P2 | `admissions` | Same |
| 06.01 | [Regularised Boosting](06_xgboost/01_regularised_boosting.ipynb) | P2 | `admissions` | Readmission — the production baseline |
| 06.02 | [Advanced Features](06_xgboost/02_advanced_features.ipynb) | P2 | `admissions` | Monotone-in-severity constraint; custom loss; missing labs |
| 07.01 | [LightGBM](07_lightgbm_catboost/01_lightgbm.ipynb) | P4 | `cohort` | Cohort at 100k rows — speed |
| 07.02 | [CatBoost](07_lightgbm_catboost/02_catboost.ipynb) | P2 | `admissions` | Admissions — many categoricals |
| 08.01 | [Binned Features (sklearn)](08_hist_gb/01_binned_features_sklearn.ipynb) | P2 | `admissions` | Speed vs exact |
| 09.01 | [Stacking & Blending](09_stacking/01_stacking_blending.ipynb) | P2 | `admissions` | RF + GBM + logistic for readmission |
| 09.02 | [Voting](09_stacking/02_voting.ipynb) | P1 | `screening` | Diverse diagnostic classifiers |
| 10.01 | [Isolation Forest & Rotation Forest](10_other_ensembles/01_isolation_forest_rotation_forest.ipynb) | P4 | `admissions` | Anomalous admissions; rotated bagging |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 06_ensembles` checks all of it.
