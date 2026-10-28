"""H11 — stigmergy: no agent file names another agent. H1 — next.py returns the first stub on a fresh scaffold."""
import os, re, shutil, subprocess, sys
ROOT = os.path.join(os.path.dirname(__file__), "..")

def test_h11_agents_do_not_name_each_other():
    agents = {f[:-3] for f in os.listdir(os.path.join(ROOT, ".claude", "agents")) if f.endswith(".md")}
    for a in agents:
        body = open(os.path.join(ROOT, ".claude", "agents", f"{a}.md")).read().split("---", 2)[-1]
        for other in agents - {a}:
            assert not re.search(rf"\b{other}\b", body, re.I), f"{a}.md names {other}"

def test_h1_next_is_first_stub(tmp_path):
    # a fresh scaffold, not the live tree (where 00.01.01 is already built)
    for d in ("scripts", "curriculum"):
        shutil.copytree(os.path.join(ROOT, d), tmp_path / d)
    subprocess.run([sys.executable, "scripts/scaffold.py", "--module", "00"], capture_output=True, cwd=tmp_path, check=True)
    out = subprocess.run([sys.executable, "scripts/next.py"], capture_output=True, text=True, cwd=tmp_path).stdout.strip()
    assert out.endswith("00_mathematical_foundations/01_linear_algebra/01_vectors_matrices_operations.ipynb")

def test_little_book_runs_on_empty_repo():
    r = subprocess.run([sys.executable, "scripts/little_book.py"], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0 and os.path.exists(os.path.join(ROOT, "LITTLE_BOOK.md"))
