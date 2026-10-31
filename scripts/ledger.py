#!/usr/bin/env python3
"""ledger.py — append a build record; regenerate LEDGER.md.

    python scripts/ledger.py add --id 00.01.01 --path ... --attempt 1 --verdict BUILT \
        --gates "G1..G11 pass" --skeptic PASS --tokens 91000 --seconds 540
    python scripts/ledger.py summary
    python scripts/ledger.py spent --after 12     # usd summed over rows after line 12 (one run's rows)
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
    if a.verdict == "ACCEPTED" and a.by != "human":
        sys.exit("ledger: ACCEPTED is a human /skeptic PASS — it needs --by human")
    rec = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "id": a.id, "path": a.path, "attempt": a.attempt, "verdict": a.verdict,
        "gates": a.gates, "skeptic": a.skeptic, "findings": a.findings,
        "tokens": a.tokens, "usd": a.usd, "seconds": a.seconds, "understood": None,
        "abstained": a.abstained, "exploratory": a.exploratory, "by": a.by,
    }
    with LEDGER.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    summary()


def summary() -> list[str]:
    recs = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()] if LEDGER.exists() else []
    built = [r for r in recs if r["verdict"] == "BUILT"]
    latest = {r["id"]: r for r in recs}
    blocked = [r for r in latest.values() if r["verdict"] == "BLOCKED"]  # a later ACCEPTED row (human PASS) lifts it
    accepted = {r["id"] for r in recs if r["verdict"] == "ACCEPTED"}  # counted apart, so pass^1 / pass@3 stay the agent's
    revise = [r for r in recs if r["verdict"] == "REVISE"]
    tok = sorted(r["tokens"] for r in built if r.get("tokens"))
    sec = sorted(r["seconds"] for r in built if r.get("seconds"))
    usd = sorted(r["usd"] for r in built if r.get("usd") is not None)
    med = lambda xs: xs[len(xs) // 2] if xs else "—"
    # pass^1: BUILT at attempt 1; pass@3: BUILT at any attempt — both over every notebook with a row
    ids = set(latest)
    first = {r["id"] for r in built if r["attempt"] == 1}
    ever = {r["id"] for r in built}
    rate = lambda s: f"{len(s)}/{len(ids)} ({100 * len(s) / len(ids):.0f}%)" if ids else "—"
    head = [
        "# Build Ledger", "",
        "Rows before 2026-10-29 record tokens under the earlier single-field definition; later rows sum the four "
        "usage fields (input, output, cache read, cache creation).", "",
        f"**Built** {len(built)} · **Accepted** {len(accepted)} (human) · **Revise cycles** {len(revise)} · **Blocked** {len(blocked)} · "
        f"**Median tokens/built** {med(tok)} · **Median seconds/built** {med(sec)}", "",
        f"**pass^1** {rate(first)} — BUILT at the first attempt, over notebooks with any row  ",
        f"**pass@3** {rate(ever)} — BUILT within three attempts, over the same notebooks  ",
        f"**Median usd/built** {med(usd)} ({len(usd)} of {len(built)} BUILT rows carry usd)", "",
    ]
    lines = head + [
        "| ts | id | attempt | verdict | gates | skeptic | abst | expl | tokens | usd | s | understood |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in reversed(recs[-200:]):
        by = f" · {r['by']}" if r.get("by", "builder") != "builder" else ""
        lines.append(f"| {r['ts'][:16]} | {r['id']} | {r['attempt']}{by} | **{r['verdict']}** | {r['gates']} | {r['skeptic']} | {r.get('abstained', 0)} | {r.get('exploratory', 0)} | {r.get('tokens') or ''} | {r.get('usd') or ''} | {r.get('seconds') or ''} | {r.get('understood') if r.get('understood') is not None else ''} |")
    if blocked:
        lines += ["", "## Blocked — do not retry without a manifest change", ""]
        lines += [f"- `{r['id']}` — {r['findings']}" for r in blocked]
    MD.write_text("\n".join(lines) + "\n")
    return head


def spent(after: int) -> float:
    """usd over the ledger rows after line `after` — the rows one run appended. Rows without usd count as 0."""
    rows = [ln for ln in LEDGER.read_text().splitlines() if ln.strip()] if LEDGER.exists() else []
    return round(sum(json.loads(ln).get("usd") or 0 for ln in rows[after:]), 2)


def main() -> int:
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add")
    for k in ["id", "path", "verdict", "gates", "skeptic"]:
        p.add_argument(f"--{k}", required=True)
    p.add_argument("--attempt", type=int, default=1); p.add_argument("--findings", default="")
    p.add_argument("--tokens", type=int); p.add_argument("--usd", type=float); p.add_argument("--seconds", type=int)
    p.add_argument("--abstained", type=int, default=0); p.add_argument("--exploratory", type=int, default=0)
    p.add_argument("--by", default="builder", help="builder, or human for a hand-edited notebook /skeptic passed")
    sub.add_parser("summary")
    sub.add_parser("spent").add_argument("--after", type=int, default=0, help="ledger line count when the run started")
    a = ap.parse_args()
    if a.cmd == "add":
        add(a)
    elif a.cmd == "spent":
        print(spent(a.after))
    else:
        print("\n".join(summary()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
