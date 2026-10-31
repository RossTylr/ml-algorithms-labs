#!/usr/bin/env python3
"""
scaffold.py — Generate the repo tree, module READMEs and notebook stubs from curriculum/curriculum.yaml.

Idempotent: re-running never overwrites a notebook that already exists (built work is safe).
READMEs and INDEX.md are regenerated every run (they are derived artefacts).
The manifest is read through scripts/manifest.py, which refuses unknown or invalid fields rather than defaulting them.

Usage:
    python scripts/scaffold.py            # scaffold everything
    python scripts/scaffold.py --module 04
    python scripts/scaffold.py --dry-run
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nbformat
import yaml
from manifest import ManifestError, load_manifest
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parent.parent
LIBRARY = ROOT / "library" / "curated.yaml"
GOALS = {"predict": "Predict — the model's job is accuracy on unseen patients; coefficients are not mechanisms.",
         "explain": "Explain — the model's job is to say something true about the process; prediction is secondary.",
         "decide": "Decide — the model feeds an action; the cost of being wrong in each direction matters more than accuracy."}
GDS = {1: "Gathering, preparation, exploration", 2: "Representation and transformation", 3: "Computing with data",
       4: "Data modelling", 5: "Visualisation and presentation", 6: "Science about data science"}


def nb_path(module: dict, topic: dict, nb: dict) -> Path:
    return (
        ROOT
        / f"{module['id']}_{module['slug']}"
        / f"{topic['idx']:02d}_{topic['slug']}"
        / f"{nb['n']:02d}_{nb['slug']}.ipynb"
    )


def slugify(title: str) -> str:
    out = []
    for ch in title.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -/&,":
            out.append("_")
    s = "".join(out)
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")


def load_library() -> dict:
    return yaml.safe_load(LIBRARY.read_text()) if LIBRARY.exists() else {}


def stub_notebook(m: dict, t: dict, nb: dict, meta: dict, bands: dict, lib: dict | None = None) -> nbformat.NotebookNode:
    """The stub carries every gate-checked section with placeholders. Claude Code fills; validate.py checks."""
    band = nb["band"]
    band_name = bands[band]["name"]
    band_q = bands[band]["question"]
    prereqs = ", ".join(m["prereqs"]) or "None"
    experiments = nb["experiments"]
    lib = lib or {}
    study = nb.get("study")
    if study in lib:
        e = lib[study]
        study_line = f"**In the spirit of**: {e['authors']} ({e['year']}), *{e['title']}* — reproduce: {e.get('reproduce', '')}  \n"
    elif study:
        study_line = f"**In the spirit of**: {study}  \n"
    else:
        study_line = ""
    goal = nb["goal"]; gds = nb["gds"]
    goal_line = f"**Goal**: `{goal}` — {GOALS[goal]}  \n**GDS division**: {gds} {GDS[gds]}  \n"
    refs = [k for k in nb.get("refs", []) if k in lib]
    if study in lib and study not in refs:
        refs = [study] + refs
    ref_lines = "\n".join(f"- {lib[k]['authors']} ({lib[k]['year']}). *{lib[k]['title']}*. `library:{k}`" for k in refs) or "- "

    cells = [
        new_markdown_cell(
            f"# {nb['title']}\n\n"
            f"**Module**: {m['id']} {m['title']} · **Topic**: {t['title']} · **Notebook**: {nb['n']:02d}  \n"
            f"**Prerequisites**: {prereqs} · **Estimated time**: 60 min  \n"
            f"**Priority band**: {band} {band_name} — *{band_q}*  \n"
            f"{goal_line}"
            f"{study_line}"
            f"**Dataset**: `{nb['dataset']}`"
        ),
        new_markdown_cell(
            "## Learning Objectives\n\n"
            "By the end of this notebook you will be able to:\n\n"
            "1. _objective_\n2. _objective_\n3. _objective_"
        ),
        new_code_cell(
            "import numpy as np\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "import warnings\n"
            "warnings.filterwarnings('ignore')\n\n"
            "from shared.plotting import set_style, PALETTE\n"
            "from shared.explanation import rfi, clinical_reading, three_registers\n"
            f"from datasets import {meta_loader(nb['dataset'])}\n\n"
            "set_style()\n"
            f"SEED = {meta['seed']}\n"
            "np.random.seed(SEED)"
        ),
        new_markdown_cell(
            "---\n## 1. The Clinical Problem\n\n"
            f"🗣️ **Plain** — _{nb['subject']}_\n\n"
            "_Show the data before naming the method. Plot it. Let the reader see the problem._"
        ),
        new_code_cell("# VISUAL 1 — the raw clinical data\n"),
        new_markdown_cell(
            f"---\n## 2. What Is {nb['title']}?\n\n"
            "🗣️ **Plain**\n\n_analogy, no jargon_\n\n"
            "💻 **Developer**\n\n_pseudocode, API, complexity_\n\n"
            "🔬 **Technical**\n\n_formal definition, objective, assumptions_"
        ),
        new_markdown_cell("---\n## 3. Visual Intuition"),
        new_code_cell("# VISUAL 2 — concept diagram or step-through animation\n"),
        new_markdown_cell("---\n## 4. Implementation from Scratch"),
        new_code_cell("# NumPy implementation, heavily commented\n"),
        new_markdown_cell("---\n## 5. Library Implementation"),
        new_code_cell("# sklearn / torch / library version\n"),
        new_markdown_cell(
            "---\n## 6. Experiments & Variations\n\n"
            + "\n".join(f"### Experiment {i + 1}: {e}" for i, e in enumerate(experiments))
        ),
    ]
    for i, e in enumerate(experiments):
        cells.append(new_code_cell(f"# VISUAL {3 + i} — Experiment {i + 1}: {e}\n"))
        cells.append(new_markdown_cell("🗣️ _what changed, in plain terms_  \n🔬 _why, mathematically_"))
    cells += [
        new_markdown_cell("---\n## 7. Failure Modes & Edge Cases"),
        new_code_cell("# VISUAL — deliberately break the method; show what bad looks like and why\n"),
        new_markdown_cell(
            "---\n## 8. Results, Findings & Implications\n\n"
            "### 📊 Results\n\n_table or figure summarising all experiments_\n\n"
            "### 🔍 Findings\n\n_patterns, surprises_\n\n"
            "### 💡 Implications\n\n_when to use, when to avoid_\n\n"
            "### ⚠️ Considerations\n\n"
            "- **Assumptions**: \n- **Computational cost**: \n- **Scaling**: \n- **Common mistakes**: \n- **Ethics / safety**: "
        ),
        new_markdown_cell(
            "---\n## 9. Clinical Reading\n\n"
            f"_{band_q}_\n\n"
            "_What this result means at the bedside, in the clinic, or in the field. "
            "What a clinician would do differently having seen it. What they must not conclude from it._"
        ),
        new_markdown_cell(
            "---\n## 10. Connections\n\n- **Builds on**: \n- **Leads to**: \n- **Alternatives**: "
        ),
        new_markdown_cell("---\n## 11. Key Takeaways\n\n1. \n2. \n3. "),
        new_markdown_cell("---\n## References\n\n" + ref_lines),
    ]
    nbk = new_notebook(cells=cells)
    nbk.metadata["ml_mastery"] = {
        "id": f"{m['id']}.{t['idx']:02d}.{nb['n']:02d}",
        "band": band,
        "dataset": nb["dataset"],
        "visuals_min": nb["visuals"],
        "goal": goal, "gds": gds, "study": study, "refs": refs,
        "experiments": nb["experiments"],
        "build": nb.get("build"),
        "status": "stub",
    }
    nbk.metadata["kernelspec"] = {"display_name": "ml-algorithms-labs", "language": "python", "name": "ml-algorithms-labs"}
    return nbk


def meta_loader(dataset: str) -> str:
    if dataset == "synthetic":
        return "synthetic"
    return f"load_{dataset}"


def module_readme(m: dict, bands: dict) -> str:
    rows = []
    for t in m["topics"]:
        for nb in t["notebooks"]:
            p = f"{t['idx']:02d}_{t['slug']}/{nb['n']:02d}_{nb['slug']}.ipynb"
            rows.append(
                f"| {t['idx']:02d}.{nb['n']:02d} | [{nb['title']}]({p}) | {nb['band']} | {nb.get('goal','')} | `{nb['dataset']}` | {('`'+nb['study']+'`') if nb.get('study') else ''} | {nb['subject']} |"
            )
    table = "\n".join(rows)
    prereqs = ", ".join(m["prereqs"]) or "None"
    n = sum(len(t["notebooks"]) for t in m["topics"])
    return f"""# Module {m['id']} — {m['title']}

