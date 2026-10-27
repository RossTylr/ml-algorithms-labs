# Module 27 — Explainability

**Tier** 3 · **Notebooks** 6 · **Prerequisites** 06, 16

> No model reaches a clinician without an answer to 'why?'

## Notebooks

| # | Notebook | Band | Dataset | Clinical problem |
|---|----------|------|---------|------------------|
| 01.01 | [Feature Importance — MDI, Permutation, Drop-Column](01_global/01_feature_importance_mdi_permutation_drop_column.ipynb) | P2 | `admissions` | Readmission — three methods disagree |
| 01.02 | [PDP & ICE](01_global/02_pdp_ice.ipynb) | P2 | `admissions` | Age and severity effects |
| 02.01 | [SHAP — Theory & Practice](02_local/01_shap_theory_practice.ipynb) | P2 | `admissions` | Why this patient was flagged |
| 02.02 | [LIME, Anchors & Counterfactuals](02_local/02_lime_anchors_counterfactuals.ipynb) | P2 | `admissions` | One flag, three explanations; what would un-flag them |
| 03.01 | [Grad-CAM, Integrated Gradients & Attention Viz](03_deep/01_grad_cam_integrated_gradients_attention_viz.ipynb) | P1 | `imaging` | Where the CNN looked; which words the transformer weighed |
| 03.02 | [Mechanistic Interpretability](03_deep/02_mechanistic_interpretability.ipynb) | P1 | `synthetic` | Circuits in a small diagnostic network |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 27_explainability` checks all of it.
