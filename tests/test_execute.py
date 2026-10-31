"""G12 — every notebook with status built executes clean under nbconvert. Nightly tier (`execute`)."""
import json, os, subprocess, sys
import pytest
ROOT = os.path.join(os.path.dirname(__file__), "..")

def _built():
    out = []
    for d, _, files in sorted(os.walk(ROOT)):
        rel = os.path.relpath(d, ROOT)
        if not rel[:2].isdigit() or ".ipynb_checkpoints" in rel:
            continue
        for f in sorted(files):
            if f.endswith(".ipynb"):
                meta = json.load(open(os.path.join(d, f)))["metadata"].get("ml_mastery", {})
                if meta.get("status") == "built":
                    out.append(pytest.param(os.path.join(rel, f), id=meta["id"]))
    return out

@pytest.mark.execute
@pytest.mark.parametrize("path", _built())
def test_built_notebook_executes(path):
    r = subprocess.run([sys.executable, "scripts/validate.py", path, "--execute"], capture_output=True, text=True, cwd=ROOT)
    assert "✓ G12" in r.stdout, r.stdout[-2000:]
