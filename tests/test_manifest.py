"""R9 — the one manifest loader refuses what it does not understand, naming the notebook id and the field."""
import copy, os, sys
import pytest
import yaml
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from manifest import ManifestError, load_manifest  # noqa: E402

LIVE = yaml.safe_load(open(os.path.join(ROOT, "curriculum", "curriculum.yaml")))


def _first(man):
    return man["modules"][0]["topics"][0]["notebooks"][0]  # 00.01.01


def _load(tmp_path, change):
    man = copy.deepcopy(LIVE); change(man)
    p = tmp_path / "curriculum.yaml"; p.write_text(yaml.safe_dump(man, allow_unicode=True, sort_keys=False))
    return load_manifest(p)


def test_live_manifest_loads():
    assert load_manifest()["modules"]


def test_bad_goal_is_refused_by_id_and_field(tmp_path):
    with pytest.raises(ManifestError, match=r"00\.01\.01: goal — 'forecast' is not one of predict\|explain\|decide"):
        _load(tmp_path, lambda m: _first(m).update(goal="forecast"))


CASES = {
    "unknown field": (lambda m: _first(m).update(priority="high"), r"00\.01\.01: priority — unknown field"),
    "missing field": (lambda m: _first(m).pop("gds"), r"00\.01\.01: gds — missing"),
    "band": (lambda m: _first(m).update(band="P6"), r"00\.01\.01: band — 'P6' is outside P1–P5"),
    "gds": (lambda m: _first(m).update(gds=7), r"00\.01\.01: gds — 7 is outside 1–6"),
    "study": (lambda m: _first(m).update(study="Somebody et al. 2020"), r"00\.01\.01: study — 'Somebody et al\. 2020' is not a key"),
    "refs": (lambda m: _first(m).update(refs=["deisenroth2020", "nobody1999"]), r"00\.01\.01: refs — 'nobody1999' is not a key"),
    "dataset": (lambda m: _first(m).update(dataset="screenings"), r"00\.01\.01: dataset — 'screenings' is not exported"),
    "duplicate id": (lambda m: m["modules"][0]["topics"][0]["notebooks"].append(copy.deepcopy(_first(m))), r"00\.01\.01: n — duplicate id"),
}


@pytest.mark.parametrize("case", CASES)
def test_invalid_field_is_refused(tmp_path, case):
    change, msg = CASES[case]
    with pytest.raises(ManifestError, match=msg):
        _load(tmp_path, change)
