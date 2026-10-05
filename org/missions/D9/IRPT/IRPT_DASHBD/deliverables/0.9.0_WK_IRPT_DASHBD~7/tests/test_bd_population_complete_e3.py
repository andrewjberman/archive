"""Offline tests for bd_population_complete_e3.py: the complement, the landed set, the re-mint cadence, the denominators and the
--go refusal. No network, no Black Diamond call, no credential: boto3 and the estate helpers are stubs, and a refusal test
replaces both module entries with tripwires."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "bd_population_complete_e3.py"


def _load():
    spec = importlib.util.spec_from_file_location("bd_population_complete_e3_under_test", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class StubOn:
    @staticmethod
    def address(*parts, object=None):
        return "s3://bkt/" + "/".join(parts) + "/" + object


class StubB20:
    TRANSIENT_HTTP = (429, 502, 503, 504)

    @staticmethod
    def _address(on, pull, acct_id):
        return on.address("bd", "49f", "bronze", "rp", "pull=" + pull, object="acct=%s.json" % acct_id)


class StubS3:
    def __init__(self, keys=()):
        self.keys = list(keys)
        self.put = []

    def get_paginator(self, name):
        outer = self

        class P:
            def paginate(self, Bucket, Prefix):
                yield {"Contents": [{"Key": k} for k in outer.keys]}
        return P()

    def put_object(self, Bucket, Key, Body, ContentType):
        self.put.append(Key)


class StubHelpers:
    """Counts the mints; a script that scripted statuses by call index can inject errors."""

    def __init__(self, script=None):
        self.mints = 0
        self.sessions = 0
        self.requested = []
        self.tokens = []
        self.script = script or {}

    def load_bd_session(self):
        self.sessions += 1
        return "cookie-stub"

    def get_clientview_token(self, cookie):
        self.mints += 1
        return "token-%d" % self.mints

    def _request(self, method, path, token, body, raw):
        n = len(self.requested)
        self.requested.append(body["id"])
        self.tokens.append(token)
        if n in self.script:
            raise RuntimeError("HTTP %d: stub" % self.script[n])
        return b'{"ok": true}'


def _e20(n):
    reqs = [{"account": "%010d" % i, "bd_account": str(1000 + i), "segments": [{}], "body": {"id": 1000 + i}} for i in range(n)]
    return {"word": "w", "request_list": reqs, "request_bodies_sha256": "abc",
            "route": {"paths": {"performancePeriod": "/p"}}}


def _keys(ids):
    return ["bkt/bd/49f/bronze/rp/pull=20261004/acct=%s.json" % i for i in ids] + ["bkt/bd/49f/bronze/rp/pull=20261004/other.txt"]


def _run(mod, e20, landed, h, ruling=None):
    plan = mod.derive_plan(e20, landed)
    s3 = StubS3()
    rec = mod.run_complement(e20, plan, h, s3, StubOn, StubB20, ruling or {"pace_rps": 2.0, "ruling_id": "r"},
                             sleep=lambda s: None, clock=lambda: 0.0)
    return plan, rec, s3


def test_complement_excludes_every_landed_account():
    mod = _load()
    s3 = StubS3(_keys([1001, 1003, 1005]))
    landed = mod.list_landed(s3, StubOn, StubB20)
    assert landed == {"1001", "1003", "1005"}  # only acct=<id>.json keys count
    plan = mod.derive_plan(_e20(8), landed)
    assert plan["landed"] == 3 and plan["complement"] == 5
    assert plan["landed"] + plan["complement"] == plan["requests_planned"] == 8
    assert not set(plan["complement_accounts"]) & set(plan["landed_accounts"])
    assert plan["vendor_calls"] == 0 and plan["dry_run"] == 1


def test_a_landed_account_is_never_requested():
    mod = _load()
    h = StubHelpers()
    plan, rec, s3 = _run(mod, _e20(8), {"1001", "1003", "1005"}, h)
    assert sorted(h.requested) == [1000, 1002, 1004, 1006, 1007]
    assert not {1001, 1003, 1005} & set(h.requested)
    assert len(h.requested) == len(set(h.requested)) == plan["complement"]
    assert rec["landed_this_run"] == 5 and rec["aborted"] is None
    assert len(s3.put) == 5 and all("1001" not in k and "1003" not in k for k in s3.put)


def test_the_bearer_is_re_minted_every_10_calls():
    mod = _load()
    h = StubHelpers()
    _plan, rec, _s3 = _run(mod, _e20(35), set(), h)
    assert len(h.requested) == 35
    assert h.mints == rec["session_token_mints"] == 4  # calls 1, 11, 21, 31
    assert h.sessions == h.mints  # every mint is a fresh sign-in through load_bd_session
    for i in range(35):  # no token ever signs more than 10 calls
        assert h.tokens[i] == "token-%d" % (i // 10 + 1)


def test_both_denominators_are_printed(capsys):
    mod = _load()
    plan = mod.derive_plan(_e20(6), {"1000", "1002"})
    mod.print_denominators(plan)
    out = capsys.readouterr().out
    assert "denominators: planned 6 = landed 2 + complement 4" in out
    assert "complement accounts 4" in out and "landed accounts 2" in out


def test_run_refuses_without_go(tmp_path, monkeypatch):
    mod = _load()

    class Tripwire:
        def __getattr__(self, name):
            raise AssertionError("run reached the network layer (%s) before a refusal" % name)

    monkeypatch.setitem(sys.modules, "bd_adapter", Tripwire())
    monkeypatch.setitem(sys.modules, "boto3", Tripwire())
    (tmp_path / mod.COMPLETION_PLAN_NAME).write_text("{}", encoding="utf-8")
    (tmp_path / "E3_SHAPE_RULING.json").write_text(json.dumps({"pace_rps": 2}), encoding="utf-8")
    with pytest.raises(SystemExit, match="run --go"):
        mod.refusal_checks(tmp_path, tmp_path, ["x", ".", "run"])
    with pytest.raises(SystemExit, match="run --go"):
        mod.refusal_checks(tmp_path, tmp_path, ["x", ".", "plan", "--go"])
    plan, ruling = mod.refusal_checks(tmp_path, tmp_path, ["x", ".", "run", "--go"])
    assert ruling["pace_rps"] == 2


def test_run_refuses_without_the_plan_or_the_ruling(tmp_path):
    mod = _load()
    with pytest.raises(SystemExit, match="no completion plan"):
        mod.refusal_checks(tmp_path, tmp_path, ["x", ".", "run", "--go"])
    (tmp_path / mod.COMPLETION_PLAN_NAME).write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit, match="E3_SHAPE_RULING"):
        mod.refusal_checks(tmp_path, tmp_path, ["x", ".", "run", "--go"])


def test_a_401_directly_after_a_fresh_mint_is_a_stop_not_a_retry():
    mod = _load()
    h = StubHelpers(script={0: 401})
    _plan, rec, _s3 = _run(mod, _e20(5), set(), h)
    assert len(h.requested) == 1 and rec["aborted"] == "HTTP 401" and "fresh mint" in rec["stop_reason"]
    assert rec["retries_used"] == 0


def test_one_transient_retry_then_abort_on_first_non_transient():
    mod = _load()
    h = StubHelpers(script={1: 503, 2: 503})
    _plan, rec, _s3 = _run(mod, _e20(6), set(), h)
    assert rec["retries_used"] == 1 and rec["aborted"] == "HTTP 503"
    assert len(h.requested) == 3  # account 0; account 1 twice (the one retry); the second 503 aborts
