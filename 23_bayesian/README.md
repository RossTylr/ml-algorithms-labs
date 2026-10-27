# Module 23 — Bayesian Methods

**Tier** 3 · **Notebooks** 8 · **Prerequisites** 00, 02

> Uncertainty as a first-class clinical output.

## Notebooks

| # | Notebook | Band | Dataset | Clinical problem |
|---|----------|------|---------|------------------|
| 01.01 | [Bayesian Inference Fundamentals](01_inference/01_bayesian_inference_fundamentals.ipynb) | P1 | `screening` | A test's true positive rate — full posterior |
| 01.02 | [MCMC — Metropolis-Hastings & Gibbs](01_inference/02_mcmc_metropolis_hastings_gibbs.ipynb) | P3 | `trial` | Trial effect and variance jointly |
| 01.03 | [HMC, NUTS & Variational Inference](01_inference/03_hmc_nuts_variational_inference.ipynb) | P3 | `trial` | A hierarchical multi-site trial |
| 02.01 | [Bayesian Neural Networks](02_models/01_bayesian_neural_networks.ipynb) | P1 | `imaging` | Lesion classifier that knows when it doesn't know |
| 02.02 | [Gaussian Processes (Deep Dive)](02_models/02_gaussian_processes_deep_dive.ipynb) | P4 | `vitals` | Vitals — kernels, posterior, forecasting |
| 02.03 | [Bayesian Optimisation](02_models/03_bayesian_optimisation.ipynb) | P2 | `admissions` | Tuning a readmission model; dose finding |
| 03.01 | [PyMC, Stan & NumPyro](03_programming/01_pymc_stan_numpyro.ipynb) | P3 | `trial` | A full trial model with covariates |
| 03.02 | [Bayesian Nonparametrics](03_programming/02_bayesian_nonparametrics.ipynb) | P1 | `cohort` | Phenotypes without choosing k |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 23_bayesian` checks all of it.
