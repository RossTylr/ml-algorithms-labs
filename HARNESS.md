# HARNESS.md — Building ml-algorithms-labs with agents, loops and minimal prompts

> Ideation + the executable minimum. Decisions are recorded inline (D-n) with reasoning.
> Companion to CLAUDE.md. CLAUDE.md governs *what a notebook is*; this governs *how the loop runs*.

---

## 0. What the quant-desk pattern actually contains

The "AI quant research team" setup has five agents and a terminal. Strip the product and four mechanisms remain:

| Mechanism | In the desk | Worth stealing? | Our analogue |
|---|---|---|---|
| **Fixed verdict contract** | DATA VALIDATED / TRADE-OFF / NO EDGE, computed by the server, never by the agent | **Yes** | `scripts/validate.py` → BUILT / REVISE / BLOCKED. Nobody argues with it. |
| **Role separation** | the agent that had the idea never grades it; the skeptic runs on the strongest model | **Yes** | a **skeptic** subagent in a fresh context that never saw the build — the "held-out window" for prose |
| **Ledger memory** | `research.md`: every test logged with verdict before any summary; NO EDGE is a result, never retest without a new reason | **Yes** | `ledger.jsonl` + `LEDGER.md`: every attempt, every gate, every skeptic finding; 3 fails → BLOCKED, don't retry without a manifest change |
| **Sweep, never guess** | twenty configurations from one prompt; a real edge is a plateau | **Yes, already in** | `experiments:` in the manifest demand parameter sweeps and failure modes per notebook |
| Lead that plans | Opus turns a question into a plan, decides what runs next | **No** | the manifest is the plan; `scripts/next.py` is deterministic. A planning agent is RULE 1 drift. |
| Librarian | searches a strategy library | **No** | `study:` is pre-selected per notebook; references are the builder's job inside the notebook |
| Scout checks data first | confirm the universe before testing | **Partly** | `tests/` already proves every generator. A per-notebook scout is ceremony. |

**D-1** Two agents, not five: **builder** and **skeptic**. Everything else is a script or the manifest.
*Reason*: each additional seat is a place for process to start generating work. Two is the minimum that gives role separation.

**D-2** The skeptic may only ever output `PASS` or `REVISE + ≤3 findings`, scoped to the notebook in hand.
*Reason*: a skeptic that can say "you should also add a notebook on X" is a planner wearing a hat.

---

## 1. The loop

```
                ┌──────────────────────────────────────────────────────────────┐
                │  scripts/next.py  → path of next unbuilt stub (build order)  │
                └──────────────┬───────────────────────────────────────────────┘
                               ▼
   ┌───────────┐   fill   ┌─────────┐  G1–G12  ┌──────────┐  fresh ctx  ┌─────────┐
   │ stub      │ ───────▶ │ builder │ ───────▶ │ validate │ ──────────▶ │ skeptic │
   └───────────┘          └─────────┘          └──────────┘             └─────────┘
                               ▲                    │ FAIL                   │ REVISE (≤3)
                               └────────────────────┴────────────────────────┘
                                          max 2 revision cycles, then BLOCKED
                               │ PASS + PASS
                               ▼
                   ┌────────────────────────────┐
                   │ ledger.jsonl ← append       │
                   │ git commit  "nb(NN.MM.KK)"  │
                   │ learn/queue ← quiz + digest │
                   └────────────────────────────┘
```

Verdicts (the contract):

| Verdict | Meaning | Who decides |
|---|---|---|
| **BUILT** | all gates pass; skeptic found nothing it could substantiate | `validate.py` AND skeptic |
| **REVISE** | a gate failed, or skeptic has ≤3 substantiated findings | either |
| **BLOCKED** | 3 attempts failed, or a dependency cannot be installed | `loop.sh` |

**D-3** `validate.py` runs *before* the skeptic. *Reason*: don't spend the expensive model on a notebook with no figures.

**D-4** Revision goes back to the **same builder context** (via `SendMessage`/resume), not a new one. *Reason*: it has the notebook loaded; a fresh builder would re-read 200 cells.

---

## 2. Three harness tiers — demo in this order

### T0 — bash + headless Claude (demo tonight)
```bash
scripts/loop.sh 3          # build the next 3 notebooks, sequentially
```
One `claude -p` call per notebook. No subagents, no skeptic. Measures the floor: can one prompt + CLAUDE.md + the stub produce a gate-passing notebook? Record tokens, wall time, first-attempt gate pass rate.

### T1 — Claude Code subagents + skill (the working configuration)
```
.claude/agents/builder.md     model: sonnet   tools: Read Write Edit Bash NotebookEdit
.claude/agents/skeptic.md     model: opus     tools: Read Bash(validate only)
.claude/skills/build-next/    /build-next → next.py → builder → validate → skeptic → ledger → commit
```
Prompt from you: `/build-next` (or `/build-next 5`). That is the whole interface.

### T2 — parallel seats by module (only if T1 pass rate > 80%)
Notebooks are independent by construction (HC-1), so N builders can run in N git worktrees on N modules with **no coordinator** — `next.py --module 04` gives each seat its own queue. A merge is a merge of disjoint files.
**D-5** Parallelism is allowed; a coordinator is not. If two seats ever need to talk, the design is wrong.

