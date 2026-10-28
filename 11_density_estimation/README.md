# Module 11 — Density Estimation

**Tier** 3 · **Notebooks** 3 · **Prerequisites** 02, 07

> Reference ranges and what 'normal' really looks like.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Bandwidth & Kernels](01_kde/01_bandwidth_kernels.ipynb) | P1 | predict | `screening` |  | A biomarker's reference range by age |
| 01.02 | [Multivariate KDE & Histograms](01_kde/02_multivariate_kde_histograms.ipynb) | P1 | predict | `screening` |  | Two biomarkers jointly |
| 02.01 | [GMM as Density & Normalising Flows](02_parametric_flows/01_gmm_as_density_normalising_flows.ipynb) | P1 | predict | `synthetic` |  | A multimodal lab distribution |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 11_density_estimation` checks all of it.
