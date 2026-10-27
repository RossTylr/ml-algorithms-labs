# CLAUDE.md — ml-algorithms-labs (Health Data Science edition)

## What this repo is
A 30-module, ~330-notebook curriculum teaching every major ML algorithm through clinical problems.
Every notebook: one method, one clinical question, three explanation registers, visual-first, gated.

## The one rule
**One seat builds one notebook at a time. Everything else is silent.**
`scripts/validate.py` BOUNDS what may be claimed as built. It never generates tasks. Do not add
coordinators, readouts, trackers or plans — the manifest is the plan, the gate is the review.

## Source of truth
`curriculum/curriculum.yaml`. Modules, topics, notebooks, subjects, datasets, priority bands, gates.
Change the manifest, re-run `scripts/scaffold.py`; never hand-edit a README or INDEX.md.

## Build loop (the whole process)
```
1. python scripts/scaffold.py                 # idempotent; stubs for anything missing
2. open the next stub in build order           # see INDEX.md; Tier 1 first (00–06, 29)
3. fill it — follow the stub's sections exactly
4. python scripts/validate.py <path>           # G1–G11; add --execute for G12
5. commit when PASS                             # message: "nb(04.01.01): OLS intuition — PASS G1–G12"
```
A notebook with `metadata.ml_mastery.status == "stub"` and `_objective_` still in it is unbuilt.
When built, set `status: "built"` in the notebook metadata.

## Hard constraints
- HC-1 Self-contained: no notebook imports from another notebook. Only `shared/` and `datasets/`.
- HC-2 `SEED = 42`; `set_style()` in the setup cell.
- HC-3 Three registers in every concept section: 🗣️ Plain · 💻 Developer · 🔬 Technical.
- HC-4 Minimum visuals per `curriculum.yaml` (`visuals:`, default 7). Colourblind-safe `PALETTE`.
- HC-5 Every notebook ends with Results/Findings/Implications/Considerations AND Clinical Reading.
- HC-6 Clinical Reading says what a clinician would do differently and what they must NOT conclude.
- HC-7 Synthetic data only. `study:` entries are "in the spirit of" — never claim to reproduce a paper's numbers.
- HC-8 British English. Patients, not users. Sensitivity/specificity, not just precision/recall.

## Registers — what each sounds like
- 🗣️ Plain: an analogy a nurse or a section commander follows first time. No undefined jargon.
- 💻 Developer: pseudocode, API, complexity, memory. A dev could implement from it.
- 🔬 Technical: notation, objective, assumptions, convergence. Citeable.

## Priority bands (clinical framing, from the manifest)
P1 Diagnostics · P2 Treatment · P3 Efficacy · P4 Health tech / operations · P5 Military-medicine thread.
The band is on the title cell. The Clinical Reading answers the band's question.

## Datasets (all synthetic, `datasets/__init__.py`)
screening · admissions · trial · vitals · prescribing · cohort · notes · referrals · imaging · evac · synthetic.*
Each has a known generating mechanism. Use `return_truth=True` where offered to check the method against truth.

## Layout
```
curriculum/curriculum.yaml   manifest
scripts/scaffold.py          manifest → tree + stubs + READMEs + INDEX.md
scripts/validate.py          gates G1–G12
shared/                      plotting · evaluation · explanation · experiment · rl
datasets/                    ten clinical generators + synthetic/
NN_module/MM_topic/KK_notebook.ipynb
tests/                       generators + shared smoke tests
```

## Conventions
- Paths `NN_module/MM_topic/KK_slug.ipynb`; ids `NN.MM.KK` in notebook metadata.
- Figures: `figsize=(12,6)` single, `shared.plotting.grid(n)` for panels. Title, labels, legend always.
- Code cells ≤ 30 lines without an explaining markdown cell.
- Commit per notebook. No batch commits of unvalidated work.
