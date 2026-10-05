"""Offline refusal tests for bd_population_pull_e3.py `pull`. No network, no boto3, no Black Diamond call: build_plan is
stubbed, and sys.modules entries for bd_adapter and boto3 are replaced by tripwires that fail the test if `pull` reaches them."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "bd_population_pull_e3.py"


def _load(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("bd_population_pull_e3_under_test", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "HERE", tmp_path)

    class Tripwire:
        def __getattr__(self, name):
            raise AssertionError("pull reached the network layer (%s) before a refusal" % name)

    monkeypatch.setitem(sys.modules, "bd_adapter", Tripwire())
    monkeypatch.setitem(sys.modules, "boto3", Tripwire())
    return mod


def _plan(sha="aaa"):
    return {"word": "66f1e98e98 card 2", "dry_run": 1, "vendor_calls": 0, "accounts_total": 1, "mapped": 1, "unmapped": [],
            "requests": 1, "request_bodies_sha256": sha, "request_list": [{"account": "0000000001"}]}


def _ruling(tmp_path):
    (tmp_path / "E3_SHAPE_RULING.json").write_text(
        json.dumps({"ruling_id": "batch-245", "pace_rps": 2, "abort_rule": "first non-transient error"}), encoding="utf-8")


def test_pull_refuses_without_go(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    _ruling(tmp_path)
    with pytest.raises(SystemExit) as e:
        mod.main(["x", str(tmp_path), "pull"])
    assert "--go" in str(e.value)


def test_pull_refuses_when_written_plan_hash_differs(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    _ruling(tmp_path)
    (tmp_path / "BD_POPULATION_PLAN_E3.json").write_text(json.dumps(_plan("aaa")), encoding="utf-8")
    monkeypatch.setattr(mod, "build_plan", lambda root: _plan("bbb"))
    with pytest.raises(SystemExit) as e:
        mod.main(["x", str(tmp_path), "pull", "--go"])
    assert "hash differs" in str(e.value)


def test_pull_refuses_a_second_pull_when_a_record_exists(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    _ruling(tmp_path)
    (tmp_path / "BD_POPULATION_PULL_E3.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(mod, "build_plan", lambda root: pytest.fail("rebuilt the plan before the second-pull refusal"))
    with pytest.raises(SystemExit) as e:
        mod.main(["x", str(tmp_path), "pull", "--go"])
    assert "no second pull" in str(e.value)


def test_pull_refuses_without_the_shape_ruling_file(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    (tmp_path / "BD_POPULATION_PLAN_E3.json").write_text(json.dumps(_plan()), encoding="utf-8")
    monkeypatch.setattr(mod, "build_plan", lambda root: pytest.fail("rebuilt the plan before the ruling refusal"))
    with pytest.raises(SystemExit) as e:
        mod.main(["x", str(tmp_path), "pull", "--go"])
    assert "E3_SHAPE_RULING.json" in str(e.value) and "ruling" in str(e.value)


def test_pull_refuses_a_ruling_file_that_names_no_pace(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    (tmp_path / "E3_SHAPE_RULING.json").write_text(json.dumps({"ruling_id": "batch-245"}), encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        mod.main(["x", str(tmp_path), "pull", "--go"])
    assert "pace_rps" in str(e.value)
