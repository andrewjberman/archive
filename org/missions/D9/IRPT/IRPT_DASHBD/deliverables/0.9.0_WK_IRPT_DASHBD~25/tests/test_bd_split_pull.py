"""Offline tests for bd_split_pull.py: the split ranges, one call per account, the new-pull refusal, the --go refusals (run and sweep), the
widened-plan refusal and the denominators. No network, no Black Diamond call, no credential: boto3, the estate helpers, the clock and
sleep are stubs or are never reached."""
import importlib.util
import json
import threading
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "bd_split_pull.py"


def _load():
    spec = importlib.util.spec_from_file_location("bd_split_pull_under_test", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = _load()
B20 = M.load_b20()
CONC = M.load_conc()


class StubOn:
    @staticmethod
    def address(*parts, object=None):
        return "s3://bkt/" + "/".join(parts) + "/" + object


class StubAdapter:
    @staticmethod
    def build_period_request(bd, start, end, s2, year, method):
        return {"parameters": {"accountFilters": {"accounts": [bd]}, "asOfDate": {"asOfDate": "x"}, "dateRanges": []}}, 0


def _rows(n=3):
    return [{"account": "%010d" % (100 + i), "segment": {"start": "2024-07-09", "end": "2026-10-01"}} for i in range(n)]


def _xref(n=3):
    return {"%010d" % (100 + i): ["z01%d" % (1000 + i)] for i in range(n)}


def _plan(rows=None, xref=None, existing=("20261004",), pull="split20261007"):
    rows = _rows() if rows is None else rows
    xref = _xref() if xref is None else xref
    return M.derive_plan(rows, xref, "xref/key", list(existing), pull, StubOn, B20, StubAdapter, {"paths": {"performancePeriod": "/p"}})


def test_each_request_carries_the_two_split_ranges():
    plan = _plan()
    for q in plan["request_list"]:
        assert q["ranges"] == [{"start": "2024-07-09", "end": "2025-01-08"}, {"start": "2025-01-10", "end": "2026-10-01"}]
        assert [(d["startDate"], d["endDate"]) for d in q["body"]["parameters"]["dateRanges"]] == [
            ("2024-07-09", "2025-01-08"), ("2025-01-10", "2026-10-01")]
    assert plan["range_count"] == 2 * len(plan["request_list"])


def test_one_call_per_account_and_no_account_twice():
    plan = _plan()
    accts = [q["account"] for q in plan["request_list"]]
    assert len(accts) == len(set(accts)) == 3
    with pytest.raises(SystemExit):
        _plan(rows=_rows(2) + [_rows(1)[0]], xref=_xref(2))


def test_two_accounts_on_one_bd_id_are_unmapped_never_guessed():
    xref = {"%010d" % 100: ["z011000"], "%010d" % 101: ["z011000"], "%010d" % 102: ["z011002"]}
    plan = _plan(xref=xref)
    assert [q["account"] for q in plan["request_list"]] == ["%010d" % 102]
    assert len(plan["unmapped"]) == 2 and plan["record_rows"] == 3 and plan["planned"] == 1


def test_landing_keys_are_builder_output_under_the_new_pull():
    plan = _plan()
    for q in plan["request_list"]:
        assert q["landing_key"] == B20._address(StubOn, "split20261007", q["bd_account"])
        assert "pull=split20261007" in q["landing_key"]


def test_plan_refuses_a_pull_token_already_landed():
    with pytest.raises(SystemExit):
        _plan(existing=("20261004", "split20261007"))
    with pytest.raises(SystemExit):
        _plan(existing=("pull=split20261007",))


def test_run_and_sweep_refuse_without_go():
    for mode in ("run", "sweep"):
        with pytest.raises(SystemExit) as e:
            M.refusal_checks(Path("."), ["x", ".", mode], mode, CONC)
        assert "--go" in str(e.value)
        with pytest.raises(SystemExit):
            M.main(["x", ".", mode])


def test_run_refuses_a_plan_whose_counts_are_not_2299_and_4598(tmp_path):
    plan = _plan()
    plan["ruling"] = CONC.RULING
    (tmp_path / M.PLAN_NAME).write_text(json.dumps(plan), encoding="utf-8")
    for mode in ("run", "sweep"):
        with pytest.raises(SystemExit) as e:
            M.refusal_checks(tmp_path, ["x", ".", mode, "--go"], mode, CONC)
        assert "2299" in str(e.value)
    wide = _plan(rows=_rows(2300), xref=_xref(2300))  # a widened plan: 2,300 requests, 4,600 ranges
    with pytest.raises(SystemExit):
        M.check_plan_counts(wide)


def test_the_right_sized_plan_passes_the_count_check_and_the_ruling_must_match(tmp_path):
    rows = [{"account": "%010d" % (100 + i), "segment": {"start": "2024-07-09", "end": "2026-10-01"}} for i in range(M.EXPECTED_REQUESTS)]
    xref = {"%010d" % (100 + i): ["z01%d" % (100000 + i)] for i in range(M.EXPECTED_REQUESTS)}
    plan = _plan(rows=rows, xref=xref)
    M.check_plan_counts(plan)
    assert (len(plan["request_list"]), plan["range_count"]) == (2299, 4598)
    (tmp_path / M.PLAN_NAME).write_text(json.dumps(plan), encoding="utf-8")  # no ruling object
    with pytest.raises(SystemExit) as e:
        M.refusal_checks(tmp_path, ["x", ".", "run", "--go"], "run", CONC)
    assert "ruling" in str(e.value)
    plan["ruling"] = CONC.RULING
    (tmp_path / M.PLAN_NAME).write_text(json.dumps(plan), encoding="utf-8")
    assert M.refusal_checks(tmp_path, ["x", ".", "run", "--go"], "run", CONC)["pull"] == "split20261007"


def test_both_denominators_are_printed(capsys):
    M.print_denominators(_plan(xref={"%010d" % 100: ["z011000"]}))
    out = capsys.readouterr().out
    assert "denominators: record rows 3 = planned 1 + unmapped 2" in out
    assert "requests 1, ranges 2" in out


def test_existing_pull_prefixes_are_listed_from_s3_common_prefixes():
    class Pager:
        def paginate(self, **kw):
            assert kw["Delimiter"] == "/" and kw["Prefix"].endswith("reporting_performance/")
            return [{"CommonPrefixes": [{"Prefix": kw["Prefix"] + "pull=20261004/"}, {"Prefix": kw["Prefix"] + "pull=20261003/"}]}]

    class S3:
        def get_paginator(self, name):
            assert name == "list_objects_v2"
            return Pager()

    assert M.list_existing_pulls(S3(), StubOn, B20) == ["20261003", "20261004"]


def test_the_coordinator_lands_each_split_call_at_its_plan_landing_key():
    plan = _plan()
    plan["ruling"] = dict(CONC.RULING, ramp_after_s=10 ** 9)
    todo = [dict(q, segments=q["ranges"]) for q in plan["request_list"]]
    puts, calls = [], []

    class H:
        DRY_RUN = False

        def load_bd_session(self):
            return "c"

        def get_clientview_token(self, c):
            return "t"

        def _request(self, method, path, token=None, body=None, raw=False):
            calls.append(body["parameters"]["accountFilters"]["accounts"][0])
            return b"{}"

    class S3:
        lock = threading.Lock()

        def put_object(self, Bucket, Key, **kw):
            with self.lock:
                puts.append("s3://%s/%s" % (Bucket, Key))

    t = [0.0]
    lock = threading.Lock()

    def clock():
        with lock:
            return t[0]

    def sleep(s):
        with lock:
            t[0] += s

    rec = CONC.run_concurrent(todo, "/p", H(), S3(), StubOn, M.PlanLanding(plan), plan["ruling"], clock=clock, sleep=sleep)
    assert sorted(puts) == sorted(q["landing_key"] for q in plan["request_list"])
    assert len(calls) == len(set(calls)) == 3 and rec["landed_this_run"] == 3 and rec["failed_count"] == 0