### Unattended — scheduled task
A nightly Claude Code scheduled task runs `/build-next 4` at 02:00. Morning: ledger shows 4 lines, `learn/queue` shows 4 items. That is the "let it run" mode. Daily cap is the token budget, not a count.

---

## 3. Concurrent learning — the thing the quant desk doesn't have

You are not a hedge fund outsourcing research. You are learning the material while the machine writes it. Three mechanisms, all byproducts of the loop, none requiring extra prompts:

**L1 — Quiz per notebook.** The builder's last act is to write `learn/queue/NN.MM.KK.quiz.md`: five questions derived from the notebook's own Learning Objectives, answers at the bottom. You answer before you read the notebook. Score goes in the ledger (`understood: 0–5`).

**L2 — Skeptic digest.** The skeptic's substantiated findings are the best teaching material in the repo: *here is where a strong model got the 🔬 register subtly wrong, or let the Clinical Reading overclaim*. `learn/digest.md` accumulates them, newest first, tagged by module. Reading the digest is reading a syllabus of real pitfalls.

**L3 — Teach-back on a sample.** For one notebook in five (`next.py` marks it `teachback: true`), the builder leaves the 🗣️ Plain register of section 2 as a placeholder. You write it. Then `/skeptic` grades *your* paragraph against the 💻 and 🔬 registers. The diff is the lesson.

**D-6** Learning artefacts are written by the builder in the same run, not by a third agent. *Reason*: RULE 1 again — a "tutor" agent would start proposing curricula.

Morning cadence (15 min): read ledger → take 4 quizzes → read digest → mark `understood` → done. The build continues regardless of whether you do this; the learning compounds if you do.

---

## 4. Minimal prompt set

| Prompt | What happens |
|---|---|
| `/build-next` | build one notebook through the full loop |
| `/build-next 5` | five, sequentially, stop on BLOCKED |
| `/skeptic <path>` | run the skeptic alone on any notebook (including one you edited) |
| `/learn` | print today's queue and digest |

Nothing else. If you find yourself writing a fourth kind of prompt, it belongs in the manifest or CLAUDE.md.

---

## 5. Demo / test plan — numbered, machine-checkable

| # | Test | Pass condition | Tier |
|---|---|---|---|
| H1 | `scripts/next.py` returns `00_mathematical_foundations/01_linear_algebra/01_vectors_matrices_operations.ipynb` on a fresh scaffold | exact path | T0 |
| H2 | `scripts/loop.sh 1` produces a notebook that passes G1–G11 on first attempt | `validate.py` exit 0 | T0 |
| H3 | Same notebook passes G12 (`--execute`) | exit 0 | T0 |
| H4 | Ledger has exactly one line with `attempt: 1` and token/time fields populated | `jq` check | T0 |
| H5 | `/build-next` runs builder → validate → skeptic → commit with no human input | one commit `nb(00.01.01)` | T1 |
| H6 | Skeptic on a deliberately broken notebook (wrong 🔬 claim planted) returns REVISE with the planted error in its ≤3 findings | finding text matches | T1 |
| H7 | `/build-next 5` over Module 00: ≥ 4/5 BUILT, 0 BLOCKED | ledger count | T1 |
| H8 | Cost: median tokens per BUILT notebook < 150k; median wall time < 12 min | ledger stats | T1 |
| H9 | Two worktree seats on modules 04 and 05 complete 3 each with a clean merge | `git merge` no conflicts | T2 |
| H10 | Nightly scheduled task produces ≥ 3 BUILT lines in the ledger by 07:00 | ledger timestamps | sched |

H1–H4 tonight. H5–H8 this week. H9–H10 only if H7 holds.

---

## 6. What's in the box now

```
scripts/next.py              deterministic "next stub in build order"; --module; --teachback flag every 5th
scripts/loop.sh              T0: N × (claude -p → validate → ledger → commit)
scripts/ledger.py            append / summarise ledger.jsonl → LEDGER.md
.claude/agents/builder.md    the builder subagent
.claude/agents/skeptic.md    the skeptic subagent (opus, fresh context, PASS | REVISE ≤3)
.claude/skills/build-next/   /build-next skill wiring the loop
.claude/skills/skeptic/      /skeptic
learn/                       queue/ and digest.md
```

---

## 7. Risks recorded

- **R1 Skeptic drift.** The skeptic will try to be helpful and suggest additions. The agent file forbids it and the skill truncates output to three findings. Watch the digest for "you could also…" phrasing — that is the leak.
- **R2 Gate gaming.** A builder can satisfy G5 with seven trivial plots. Mitigation: the skeptic's brief includes "do the figures carry the argument, or pad it?"
- **R3 Register collapse.** 🗣️ Plain drifting into 💻 Developer with analogies bolted on. The skeptic checks the Plain paragraph against the "nurse or section commander, first time" test.
- **R4 Clinical overclaim.** The most dangerous failure in this repo: a Clinical Reading that implies a synthetic result transfers to practice. The skeptic checks every Clinical Reading contains a "must not conclude" clause (G8 only checks presence).
- **R5 Cost runaway unattended.** `loop.sh` and the scheduled task take a count, and the ledger tracks tokens. Set a daily token ceiling in the scheduled task prompt.