**Tier** {m['tier']} · **Notebooks** {n} · **Prerequisites** {prereqs}

> {m['purpose']}

## Notebooks

| # | Notebook | Band | Goal | Dataset | Study | Clinical problem |
|---|----------|------|------|---------|-------|------------------|
{table}

## Priority bands

{chr(10).join(f"- **{k}** {v['name']} — {v['question']}" for k, v in bands.items())}

## Conventions

Every notebook carries three explanation registers (plain, developer, technical), a minimum visual count, a failure-modes
section, a results / findings / implications / considerations block, and a clinical reading. Experiments are the manifest's
pre-registered list. `python scripts/validate.py {m['id']}_{m['slug']}` gates the module.
"""


def write_index(manifest: dict) -> None:
    lines = ["# Curriculum Index\n", "| Module | Title | Tier | Notebooks | Bands |", "|---|---|---|---|---|"]
    total = 0
    for m in manifest["modules"]:
        n = sum(len(t["notebooks"]) for t in m["topics"])
        total += n
        bands = sorted({nb["band"] for t in m["topics"] for nb in t["notebooks"]})
        lines.append(f"| {m['id']} | [{m['title']}]({m['id']}_{m['slug']}/README.md) | {m['tier']} | {n} | {' '.join(bands)} |")
    lines.append(f"\n**Total notebooks**: {total}")
    (ROOT / "INDEX.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", help="only this module id, e.g. 04")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    try:
        manifest = load_manifest()
    except ManifestError as e:
        print(e, file=sys.stderr)
        return 1
    lib = load_library()
    bands = manifest["priority_bands"]
    created = skipped = 0

    for m in manifest["modules"]:
        if args.module and m["id"] != args.module:
            continue
        for i, t in enumerate(m["topics"], 1):
            t["idx"] = i
            for nb in t["notebooks"]:
                nb["slug"] = slugify(nb["title"])
                p = nb_path(m, t, nb)
                if p.exists():
                    skipped += 1
                    continue
                if not args.dry_run:
                    p.parent.mkdir(parents=True, exist_ok=True)
                    nbformat.write(stub_notebook(m, t, nb, manifest["meta"], bands, lib), p)
                created += 1
        if not args.dry_run:
            (ROOT / f"{m['id']}_{m['slug']}" / "README.md").write_text(module_readme(m, bands))

    if not args.dry_run and not args.module:
        write_index(manifest)

    print(f"scaffold: {created} stubs created, {skipped} existing notebooks left untouched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
