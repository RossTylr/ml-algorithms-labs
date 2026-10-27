#!/usr/bin/env bash
# loop.sh — T0 harness. N × (next → claude -p → validate → ledger → commit). No subagents, no skeptic.
# Usage: scripts/loop.sh [N] [--execute]
set -euo pipefail
cd "$(dirname "$0")/.."
N="${1:-1}"; EXEC="${2:-}"
for _ in $(seq 1 "$N"); do
  REC=$(python scripts/next.py --json) || { echo "nothing left to build"; exit 0; }
  P=$(echo "$REC" | python -c 'import json,sys;print(json.load(sys.stdin)["path"])')
  ID=$(echo "$REC" | python -c 'import json,sys;print(json.load(sys.stdin)["id"])')
  TB=$(echo "$REC" | python -c 'import json,sys;print(json.load(sys.stdin)["teachback"])')
  echo "▶ $ID  $P  (teachback=$TB)"
  T0=$(date +%s)
  for ATTEMPT in 1 2 3; do
    claude -p --output-format json \
      "Read CLAUDE.md. Build the notebook at $P in place: fill every placeholder, keep every section heading, meet its visuals_min, set metadata.ml_mastery.status to \"built\". Teachback=$TB (if true, leave the 🗣️ Plain paragraph of section 2 as '_teachback: Ross writes this_'). When done also write learn/queue/$ID.quiz.md with five questions from the Learning Objectives and answers at the bottom. Then run: python scripts/validate.py $P $EXEC and fix anything that fails before finishing." \
      > "/tmp/build_$ID.json" || true
    if python scripts/validate.py "$P" $EXEC > "/tmp/gate_$ID.txt"; then VER=BUILT; break; else VER=REVISE; fi
  done
  [[ "$VER" == "REVISE" ]] && VER=BLOCKED
  TOK=$(python -c 'import json,sys;d=json.load(open(sys.argv[1]));u=d.get("usage",{});print(u.get("input_tokens",0)+u.get("output_tokens",0))' "/tmp/build_$ID.json" 2>/dev/null || echo 0)
  python scripts/ledger.py add --id "$ID" --path "$P" --attempt "$ATTEMPT" --verdict "$VER" \
    --gates "$(grep -c '✓' "/tmp/gate_$ID.txt")/11 pass" --skeptic "n/a (T0)" --tokens "$TOK" --seconds $(( $(date +%s) - T0 )) \
    --findings "$(grep '✗' "/tmp/gate_$ID.txt" | tr '\n' ';' | head -c 300)"
  if [[ "$VER" == "BUILT" ]]; then
    git add "$P" learn/ ledger.jsonl LEDGER.md && git commit -qm "nb($ID): built — PASS G1–G11" || true
  else
    echo "✗ $ID BLOCKED after $ATTEMPT attempts"; exit 1
  fi
done
