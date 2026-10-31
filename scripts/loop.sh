#!/usr/bin/env bash
# loop.sh — T0 harness. N × (next → claude -p → validate → ledger → commit). No subagents, no skeptic.
# Usage: scripts/loop.sh [N] [--execute] [--usd <ceiling>]
# Same stop rules as /build-next: BLOCKED is committed; with N given the run moves on and stops only after
# two consecutive BLOCKED; with --usd it stops with "ceiling reached" once this run's ledger usd exceeds the ceiling.
set -euo pipefail
cd "$(dirname "$0")/.."
N=1; COUNT=""; EXEC=""; USD=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --execute) EXEC="--execute" ;;
    --usd) USD="$2"; shift ;;
    *) N="$1"; COUNT=1 ;;
  esac
  shift
done
START=0; [[ -f ledger.jsonl ]] && START=$(wc -l < ledger.jsonl | tr -d ' ')
STREAK=0
for _ in $(seq 1 "$N"); do
  if [[ -n "$USD" ]]; then
    SPENT=$(python scripts/ledger.py spent --after "$START")
    if awk -v s="$SPENT" -v c="$USD" 'BEGIN { exit !(s > c) }'; then echo "ceiling reached"; exit 0; fi
  fi
  REC=$(python scripts/next.py --json) || { echo "nothing left to build"; exit 0; }
  P=$(echo "$REC" | python -c 'import json,sys;print(json.load(sys.stdin)["path"])')
  ID=$(echo "$REC" | python -c 'import json,sys;print(json.load(sys.stdin)["id"])')
  TITLE=$(echo "$REC" | python -c 'import json,sys;print(json.load(sys.stdin)["title"])')
  TB=$(echo "$REC" | python -c 'import json,sys;print(json.load(sys.stdin)["teachback"])')
  echo "▶ $ID  $P  (teachback=$TB)"
  T0=$(date +%s); rm -f "/tmp/build_${ID}"_a*.json
  for ATTEMPT in 1 2 3; do
    claude -p --permission-mode acceptEdits --allowedTools "Bash(python scripts/validate.py:*)" \
      --output-format json \
      "Read AGENTS.md. Build the notebook at $P in place: fill every placeholder, keep every section heading, meet its visuals_min, leave metadata.ml_mastery.status as \"stub\". Teachback=$TB (if true, leave the 🗣️ Plain paragraph of section 2 as '_teachback: Ross writes this_'). Mark one code cell # CENTRAL. Write learn/queue/$ID.quiz.md per learn/QUIZ_TEMPLATE.md (six questions if study is set, hints ladder, answers at the bottom). Then run: python scripts/validate.py $P $EXEC and fix anything that fails before finishing." \
      > "/tmp/build_${ID}_a$ATTEMPT.json" || true
    if python scripts/validate.py "$P" $EXEC > "/tmp/gate_$ID.txt"; then VER=BUILT; break; else VER=REVISE; fi
  done
  [[ "$VER" == "REVISE" ]] && VER=BLOCKED
  python -c 'import json,sys;p,s=sys.argv[1:];nb=json.load(open(p));nb["metadata"]["ml_mastery"]["status"]=s;open(p,"w").write(json.dumps(nb,indent=1,ensure_ascii=False))' "$P" "$(echo "$VER" | tr 'A-Z' 'a-z')"
  # cost of every attempt: all four usage fields (cache reads dominate) and the session USD
  read -r TOK USD_NB <<< "$(python -c 'import json,sys;K=("input_tokens","output_tokens","cache_read_input_tokens","cache_creation_input_tokens");D=[json.loads(t) for t in (open(f).read() for f in sys.argv[1:]) if t.lstrip().startswith("{")];print(sum(d.get("usage",{}).get(k) or 0 for d in D for k in K),round(sum(d.get("total_cost_usd") or 0 for d in D),2))' "/tmp/build_${ID}"_a*.json 2>/dev/null || echo "0 0")"
  python scripts/ledger.py add --id "$ID" --path "$P" --attempt "$ATTEMPT" --verdict "$VER" \
    --gates "$(grep -c '✓' "/tmp/gate_$ID.txt")/$(grep -cE '✓|✗' "/tmp/gate_$ID.txt") pass" --skeptic "n/a (T0)" \
    --tokens "$TOK" --usd "$USD_NB" --seconds $(( $(date +%s) - T0 )) \
    --findings "$(grep '✗' "/tmp/gate_$ID.txt" | tr '\n' ';' | head -c 300)"
  git add "$P" learn/ library/briefs/ ledger.jsonl LEDGER.md
  if [[ "$VER" == "BUILT" ]]; then
    git commit -qm "nb($ID): built — PASS G1–G14" || true
    STREAK=0
  else
    git commit -qm "nb($ID): $TITLE — BLOCKED attempt $ATTEMPT" || true
    echo "✗ $ID BLOCKED after $ATTEMPT attempts"
    STREAK=$((STREAK + 1))
    [[ -z "$COUNT" ]] && exit 1
    if [[ "$STREAK" -ge 2 ]]; then echo "stopped: two BLOCKED in a row"; exit 1; fi
  fi
done
