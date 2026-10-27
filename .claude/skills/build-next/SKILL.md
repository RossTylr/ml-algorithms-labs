---
name: build-next
description: Build the next unbuilt ml-algorithms-labs notebook through builder → validate → skeptic → ledger → commit. Optional count argument.
---
# /build-next [N]

Run this loop N times (default 1). Stop on BLOCKED.

1. `python scripts/next.py --json` → path, id, teachback.
2. Launch the **builder** subagent with: "Build `<path>`. teachback=<flag>." Wait for its gate ledger.
3. `python scripts/validate.py <path>` — if FAIL, send the failing gates back to the SAME builder (SendMessage) once; if still FAIL, once more; then BLOCKED.
4. Launch the **skeptic** subagent (fresh) with: "Skeptic review of `<path>`." Parse VERDICT.
5. If REVISE: send F1–F3 verbatim to the same builder; re-run step 3 and step 4 once. If still REVISE → BLOCKED.
6. Append skeptic findings (if any) to `learn/digest.md` under a `## <id>` heading, newest first.
7. `python scripts/ledger.py add --id <id> --path <path> --attempt <n> --verdict <BUILT|BLOCKED> --gates "<x>/11 pass" --skeptic <PASS|REVISE> --findings "<F1;F2;F3>" --tokens <sum if known> --seconds <elapsed>`
8. If BUILT: `git add <path> learn/ ledger.jsonl LEDGER.md && git commit -m "nb(<id>): built — PASS G1–G11, skeptic PASS"`.

Report one line per notebook: `<id> <verdict> attempts=<n> skeptic=<verdict>`. Nothing else. Do not summarise the notebook. Do not suggest what to build next.
