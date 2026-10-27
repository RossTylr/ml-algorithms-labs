# Module 08 — Dimensionality Reduction

**Tier** 2 · **Notebooks** 12 · **Prerequisites** 00, 07

> Seeing a 50-biomarker patient in two dimensions without lying.

## Notebooks

| # | Notebook | Band | Dataset | Clinical problem |
|---|----------|------|---------|------------------|
| 01.01 | [Eigendecomposition & Variance](01_pca/01_eigendecomposition_variance.ipynb) | P1 | `cohort` | 15 cohort features → 2D |
| 01.02 | [Reconstruction & Compression](01_pca/02_reconstruction_compression.ipynb) | P1 | `imaging` | Lesion patches compressed and rebuilt |
| 01.03 | [Incremental, Sparse & Kernel PCA](01_pca/03_incremental_sparse_kernel_pca.ipynb) | P1 | `synthetic` | Streaming; interpretable loadings; a curved biomarker manifold |
| 02.01 | [Truncated SVD, Factor Analysis & ICA](02_linear_other/01_truncated_svd_factor_analysis_ica.ipynb) | P1 | `notes` | Note TF-IDF; latent symptom factors; separating mixed physiological signals |
| 02.02 | [NMF & LDA (Supervised)](02_linear_other/02_nmf_lda_supervised.ipynb) | P1 | `imaging` | Lesion parts; disease-aware projection |
| 03.01 | [t-SNE](03_manifold/01_t_sne.ipynb) | P1 | `imaging` | Lesion patches — perplexity and what the plot lies about |
| 03.02 | [UMAP](03_manifold/02_umap.ipynb) | P1 | `imaging` | Same — global structure |
| 03.03 | [Isomap, LLE, Spectral Embedding & MDS](03_manifold/03_isomap_lle_spectral_embedding_mds.ipynb) | P1 | `synthetic` | A curved manifold four ways; a patient-distance matrix with no features |
| 03.04 | [Random Projections](03_manifold/04_random_projections.ipynb) | P4 | `cohort` | JL lemma on the cohort |
| 04.01 | [Autoencoders & VAEs for Reduction](04_neural/01_autoencoders_vaes_for_reduction.ipynb) | P1 | `imaging` | Lesion patches — linear AE ≈ PCA, then non-linear |
| 05.01 | [Filter Methods — MI & Chi²](05_feature_selection/01_filter_methods_mi_chi².ipynb) | P1 | `screening` | Which tests carry information about outcome |
| 05.02 | [Wrapper & Embedded — RFE & Boruta](05_feature_selection/02_wrapper_embedded_rfe_boruta.ipynb) | P1 | `screening` | The minimum panel |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 08_dimensionality_reduction` checks all of it.
