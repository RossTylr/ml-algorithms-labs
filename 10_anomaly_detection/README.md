# Module 10 — Anomaly Detection

**Tier** 2 · **Notebooks** 7 · **Prerequisites** 05, 07

> Deterioration, sensor failure, fraud, the one admission that doesn't fit.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Random Partitioning & Scoring](01_isolation/01_random_partitioning_scoring.ipynb) | P4 | predict | `vitals` |  | Vitals monitor faults — spikes, stuck values, drift |
| 02.01 | [LOF](02_density_based/01_lof.ipynb) | P1 | predict | `cohort` |  | Patients unusual relative to their neighbours |
| 02.02 | [One-Class SVM & Elliptic Envelope](02_density_based/02_one_class_svm_elliptic_envelope.ipynb) | P4 | predict | `vitals` |  | A boundary around normal physiology |
| 03.01 | [HBOS, COPOD & ECOD](03_fast_methods/01_hbos_copod_ecod.ipynb) | P4 | predict | `vitals` |  | Ward-scale real-time scoring |
| 03.02 | [Z-Score, IQR & Grubbs](03_fast_methods/02_z_score_iqr_grubbs.ipynb) | P4 | predict | `vitals` |  | Simple first |
| 04.01 | [Autoencoder Reconstruction Error](04_learned/01_autoencoder_reconstruction_error.ipynb) | P4 | predict | `vitals` |  | Deterioration as a bad reconstruction — in the spirit of NEWS2 early-warning comparison |
| 04.02 | [SUOD & Method Comparison](04_learned/02_suod_method_comparison.ipynb) | P5 | predict | `vitals` |  | Deployed monitoring with intermittent data — method × failure-type matrix |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 10_anomaly_detection` gates the module.
