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
    python scripts/validate.py --all --built-only         # only notebooks with status "built"

Gates G1–G12 per curriculum.yaml. Added by the paper fold (slice 4):
  G13  every ⛔ Abstention block names the experiment and gives a specific reason (Kalai 2025: reward abstention over padding)
  G14  experiment headings are the manifest's pre-registered list; extras must say (exploratory)  (Box 1976; AlphaCodium)
  HC-12 exactly one code cell is marked # CENTRAL — the figure LITTLE_BOOK.md carries
G4 checks the three registers anywhere AND inside the `## 2. What Is …` concept section (HC-3).
  W1   figure titles that describe rather than state a finding — warning only (Knaflic)
Abstention format, in a markdown cell where the figure/finding would have been:
  ⛔ Abstention — <experiment name> — <reason, ≥25 chars, specific>
A specific abstention relieves one figure from G5 (max two per notebook).
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


ABSTAIN_LINE = re.compile(r"^⛔\s*Abstention\b.*$", re.M)
# separators: em dash or colon, or a hyphen with space either side — so "rank-deficient panels" is one experiment name
ABSTAIN_RE = re.compile(r"^⛔\s*Abstention(?:\s*[—:]\s*|\s+-\s+)(?P<exp>.+?)(?:\s*[—:]\s*|\s+-\s+)(?P<reason>.+)$")
VAGUE = re.compile(r"too (complex|hard|difficult)|out of scope|not enough time|beyond this notebook", re.I)


def abstentions(nb) -> list[tuple[str, str, bool]]:
    """(experiment, reason, specific?) for every ⛔ Abstention line. Specific = reason ≥25 chars and not a vague phrase;
    a line that does not parse into experiment and reason is not specific."""
    out = []
    for line in ABSTAIN_LINE.findall(md_text(nb)):
        m = ABSTAIN_RE.match(line)
        exp, reason = (m.group("exp").strip(), m.group("reason").strip()) if m else (line, "")
        out.append((exp, reason, len(reason) >= 25 and not VAGUE.search(reason)))
    return out


def concept_sections(nb) -> dict[str, str]:
    """heading → body for each `## 2. What Is …` section: the concept section HC-3 requires all three registers in."""
    return {m.group(1).strip(): m.group(2) for m in re.finditer(r"^##\s+(2\.[^\n]*|What Is[^\n]*)$(.*?)(?=^##\s|\Z)", md_text(nb), re.M | re.S)}


def experiment_headings(nb) -> list[str]:
    return [h.strip() for h in re.findall(r"^###\s*Experiment\s*\d+\s*:\s*(.+)$", md_text(nb), re.M)]


def exploratory(nb) -> list[str]:
    """Experiment headings not in the manifest's pre-registered list and not marked (exploratory)."""
    reg = [e.lower() for e in nb.metadata.get("ml_mastery", {}).get("experiments", [])]
    out = []
    for h in experiment_headings(nb):
        if "(exploratory)" in h.lower():
            continue
        if not any(h.lower().startswith(r[:40]) or r.startswith(h.lower()[:40]) for r in reg):
            out.append(h)
    return out


def descriptive_titles(nb) -> list[str]:
    """Figure titles that describe rather than state a finding — warn only."""
    titles = re.findall(r"set_title\(\s*[frb]?['\"]([^'\"]{6,})['\"]", code_text(nb)) + re.findall(r"suptitle\(\s*[frb]?['\"]([^'\"]{6,})['\"]", code_text(nb))
    bad = []
    for t in titles:
        words = t.lower().split()
        if (" vs " in f" {t.lower()} " or " by " in f" {t.lower()} ") and len(words) <= 6:
            bad.append(t)
    return bad


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

    # G4 registers — present in the notebook, and all three inside every concept section
    missing = [r for r in REGISTERS if r not in md]
    concept = concept_sections(nb)
    thin = {h: [r for r in REGISTERS if r not in body] for h, body in concept.items()}
    thin = {h: rs for h, rs in thin.items() if rs}
    why = (f"missing {missing}" if missing else "no '## 2. What Is' concept section" if not concept
           else f"concept section '{next(iter(thin))[:40]}' missing {next(iter(thin.values()))}" if thin else "all registers")
    out.append(("G4", not missing and bool(concept) and not thin, why))

    # G5 visuals — a specific abstention relieves one figure each (max two)
    abst = abstentions(nb)
    relief = min(2, sum(1 for _, _, ok in abst if ok))
    nfig = count_figures(nb)
    out.append(("G5", nfig >= visuals_min - relief, f"{nfig}/{visuals_min} figures" + (f" (−{relief} abstained)" if relief else "")))

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

    # G13 abstentions must be specific
    vague = [e for e, _, ok in abst if not ok]
    out.append(("G13", not vague, f"{len(abst)} abstention(s), all specific" if not vague else f"non-specific abstention for {vague}"))

    # G14 pre-registration: experiment headings ⊆ manifest list unless marked (exploratory)
    extra = exploratory(nb)
    out.append(("G14", not extra, "experiments match manifest" if not extra else f"unregistered: {extra[:2]}"))

    # HC-12 exactly one code cell marked # CENTRAL
    n = sum(1 for c in nb.cells if c.cell_type == "code" and "# CENTRAL" in c.source)
    out.append(("HC-12", n == 1, f"{n} cell(s) marked # CENTRAL"))

    # W1 figure titles (warning only, never fails)
    desc = descriptive_titles(nb)
    if desc:
        out.append(("W1", True, f"warn: descriptive titles {desc[:2]}"))

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
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        print(f"\n{'PASS' if passed else 'FAIL'}  {rel}")
        for g, ok, why in results:
            print(f"  {'✓' if ok else '✗'} {g:<4} {why}")
    return passed


def status(path: Path) -> str | None:
    return nbformat.read(path, as_version=4).metadata.get("ml_mastery", {}).get("status")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="notebook path or module directory")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--execute", action="store_true", help="also run each notebook (G12)")
    ap.add_argument("--built-only", action="store_true", help="only status built; blocked and stub are excluded")
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
        paths = [p for p in paths if status(p) == "built"]

    results = [validate_one(p, gates, args.execute) for p in paths]
    n_pass = sum(results)
    print(f"\n{n_pass}/{len(results)} notebooks pass all gates")
    return 0 if n_pass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
