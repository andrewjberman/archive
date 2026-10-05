"""Offline tests for bd_population_concurrent_e3.py: the shared bearer, the ramp, the 429 halving, FAILED recording, the consecutive and
FAILED-cap aborts, the 401 rules, the one-queue guarantee, the --go refusals (run and sweep) and the denominators. No network, no Black
Diamond call, no credential: boto3, the estate helpers, the clock and sleep are stubs."""
import importlib.util
import json
import threading
import urllib.error
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "bd_population_concurrent_e3.py"


def _load():
    spec = importlib.util.spec_from_file_location("bd_population_concurrent_e3_under_test", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = _load()


class FakeTime:
    """A shared fake clock: sleep advances it, so the pacer, the ramp and the bearer age run without waiting."""

    def __init__(self):
        self.t, self.sleeps, self.lock = 0.0, [], threading.Lock()

    def clock(self):
        with self.lock:
            return self.t

    def sleep(self, s):
        with self.lock:
            self.t += s
            self.sleeps.append(s)

    def advance(self, s):
        with self.lock:
            self.t += s


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
    def __init__(self, fail=False):
        self.put, self.fail, self.lock = [], fail, threading.Lock()

    def put_object(self, Bucket, Key, Body, ContentType):
        if self.fail:
            raise OSError("put failed")
        with self.lock:
            self.put.append(Key)


class StubHelpers:
    """script maps (bd account, attempt number) to an exception to raise, or (seconds, exception) to advance the clock first."""

    def __init__(self, ft, script=None):
        self.ft, self.script, self.lock = ft, script or {}, threading.Lock()
        self.mints = self.sessions = 0
        self.requested, self.tokens, self.attempts = [], set(), {}

    def load_bd_session(self):
        with self.lock:
            self.sessions += 1
        return "cookie"

    def get_clientview_token(self, cookie):
        with self.lock:
            self.mints += 1
            return "tok%d" % self.mints

    def _request(self, method, path, token, body, raw):
        acct = body["acct"]
        with self.lock:
            n = self.attempts[acct] = self.attempts.get(acct, 0) + 1
            self.requested.append(acct)
            self.tokens.add(token)
            hit = self.script.get((acct, n))
        if hit is not None:
            if isinstance(hit, tuple):
                self.ft.advance(hit[0])
                hit = hit[1]
            raise hit
        return b'{"ok": 1}'


def _reqs(n, start=0):
    return [{"account": "A%d" % i, "bd_account": str(i), "segments": [1], "body": {"acct": str(i)}} for i in range(start, start + n)]


def _ruling(**kw):
    r = {k: v for k, v in M.RULING.items() if k != "ruling_ids"}
    r.update(kw)
    return r


def _go(n, ruling=None, script=None, landed=(), s3=None, checkpoint=None):
    ft = FakeTime()
    h = StubHelpers(ft, script)
    s3 = s3 or StubS3()
    rec = M.run_concurrent(_reqs(n), "/p", h, s3, StubOn, StubB20, ruling or _ruling(), landed_set=landed, clock=ft.clock,
                           sleep=ft.sleep, checkpoint=checkpoint)
    return rec, h, s3, ft


def test_shared_bearer_is_minted_by_the_coordinator_alone():
    rec, h, _s3, _ft = _go(60, _ruling(workers_start=6, workers_max=6))
    assert rec["landed_this_run"] == 60 and rec["vendor_calls"] == 60 and rec["aborted"] is None
    assert h.mints == 1 and h.sessions == 1 and h.tokens == {"tok1"}  # one shared bearer for six workers, not one per worker
    rec2, h2, _s, _t = _go(60, _ruling(workers_start=6, workers_max=6, mint_interval_s=10))
    assert 2 <= h2.mints <= 10 and h2.mints == rec2["bearer_mints"]  # re-minted by age, still far below the 60 calls
    assert h2.sessions == h2.mints


def test_ramp_goes_from_2_to_6_only_after_ramp_after_s_with_no_401_or_429():
    rec, _h, _s3, _ft = _go(80, _ruling(ramp_after_s=10))
    ramp = [e for e in rec["events"] if e["event"] == "ramp"]
    assert len(ramp) == 1 and ramp[0]["t"] >= 10 and ramp[0]["workers"] == 6
    assert rec["peak_in_flight_before_ramp"] <= 2 and rec["ramped"] and rec["workers_target"] == 6
    assert rec["landed_this_run"] == 80


def test_a_429_blocks_the_ramp_halves_the_workers_and_retries_once_after_the_backoff():
    script = {("1", 1): RuntimeError("HTTP 429: slow down")}
    rec, h, _s3, ft = _go(40, _ruling(workers_start=4, workers_max=6, ramp_after_s=5), script)
    halve = [e for e in rec["events"] if e["event"] == "halve"]
    assert halve and halve[0]["workers"] == 2  # 4 halved to 2
    assert 30.0 in ft.sleeps  # no Retry-After: the 30 s backoff
    one = [r for r in rec["records"] if r["bd_account"] == "1"][0]
    assert one["retried"] and one["status"] == "LANDED" and h.attempts["1"] == 2
    assert not rec["ramped"]  # a 429 seen: the ramp never fires
    rec2, _h2, _s2, ft2 = _go(10, _ruling(workers_start=1, workers_max=1), {("2", 1): RuntimeError("HTTP 429: Retry-After: 7")})
    assert 7.0 in ft2.sleeps and rec2["landed_this_run"] == 10


def test_a_call_failing_twice_is_recorded_FAILED_and_the_run_continues():
    err = urllib.error.URLError("boom")
    script = {("3", 1): err, ("3", 2): err, ("5", 1): RuntimeError("HTTP 503: x"), ("5", 2): RuntimeError("HTTP 503: x")}
    rec, _h, _s3, _ft = _go(10, _ruling(workers_start=1, workers_max=1), script)
    assert rec["aborted"] is None and rec["landed_this_run"] == 8 and rec["failed_count"] == 2
    assert {f["bd_account"]: f["class"] for f in rec["failed"]} == {"3": "transport", "5": "5xx"}
    r3 = [r for r in rec["records"] if r["bd_account"] == "3"][0]
    assert r3["status"] == "FAILED" and r3["retried"] and r3["landed"] is None and "worker" in r3 and "bearer_generation" in r3


def test_three_consecutive_failures_abort_and_the_record_is_left_behind():
    err = urllib.error.URLError("boom")
    script = {(str(i), n): err for i in (0, 1, 2) for n in (1, 2)}
    snaps = []
    rec, _h, _s3, _ft = _go(10, _ruling(workers_start=1, workers_max=1), script, checkpoint=snaps.append)
    assert "3 consecutive" in rec["aborted"] and rec["failed_count"] == 3 and rec["not_requested"] == 7
    assert snaps and snaps[-1]["complete"] and snaps[-1]["aborted"] == rec["aborted"]  # the finally wrote it


def test_FAILED_above_failed_cap_aborts():
    err = urllib.error.URLError("boom")
    script = {(str(i), n): err for i in (0, 2, 4) for n in (1, 2)}  # never 3 in a row: only the cap can stop it
    rec, h, _s3, _ft = _go(10, _ruling(workers_start=1, workers_max=1, failed_cap=2), script)
    assert rec["failed_count"] == 3 and "FAILED 3 above failed_cap 2" in rec["aborted"] and "consecutive" not in rec["aborted"]
    assert "5" not in h.attempts


def test_a_401_within_fresh_mint_s_of_a_mint_stops_the_run():
    rec, h, _s3, _ft = _go(10, _ruling(workers_start=1, workers_max=1), {("2", 1): RuntimeError("HTTP 401: no")})
    assert "younger than fresh_mint_s" in rec["aborted"] and h.attempts["2"] == 1 and h.mints == 1  # a stop, never a retry
    assert rec["records"][-1]["status"] == "STOPPED"


def test_a_401_on_an_older_bearer_remints_and_retries_the_call():
    script = {("3", 1): (100, RuntimeError("HTTP 401: expired"))}
    rec, h, _s3, _ft = _go(10, _ruling(workers_start=1, workers_max=1, mint_interval_s=10 ** 6), script)
    assert rec["aborted"] is None and h.mints == 2 and rec["landed_this_run"] == 10 and h.attempts["3"] == 2
    assert [r for r in rec["records"] if r["bd_account"] == "3"][0]["retried"]
    assert not rec["ramped"]


def test_another_4xx_and_a_landing_failure_abort_the_whole_run():
    rec, _h, _s3, _ft = _go(10, _ruling(workers_start=1, workers_max=1), {("1", 1): RuntimeError("HTTP 403: no")})
    assert "HTTP 403" in rec["aborted"] and rec["landed_this_run"] == 1
    rec2, _h2, _s2, _ft2 = _go(10, _ruling(workers_start=1, workers_max=1), s3=StubS3(fail=True))
    assert rec2["aborted"] == "landing failure" and rec2["landed_this_run"] == 0


def test_a_landed_account_is_never_requested_and_none_is_requested_twice_across_workers():
    landed = {str(i) for i in range(0, 40, 3)}
    todo = [r for r in _reqs(40) if r["bd_account"] not in landed]
    ft = FakeTime()
    h = StubHelpers(ft)
    rec = M.run_concurrent(todo, "/p", h, StubS3(), StubOn, StubB20, _ruling(workers_start=6, workers_max=6),
                           landed_set=landed, clock=ft.clock, sleep=ft.sleep)
    assert len(h.requested) == len(set(h.requested)) == len(todo) and not (set(h.requested) & landed)
    assert rec["landed_this_run"] == len(todo)
    with pytest.raises(SystemExit):  # the guard: a todo list holding a landed account is refused before any call
        M.run_concurrent(_reqs(5), "/p", h, StubS3(), StubOn, StubB20, _ruling(), landed_set={"2"}, clock=ft.clock, sleep=ft.sleep)


def test_the_checkpoint_is_written_every_50_calls_and_in_a_finally():
    snaps = []
    rec, _h, _s3, _ft = _go(120, _ruling(workers_start=1, workers_max=1), checkpoint=snaps.append)
    assert [s["calls_recorded"] for s in snaps] == [50, 100, 120] and snaps[-1]["complete"] and rec["landed_this_run"] == 120


def test_run_and_sweep_refuse_without_go(monkeypatch, tmp_path):
    monkeypatch.setitem(__import__("sys").modules, "boto3", None)  # a tripwire: a refusal must come before any S3 or vendor use
    for mode in ("run", "sweep"):
        with pytest.raises(SystemExit) as e:
            M.main(["x", str(tmp_path), mode])
        assert "--go" in str(e.value)
        with pytest.raises(SystemExit) as e:
            M.refusal_checks(tmp_path, ["x", ".", mode, "--go"], mode)
        assert "run plan first" in str(e.value)
    (tmp_path / M.PLAN_NAME).write_text(json.dumps({"requests_planned": 1}), encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        M.refusal_checks(tmp_path, ["x", ".", "run", "--go"], "run")
    assert "ruling" in str(e.value)
    (tmp_path / M.PLAN_NAME).write_text(json.dumps({"ruling": M.RULING}), encoding="utf-8")
    assert M.refusal_checks(tmp_path, ["x", ".", "sweep", "--go"], "sweep")["ruling"] == M.RULING


def test_sweep_refuses_a_failed_set_over_the_cap_or_outside_the_three_classes():
    ok = [{"account": "A1", "bd_account": "1", "class": c} for c in ("transport", "5xx", "429")]
    M.check_sweep_set(ok, 105)
    with pytest.raises(SystemExit):
        M.check_sweep_set(ok, 2)
    with pytest.raises(SystemExit):
        M.check_sweep_set(ok + [{"account": "A9", "bd_account": "9", "class": "4xx-other"}], 105)


def test_the_plan_carries_the_ruling_and_prints_both_denominators(capsys):
    c21 = M.load_c21()
    reqs = [{"bd_account": str(i)} for i in range(10)]
    e20 = {"word": "w", "request_list": reqs, "request_bodies_sha256": "x"}
    plan = M.make_plan(c21, e20, {"0", "1", "2", "99"})
    assert plan["requests_planned"] == 10 and plan["landed"] == 3 and plan["complement"] == 7
    assert plan["requests_planned"] == plan["landed"] + plan["complement"] and plan["vendor_calls"] == 0 and plan["dry_run"] == 1
    assert plan["landed_outside_plan"] == ["99"] and not set(plan["complement_accounts"]) & set(plan["landed_accounts"])
    assert plan["ruling"]["ruling_ids"] == ["1.0.0_SA_CTO RULINGS batch 249", "1.0.0_SA_CTO RULINGS batch 250"]
    assert (plan["ruling"]["workers_start"], plan["ruling"]["workers_max"], plan["ruling"]["ramp_after_s"],
            plan["ruling"]["aggregate_rps"]) == (2, 6, 600, 2)
    assert (plan["ruling"]["retries_per_call"], plan["ruling"]["consecutive_failures_abort"], plan["ruling"]["failed_cap"],
            plan["ruling"]["mint_interval_s"], plan["ruling"]["fresh_mint_s"]) == (1, 3, 105, 120, 30)
    M.print_denominators(c21, plan)
    assert "denominators: planned 10 = landed 3 + complement 7" in capsys.readouterr().out
