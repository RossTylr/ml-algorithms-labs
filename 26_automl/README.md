# Module 26 — AutoML & NAS

**Tier** 3 · **Notebooks** 3 · **Prerequisites** 06, 15

> Automating the search.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Grid, Random & Bayesian (Optuna)](01_hpo/01_grid_random_bayesian_optuna.ipynb) | P2 | decide | `admissions` |  | Readmission model tuning |
| 01.02 | [Hyperband & ASHA](01_hpo/02_hyperband_asha.ipynb) | P2 | decide | `admissions` |  | Early stopping |
| 02.01 | [NAS, DARTS & AutoML Frameworks](02_nas/01_nas_darts_automl_frameworks.ipynb) | P1 | predict | `imaging` | `novikov2025` | Searching a lesion classifier; auto-sklearn on admissions |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 26_automl` gates the module.
