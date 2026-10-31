#!/usr/bin/env python3
"""manifest.py — the one loader for curriculum/curriculum.yaml. It refuses what it does not understand.

Every notebook entry is checked and nothing is defaulted. Refused, each naming the notebook id and the field:
  - a field outside REQUIRED ∪ OPTIONAL, or a REQUIRED field that is missing
  - goal outside predict|explain|decide · band outside P1–P5 · gds outside 1–6
  - a study: or refs: key absent from library/curated.yaml
  - a dataset datasets/__init__.py does not export (`def load_<name>`, or a submodule such as `synthetic`)
  - a duplicate id NN.MM.KK
All problems are reported together.

    from manifest import ManifestError, load_manifest
    manifest = load_manifest()            # the parsed YAML, unchanged, once it has passed
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "curriculum" / "curriculum.yaml"
LIBRARY = ROOT / "library" / "curated.yaml"
DATASETS = ROOT / "datasets" / "__init__.py"

REQUIRED = {"n", "title", "band", "goal", "gds", "subject", "dataset", "visuals", "experiments"}
OPTIONAL = {"study", "refs", "build"}
GOALS = ("predict", "explain", "decide")
BANDS = ("P1", "P2", "P3", "P4", "P5")


class ManifestError(ValueError):
    pass


def exported_datasets(init: Path = DATASETS) -> set[str]:
    """Names datasets/__init__.py exports, read from its source without importing it."""
    tree = ast.parse(init.read_text())
    names = {n.name[len("load_"):] for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("load_")}
    names |= {a.asname or a.name for n in tree.body if isinstance(n, ast.ImportFrom) and n.level == 1 and not n.module for a in n.names}
    return names


def problems(manifest: dict, library: dict, datasets: set[str]) -> list[str]:
    out, seen = [], set()
    for m in manifest["modules"]:
        for ti, t in enumerate(m["topics"], 1):
            for e in t["notebooks"]:
                nid = f"{m['id']}.{ti:02d}.{e['n']:02d}" if isinstance(e.get("n"), int) else f"{m['id']}.{ti:02d}.?"

                def bad(field, why):
                    out.append(f"{nid}: {field} — {why}")

                for f in sorted(set(e) - REQUIRED - OPTIONAL):
                    bad(f, "unknown field")
                for f in sorted(REQUIRED - set(e)):
                    bad(f, "missing (no default is inferred)")
                if "goal" in e and e["goal"] not in GOALS:
                    bad("goal", f"{e['goal']!r} is not one of {'|'.join(GOALS)}")
                if "band" in e and e["band"] not in BANDS:
                    bad("band", f"{e['band']!r} is outside P1–P5")
                if "gds" in e and not (type(e["gds"]) is int and 1 <= e["gds"] <= 6):
                    bad("gds", f"{e['gds']!r} is outside 1–6")
                if "study" in e and e["study"] not in library:
                    bad("study", f"{e['study']!r} is not a key in library/curated.yaml")
                for k in e.get("refs", []):
                    if k not in library:
                        bad("refs", f"{k!r} is not a key in library/curated.yaml")
                if "dataset" in e and e["dataset"] not in datasets:
                    bad("dataset", f"{e['dataset']!r} is not exported by datasets/__init__.py")
                if "n" in e and not (type(e["n"]) is int and e["n"] >= 1):
                    bad("n", f"{e['n']!r} is not a positive integer")
                if "visuals" in e and not (type(e["visuals"]) is int and e["visuals"] >= 1):
                    bad("visuals", f"{e['visuals']!r} is not a positive integer")
                if "experiments" in e and not (isinstance(e["experiments"], list) and all(isinstance(x, str) for x in e["experiments"])):
                    bad("experiments", "is not a list of strings")
                if "build" in e and e["build"] != "last":
                    bad("build", f"{e['build']!r} — the only value is 'last'")
                if nid in seen:
                    bad("n", "duplicate id")
                seen.add(nid)
    return out


def load_manifest(path: Path = MANIFEST, library: Path = LIBRARY, datasets_init: Path = DATASETS) -> dict:
    manifest = yaml.safe_load(Path(path).read_text())
    found = problems(manifest, yaml.safe_load(Path(library).read_text()) or {}, exported_datasets(Path(datasets_init)))
    if found:
        raise ManifestError(f"{Path(path).name}: {len(found)} problem(s)\n" + "\n".join(f"  {p}" for p in found))
    return manifest


if __name__ == "__main__":
    try:
        load_manifest()
    except ManifestError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    print("manifest: ok")
