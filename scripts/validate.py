#!/usr/bin/env python3
"""
validate.py — Gate a notebook (or a module, or the whole repo) against curriculum.yaml `gates:`.

Each gate is a pure function over the notebook JSON. Output is a ledger: one line per gate,
PASS/FAIL, with the reason. Exit code 1 if any gate fails. This is the only quality process:
it BOUNDS what may be claimed as built. It never generates tasks.

Usage:
    python scripts/validate.py path/to/notebook.ipynb
    python scripts/validate.py 04_regression              # every notebook in the module
    python scripts/validate.py --all
    python scripts/validate.py --all --execute            # also run each notebook (slow)
    python scripts/validate.py --all --built-only         # skip untouched stubs
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import nbformat
import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "curriculum" / "curriculum.yaml"

REGISTERS = ["🗣️", "💻", "🔬"]
RFI_BLOCKS = ["📊", "🔍", "💡", "⚠️"]
FIG_PATTERNS = [
    r"plt\.show\(\)",
    r"plt\.subplots\(",
    r"plt\.figure\(",
    r"\.plot\(",
    r"px\.\w+\(",
    r"go\.Figure\(",
    r"sns\.\w+plot\(",
    r"sns\.heatmap\(",
    r"display\(fig",
    r"fig\.show\(\)",
]


def md_text(nb) -> str:
    return "\n".join(c.source for c in nb.cells if c.cell_type == "markdown")


def code_text(nb) -> str:
    return "\n".join(c.source for c in nb.cells if c.cell_type == "code")


def has_heading(nb, needle: str) -> bool:
    return re.search(rf"^#+\s*\d*\.?\s*{re.escape(needle)}", md_text(nb), re.M | re.I) is not None


def count_bullets_under(nb, heading: str) -> int:
    md = md_text(nb)
    m = re.search(rf"^#+\s*\d*\.?\s*{re.escape(heading)}.*?$(.*?)(?=^#+\s|\Z)", md, re.M | re.S | re.I)
    if not m:
        return 0
    body = m.group(1)
    return len([ln for ln in body.splitlines() if re.match(r"^\s*(\d+\.|[-*])\s+\S", ln)])


def count_figures(nb) -> int:
    code = code_text(nb)
    # Count subplots/figure creations and show() calls; take the max as a conservative figure count.
    shows = len(re.findall(r"plt\.show\(\)|fig\.show\(\)", code))
    creates = len(re.findall(r"plt\.subplots\(|plt\.figure\(|px\.\w+\(|go\.Figure\(", code))
    return max(shows, creates)


def gate_results(nb, path: Path, gates: dict, execute: bool) -> list[tuple[str, bool, str]]:
    md = md_text(nb)
    code = code_text(nb)
    meta = nb.metadata.get("ml_mastery", {})
    visuals_min = int(meta.get("visuals_min", 7))
    out = []

    # G1 title cell
    first = nb.cells[0].source if nb.cells else ""
    ok = all(k in first for k in ["**Module**", "**Notebook**", "**Prerequisites**", "**Estimated time**", "**Priority band**"])
    out.append(("G1", ok, "title metadata present" if ok else "title cell missing one of Module/Notebook/Prerequisites/Estimated time/Priority band"))

    # G2 objectives
    n = count_bullets_under(nb, "Learning Objectives")
    ok = 3 <= n <= 5 and "_objective_" not in md
    out.append(("G2", ok, f"{n} objectives"))

    # G3 setup
    ok = "set_style" in code and re.search(r"SEED\s*=\s*42", code) is not None
    out.append(("G3", ok, "set_style + SEED=42" if ok else "setup cell incomplete"))

    # G4 registers
    missing = [r for r in REGISTERS if r not in md]
    out.append(("G4", not missing, "all registers" if not missing else f"missing {missing}"))

    # G5 visuals
    nfig = count_figures(nb)
    out.append(("G5", nfig >= visuals_min, f"{nfig}/{visuals_min} figures"))

    # G6 failure modes
    ok = has_heading(nb, "Failure Modes")
    out.append(("G6", ok, "present" if ok else "no 'Failure Modes' heading"))

    # G7 RFI
    ok = has_heading(nb, "Results, Findings & Implications") and all(b in md for b in RFI_BLOCKS)
    placeholders = any(p in md for p in ["_table or figure summarising", "_patterns, surprises_", "_when to use, when to avoid_"])
    out.append(("G7", ok and not placeholders, "RFI complete" if ok and not placeholders else "RFI missing or still placeholder"))

    # G8 clinical reading
    ok = has_heading(nb, "Clinical Reading") and "_What this result means" not in md
    out.append(("G8", ok, "present" if ok else "Clinical Reading missing or placeholder"))

    # G9 connections
    ok = has_heading(nb, "Connections")
    out.append(("G9", ok, "present" if ok else "no 'Connections' heading"))

    # G10 takeaways
    n = count_bullets_under(nb, "Key Takeaways")
    out.append(("G10", 3 <= n <= 5, f"{n} takeaways"))

    # G11 imports
    bad = re.findall(r"^\s*(?:from|import)\s+(\d{2}_\w+)", code, re.M)
    out.append(("G11", not bad, "no cross-notebook imports" if not bad else f"imports {bad}"))

    # G12 execute (optional)
    if execute:
        r = subprocess.run(
            [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute",
             "--ExecutePreprocessor.timeout=600", "--output", "/tmp/_validate_out.ipynb", str(path)],
            capture_output=True, text=True, cwd=ROOT,
        )
        out.append(("G12", r.returncode == 0, "executes clean" if r.returncode == 0 else r.stderr.strip().splitlines()[-1][:120]))
    return out


def validate_one(path: Path, gates: dict, execute: bool, quiet: bool = False) -> bool:
    nb = nbformat.read(path, as_version=4)
    results = gate_results(nb, path, gates, execute)
    passed = all(ok for _, ok, _ in results)
    if not quiet:
        rel = path.relative_to(ROOT)
        print(f"\n{'PASS' if passed else 'FAIL'}  {rel}")
        for g, ok, why in results:
            print(f"  {'✓' if ok else '✗'} {g:<4} {why}")
    return passed


def is_stub(path: Path) -> bool:
    nb = nbformat.read(path, as_version=4)
    return nb.metadata.get("ml_mastery", {}).get("status") == "stub" and "_objective_" in md_text(nb)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="notebook path or module directory")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--execute", action="store_true", help="also run each notebook (G12)")
    ap.add_argument("--built-only", action="store_true", help="skip untouched stubs")
    args = ap.parse_args()

    with MANIFEST.open() as f:
        gates = yaml.safe_load(f)["gates"]

    if args.all:
        paths = sorted(p for p in ROOT.glob("[0-9][0-9]_*/**/*.ipynb") if ".ipynb_checkpoints" not in p.parts)
    elif args.target:
        t = ROOT / args.target
        paths = [t] if t.suffix == ".ipynb" else sorted(t.glob("**/*.ipynb"))
    else:
        ap.print_help()
        return 2

    if args.built_only:
        paths = [p for p in paths if not is_stub(p)]

    results = [validate_one(p, gates, args.execute) for p in paths]
    n_pass = sum(results)
    print(f"\n{n_pass}/{len(results)} notebooks pass all gates")
    return 0 if n_pass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
