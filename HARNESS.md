# Harness

How the notebooks get built: the loop, the agents, the gates, and the learning cadence that runs alongside. Companion to `CLAUDE.md`, which governs what a notebook is; this document governs how the loop runs. Design decisions are recorded inline as D-1 to D-6 with their reasoning.

## 1. Origin and what was kept

The design borrows from the "AI research desk" pattern — a lead that plans, agents that run tests, a sceptic that tries to break every result, a ledger that remembers what failed. Stripped of its product, four mechanisms survive scrutiny and three do not.

| Mechanism | Kept | Form here |
|---|---|---|
| Fixed verdict contract — the verdict is computed, never argued | Yes | `scripts/validate.py` returns BUILT, REVISE or BLOCKED |
| Role separation — the agent that built the work never grades it | Yes | a reviewer in a fresh context that has not seen the build |
| Ledger memory — every attempt logged with its verdict; a failure is a result, not retried without a new reason | Yes | `ledger.jsonl` and `LEDGER.md`; three failures block the notebook until the manifest changes |
| Sweep, never guess — one configuration proves nothing | Already present | the manifest's pre-registered experiments require sweeps and failure modes |
| A lead that plans | No | the manifest is the plan and `scripts/next.py` is deterministic; a planning agent generates work, which is the drift the harness exists to prevent |
| A librarian | No | each notebook's `study:` and `refs:` are set in advance |
| A scout that checks data first | No | the generators are proven once, in `tests/` |

**D-1.** Two agents — a builder and a reviewer — and nothing else. Each additional seat is a place for process to begin producing tasks. Two is the minimum that gives role separation.

**D-2.** The reviewer may output only PASS, or REVISE with at most three substantiated findings, scoped to the notebook in hand. A reviewer that can say "a notebook on X is also needed" is a planner by another name.

## 2. The loop

```
next.py ──> stub ──> builder ──> validate.py ──> reviewer ──> ledger ──> commit
                        ^            |  FAIL         |  REVISE
                        └────────────┴───────────────┘
                              at most two revision cycles, then BLOCKED
```

| Verdict | Meaning | Decided by |
|---|---|---|
| BUILT | every gate passes and the reviewer found nothing it could substantiate | validator and reviewer |
| REVISE | a gate failed, or the reviewer has one to three substantiated findings | either |
| BLOCKED | three attempts failed, or a dependency cannot be installed | the loop |

**D-3.** The validator runs before the reviewer, so the expensive model is not spent on a notebook with no figures.

**D-4.** Revisions return to the same builder context rather than a fresh one; the notebook is already loaded.

## 3. Three configurations, tried in order

**T0 — headless.** `scripts/loop.sh N` makes one `claude -p` call per notebook, gates it, records it, commits it. No agents, no reviewer. This measures the floor: whether one prompt plus `CLAUDE.md` plus the stub produces a gate-passing notebook, and at what cost in tokens and time.

**T1 — agents.** `/build-next` in Claude Code runs the full loop: `.claude/agents/builder.md` fills the stub, the validator gates it, `.claude/agents/skeptic.md` reviews it in a fresh context, the ledger records the outcome, the notebook is committed. Tier-3 notebooks are routed to the stronger model. This is the working configuration and the whole interface is one command.

**T2 — parallel seats.** Notebooks are independent by construction, so several builders can run in separate git worktrees on separate modules with `next.py --module NN` giving each its own queue. A merge is a merge of disjoint files.

**D-5.** Parallelism is permitted; a coordinator is not. If two seats ever need to talk, the design is wrong.

**Unattended.** A nightly scheduled task runs `/build-next 4` with a token ceiling stated in the prompt. The ledger and the learning queue are what a returning reader sees in the morning.

### Why no coordinator works

Heylighen (2016; `library:heylighen2016`) defines stigmergy as coordination through traces left in a shared medium rather than messages between agents. That is this harness exactly: builder and reviewer never address each other; they read and write the repository — stub, notebook, ledger, digest, next stub. A coordinator would be a second medium competing with the first. Test H11 enforces it: no agent file may name another agent.

Anthropic's *Building effective agents* (`library:anthropic2024`) describes the builder–reviewer pair as an evaluator–optimiser loop and recommends one further pattern, routing by task type, which `/build-next` does by tier.

## 4. Learning alongside the build

The author is learning the material while the machine writes it. Three mechanisms fall out of the loop without extra prompts.

**Quiz per notebook.** The builder's last act is `learn/queue/NN.MM.KK.quiz.md`: five questions derived from the notebook's own objectives, a sixth where a paper is being reproduced — *what did the paper claim that this synthetic reproduction could not test?* — each with a two-step hints ladder. Score is correct answers less half a point per hint, recorded in the ledger (Nori et al. 2025, *Sequential Diagnosis*: accuracy and the cost of information requested).

