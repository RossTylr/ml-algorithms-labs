# Getting started

Instructions for the first build session, using Claude Code inside Cursor on a Mac. Two kinds of input are involved and they go in different places:

- **Terminal commands** go in Cursor's integrated terminal (View → Terminal, or Ctrl+`).
- **Claude Code prompts** go in the Claude Code pane or in a terminal where `claude` is running. These begin with a slash.

Each step states which. Expected results are given so a departure is visible straight away.

## Part A — set up (once, about five minutes)

| Step | Where | Do | Expect |
|---|---|---|---|
| A1 | Terminal | `cd ~/Projects` then `git clone https://github.com/RossTylr/ml-algorithms-labs.git` | a folder `ml-algorithms-labs` |
| A2 | Cursor | File → Open Folder → `ml-algorithms-labs` | Cursor reopens in the repo; `CLAUDE.md` is picked up automatically and points to `AGENTS.md`, the single guide |
| A3 | Terminal | `python3 -m venv .venv` | a `.venv` folder |
| A4 | Terminal | `source .venv/bin/activate` | prompt shows `(.venv)` |
| A5 | Terminal | `pip install -r requirements/base.txt pytest` | about two minutes; no errors |
| A6 | Terminal | `python -m ipykernel install --user --name ml-algorithms-labs` | `Installed kernelspec …` — needed for gate G12 |
| A7 | Terminal | `cp .claude/settings.local.example.json .claude/settings.local.json`, then edit the papers path in `additionalDirectories` if yours differs | no output; Claude Code now runs every command in /build-next and /skeptic without asking and can read the papers folder (the copy is git-ignored, so local edits stay local). File edits still ask unless you start claude with `--permission-mode acceptEdits` for unattended runs |
| A8 | Terminal | `pytest -q` | `59 passed, 1 deselected` (the deselected test executes notebooks; it runs nightly) |
| A9 | Terminal | `python scripts/next.py` | the path of the first notebook in build order whose status is `stub` (on an empty scaffold, `00_mathematical_foundations/01_linear_algebra/01_vectors_matrices_operations.ipynb` — test H1) |

If A8 or A9 differs, stop and fix before building anything. Nothing downstream is meaningful until the scaffold is proven.

## Part B — the first build, headless (the floor)

This runs one build with no agents and no reviewer. It measures whether one prompt plus `AGENTS.md` plus the stub produces a gate-passing notebook, and what it costs.

| Step | Where | Do | Expect |
|---|---|---|---|
| B1 | Terminal | `scripts/loop.sh 1` | five to ten minutes; ends with `nb(00.01.01)` committed, or `BLOCKED` |
| B2 | Terminal | `cat LEDGER.md` | one row: attempt, verdict, gates passed, tokens, seconds |
| B3 | Terminal | `python scripts/validate.py 00_mathematical_foundations/01_linear_algebra/01_vectors_matrices_operations.ipynb --execute` | `PASS` with G12 ticked |

Record three numbers from B2: attempts, tokens, seconds. They are the baseline every later configuration is judged against.

If B1 ends BLOCKED, the ledger row names the failing gates. The three usual causes: `claude` is not on the PATH (install Claude Code first); the kernel from A6 is missing (G12); the builder left `_objective_` placeholders (G2). The third is a prompt problem, not a gate problem, and is the measurement Part B exists to take.

## Part C — the loop with agents (the working configuration)

On a Mac, before any `/build-next N`, run `caffeinate -is -w $(pgrep -n claude)` in a second terminal. It keeps the machine from idle and system sleep (system sleep only while on mains power) until that Claude Code process exits, so a long run is not cut off when the lid or the screen goes quiet.

| Step | Where | Do | Expect |
|---|---|---|---|
| C1 | Terminal | `claude` | Claude Code starts in the repo |
| C2 | Claude Code | `/build-next` | one line: `<id> BUILT attempts=1 skeptic=PASS` (or BLOCKED) for the stub `next.py` names |
| C3 | Terminal | `cat LEDGER.md` | two rows now; the second has a reviewer verdict |
| C4 | Claude Code | record the weekly usage % (`/usage`); `/build-next 5`; record the weekly usage % again; then in a terminal `python scripts/ledger.py summary` | five lines; at least four BUILT, none BLOCKED. Report the usage % before and after, and pass^1 and pass@3 from the summary |
| C5 | Terminal | `git log --oneline \| head` | one commit per built notebook |

C4 is test H7. If it holds, the loop can be left running. If it does not, read `learn/digest.md` — the reviewer's findings say where the builder is failing and whether the fix belongs in `AGENTS.md`, the builder agent file, or the manifest.

## Part D — the reproduction test

The first notebook that reproduces a paper's figure is the Lasso notebook (Hastie, Tibshirani and Tibshirani 2018, Figure 1). Either let `/build-next` reach it, or jump to it:

| Step | Where | Do | Expect |
|---|---|---|---|
| D1 | Claude Code | `/build-next` repeated, or jump with the headless prompt below | the notebook contains a figure captioned as a reproduction of the paper's, or an abstention explaining why it cannot |
| D2 | Terminal | `python scripts/validate.py 04_regression/04_regularised/02_lasso.ipynb --execute` | PASS |

Headless jump:

```
claude -p "Read AGENTS.md. Build 04_regression/04_regularised/02_lasso.ipynb in place. Then run python scripts/validate.py on it and fix any failures."
```

## Part E — the daily fifteen minutes

| Step | Where | Do |
|---|---|---|
| E1 | Terminal | `cat LEDGER.md` — what was built, what the reviewer said |
| E2 | Terminal | `ls learn/queue/` then open the newest quiz; answer before opening the notebook; note the score |
| E3 | Terminal | `cat learn/digest.md` — the reviewer's findings, newest first |
| E4 | Terminal | `python scripts/little_book.py && open LITTLE_BOOK.md` |
| E5 | Claude Code | `/skeptic <path>` on any notebook edited by hand, including a teach-back paragraph; a PASS on a built or blocked notebook marks it `accepted` and commits it |
| E6 | Terminal | `git push` |

## Part F — unattended

Once C4 holds, schedule the loop. In Claude Code:

```
/schedule "nightly build" --cron "0 2 * * *" --prompt "/build-next 4"
```

Or use the scheduled-task interface in the Claude app with the same prompt and cadence. The count bounds the night's work, and two BLOCKED notebooks in a row stop it early. The morning check is Part E.

## The complete prompt set

| Prompt | Use |
|---|---|
| `/build-next` | the normal case |
| `/build-next N` | N in sequence; BLOCKED is committed and the run moves on; stops after two BLOCKED in a row |
| `/skeptic <path>` | review alone, on any notebook |
| `claude -p "Read AGENTS.md. Build <path> in place. Then run python scripts/validate.py <path> and fix any failures."` | headless, no agents |

There is no fifth prompt. A need that seems to call for one belongs in the manifest or in `AGENTS.md`.
