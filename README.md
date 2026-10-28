# ml-algorithms-labs

A curriculum of machine-learning algorithms, each taught through a clinical problem. Thirty modules, 266 notebooks, three explanation registers in every notebook, visual-first, and gated by a validator rather than by opinion.

Built and maintained by Ross Taylor as a working health-data-science reference and a structured route through the field. Synthetic data throughout; nothing here is, or derives from, a real patient record.

## Premise

Most machine-learning curricula teach the algorithm and then attach a toy example. This one starts from the clinic. Each notebook poses one of five questions — does this patient have the condition; what should be done and what will follow; did the intervention work and for whom; can the system run safely at scale; does it hold under austerity and a hostile clock — and answers it with one method on data whose generating mechanism is known. Because the mechanism is known, every method can be checked against the truth rather than against a benchmark score.

The military-medicine thread is woven through the other modules rather than isolated: triage imbalance, casualty-evacuation reinforcement learning, offline note models, deployed monitoring, facility placement.

## How a notebook reads

Every concept is explained three ways, side by side, in the same cell block.

| Register | Written for | Sounds like |
|---|---|---|
| Plain | a nurse, a section commander, a manager | an analogy that works first time, with no undefined term |
| Developer | an engineer new to ML | pseudocode, the API, cost in time and memory |
| Technical | a postgraduate or a paper reader | notation, the objective, the assumptions, convergence |

The method is then built from scratch, run with the library implementation, and pushed until it fails. Experiments are pre-registered in the manifest. Each notebook closes with a structured block — results, findings, implications, considerations — and a clinical reading stating what a clinician would do differently and what they must not conclude.

Where a notebook recreates a known study it says so, as "in the spirit of", on synthetic data, with no claim to the paper's figures.

## Structure

| Area | Modules | Status |
|---|---|---|
| Foundations | 00 mathematics, 01 programming, 02 statistics, 03 data engineering | Tier 1 |
| Core supervised | 04 regression, 05 classification, 06 ensembles, 29 evaluation | Tier 1 |
| Unsupervised | 07 clustering, 08 dimensionality reduction, 09 association, 10 anomaly, 11 density, 12 text, 13 graphs, 14 semi-supervised | Tier 2–3 |
| Deep learning | 15 foundations, 16 CNNs, 17 sequences, 18 transformers, 19 generative, 20 GNNs | Tier 2–3 |
| Advanced | 21 reinforcement learning, 22 time series, 23 Bayesian, 24 graphical models, 25 meta-learning, 26 AutoML, 27 explainability, 28 specialised | Tier 2–3 |

The full table is in [INDEX.md](INDEX.md). Tier 1 is built first.

## Datasets

All synthetic, seeded, and generated from a known mechanism in `datasets/`.

| Dataset | Use | What it holds |
|---|---|---|
| `screening` | diagnostics | biomarker panel with disease status; two strong markers, three weak, one collinear pair |
| `admissions` | treatment, operations | acute admissions with length of stay, readmission and mortality; repeat patients; one column that leaks by design |
| `trial` | efficacy | two-arm RCT with heterogeneous effect, adherence and censoring; true effect known |
| `vitals` | monitoring | hourly observations with labelled deterioration onsets and injected sensor faults |
| `prescribing` | treatment | medication baskets with comorbidities and adverse-event flags |
| `cohort` | population health | five latent risk segments |
| `notes` | text | template-generated triage notes with urgency and disposition |
| `referrals` | networks | clinician and team referral graph with site communities |
| `imaging` | vision | small lesion patches with ground-truth masks |
| `evac` | military thread | casualty-evacuation grid with terrain, threat lanes and a clock |
| `areas` | spatial | small-area counts with spatial and unstructured risk; facility sites |

`datasets.baselines` provides rule-based clinician proxies so that "better than a clinician" has a number.

## The library

A curated collection of papers underpins the curriculum (`library/`). Each notebook's `study:` field names the paper whose central figure it reproduces; `refs:` populate the References cell; the critique papers — on p-values, significance, the two cultures, GNN evaluation, time-series baselines, hallucination — are the reviewer's named checks. `library/INDEX.md` lists the catalogue and the two planning documents record how it was folded in.

## Build process

The manifest `curriculum/curriculum.yaml` is the single source of truth. A script generates the tree and the stubs; a validator gates each notebook; a ledger records every attempt. There is no other process.

```
python scripts/scaffold.py                       # idempotent; stubs for anything missing
python scripts/next.py                           # next unbuilt notebook in build order
python scripts/validate.py <path>                # gates G1–G14; --execute runs the notebook
python scripts/ledger.py summary                 # LEDGER.md
python scripts/little_book.py                    # LITTLE_BOOK.md from everything built
```

Gates: title metadata, objectives, setup and seed, three registers, visual count, failure modes, the closing block, the clinical reading, connections, takeaways, no cross-notebook imports, clean execution, specific abstention, pre-registered experiments. An abstention — a stated reason why a figure or experiment cannot be done honestly on synthetic data — is accepted by the gate; padding is not.

With Claude Code, `/build-next` runs the loop end to end: a builder fills the next stub, the validator gates it, a reviewer with no sight of the build attacks it, the ledger records the outcome, and the notebook is committed. `HARNESS.md` describes the design and the reasoning behind it.

## Quick start

```bash
git clone https://github.com/RossTylr/ml-algorithms-labs.git
cd ml-algorithms-labs
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements/base.txt
pytest -q
python scripts/next.py
```

Tier 1 needs no further dependencies. Optional extras for later modules are listed in `requirements/`. Step-by-step instructions for the first session, including Claude Code in Cursor, are in [GETTING_STARTED.md](GETTING_STARTED.md).

## Layout

```
curriculum/curriculum.yaml   manifest
library/                     paper catalogue and planning documents
scripts/                     scaffold, validate, next, ledger, little_book, library
shared/                      plotting, evaluation, explanation, experiment, rl
datasets/                    generators, synthetic variants, clinician baselines
NN_module/MM_topic/KK.ipynb  notebooks
tests/                       generators, utilities, gates, harness
```

## Licence

MIT.
