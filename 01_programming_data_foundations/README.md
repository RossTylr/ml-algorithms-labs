# Module 01 — Programming & Data Foundations

**Tier** 1 · **Notebooks** 12 · **Prerequisites** 00

> The Python patterns health data work requires.

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
| 01.01 | [Core Python for Health Data](01_python_patterns/01_core_python_for_health_data.ipynb) | P4 | predict | `synthetic` |  | Processing an HL7-style event stream — count, filter, transform |
| 01.02 | [Pythonic Patterns & Refactoring](01_python_patterns/02_pythonic_patterns_refactoring.ipynb) | P4 | predict | `synthetic` |  | Refactor a 100-line audit script |
| 02.01 | [Arrays, Broadcasting & Vectorisation](02_numpy/01_arrays_broadcasting_vectorisation.ipynb) | P1 | predict | `imaging` |  | A lesion patch as an array — windowing, contrast, thresholding |
| 02.02 | [Linear Algebra, Random & einsum](02_numpy/02_linear_algebra_random_einsum.ipynb) | P4 | predict | `synthetic` |  | Bed-flow balance as Ax=b; Monte Carlo bed occupancy |
| 03.01 | [DataFrames & Core Operations](03_pandas/01_dataframes_core_operations.ipynb) | P2 | decide | `admissions` |  | An admissions extract with gaps and mixed types |
| 03.02 | [GroupBy, Merge & Reshape](03_pandas/02_groupby_merge_reshape.ipynb) | P4 | predict | `admissions` |  | Admissions by department × month; join to a staffing table |
| 04.01 | [Matplotlib, Seaborn & Plotly](04_visualisation/01_matplotlib_seaborn_plotly.ipynb) | P4 | predict | `vitals` |  | A week of vitals across a ward — which chart tells the story? |
| 05.01 | [Missing Values, Outliers & Coercion](05_data_wrangling/01_missing_values_outliers_coercion.ipynb) | P2 | decide | `admissions` |  | Deliberately messy admissions — MCAR/MAR/MNAR labs, impossible LOS, inconsistent dates |
| 06.01 | [SQL for Health Data](06_sql/01_sql_for_health_data.ipynb) | P4 | predict | `prescribing` |  | Patients–admissions–prescriptions in DuckDB |
| 07.01 | [Git Workflows for Analysis](07_git/01_git_workflows_for_analysis.ipynb) | P4 | predict | `synthetic` |  | Branching for model experiments; never committing PHI |
| 08.01 | [Reproducible Clinical Analysis](08_reproducibility/01_reproducible_clinical_analysis.ipynb) | P3 | explain | `trial` |  | A trial analysis that gives different p-values each run — then fixing it |
| 09.01 | [Testing, Modular Code & Packaging](09_software_engineering/01_testing_modular_code_packaging.ipynb) | P4 | predict | `synthetic` |  | A 500-line risk-score script → tested package |

## Priority bands

- **P1** Diagnostics — Does this person have the condition? How sure are we?
- **P2** Treatment — What should we do for this person, and what will happen if we do?
- **P3** Efficacy — Did the intervention work, for whom, and by how much?
- **P4** Health tech — Can the system run safely, at scale, in real time?
- **P5** Military thread — Does it hold under austerity, mass casualty and a hostile clock?

## Conventions

Every notebook carries three registers (🗣️ Plain · 💻 Developer · 🔬 Technical), a minimum visual count,
a *Failure Modes* section, a *Results / Findings / Implications / Considerations* block, and a *Clinical Reading*
section. `python scripts/validate.py 01_programming_data_foundations` checks all of it.
