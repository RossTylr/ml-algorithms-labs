#!/usr/bin/env python3
"""ledger.py — append a build record; regenerate LEDGER.md.

    python scripts/ledger.py add --id 00.01.01 --path ... --attempt 1 --verdict BUILT \
        --gates "G1..G11 pass" --skeptic PASS --tokens 91000 --seconds 540
    python scripts/ledger.py summary
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "ledger.jsonl"
MD = ROOT / "LEDGER.md"


def add(a) -> None:
    rec = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "id": a.id, "path": a.path, "attempt": a.attempt, "verdict": a.verdict,
        "gates": a.gates, "skeptic": a.skeptic, "findings": a.findings,
        "tokens": a.tokens, "seconds": a.seconds, "understood": None,
    }
    with LEDGER.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    summary()


def summary() -> None:
    recs = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()] if LEDGER.exists() else []
    built = [r for r in recs if r["verdict"] == "BUILT"]
    blocked = [r for r in recs if r["verdict"] == "BLOCKED"]
    revise = [r for r in recs if r["verdict"] == "REVISE"]
    tok = sorted(r["tokens"] for r in built if r.get("tokens"))
    sec = sorted(r["seconds"] for r in built if r.get("seconds"))
    med = lambda xs: xs[len(xs) // 2] if xs else "—"
    lines = [
        "# Build Ledger", "",
        f"**Built** {len(built)} · **Revise cycles** {len(revise)} · **Blocked** {len(blocked)} · "
        f"**Median tokens/built** {med(tok)} · **Median seconds/built** {med(sec)}", "",
        "| ts | id | attempt | verdict | gates | skeptic | tokens | s | understood |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in reversed(recs[-200:]):
        lines.append(f"| {r['ts'][:16]} | {r['id']} | {r['attempt']} | **{r['verdict']}** | {r['gates']} | {r['skeptic']} | {r.get('tokens') or ''} | {r.get('seconds') or ''} | {r.get('understood') if r.get('understood') is not None else ''} |")
    if blocked:
        lines += ["", "## Blocked — do not retry without a manifest change", ""]
        lines += [f"- `{r['id']}` — {r['findings']}" for r in blocked]
    MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add")
    for k in ["id", "path", "verdict", "gates", "skeptic"]:
        p.add_argument(f"--{k}", required=True)
    p.add_argument("--attempt", type=int, default=1); p.add_argument("--findings", default="")
    p.add_argument("--tokens", type=int); p.add_argument("--seconds", type=int)
    sub.add_parser("summary")
    a = ap.parse_args()
    add(a) if a.cmd == "add" else summary()
    return 0


if __name__ == "__main__":
    sys.exit(main())
