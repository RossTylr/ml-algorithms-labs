# Module 24 — Probabilistic Graphical Models

**Tier** 3 · **Notebooks** 6 · **Prerequisites** 02, 23

> Disease progression and tracking as structured uncertainty.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Bayesian Networks & MRFs](01_networks/01_bayesian_networks_mrfs.ipynb) | P1 | predict | `screening` |  | A diagnostic network of symptoms and causes; pixel labelling |
| 01.02 | [Belief Propagation](01_networks/02_belief_propagation.ipynb) | P1 | predict | `synthetic` |  | Inference on the diagnostic network |
| 02.01 | [HMMs — Forward/Backward, Viterbi, Baum-Welch](02_sequential/01_hmms_forward_backward_viterbi_baum_welch.ipynb) | P2 | decide | `vitals` |  | Hidden health state well/mild/severe from observed vitals |
| 02.02 | [CRFs](02_sequential/02_crfs.ipynb) | P1 | predict | `notes` |  | Entity labelling in notes |
| 03.01 | [Kalman, EKF & UKF](03_filtering/01_kalman_ekf_ukf.ipynb) | P5 | decide | `evac` |  | Tracking an evacuation vehicle from noisy position reports |
| 03.02 | [Particle Filters](03_filtering/02_particle_filters.ipynb) | P4 | predict | `vitals` |  | Patient state from intermittent observations |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 24_pgm` checks all of it.
