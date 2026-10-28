#!/usr/bin/env python3
"""library.py — build library/INDEX.md from curated.yaml + listing.txt. Flags duplicates and dead files.
Also verifies every `study:`/`refs:` key in curriculum.yaml exists in curated.yaml (exit 1 if not)."""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "library"
DEAD = re.compile(r"Get unlimited access|rClaudeAI|WRITE FOR US|Publish AI, ML|AI NEWS \(MOVED|Welcome Developer Guide|videoplayback", re.I)


def main() -> int:
    curated = yaml.safe_load((LIB / "curated.yaml").read_text())
    listing = [ln.strip() for ln in (LIB / "listing.txt").read_text().splitlines() if ln.strip()]
    by_file = {v["file"]: k for k, v in curated.items()}
    dup_targets = {v["duplicate_of"]: k for k, v in curated.items() if v.get("duplicate_of")}

    # manifest cross-check
    man = yaml.safe_load((ROOT / "curriculum" / "curriculum.yaml").read_text())
    used, missing = Counter(), set()
    for m in man["modules"]:
        for t in m["topics"]:
            for nb in t["notebooks"]:
                for k in ([nb.get("study")] if isinstance(nb.get("study"), str) and nb["study"] in curated else []) + list(nb.get("refs", [])):
                    if k in curated:
                        used[k] += 1
                    else:
                        missing.add(k)
    kinds = Counter(v["kind"] for v in curated.values())
    lines = ["# Library Index", "",
             f"**Files in folder** {len(listing)} · **Curated** {len(curated)} (A {kinds['A']} · B {kinds['B']} · C {kinds['C']} · D {kinds['D']}) · **Cited by manifest** {len(used)}", "",
             "Kinds: **A** seminal method (builder reproduces a figure) · **B** clinical (becomes a subject) · **C** critique (skeptic check) · **D** reference only.", "",
             "## Curated", "", "| key | kind | year | title | reproduce / check | cited |", "|---|---|---|---|---|---|"]
    for k, v in sorted(curated.items(), key=lambda kv: (kv[1]["kind"], kv[1].get("year", 0))):
        rc = v.get("reproduce") or v.get("check") or v.get("note") or ""
        lines.append(f"| `{k}` | {v['kind']} | {v.get('year','')} | {v['title']} | {rc} | {used.get(k, 0)} |")
    lines += ["", "## Flags", ""]
    for k, v in curated.items():
        if v.get("duplicate_of"):
            lines.append(f"- **duplicate**: `{v['file']}` ≡ `{v['duplicate_of']}` (`{k}`)")
    for f in listing:
        if DEAD.search(f):
            lines.append(f"- **dead/paywall capture**: `{f}`")
    lines.append("- **wrong page**: `02_Theory_and_Foundations/6088 - V323.indd (2017).pdf` is the Nature page before Rumelhart–Hinton–Williams 1986")
    lines += ["", "## Uncurated (kind D by default)", ""]
    for f in listing:
        if f not in by_file and f not in dup_targets and not DEAD.search(f):
            lines.append(f"- {f}")
    (LIB / "INDEX.md").write_text("\n".join(lines) + "\n")
    if missing:
        print(f"library: manifest cites unknown keys: {sorted(missing)}", file=sys.stderr)
        return 1
    print(f"library: {len(curated)} curated, {len(listing)} files, {len(used)} keys cited")
    return 0


if __name__ == "__main__":
    sys.exit(main())
