# Module 03 — Data Engineering Essentials

**Tier** 1 · **Notebooks** 8 · **Prerequisites** 01, 02

> Every mistake here silently ruins everything downstream — and in health, downstream is a patient.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [ETL, Validation & Contracts](01_pipelines/01_etl_validation_contracts.ipynb) | P4 | predict | `vitals` |  | Daily vitals feed — extract, unit-convert, gap-fill, validate schema |
| 02.01 | [Numerical Transforms](02_feature_engineering/01_numerical_transforms.ipynb) | P2 | decide | `admissions` | `guyon2004` | Admissions — LOS, age, comorbidity count → log, bins, interactions |
| 02.02 | [Temporal & Domain Features](02_feature_engineering/02_temporal_domain_features.ipynb) | P4 | predict | `vitals` |  | Vitals — cyclical hour-of-day, lags, rolling trends, NEWS2-style derived scores |
| 03.01 | [Standardisation, Normalisation & Robust Scaling](03_scaling/01_standardisation_normalisation_robust_scaling.ipynb) | P1 | predict | `screening` |  | Biomarkers on wildly different units; KNN/SVM/RF with and without |
| 04.01 | [Encoding Strategies](04_encoding/01_encoding_strategies.ipynb) | P2 | decide | `admissions` |  | Department (5), diagnosis code (200), GP practice (very high cardinality) |
| 05.01 | [Leakage, Stratification & Temporal Splits](05_splitting/01_leakage_stratification_temporal_splits.ipynb) | P2 | decide | `admissions` |  | Predict readmission — temporal order, imbalance, repeat patients |
| 06.01 | [Resampling & Cost-Sensitive Learning](06_imbalance/01_resampling_cost_sensitive_learning.ipynb) | P5 | decide | `synthetic` |  | Mass-casualty triage — 2% immediate, and the cost of missing one |
| 07.01 | [Systematic Exploration](07_eda/01_systematic_exploration.ipynb) | P1 | predict | `cohort` |  | A de-identified cohort extract with unlabelled columns — discover structure by method |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 03_data_engineering` checks all of it.
