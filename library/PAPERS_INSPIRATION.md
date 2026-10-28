# Wider inspiration from the library — what changes the repo, not just a notebook

> Companion to PAPERS_PLAN.md (which maps papers → notebooks). This one asks what the library says about the
> *design* of ml-algorithms-labs: its spine, its gates, its harness, its learning loop. Plan only; nothing applied.
> Each idea: source → the idea → what it would change → cost. Ideas marked *validates* the current design and change nothing.

---

## A. The spine — what organises 263 notebooks

### A1. A second axis: Donoho's six divisions of Greater Data Science
*50 Years of Data Science (2017), §8.*
Donoho splits the field into: (1) gathering/preparation/exploration, (2) representation/transformation, (3) computing with data, (4) modelling, (5) visualisation/presentation, (6) **science about data science**.
Our manifest has one axis (clinical band P1–P5). Tagging each notebook with a GDS division exposes a fact: ~75% of the repo is GDS4 modelling; GDS6 is almost empty.
**Change**: add `gds:` to each notebook (cheap, mechanical). Then see A5.
**Cost**: one manifest pass.

### A2. Declare the culture: predict or explain
*Breiman, Statistical Modeling: The Two Cultures.* Also Hardt & Recht's "prediction and action".
Every notebook serves one of two goals — predict (algorithmic culture) or understand the mechanism (data-modelling culture) — and the clinical bands already imply it: P1/P4 predict, P3 explains, P2 is where the two collide (treatment = prediction *plus* a causal claim). The manifest never says which. A notebook that doesn't declare its culture will overclaim in the Clinical Reading — a predictive model read as a mechanism.
**Change**: `goal: predict | explain | decide` on each notebook; the Clinical Reading must open by naming it. Skeptic checks the claim matches the goal.
**Cost**: manifest pass + one skeptic check.

### A3. Predict → decide → act as the P2 ordering
*Hardt & Recht, Patterns, Predictions, and Actions* — supervised learning, then causality, then sequential decisions, all as "the power of prediction" plus feedback control. *Kochenderfer, Algorithms for Decision Making* — probabilistic reasoning → simple decisions → sequential → uncertainty → multi-agent.
Both books order the material more cleanly than my modules 21/23/24 do (I have RL before Bayes before PGMs; they have Bayes → PGM → decisions → RL). Tier 3 can be re-ordered without touching any notebook — order lives in the manifest only.
**Change**: swap tier-3 build order to 23 → 24 → 21. Note it in INDEX.md.
**Cost**: three lines.

### A4. Geometric deep learning as the map for modules 16–20
*Bronstein et al., Geometric Deep Learning (2021)* — grids, groups, graphs, geodesics, gauges; every architecture is a symmetry choice.
Not a notebook. A one-page `16_cnns/../DEEP_LEARNING_MAP.md` saying: CNN = translation symmetry on a grid; GNN = permutation symmetry on a graph; transformer = permutation on a set with position injected; SSM = time-shift. Readers then see modules 16–20 as one idea, not five.
**Change**: one generated page; `symmetry:` tag on those ~45 notebooks.
**Cost**: an afternoon, once.

### A5. The last notebook is about the repo — science about data science
*Donoho GDS6; Dell'Acqua et al., "Jagged Frontier" (2023).*
After 263 builds the ledger and skeptic digest are a dataset: which methods did the builder get wrong first time, which registers slipped, which Clinical Readings overclaimed, where did the skeptic fire most. Dell'Acqua showed AI capability has a jagged edge — tasks that look equally hard are not. The digest is a map of that edge across ML.
**Change**: add `29.07.01 Science About This Repo` — P4, dataset = `ledger.jsonl` + `learn/digest.md`, built **last**. It is real analysis (physics), not a readout.
**Cost**: one manifest line now; one notebook at the end.

---

## B. The gates and the skeptic — epistemics

### B1. Pre-registration: the `experiments:` field is a protocol
*Box, Science and Statistics (1976); AlphaCodium "flow engineering" (2024); the ASA statement.*
Box's loop is theory → confront with data → revise. AlphaCodium's trick is to generate the *tests* before the code. The clinical version is pre-registration. The manifest already lists each notebook's experiments by name — that **is** a pre-registered protocol. Make it binding: the builder may run exactly those experiments; any extra is logged as *exploratory* in the ledger and the skeptic treats exploratory findings as hypothesis-generating only.
**Change**: builder.md gains one rule; ledger gains `exploratory: [...]`.
**Cost**: trivial. Prevents the builder from fishing for a pretty figure.

