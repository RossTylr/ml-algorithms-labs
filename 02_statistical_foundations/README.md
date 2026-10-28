# Module 02 — Statistical Foundations

**Tier** 1 · **Notebooks** 13 · **Prerequisites** 00, 01

> Recognise, test and handle the assumptions every clinical model makes.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Central Tendency, Dispersion & Shape](01_descriptive/01_central_tendency_dispersion_shape.ipynb) | P2 | decide | `admissions` |  | Length of stay across five departments — skewed, normal, bimodal |
| 02.01 | [Hypothesis Testing Fundamentals](02_inferential/01_hypothesis_testing_fundamentals.ipynb) | P3 | explain | `admissions` | `wasserstein2016` | Did the new discharge protocol cut LOS? Null, p-value, power |
| 02.02 | [Common Parametric Tests](02_inferential/02_common_parametric_tests.ipynb) | P3 | explain | `trial` |  | Three analgesia regimens; defect rates across three labs |
| 02.03 | [Non-Parametric & Exact Tests](02_inferential/03_non_parametric_exact_tests.ipynb) | P3 | explain | `trial` | `ramdas2024` | Ordinal pain scores across sites; rare-event 2×2 |
| 03.01 | [Discrete Distributions](03_distributions/01_discrete_distributions.ipynb) | P4 | predict | `admissions` |  | Arrivals, test positives, trials to first readmission |
| 03.02 | [Continuous Distributions](03_distributions/02_continuous_distributions.ipynb) | P2 | decide | `admissions` |  | LOS (log-normal), time to event (exponential/Weibull), lab values (Normal), dosing (Gamma) |
| 04.01 | [CLT Intuition & Implications](04_clt/01_clt_intuition_implications.ipynb) | P3 | explain | `trial` |  | Why trial mean outcomes are Normal even when individual outcomes aren't |
| 05.01 | [Measuring Relationships](05_correlation/01_measuring_relationships.ipynb) | P1 | explain | `screening` |  | Biomarkers vs outcome — linear, monotonic, non-linear, spurious |
| 06.01 | [Designing, Running & Interpreting Experiments](06_ab_testing/01_designing_running_interpreting_experiments.ipynb) | P4 | predict | `synthetic` |  | Appointment-reminder redesign — DNA rate |
| 07.01 | [Bootstrap, Permutation & Jackknife](07_resampling/01_bootstrap_permutation_jackknife.ipynb) | P3 | explain | `admissions` |  | Median LOS reduction from 200 patients — how sure? |
| 08.01 | [MLE in Practice](08_mle/01_mle_in_practice.ipynb) | P1 | predict | `screening` |  | Arrival rate; lab error; a risk score as MLE |
| 09.01 | [Two Philosophies, One Trial](09_bayes_vs_freq/01_two_philosophies_one_trial.ipynb) | P3 | explain | `trial` | `box1976` | Drug efficacy — posterior vs confidence interval on the same data |
| 10.01 | [Practical vs Statistical Significance](10_effect_sizes/01_practical_vs_statistical_significance.ipynb) | P3 | explain | `trial` |  | 1 mmHg at p<0.001 — NNT, Cohen's d, minimal clinically important difference |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 02_statistical_foundations` gates the module.
