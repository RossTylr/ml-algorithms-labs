# Module 04 — Regression

**Tier** 1 · **Notebooks** 14 · **Prerequisites** 00, 01, 02, 03

> Predicting continuous outcomes — LOS, dose, cost, biomarker trajectory.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [OLS Intuition & Mathematics](01_simple_linear/01_ols_intuition_mathematics.ipynb) | P2 | decide | `admissions` | `shalizi2024` | Length of stay from severity score alone |
| 01.02 | [Assumptions & Diagnostics](01_simple_linear/02_assumptions_diagnostics.ipynb) | P2 | decide | `admissions` |  | Same with heteroscedastic LOS, curvature, heavy tails |
| 02.01 | [Multivariate Extension](02_multiple_linear/01_multivariate_extension.ipynb) | P2 | explain | `admissions` |  | LOS from all admission features |
| 02.02 | [Multicollinearity & VIF](02_multiple_linear/02_multicollinearity_vif.ipynb) | P1 | explain | `screening` |  | Two correlated biomarkers — disentangling |
| 03.01 | [Bias–Variance & Overfitting](03_polynomial/01_biasvariance_overfitting.ipynb) | P2 | decide | `synthetic` |  | Dose–response with known quadratic truth, degrees 1–15 |
| 04.01 | [Ridge](04_regularised/01_ridge.ipynb) | P1 | predict | `screening` |  | A 50-biomarker panel, most weak |
| 04.02 | [Lasso](04_regularised/02_lasso.ipynb) | P1 | predict | `screening` | `hastie2018` | A 50-biomarker panel, most irrelevant — which tests to keep |
| 04.03 | [Elastic Net](04_regularised/03_elastic_net.ipynb) | P1 | predict | `screening` |  | Correlated biomarker groups |
| 05.01 | [Uncertainty Quantification](05_bayesian_linear/01_uncertainty_quantification.ipynb) | P3 | explain | `trial` |  | Only 40 patients in a pilot — how sure is the dose effect? |
| 06.01 | [Conditional Quantiles](06_quantile/01_conditional_quantiles.ipynb) | P4 | predict | `admissions` |  | 90th-percentile LOS for bed planning, not the mean |
| 07.01 | [RANSAC & Huber](07_robust/01_ransac_huber.ipynb) | P2 | decide | `admissions` |  | Admissions with 10% data-entry corruption |
| 08.01 | [Monotonic Constraints & Calibration](08_isotonic/01_monotonic_constraints_calibration.ipynb) | P1 | predict | `screening` |  | Calibrating a diagnostic model's probabilities |
| 09.01 | [Kernels & Priors](09_gaussian_process/01_kernels_priors.ipynb) | P4 | predict | `vitals` |  | A patient's heart rate over 72 hours — periodic (circadian) and smooth |
| 09.02 | [Posterior Inference & Uncertainty](09_gaussian_process/02_posterior_inference_uncertainty.ipynb) | P4 | predict | `vitals` |  | Same — forecasting the next 6 hours with bands |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 04_regression` gates the module.
