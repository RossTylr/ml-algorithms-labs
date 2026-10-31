# Module 05 — Classification

**Tier** 1 · **Notebooks** 18 · **Prerequisites** 04

> Diagnosis as decision boundary — what shapes can each classifier draw through a patient population?

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Sigmoid & Decision Boundary](01_logistic/01_sigmoid_decision_boundary.ipynb) | P1 | predict | `screening` |  | Disease present/absent from two biomarkers — the baseline that every 'radiologist-level' claim is measured against — in the spirit of Framingham-style risk scoring |
| 01.02 | [Multiclass & Regularisation](01_logistic/02_multiclass_regularisation.ipynb) | P5 | decide | `synthetic` |  | Triage category T1–T4 from injury features |
| 02.01 | [Distance Metrics & k Selection](02_knn/01_distance_metrics_k_selection.ipynb) | P1 | predict | `screening` |  | Patients like this patient — three diagnoses in 2D biomarker space |
| 02.02 | [Scaling & Efficiency](02_knn/02_scaling_efficiency.ipynb) | P4 | predict | `cohort` |  | Same at 100k patients |
| 03.01 | [Gaussian, Multinomial & Bernoulli](03_naive_bayes/01_gaussian_multinomial_bernoulli.ipynb) | P1 | predict | `notes` |  | Biomarkers (Gaussian); triage note words (Multinomial); symptom checklist (Bernoulli) |
| 03.02 | [Complement NB & Rare Outcomes](03_naive_bayes/02_complement_nb_rare_outcomes.ipynb) | P1 | predict | `notes` |  | Notes where the serious outcome is rare |
| 04.01 | [Splitting Criteria & Visualisation](04_decision_trees/01_splitting_criteria_visualisation.ipynb) | P1 | predict | `screening` |  | A clinical decision rule learned from data — mixed features — in the spirit of Ottawa ankle rule style decision rules |
| 04.02 | [Pruning & Overfitting](04_decision_trees/02_pruning_overfitting.ipynb) | P1 | predict | `screening` |  | Same — a rule a clinician could carry |
| 04.03 | [ID3, C4.5 & Gain Ratio](04_decision_trees/03_id3_c45_gain_ratio.ipynb) | P1 | predict | `notes` |  | Categorical-heavy symptom data |
| 05.01 | [Maximum Margin (Linear)](05_svm/01_maximum_margin_linear.ipynb) | P1 | predict | `synthetic` | `cortes1995` | Two clearly separable diagnoses |
| 05.02 | [Dual Formulation & Support Vectors](05_svm/02_dual_formulation_support_vectors.ipynb) | P1 | predict | `synthetic` |  | Why only the borderline patients define the rule |
| 05.03 | [Kernel Trick (Non-Linear)](05_svm/03_kernel_trick_non_linear.ipynb) | P1 | predict | `synthetic` |  | Diagnoses with curved boundaries — moons, rings, XOR in biomarker space |
| 05.04 | [Tuning & Multiclass](05_svm/04_tuning_multiclass.ipynb) | P1 | predict | `synthetic` |  | C/γ grid |
| 06.01 | [LDA & QDA](06_discriminant/01_lda_qda.ipynb) | P1 | predict | `screening` |  | Biomarkers — equal vs unequal covariance between disease groups |
| 07.01 | [Perceptron](07_online/01_perceptron.ipynb) | P1 | predict | `synthetic` |  | Separable, then XOR |
| 07.02 | [SGD & Passive-Aggressive](07_online/02_sgd_passive_aggressive.ipynb) | P4 | predict | `vitals` |  | A deterioration classifier learning from a live vitals stream with drift |
| 08.01 | [Centroid Classification](08_nearest_centroid/01_centroid_classification.ipynb) | P1 | predict | `screening` |  | The simplest diagnostic rule |
| 09.01 | [Probabilistic Classification](09_gp_classification/01_probabilistic_classification.ipynb) | P1 | predict | `synthetic` |  | A diagnosis with an honest uncertainty surface |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py 05_classification` gates the module.
