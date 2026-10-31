#!/usr/bin/env python3
"""little_book.py — stitch every built notebook's 🗣️ Plain paragraph (section 2) and its # CENTRAL figure caption
into LITTLE_BOOK.md, in manifest build order. One idea, one figure per page (Fleuret, 2024).
Runs on an empty repo (produces a valid, short book). Regenerate after every build."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import nbformat
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "LITTLE_BOOK.md"


def plain_paragraph(nb) -> str | None:
    """The 🗣️ paragraph of section 2 (first markdown cell headed '## 2.')."""
    for c in nb.cells:
        if c.cell_type == "markdown" and re.search(r"^##\s*2\.", c.source, re.M):
            m = re.search(r"🗣️\s*\*\*Plain\*\*\s*\n+(.+?)(?=\n\s*💻|\Z)", c.source, re.S)
            if m:
                txt = m.group(1).strip()
                return None if txt.startswith("_") else txt  # still a placeholder
    return None


def central_figure(nb) -> str | None:
    """Caption from the code cell marked # CENTRAL: the first set_title/suptitle string in it."""
    for c in nb.cells:
        if c.cell_type == "code" and "# CENTRAL" in c.source:
            m = re.search(r"(?:set_title|suptitle)\(\s*[frb]?['\"]([^'\"]+)['\"]", c.source)
            return m.group(1) if m else "(central figure)"
    return None


def main() -> int:
    man = yaml.safe_load((ROOT / "curriculum" / "curriculum.yaml").read_text())
    mods = sorted(man["modules"], key=lambda m: (m["tier"], float(m.get("order", m["id"]))))
    pages, n_built = [], 0
    for m in mods:
        mod_pages = []
        for i, t in enumerate(m["topics"], 1):
            for nb_spec in t["notebooks"]:
                slug = "".join(ch if ch.isalnum() else "_" for ch in nb_spec["title"].lower())
                slug = re.sub(r"_+", "_", slug).strip("_")
                p = ROOT / f"{m['id']}_{m['slug']}" / f"{i:02d}_{t['slug']}" / f"{nb_spec['n']:02d}_{slug}.ipynb"
                if not p.exists():
                    continue
                nb = nbformat.read(p, as_version=4)
                if nb.metadata.get("ml_mastery", {}).get("status") not in ("built", "accepted"):
                    continue
                n_built += 1
                para = plain_paragraph(nb) or "_(plain paragraph not yet written — teach-back pending)_"
                fig = central_figure(nb)
                mod_pages.append(f"### {nb_spec['title']}\n\n{para}\n\n" + (f"> 📈 *{fig}*\n\n" if fig else "") + f"<sub>{nb_spec['band']} · {nb_spec.get('goal','')} · `{p.relative_to(ROOT)}`</sub>\n")
        if mod_pages:
            pages.append(f"## {m['id']} — {m['title']}\n\n" + "\n".join(mod_pages))
    head = f"# The Little Book of Clinical ML\n\n*One idea and one figure per page. Generated from {n_built} built notebooks; regenerated on every build.*\n\n"
    OUT.write_text(head + ("\n".join(pages) if pages else "_Nothing built yet. Run `/build-next`._\n"))
    print(f"little_book: {n_built} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
