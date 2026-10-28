# Project 01 — Sidey-Gibbons replication (in spirit)

**Build after**: 05.01 logistic, 05.05 SVM, 15.01 MLP are BUILT.
**In the spirit of**: Sidey-Gibbons & Sidey-Gibbons (2019), *Machine learning in medicine: a practical introduction*, BMC Med Res Methodol — `library:sideygibbons2019`.

The paper fits a regularised GLM, an RBF-SVM and a single-layer ANN to the Wisconsin breast-cancer nuclei data (N = 683) and reports
a full comparison table with sensitivity, specificity, AUC and calibration. This project re-runs that comparison end to end on
`datasets.load_screening()` (synthetic, N = 2000, prevalence 15%), adds the clinician two-marker baseline, and ends with the
sixth quiz question: *what did the paper claim that this synthetic replication cannot test?*

Deliverable: one notebook, `01_replication.ipynb`, gated like any other (G1–G14) plus a comparison table in the paper's layout.
