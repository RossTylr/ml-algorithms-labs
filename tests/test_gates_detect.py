"""H12 — every gate fails on its planted defect. A scaffold stub is filled just enough to pass every static gate,
one defect is injected, and the gate function in scripts/validate.py must fail with that gate — and only that gate —
named. 00.01.01, the built notebook, is the positive control (G12 for it runs in the `execute` tier)."""
import os, sys
import nbformat
import pytest
import yaml
from nbformat.v4 import new_code_cell, new_markdown_cell
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import scaffold, validate  # noqa: E402

MAN = yaml.safe_load(open(os.path.join(ROOT, "curriculum", "curriculum.yaml")))
BUILT = os.path.join(ROOT, "00_mathematical_foundations/01_linear_algebra/01_vectors_matrices_operations.ipynb")


def _gates(nb, path):
    return {g: (ok, why) for g, ok, why in validate.gate_results(nb, path, MAN["gates"], False)}


def _failing(nb, path):
    return {g for g, (ok, _) in _gates(nb, path).items() if not ok}


def _minimal():
    """The scaffold stub for 00.01.01, every placeholder a static gate checks filled with the least that passes."""
    m = MAN["modules"][0]; t = dict(m["topics"][0], idx=1)
    e = dict(t["notebooks"][0]); e["slug"] = scaffold.slugify(e["title"])
    nb = scaffold.stub_notebook(m, t, e, MAN["meta"], MAN["priority_bands"], scaffold.load_library())
    fill = {
        "_objective_": "## Learning Objectives\n\n1. Read a panel as a vector\n2. Compare two patients\n3. Spot a redundant test",
        "_table or figure summarising": "## 8. Results, Findings & Implications\n\n### 📊 Results\n\nA table.\n\n### 🔍 Findings\n\nA finding.\n\n"
                                        "### 💡 Implications\n\nAn implication.\n\n### ⚠️ Considerations\n\n- **Assumptions**: stated",
        "_What this result means": "## 9. Clinical Reading\n\nWhat a clinician does differently; what they must not conclude.",
        "## 11. Key Takeaways": "## 11. Key Takeaways\n\n1. One\n2. Two\n3. Three",
    }
    for c in nb.cells:
        for needle, text in fill.items():
            if c.cell_type == "markdown" and needle in c.source:
                c.source = text
    code = [c for c in nb.cells if c.cell_type == "code"]
    code[1].source += "\n".join(["fig, ax = plt.subplots()"] * nb.metadata["ml_mastery"]["visuals_min"])
    code[2].source = "# CENTRAL\n" + code[2].source
    return nb


@pytest.fixture
def minimal(tmp_path):
    p = tmp_path / "minimal.ipynb"
    nbformat.write(_minimal(), p)
    return p


def _inject(path, change):
    nb = nbformat.read(path, as_version=4)
    change(nb)
    out = path.with_name(f"defect_{path.stem}.ipynb"); nbformat.write(nb, out)
    return nbformat.read(out, as_version=4), out


def _md(nb, needle):
    return next(c for c in nb.cells if c.cell_type == "markdown" and needle in c.source)


def _code(nb, needle):
    return next(c for c in nb.cells if c.cell_type == "code" and needle in c.source)


def _before_failure_modes(nb, cell):
    nb.cells.insert(nb.cells.index(_md(nb, "Failure Modes")), cell)


DEFECTS = {
    "G2 objective placeholder left in": ("G2", lambda nb: setattr(_md(nb, "Learning Objectives"), "source", _md(nb, "Learning Objectives").source.replace("3. Spot a redundant test", "3. _objective_"))),
    "G3 SEED = 7": ("G3", lambda nb: setattr(_code(nb, "SEED"), "source", _code(nb, "SEED").source.replace("SEED = 42", "SEED = 7"))),
    "G4 concept section without Technical": ("G4", lambda nb: setattr(_md(nb, "## 2. What Is"), "source", _md(nb, "## 2. What Is").source.split("🔬")[0])),
    "G11 import of another notebook": ("G11", lambda nb: _before_failure_modes(nb, new_code_cell("from 04_regression.01_simple_linear import fit_ols"))),
    "G13 abstention reason under 25 chars": ("G13", lambda nb: _before_failure_modes(nb, new_markdown_cell("⛔ Abstention — rank-deficient panels (redundant tests) — no time"))),
    "G13 abstention with a VAGUE reason": ("G13", lambda nb: _before_failure_modes(nb, new_markdown_cell("⛔ Abstention — scaling the panel changes the geometry — this is out of scope for the notebook as written"))),
    "G14 unregistered experiment heading": ("G14", lambda nb: _before_failure_modes(nb, new_markdown_cell("### Experiment 4: a bonus sweep nobody registered"))),
    "HC-12 two cells marked CENTRAL": ("HC-12", lambda nb: setattr(_code(nb, "VISUAL 1"), "source", "# CENTRAL\n" + _code(nb, "VISUAL 1").source)),
    "HC-12 no cell marked CENTRAL": ("HC-12", lambda nb: setattr(_code(nb, "# CENTRAL"), "source", _code(nb, "# CENTRAL").source.replace("# CENTRAL\n", ""))),
}


def test_minimal_stub_passes_every_static_gate(minimal):
    nb = nbformat.read(minimal, as_version=4)
    assert _failing(nb, minimal) == set(), _gates(nb, minimal)


@pytest.mark.parametrize("case", DEFECTS)
def test_gate_detects_its_defect(minimal, case):
    gate, change = DEFECTS[case]
    nb, path = _inject(minimal, change)
    assert _failing(nb, path) == {gate}, _gates(nb, path)


def test_built_00_01_01_passes_every_gate():
    nb = nbformat.read(BUILT, as_version=4)
    assert _failing(nb, BUILT) == set(), _gates(nb, BUILT)
    assert {"G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G13", "G14", "HC-12"} <= set(_gates(nb, BUILT))
