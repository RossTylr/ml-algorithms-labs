# Module 25 — Meta-Learning

**Tier** 3 · **Notebooks** 2 · **Prerequisites** 15, 16

> Rare diseases — learning from very few cases.

## Notebooks

| # | Notebook | Band | Dataset | Clinical problem |
|---|----------|------|---------|------------------|
| 01.01 | [Siamese, Prototypical, Matching & Relation Networks](01_metric/01_siamese_prototypical_matching_relation_networks.ipynb) | P1 | `imaging` | 5-way 1-shot rare lesion recognition |
| 02.01 | [MAML & Reptile](02_optimisation/01_maml_reptile.ipynb) | P1 | `imaging` | Adapting to a new site's scanner in 5 examples |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 25_meta_learning` checks all of it.
