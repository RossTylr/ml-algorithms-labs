# Module 00 — Mathematical Foundations

**Tier** 1 · **Notebooks** 12 · **Prerequisites** None

> Every concept motivated by a clinical use. 'Why do I need this?' before 'What is this?'

## Notebooks

| # | Notebook | Band | Dataset | Clinical problem |
|---|----------|------|---------|------------------|
| 01.01 | [Vectors, Matrices & Operations](01_linear_algebra/01_vectors_matrices_operations.ipynb) | P1 | `screening` | A patient as a vector of biomarkers; a lab panel as a matrix; similarity between patients as a dot product |
| 01.02 | [Eigenvalues & Decomposition](01_linear_algebra/02_eigenvalues_decomposition.ipynb) | P1 | `screening` | Principal directions of variation in a biomarker cloud — which combinations of tests carry the signal |
| 01.03 | [SVD & Low-Rank Approximation](01_linear_algebra/03_svd_low_rank_approximation.ipynb) | P1 | `imaging` | Compressing lesion patches — how many singular values preserve the lesion |
| 02.01 | [Derivatives & Gradients](02_calculus/01_derivatives_gradients.ipynb) | P2 | `synthetic` | Dose-response surface — the steepest path to the therapeutic window |
| 02.02 | [Chain Rule, Jacobians & Hessians](02_calculus/02_chain_rule_jacobians_hessians.ipynb) | P2 | `synthetic` | A care pathway as composed functions — how a change at triage propagates to discharge |
| 03.01 | [Probability Fundamentals & Bayes](03_probability/01_probability_fundamentals_bayes.ipynb) | P1 | `screening` | Screening a rare disease — prevalence, sensitivity, specificity, and what a positive result really means |
| 03.02 | [Distributions & Sampling](03_probability/02_distributions_sampling.ipynb) | P4 | `admissions` | ED arrivals per hour (Poisson), LOS (log-normal), survival to event (exponential), test positivity (Binomial) |
| 03.03 | [MLE & MAP Estimation](03_probability/03_mle_map_estimation.ipynb) | P1 | `screening` | Estimating a test's true positive rate from a validation sample |
| 04.01 | [Gradient Descent Variants](04_optimisation/01_gradient_descent_variants.ipynb) | P2 | `cohort` | Fitting a risk score — batch, stochastic and mini-batch on a 10k-patient cohort |
| 04.02 | [Constrained Optimisation](04_optimisation/02_constrained_optimisation.ipynb) | P4 | `synthetic` | Theatre scheduling — maximise cases under staff-hours and bed constraints |
| 05.01 | [Entropy, Divergence & Mutual Information](05_information_theory/01_entropy_divergence_mutual_information.ipynb) | P1 | `screening` | How much does each test tell you? Information gain of a biomarker about disease status |
| 06.01 | [Stability, Precision & Solvers](06_numerical_methods/01_stability_precision_solvers.ipynb) | P4 | `synthetic` | Where rounding kills — cumulative drug dosing, ill-conditioned risk models |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 00_mathematical_foundations` checks all of it.
