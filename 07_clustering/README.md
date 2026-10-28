# Module 07 — Clustering

**Tier** 2 · **Notebooks** 15 · **Prerequisites** 00, 03

> Finding patient phenotypes nobody labelled.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Lloyd's Algorithm](01_kmeans/01_lloyds_algorithm.ipynb) | P1 | explain | `cohort` |  | Population segments for proactive care |
| 01.02 | [Evaluation & k Selection](01_kmeans/02_evaluation_k_selection.ipynb) | P1 | explain | `cohort` |  | How many phenotypes? |
| 01.03 | [Mini-Batch, K-Medoids, K-Modes, K-Prototypes](01_kmeans/03_mini_batch_k_medoids_k_modes_k_prototypes.ipynb) | P1 | predict | `cohort` |  | Scale; outlier patients; coded diagnoses; mixed |
| 01.04 | [Fuzzy C-Means](01_kmeans/04_fuzzy_c_means.ipynb) | P1 | predict | `cohort` |  | Patients between phenotypes |
| 02.01 | [Agglomerative Linkage & Dendrograms](02_hierarchical/01_agglomerative_linkage_dendrograms.ipynb) | P1 | predict | `synthetic` |  | Nested disease subtypes |
| 02.02 | [Cutting, Divisive & BIRCH](02_hierarchical/02_cutting_divisive_birch.ipynb) | P4 | predict | `cohort` |  | Choosing a cut; top-down; 500k streaming records |
| 03.01 | [DBSCAN](03_density/01_dbscan.ipynb) | P1 | predict | `synthetic` |  | Phenotypes with irregular shapes and noise patients |
| 03.02 | [OPTICS & HDBSCAN](03_density/02_optics_hdbscan.ipynb) | P1 | predict | `synthetic` |  | Variable-density phenotypes |
| 03.03 | [Mean Shift](03_density/03_mean_shift.ipynb) | P1 | predict | `synthetic` |  | Multimodal biomarker space |
| 04.01 | [EM Algorithm](04_gmm/01_em_algorithm.ipynb) | P1 | predict | `synthetic` |  | Overlapping disease subgroups |
| 04.02 | [Model Selection & Bayesian GMM](04_gmm/02_model_selection_bayesian_gmm.ipynb) | P1 | predict | `synthetic` |  | Unknown subgroup count |
| 05.01 | [Spectral Clustering](05_graph_based/01_spectral_clustering.ipynb) | P1 | predict | `synthetic` |  | Interleaved trajectories |
| 05.02 | [Affinity Propagation](05_graph_based/02_affinity_propagation.ipynb) | P1 | predict | `cohort` |  | Exemplar patients |
| 06.01 | [Self-Organising Maps](06_other_clustering/01_self_organising_maps.ipynb) | P1 | predict | `cohort` |  | Topological map of a cohort |
| 06.02 | [CURE & CLARANS](06_other_clustering/02_cure_clarans.ipynb) | P4 | predict | `synthetic` |  | Non-spherical at scale |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 07_clustering` checks all of it.
