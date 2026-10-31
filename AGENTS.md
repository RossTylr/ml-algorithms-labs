# AGENTS.md — ml-algorithms-labs (Health Data Science edition)

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
Status follows the verdict: the builder leaves `status: "stub"`; the loop sets `"built"` on BUILT and `"blocked"` on BLOCKED; only a human `/skeptic` PASS after a hand edit sets `"accepted"`, which counts as built but is tallied apart in the ledger. Gates are G1–G14 plus HC-12 (G12 execute is optional, G13 abstention, G14 pre-registration, HC-12 exactly one `# CENTRAL`).

## Working on a notebook
1. **Orient.** Read the stub's title cell (band, goal) and its pre-registered experiments (section 6 headings, `metadata.ml_mastery.experiments`). State them in one line before anything else.
2. **Say what BUILT means here.** Before writing, state what BUILT means for this notebook: which gates bind (its `visuals_min`, its experiments in order, any `study:` figure) and what its `goal:` lets Findings and Clinical Reading claim.
3. **Build only this notebook.** One path. No other notebook, shared module or generator changes in the same piece of work.
4. **Never expand scope.** A figure or experiment you need that the manifest does not list is a `⛔ Abstention` or an `(exploratory)` heading — never a manifest edit.
5. **Report plainly.** Say in plain language what changed and what a reader can now do that they could not before; then the gate ledger verbatim.

## Hard constraints
- HC-1 Self-contained: no notebook imports from another notebook. Only `shared/` and `datasets/`.
- HC-2 `SEED = 42`; `set_style()` in the setup cell.
- HC-3 Three registers in every concept section: 🗣️ Plain · 💻 Developer · 🔬 Technical.
- HC-4 Minimum visuals per `curriculum.yaml` (`visuals:`, default 7). Colourblind-safe `PALETTE`.
- HC-5 Every notebook ends with Results/Findings/Implications/Considerations AND Clinical Reading.
- HC-6 Clinical Reading says what a clinician would do differently and what they must NOT conclude.
- HC-7 Synthetic data only. `study:` entries are "in the spirit of" — never claim to reproduce a paper's numbers. Every generator parameter is an assumption, listed in [datasets/ASSUMPTIONS.md](datasets/ASSUMPTIONS.md).
- HC-8 British English. Patients, not users. Sensitivity/specificity, not just precision/recall.
- HC-9 Pre-registration: the experiments are the manifest's `experiments:` list, in order. Extras are headed `(exploratory)`.
- HC-10 Abstention beats padding: `⛔ Abstention — <experiment> — <specific reason>` is a legal, gate-accepted answer.
- HC-11 Goal discipline: the title cell's `goal:` (predict / explain / decide) bounds every claim in Findings and Clinical Reading.
- HC-12 Figure titles state the finding, not the axes. Exactly one code cell is marked `# CENTRAL`.

## Registers — what each sounds like
- 🗣️ Plain: an analogy a nurse or a section commander follows first time. No undefined jargon.
- 💻 Developer: pseudocode, API, complexity, memory. A dev could implement from it.
- 🔬 Technical: notation, objective, assumptions, convergence. Citeable.

## Manifest fields on every notebook
`band` P1–P5 · `goal` predict|explain|decide · `gds` 1–6 (Donoho) · `dataset` · `study` (library key: reproduce that paper's central figure, in spirit) · `refs` (library keys → References cell) · `visuals` · `experiments` (pre-registered) · `build: last` (29.meta only).
The library is `library/curated.yaml`; the builder reads a PDF only when `study:` names it, and only once: on first contact it writes `library/briefs/<key>.md`, which every later notebook citing that key reads instead.

## Priority bands (clinical framing, from the manifest)
P1 Diagnostics · P2 Treatment · P3 Efficacy · P4 Health tech / operations · P5 Military-medicine thread.
The band is on the title cell. The Clinical Reading answers the band's question.

## Datasets (all synthetic, `datasets/__init__.py`)
screening · admissions · trial · vitals · prescribing · cohort · notes · referrals · imaging · evac · areas · synthetic.*
Each has a known generating mechanism. Use `return_truth=True` where offered to check the method against truth.
`datasets.baselines.clinician_baseline(name, df)` gives the rule-based human yardstick for the error-analysis experiment.

## Layout
```
curriculum/curriculum.yaml   manifest
scripts/scaffold.py          manifest → tree + stubs + READMEs + INDEX.md
scripts/validate.py          gates G1–G14, HC-12 (+W1 warning)
scripts/next.py              next stub in build order; teach-back on the jagged edge
scripts/ledger.py            ledger.jsonl → LEDGER.md
scripts/little_book.py       built 🗣️ paragraphs + # CENTRAL figures → LITTLE_BOOK.md
scripts/library.py           library/curated.yaml + listing.txt → INDEX.md; checks manifest keys
scripts/enrich_manifest.py   one-off, idempotent: goal/gds/study/refs/error-analysis
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
