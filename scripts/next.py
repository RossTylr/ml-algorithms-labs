#!/usr/bin/env python3
"""next.py — print the path of the next unbuilt stub in build order. Deterministic. No planning.

Build order: tier (1→3), then module id, then topic, then notebook.
A notebook is unbuilt if metadata.ml_mastery.status == "stub"; "built" and "blocked" are skipped.
BLOCKED notebooks (in ledger.jsonl) are skipped too.

    python scripts/next.py                 # one path
    python scripts/next.py --n 5           # five paths
    python scripts/next.py --module 04     # restrict to a module
    python scripts/next.py --json          # path + id + title + teachback flag
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import nbformat
from manifest import ManifestError, load_manifest

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


def revise_topics() -> set[str]:
    """Topics (NN.MM) whose most recent ledger record carried a skeptic REVISE — teach-back targets (Dell'Acqua: the jagged edge)."""
    if not LEDGER.exists():
        return set()
    last = {}
    for ln in LEDGER.read_text().splitlines():
        if ln.strip():
            rec = json.loads(ln); last[rec["id"][:5]] = rec.get("skeptic", "")
    return {k for k, v in last.items() if v.startswith("REVISE")}


def built_count() -> int:
    if not LEDGER.exists():
        return 0
    return sum(1 for ln in LEDGER.read_text().splitlines() if ln.strip() and json.loads(ln).get("verdict") == "BUILT")


def candidates(manifest: dict, module: str | None):
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
            yield p, meta, nb.cells[0].source.splitlines()[0].lstrip("# ").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--module")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        manifest = load_manifest()
    except ManifestError as e:
        print(e, file=sys.stderr); return 1
    base = built_count()
    jagged = revise_topics()
    out = []
    for i, (p, meta, title) in enumerate(candidates(manifest, a.module)):
        if i >= a.n:
            break
        rel = str(p.relative_to(ROOT))
        teachback = (meta["id"][:5] in jagged) or ((base + i + 1) % 5 == 0)
        out.append({"path": rel, "id": meta["id"], "title": title, "band": meta.get("band"), "visuals_min": meta.get("visuals_min"), "teachback": teachback})
    if not out:
        print("NONE", file=sys.stderr); return 1
    for rec in out:
        print(json.dumps(rec) if a.json else rec["path"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
