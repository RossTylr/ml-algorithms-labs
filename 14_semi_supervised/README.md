# Module 14 — Semi-Supervised Learning

**Tier** 3 · **Notebooks** 4 · **Prerequisites** 05, 07

> Labels are expensive — a consultant's time.

## Notebooks

| # | Notebook | Band | Dataset | Clinical problem |
|---|----------|------|---------|------------------|
| 01.01 | [Self-Training & Co-Training](01_pseudo_labelling/01_self_training_co_training.ipynb) | P1 | `screening` | 50 of 500 patients adjudicated |
| 02.01 | [Label Propagation & Spreading](02_graph_based/01_label_propagation_spreading.ipynb) | P1 | `screening` | Labels flow along patient similarity |
| 03.01 | [TSVM, MixMatch & FixMatch](03_deep/01_tsvm_mixmatch_fixmatch.ipynb) | P1 | `imaging` | Lesion patches with few radiologist labels |
| 03.02 | [Contrastive Learning — SimCLR, BYOL, MoCo](03_deep/02_contrastive_learning_simclr_byol_moco.ipynb) | P1 | `imaging` | Patch representations without labels |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 14_semi_supervised` checks all of it.
