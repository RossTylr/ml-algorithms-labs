---
name: skeptic
description: Run the skeptic subagent alone on a given notebook path (including one Ross edited by hand) and append findings to learn/digest.md. A human-invoked PASS on a built or blocked notebook marks it accepted.
---
# /skeptic <path>

1. Launch the **skeptic** subagent with: "Skeptic review of `<path>`."
2. Print its output verbatim.
3. Append it to `learn/digest.md` under `## <path> — <date>`, newest first.
4. Human acceptance. This skill is the only thing that sets status `accepted`, and only when ALL hold: a person typed `/skeptic` (never inside /build-next, a scheduled task or another agent); the notebook's `metadata.ml_mastery.status` is `built` or `blocked`; VERDICT is PASS; and `python scripts/validate.py <path>` passes. Then:
   - `python -c 'import json,sys;p,s=sys.argv[1:];nb=json.load(open(p));nb["metadata"]["ml_mastery"]["status"]=s;open(p,"w").write(json.dumps(nb,indent=1,ensure_ascii=False))' <path> accepted`
   - `python scripts/ledger.py add --id <id> --path <path> --attempt <the id's last ledger attempt + 1> --verdict ACCEPTED --gates "<✓ count>/<✓ + ✗ count> pass" --skeptic PASS --by human`
   - `python scripts/little_book.py`
   - `git add <path> learn/ ledger.jsonl LEDGER.md LITTLE_BOOK.md && git commit -m "nb(<id>): <title> — ACCEPTED by human, skeptic PASS"`

   In every other case change no status and record nothing beyond step 3.
Nothing else.
