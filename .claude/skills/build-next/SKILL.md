---
name: build-next
description: Build the next unbuilt ml-algorithms-labs notebook through builder → validate → skeptic → ledger → commit. Optional count argument and usd ceiling.
---
# /build-next [N] [--usd <ceiling>]

Run this loop N times (default 1). Every notebook attempted counts toward N, whatever its verdict.

Stop rules:
- With N given, BLOCKED does not stop the run: the notebook is committed (step 10) and the loop moves to the next stub. Stop after two consecutive BLOCKED.
- At the start, record START = the line count from `wc -l ledger.jsonl` (0 if the file does not exist). If `--usd` is given, before each notebook run `python scripts/ledger.py spent --after <START>`; if the sum exceeds the ceiling, print `ceiling reached` and stop. Rows without usd count as zero.

1. `python scripts/next.py --json` → path, id, title, teachback.
2. Launch the **builder** subagent with: "Build `<path>`. teachback=<flag>." — model **opus** if the notebook's module is tier 3 (see INDEX.md), else the agent default (sonnet). Wait for its gate ledger.
3. `python scripts/validate.py <path>` — if FAIL, send the failing gates back to the SAME builder (SendMessage) once; if still FAIL, once more; then BLOCKED.
4. Launch the **skeptic** subagent (fresh) with: "Skeptic review of `<path>`." Parse VERDICT.
5. If REVISE: send F1–F3 verbatim (not U-lines — an Unknown is never a revision) to the same builder, with: "Edit only the cells these findings name and change nothing else."; re-run step 3 and step 4 once. If still REVISE → BLOCKED.
6. Append skeptic findings and Unknowns (F- and U-lines, if any) to `learn/digest.md` under a `## <id>` heading, newest first.
7. `python scripts/ledger.py add --id <id> --path <path> --attempt <n> --verdict <BUILT|BLOCKED> --gates "<✓ count>/<✓ + ✗ count> pass" --skeptic <PASS|REVISE> --findings "<F1;F2;F3>" --tokens <total> --usd <session cost> --seconds <elapsed>` — tokens = input_tokens + output_tokens + cache_read_input_tokens + cache_creation_input_tokens from each usage block, summed over every builder and skeptic run; pass `--usd` only when the cost is known.
8. Set status from the verdict — `built` on BUILT, `blocked` on BLOCKED: `python -c 'import json,sys;p,s=sys.argv[1:];nb=json.load(open(p));nb["metadata"]["ml_mastery"]["status"]=s;open(p,"w").write(json.dumps(nb,indent=1,ensure_ascii=False))' <path> <built|blocked>`
9. `python scripts/little_book.py` (regenerates LITTLE_BOOK.md from everything built).
10. Commit either verdict with `git add <path> learn/ ledger.jsonl LEDGER.md LITTLE_BOOK.md`, then:
    - BUILT: `git commit -m "nb(<id>): built — PASS G1–G14, skeptic PASS"`
    - BLOCKED: `git commit -m "nb(<id>): <title> — BLOCKED attempt <n>"` — a failed attempt is a result; the ledger row must point at a commit that holds it.

Report one line per notebook: `<id> <verdict> attempts=<n> skeptic=<verdict>`. If the run stops early, one more line: `ceiling reached` or `stopped: two BLOCKED in a row`. Nothing else. Do not summarise the notebook. Do not suggest what to build next.