**Reviewer digest.** The reviewer's substantiated findings accumulate in `learn/digest.md`, newest first. Each is a place a strong model got the technical register subtly wrong or let a clinical reading overclaim. Read in sequence they form a syllabus of real pitfalls.

**Teach-back on the jagged edge.** Where the reviewer last returned REVISE on a topic — and otherwise every fifth notebook — the builder leaves the plain-language paragraph of section 2 blank. The author writes it; `/skeptic` grades it against the developer and technical registers. Dell'Acqua et al. (2023) showed that model capability has a jagged edge across tasks that look equally hard; those edges are where a human explanation is worth most.

**The Little Book.** `scripts/little_book.py` stitches every built notebook's plain paragraph and its one central figure into `LITTLE_BOOK.md`, in build order, after Fleuret (2024). It is regenerated on every build and is the thing to read away from a screen.

**The closing notebook.** `29.meta.1` is built last, from the ledger and digest, as data: which methods the builder got wrong first time, which registers slipped, where clinical readings overclaimed. Donoho's sixth division — science about data science — applied to the repository itself.

**D-6.** Learning artefacts are written by the builder in the same run, not by a third agent. A tutor agent would begin proposing curricula.

Morning cadence, fifteen minutes: read the ledger, take the quizzes, read the digest, record the scores. The build continues whether or not this happens; the learning compounds if it does.

## 5. The prompt set

| Prompt | Effect |
|---|---|
| `/build-next` | one notebook through the full loop |
| `/build-next N` | N notebooks, sequentially, stopping on BLOCKED |
| `/skeptic <path>` | the reviewer alone, on any notebook including one edited by hand |
| `claude -p "Read CLAUDE.md. Build <path> in place; then run python scripts/validate.py <path> and fix failures."` | the headless floor, no agents |

If a fifth kind of prompt becomes necessary, the need belongs in the manifest or `CLAUDE.md`, not in a prompt.

## 6. Tests

| Test | Condition | Configuration |
|---|---|---|
| H1 | `next.py` returns `00.01.01` on a fresh scaffold | T0 |
| H2 | `loop.sh 1` produces a notebook passing G1–G11 and G13–G14 at first attempt | T0 |
| H3 | the same notebook passes G12 (`--execute`) | T0 |
| H4 | the ledger holds one line with attempt 1 and token and time fields populated | T0 |
| H5 | `/build-next` runs builder, validator, reviewer and commit with no human input | T1 |
| H6 | the reviewer, given a notebook with a planted false technical claim, returns REVISE naming it | T1 |
| H7 | `/build-next 5` over module 00 yields at least four BUILT and no BLOCKED | T1 |
| H8 | median tokens per BUILT notebook under 150k; median wall time under twelve minutes | T1 |
| H9 | two worktree seats on modules 04 and 05 complete three each and merge cleanly | T2 |
| H10 | the nightly task produces at least three BUILT lines by morning | unattended |
| H11 | no agent file names another agent | `tests/test_harness.py` |

H1 and H11 are automated. H2–H4 are the first evening's work; H5–H8 the first week; H9–H10 only if H7 holds.

## 7. Components

```
scripts/next.py              next stub in build order; --module; teach-back flag
scripts/loop.sh              T0 loop
scripts/ledger.py            ledger.jsonl and LEDGER.md
scripts/little_book.py       LITTLE_BOOK.md
.claude/agents/builder.md    the builder
.claude/agents/skeptic.md    the reviewer: fresh context, PASS or REVISE with at most three findings, named checks
.claude/skills/build-next/   the loop as a slash command
.claude/skills/skeptic/      the reviewer as a slash command
learn/                       quiz queue, digest, quiz template
```

## 8. Risks

| | Risk | Mitigation |
|---|---|---|
| R1 | Reviewer drift — the reviewer tries to be helpful and suggests additions | forbidden in the agent file; output truncated to three findings; the phrase "could also" in the digest is the leak to watch for |
| R2 | Gate gaming — seven trivial plots satisfy the visual count | the reviewer's brief asks whether each figure carries the argument; a specific abstention is a legal alternative to padding (Kalai et al. 2025) |
| R3 | Register collapse — the plain register drifts into developer prose with analogies attached | the reviewer tests the plain paragraph against a reader with no background, first time |
| R4 | Clinical overclaim — a clinical reading implying a synthetic result transfers to practice | the reviewer requires a "must not conclude" clause and a statement that the result is retrospective and synthetic (Rajpurkar et al. 2022) |
| R5 | Cost runaway when unattended | the loop and the scheduled task take a count; the ledger tracks tokens; the nightly prompt states a ceiling |
