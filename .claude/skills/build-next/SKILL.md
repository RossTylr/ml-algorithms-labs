---
name: build-next
description: Build the next unbuilt ml-algorithms-labs notebook through builder → validate → skeptic → ledger → commit. Optional count argument.
---
# /build-next [N]

Run this loop N times (default 1). Stop on BLOCKED.

1. `python scripts/next.py --json` → path, id, teachback.
2. Launch the **builder** subagent with: "Build `<path>`. teachback=<flag>." — model **opus** if the notebook's module is tier 3 (see INDEX.md), else the agent default (sonnet). Wait for its gate ledger.
3. `python scripts/validate.py <path>` — if FAIL, send the failing gates back to the SAME builder (SendMessage) once; if still FAIL, once more; then BLOCKED.
4. Launch the **skeptic** subagent (fresh) with: "Skeptic review of `<path>`." Parse VERDICT.
5. If REVISE: send F1–F3 verbatim to the same builder; re-run step 3 and step 4 once. If still REVISE → BLOCKED.
6. Append skeptic findings (if any) to `learn/digest.md` under a `## <id>` heading, newest first.
7. `python scripts/ledger.py add --id <id> --path <path> --attempt <n> --verdict <BUILT|BLOCKED> --gates "<✓ count>/<✓ + ✗ count> pass" --skeptic <PASS|REVISE> --findings "<F1;F2;F3>" --tokens <total> --usd <session cost> --seconds <elapsed>` — tokens = input_tokens + output_tokens + cache_read_input_tokens + cache_creation_input_tokens from each usage block, summed over every builder and skeptic run; pass `--usd` only when the cost is known.
8. Set status from the verdict — `built` on BUILT, `blocked` on BLOCKED: `python -c 'import json,sys;p,s=sys.argv[1:];nb=json.load(open(p));nb["metadata"]["ml_mastery"]["status"]=s;open(p,"w").write(json.dumps(nb,indent=1,ensure_ascii=False))' <path> <built|blocked>`
9. `python scripts/little_book.py` (regenerates LITTLE_BOOK.md from everything built).
10. If BUILT: `git add <path> learn/ ledger.jsonl LEDGER.md LITTLE_BOOK.md && git commit -m "nb(<id>): built — PASS G1–G14, skeptic PASS"`.

Report one line per notebook: `<id> <verdict> attempts=<n> skeptic=<verdict>`. Nothing else. Do not summarise the notebook. Do not suggest what to build next.
