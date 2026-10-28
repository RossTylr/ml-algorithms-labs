#!/usr/bin/env python3
"""next.py — print the path of the next unbuilt stub in build order. Deterministic. No planning.

Build order: tier (1→3), then module id, then topic, then notebook.
A notebook is unbuilt if metadata.ml_mastery.status == "stub".
BLOCKED notebooks (in ledger.jsonl) are skipped.

    python scripts/next.py                 # one path
    python scripts/next.py --n 5           # five paths
    python scripts/next.py --module 04     # restrict to a module
    python scripts/next.py --json          # path + id + teachback flag
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import nbformat
import yaml

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "ledger.jsonl"


def blocked_ids() -> set[str]:
    if not LEDGER.exists():
        return set()
    out = set()
    for line in LEDGER.read_text().splitlines():
        if line.strip():
            rec = json.loads(line)
            if rec.get("verdict") == "BLOCKED":
                out.add(rec["id"])
    return out


def built_count() -> int:
    if not LEDGER.exists():
        return 0
    return sum(1 for ln in LEDGER.read_text().splitlines() if ln.strip() and json.loads(ln).get("verdict") == "BUILT")


def candidates(module: str | None):
    manifest = yaml.safe_load((ROOT / "curriculum" / "curriculum.yaml").read_text())
    mods = sorted(manifest["modules"], key=lambda m: (m["tier"], float(m.get("order", m["id"]))))
    total = sum(len(t["notebooks"]) for m in manifest["modules"] for t in m["topics"])
    n_built = built_count()
    skip = blocked_ids()
    for m in mods:
        if module and m["id"] != module:
            continue
        mdir = ROOT / f"{m['id']}_{m['slug']}"
        for p in sorted(mdir.glob("*/*.ipynb")):
            nb = nbformat.read(p, as_version=4)
            meta = nb.metadata.get("ml_mastery", {})
            if meta.get("status") != "stub" or meta.get("id") in skip:
                continue
            if meta.get("build") == "last" and n_built < total - 1:
                continue  # 29.meta.1 waits until everything else is BUILT
            yield p, meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--module")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    base = built_count()
    out = []
    for i, (p, meta) in enumerate(candidates(a.module)):
        if i >= a.n:
            break
        rel = str(p.relative_to(ROOT))
        teachback = (base + i + 1) % 5 == 0
        out.append({"path": rel, "id": meta["id"], "band": meta.get("band"), "visuals_min": meta.get("visuals_min"), "teachback": teachback})
    if not out:
        print("NONE", file=sys.stderr); return 1
    for rec in out:
        print(json.dumps(rec) if a.json else rec["path"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
