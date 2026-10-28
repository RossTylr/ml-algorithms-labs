# Module 28 — Specialised & Emerging

**Tier** 3 · **Notebooks** 11 · **Prerequisites** None

> Methods the clinic has always needed.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Kaplan-Meier & Cox PH](01_survival/01_kaplan_meier_cox_ph.ipynb) | P3 | explain | `trial` | `Cox (1972); KM on trial endpoints` | Time to readmission by arm; hazard ratios |
| 01.02 | [Random Survival Forests & DeepSurv](01_survival/02_random_survival_forests_deepsurv.ipynb) | P3 | explain | `trial` |  | Non-linear survival |
| 02.01 | [Propensity Scores & Instrumental Variables](02_causal/01_propensity_scores_instrumental_variables.ipynb) | P3 | explain | `admissions` |  | Did the treatment work when it wasn't randomised? |
| 02.02 | [Diff-in-Diff, DoWhy & Double ML](02_causal/02_diff_in_diff_dowhy_double_ml.ipynb) | P3 | explain | `admissions` |  | A policy change across sites; graphs; debiased estimation |
| 03.01 | [Spatial Accessibility to Care — 2SFCA](03_spatial/01_spatial_accessibility_to_care_2sfca.ipynb) | P5 | decide | `areas` | `luo2003` | Travel-time access to a Role 2 / primary-care site on a synthetic grid — where should the next facility go? |
| 04.01 | [Collaborative Filtering & Matrix Factorisation](04_recommenders/01_collaborative_filtering_matrix_factorisation.ipynb) | P2 | decide | `prescribing` |  | Patients like this one responded to… |
| 04.02 | [NCF, Content-Based, Hybrid & Two-Tower](04_recommenders/02_ncf_content_based_hybrid_two_tower.ipynb) | P2 | decide | `notes` | `manning2009` | Guideline retrieval |
| 05.01 | [LoRA, QLoRA & Quantisation](05_llm/01_lora_qlora_quantisation.ipynb) | P5 | decide | `notes` |  | A clinical note model small enough to run offline at a forward site |
| 05.02 | [RAG & Agents](05_llm/02_rag_agents.ipynb) | P1 | predict | `notes` | `lewis2021` | Guideline-grounded answers; a Sequential-Diagnosis-style gatekeeper loop scored on accuracy AND information cost |
| 06.01 | [Vision-Language, Audio & Knowledge Graph Embeddings](06_multimodal/01_vision_language_audio_knowledge_graph_embeddings.ipynb) | P1 | predict | `synthetic` |  | Image–report pairing; dictation; drug–disease graph |
| 07.01 | [Genetic Algorithms, CMA-ES & NEAT](07_evolutionary/01_genetic_algorithms_cma_es_neat.ipynb) | P4 | predict | `synthetic` |  | Rota optimisation; evolving a monitoring controller |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 28_specialised` checks all of it.
