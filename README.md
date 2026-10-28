# ML Mastery — Health Data Science Edition

> Every major machine-learning algorithm, taught through a clinical problem.
> 30 modules · 266 notebooks · three explanation registers · visual-first · machine-gated · paper-anchored.

## Why this repo exists

Most ML curricula teach the algorithm, then bolt on a toy example. This one starts from the clinic:
*does this patient have the condition? what should we do? did it work? can the system run safely?
does it hold up under a mass-casualty clock?* Each notebook answers one of those questions with one method,
on synthetic data whose generating mechanism is known — so you can check the algorithm against the truth.

## How a notebook reads

Every concept is explained three ways, side by side:

| Register | Audience | Sounds like |
|---|---|---|
| 🗣️ **Plain** | a nurse, a section commander, a manager | "Imagine a screening test for a disease one person in a hundred has…" |
| 💻 **Developer** | a software engineer new to ML | pseudocode, the API, what it costs in time and memory |
| 🔬 **Technical** | a masters student, a paper reader | notation, the objective, the assumptions, convergence |

Then the method is **built from scratch**, run with the library, **pushed until it breaks**, and the experiments
close with *Results → Findings → Implications → Considerations* and a **Clinical Reading**: what a clinician
would do differently, and what they must not conclude.

## Priority bands

| Band | Question |
|---|---|
| **P1 Diagnostics** | Does this person have the condition? How sure are we? |
| **P2 Treatment** | What should we do, and what will happen if we do? |
| **P3 Efficacy** | Did the intervention work, for whom, by how much? |
| **P4 Health tech** | Can the system run safely, at scale, in real time? |
| **P5 Military thread** | Does it hold under austerity, mass casualty and a hostile clock? |

P5 is woven through the other modules (triage imbalance, evacuation RL, offline note models, deployed
monitoring) rather than quarantined in its own module.

## The companion datasets

All synthetic, all seeded, all with a known mechanism. `datasets/__init__.py`.

| Dataset | Band | What it is |
|---|---|---|
| `screening` | P1 | biomarker panel + disease status; two strong markers, three weak, one collinear pair |
| `admissions` | P2 | acute admissions — LOS, readmission, mortality; repeat patients; a leaking column on purpose |
| `trial` | P3 | two-arm RCT with heterogeneous effect, adherence, censoring; true effect known |
| `vitals` | P4 | hourly HR/RR/SpO₂/SBP/temp; labelled deterioration onsets; injected sensor faults |
| `prescribing` | P2 | medication baskets with comorbidities; adverse-event flags on known risky pairs |
| `cohort` | P1 | population records with five latent risk segments |
| `notes` | P1 | template-generated triage notes with urgency and disposition |
| `referrals` | P4 | clinician/team referral network with site communities and specialty hubs |
| `imaging` | P1 | 16×16 lesion patches with ground-truth masks |
| `evac` | P5 | casualty evacuation grid — terrain, threat lanes, Role 1, Role 2, a clock |

Where a notebook recreates a known study it says so in the manifest (`study:`) — *in the spirit of*,
with synthetic data, never claiming the paper's numbers.

## Modules

See [INDEX.md](INDEX.md) for the full table. Tier 1 (build first): **00–06 and 29** — foundations, regression,
classification, ensembles, evaluation. Tier 2: clustering, dimensionality reduction, association rules,
anomaly detection, neural foundations, CNNs, time series. Tier 3: everything else.

## Quick start

```bash
git clone https://github.com/RossTylr/ml-algorithms-labs && cd ml-algorithms-labs
python -m venv .venv && source .venv/bin/activate
pip install -r requirements/base.txt          # Tier 1 needs nothing more
pytest -q                                     # generators and shared utilities
python scripts/scaffold.py                    # idempotent; creates any missing stubs
python scripts/validate.py --all --built-only # gate everything that has been built
```

## Building a notebook

The manifest is the plan; the validator is the review. There is no other process.

```bash
python scripts/scaffold.py                                    # stubs exist for every notebook
# fill 04_regression/01_simple_linear/01_ols_intuition_mathematics.ipynb
python scripts/validate.py 04_regression/01_simple_linear/01_ols_intuition_mathematics.ipynb
python scripts/validate.py <same> --execute                   # also runs it (G12)
git commit -am "nb(04.01.01): OLS intuition — PASS G1–G12"
```

Gates (from `curriculum/curriculum.yaml`): title metadata · objectives · setup/seed · three registers ·
visual count · failure modes · RFI block · clinical reading · connections · takeaways · no cross-notebook
imports · executes clean · **specific abstention** · **pre-registered experiments**. A warning (not a failure)
flags figure titles that describe rather than state a finding.

## The library

Ross's paper collection is catalogued in `library/` (140 curated of 292 files). Each notebook's `study:` names the
paper whose central figure it reproduces *in spirit*; `refs:` fill the References cell; the critique papers are the
skeptic's named checks. See `library/INDEX.md` and `HARNESS.md` §6b–6c for how the library shaped the loop.

## Layout

```
curriculum/curriculum.yaml   the manifest — modules, topics, notebooks, subjects, bands, gates
scripts/scaffold.py          manifest → directory tree, stubs, READMEs, INDEX.md
scripts/validate.py          the gate
shared/                      plotting · evaluation · explanation · experiment · rl
datasets/                    ten clinical generators + synthetic/
NN_module/MM_topic/KK_notebook.ipynb
tests/
```

## Licence

MIT. Synthetic data throughout; nothing here is or derives from real patient records.