### B2. Reward abstention — the Kalai principle applied to our own gates
*Kalai et al., Why Language Models Hallucinate (2025):* evaluation that penalises "I don't know" produces confident guessing.
Our gates do this too. G5 counts figures; a builder under pressure pads. G7 demands findings; a builder with nothing to find invents. The fix is a legal abstention: a notebook may declare `CANNOT-REPRODUCE: <reason>` for a `study:` figure, or `NULL-RESULT` for an experiment, and the gate accepts it when the reason is specific.
**Change**: `validate.py` accepts a ` Abstention` block in place of a figure/finding if it cites the experiment id and a reason; ledger records it; skeptic checks the reason is real.
**Cost**: ~30 lines. Changes the incentive for every notebook.

### B3. The critique papers as named skeptic checks — expanded list
Already in PAPERS_PLAN §3. Two additions from the deeper read:
- **Rajpurkar et al. 2022**: the bar for medical AI is *prospective*; nearly everything is retrospective. Every Clinical Reading's "must not conclude" clause must say the result is retrospective and synthetic.
- **Dell'Acqua "jagged frontier"**: the skeptic flags where the notebook's difficulty *for the builder* (attempts, revisions) diverges from the method's difficulty *for a reader* — that mismatch is itself a finding for the digest.

### B4. Figure titles are findings, not descriptions
*Knaflic, Storytelling with Data; DataCamp 8 rules.* One message per chart; the title is the takeaway.
"Readmission risk doubles above severity 7" not "Readmission vs severity". This is checkable: a title that contains "vs" / "by" / "over" and no verb is descriptive.
**Change**: convention in CLAUDE.md; a *soft* check in `validate.py` (warn, not fail — RULE 1).
**Cost**: trivial; large effect on how the notebooks read.

### B5. Error analysis as a standing experiment
*Ng, Machine Learning Yearning, ch. 14–19:* look at the worst dev-set cases by hand; the eyeball set.
No notebook in the manifest does this, and it is the most clinical thing a data scientist does — the 20 patients the model got most wrong, categorised. For P1 notebooks it is also where the "human-level performance" yardstick lives: Ng's whole method is to compare with human error.
**Change**: every P1/P2 classification notebook gets a fixed final experiment `"error analysis: 20 worst cases, categorised"`, and a `clinician_baseline` — a simple rule-based proxy in `datasets/` (e.g. a NEWS2-like score on `vitals`, a two-biomarker threshold on `screening`) so "beats a clinician?" has a number.
**Cost**: manifest pass on ~40 notebooks + one small function per dataset.

---

## C. The harness

### C1. It is stigmergic — say so, and keep it so
*Heylighen, Stigmergy as a universal coordination mechanism (2016):* coordination through traces left in a shared medium, not through messages between agents.
That is exactly the design: builder and skeptic never talk; they read and write the repo (stub → notebook → ledger → digest). The paper gives the theoretical reason RULE 1 works: a coordinator is a second medium competing with the first.
**Change**: one paragraph in HARNESS.md; a test — H11: no agent file may reference another agent by name.
**Cost**: none. validates.

### C2. Evaluator–optimiser, routing, and nothing else
*Anthropic, Building effective agents (2024):* simple composable patterns beat frameworks; the evaluator–optimiser loop; routing by task type.
Builder/skeptic **is** evaluator–optimiser. . The one pattern worth adding is routing: tier-3 notebooks (RL, diffusion, SSMs) are harder; route them to an opus builder, tier-1 to sonnet. `next.py` already emits the tier.
**Change**: `/build-next` picks the builder model by tier.
**Cost**: three lines in the skill.

### C3. The gatekeeper as a harness and a learning pattern
*Nori et al., Sequential Diagnosis (2025):* a gatekeeper reveals findings only when asked; performance is accuracy **and** cost of information requested.
Two uses. (i) For the skeptic: give it the notebook *without* the Results section and ask what it predicts the findings will be, then reveal — a skeptic that predicted the result adds nothing; one that is surprised has found the interesting notebook. (ii) For Ross: a *gatekeeper quiz* mode — answer with hints purchased at a cost, score = accuracy minus hints. This is the Sequential Diagnosis benchmark applied to learning.
**Change**: (i) optional skeptic mode; (ii) `learn/queue` quiz format gains a hints ladder.
**Cost**: (i) a prompt variant; (ii) a quiz template change.

### C4. The Bitter Lesson applied to the builder prompt
*Sutton (2019):* general methods + compute beat hand-crafted knowledge.
Risk: the temptation to keep enriching builder.md with clinical lore until the prompt is the product. Sutton says keep the prompt general, put the specifics in the manifest row, and let the gate + skeptic do the correcting.
**Change**: a cap — builder.md stays under 40 lines; everything else is manifest data. validates current size.

---

## D. The learning loop

### D1. The Little Book — a free derived artefact
*Fleuret, The Little Book of Deep Learning (2024):* 160 phone-sized pages, one idea and one figure per page.
Every notebook has a plain Plain paragraph for section 2 and one "central" figure. A script concatenates them in manifest order → `LITTLE_BOOK.md` (and a PDF). It costs nothing, it is regenerated on every build, and it is the thing you can read on the train. By module 06 it is a readable pamphlet; by 29 it is a book.
**Change**: `scripts/little_book.py`; the builder marks one figure `# CENTRAL` per notebook.
**Cost**: an hour, once.

### D2. The quiz gets a sixth question and a cost
From PAPERS_PLAN §6 (what could the reproduction not test?) plus C3(ii) hints-at-a-cost.

### D3. Teach-back on the jagged edge, not every fifth
*Dell'Acqua.* Currently teach-back is every 5th notebook. Better: teach-back where the **skeptic fired** — those are the notebooks where the model's frontier is jagged, so they are where a human explanation is worth most. `next.py` can read the ledger.
**Change**: `teachback = (last skeptic verdict on this topic was REVISE) or every 5th`.
**Cost**: five lines.

### D4. One dataset, many methods — the Mehta precedent
*Mehta et al., A high-bias, low-variance introduction to ML for physicists (2019):* a 124-page review built on Jupyter notebooks, one physics dataset (Ising) carried across every method, a "physics intuition" register throughout.
This is the closest existing thing to our design and it works. validates companion datasets and the clinical register. One thing they do that we don't: a **closing section per method on "what the physics tells you the method is doing"** — ours should be "what the clinic tells you the method is doing", which is what the Clinical Reading is for. .

### D5. Sidey-Gibbons as the first capstone
*Sidey-Gibbons & Sidey-Gibbons, ML in medicine: a practical introduction (2019):* GLM, SVM, single-layer ANN on Wisconsin breast cancer, N=683, with the full evaluation.
That is three of our notebooks (05.01, 05.05, 15.01) on `screening`. A capstone that re-runs the paper's comparison table end-to-end on synthetic data, then asks the sixth quiz question, is the right first project.
**Change**: `projects/01_sidey_gibbons_replication/` — the first project, built after module 05.

---

## E. Things in the library that should *not* change the repo

- **Textbooks** (Murphy ×2, Prince, Mohri, Shalev-Shwartz, Bishop, ESL, Goodfellow, Géron ×2, Chollet, Huyen, Reddi, Reliable ML, Design Patterns): references only. The *ML Design Patterns* vocabulary (Reframing, Cascade, Neutral Class, Rebalancing, Useful Overfitting) is worth a `patterns:` cross-ref tag, nothing more.
- **Futures/essays** (Situational Awareness, AI 2027, Gradual Disempowerment, Amodei, Agent Economy, Stratechery, Useful Fictions): none belong in a methods curriculum. Catalogue and leave.
- **Course decks and videos** (Google ML course, DeepMind talks, 3Blue1Brown clips): the Google PMLE guide is a useful *coverage checklist* against modules 03 and 29; everything else is reference.
- **Duplicates and dead files**: nine duplicate pairs, five empty Medium captures, the wrong Nature page. Flag in `library/INDEX.md`; do not delete anything in the folder.

---

## F. If only five things get done

1. **B2 abstention** — changes the incentive on every notebook; cheapest honesty gain available.
2. **A2 goal: predict/explain/decide** — stops the single most likely clinical overclaim.
3. **B5 error analysis + clinician baseline** — the most clinical experiment in the repo, currently absent.
4. **D1 Little Book** — the derived artefact that makes the build visible as learning.
5. **A5 the last notebook** — makes the ledger and digest into physics.

Everything else is either validation () or a tag.
