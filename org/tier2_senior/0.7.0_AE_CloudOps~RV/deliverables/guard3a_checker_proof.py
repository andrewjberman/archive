#!/usr/bin/env python3
"""GUARD-3a proof -- the checker's per-series benchmark compare, on REAL served objects.

OPAL_BBGTML.TO-GUARD-3 criterion AC1. Reads two archived VersionIds of the served key and a
PLANTED body derived from them. Writes NOTHING to S3. Writes nothing to the production log or
any inbox either: the checker module's LOG/ESCALATION constants and its summon() are redirected
to a scratch recorder before main() is called, so the real freshness_check.log -- the artifact
the first-live-read is measured from -- stays clean.

Arms:
  A1  VersionId Qbef40yVOC1A7F31_vikeqMQSDK198.e (2026-10-06T16:16:52Z)
      -> SERIES-BEHIND naming 9 series: index 2026-09-29 on 5 models, etf 2026-09-29 on 4.
  A2  VersionId fxNfvcQ8KZE2iB5YYF64oMVyXZZcuRDe (2026-10-07T01:28:18Z)
      -> no summons, 10 of 10 series current.
  A3  A2's body with benchmark_last_date REMOVED from one model -> SERIES-NOT-MEASURED.
      Planted from the CURRENT body on purpose: one variable moves, so a not-measured verdict
      cannot be the behind-ness leaking through.
  A4  PRECEDENCE: A1's body (9 genuinely behind) with the field removed from one model
      -> still SERIES-NOT-MEASURED, never SERIES-BEHIND. An incomplete grade must not be
      reported as a complete one.
  A5  The exit contract, through the REAL main(): A1 -> 4, A2 -> 0, A3 -> 5, and a summons
      recorded for 4 and 5 with an entry_step that is not the generic fallback.
  A6  NEGATIVE CONTROL on the instrument: a body whose every series is AHEAD of data_as_of must
      not read CURRENT. Without this, "CURRENT" on A2 could be a function that always says
      CURRENT.

Exit 0 only if every arm matches. Any mismatch prints the delta and exits 1.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[4]
CHECKER = REPO / "integrations" / "bloomberg" / "pipeline" / "freshness_check.py"

BUCKET = "opal-data-portal-v2"
KEY = "json/benchmarks/model_portfolio_benchmarks.json"
V_BEHIND = "Qbef40yVOC1A7F31_vikeqMQSDK198.e"
V_CURRENT = "fxNfvcQ8KZE2iB5YYF64oMVyXZZcuRDe"

failures: list = []


def check(label: str, got, want) -> None:
    ok = got == want
    if not ok:
        failures.append(label)
    print(f"  {'OK  ' if ok else 'FAIL'} {label}")
    if not ok:
        print(f"       want: {want!r}")
        print(f"       got : {got!r}")


def load_checker():
    spec = importlib.util.spec_from_file_location("freshness_check_under_proof", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["freshness_check_under_proof"] = mod
    spec.loader.exec_module(mod)
    return mod


def fetch(version_id: str) -> dict:
    import boto3
    body = boto3.client("s3").get_object(
        Bucket=BUCKET, Key=KEY, VersionId=version_id)["Body"].read()
    return json.loads(body)


def shape(grade: dict) -> str:
    return (f"result={grade['result']} graded={grade['graded']} behind={len(grade['behind'])} "
            f"ahead={len(grade['ahead'])} not_measured={len(grade['not_measured'])}")


def main() -> int:
    print(f"GUARD-3A PROOF -- module under proof: {CHECKER}")
    print(f"  repo root resolved: {REPO}")
    mod = load_checker()

    print("\n[A1] VersionId Qbef40yVOC1A7F31_vikeqMQSDK198.e -- the 2026-10-06 16:16:52Z body")
    b_behind = fetch(V_BEHIND)
    g1 = mod.grade_benchmark_series(b_behind)
    print(f"       {shape(g1)}")
    print(f"       detail: {g1['detail']}")
    check("A1 result is SERIES-BEHIND", g1["result"], "SERIES-BEHIND")
    check("A1 graded the full denominator (5 models x 2 sides)", g1["graded"], 10)
    check("A1 names 9 behind series", len(g1["behind"]), 9)
    check("A1 index side behind on 5 models",
          sorted(r["model"] for r in g1["behind"] if r["side"] == "index"),
          ["INT", "LT", "ST", "ULT", "UST"])
    check("A1 etf side behind on 4 models",
          sorted(r["model"] for r in g1["behind"] if r["side"] == "etf"),
          ["LT", "ST", "ULT", "UST"])
    check("A1 every behind series ends 2026-09-29",
          sorted({r["last_date"] for r in g1["behind"]}), ["2026-09-29"])
    check("A1 data_as_of is 2026-10-05", g1["data_as_of"], "2026-10-05")
    check("A1 nothing read as not-measured", g1["not_measured"], [])

    print("\n[A2] VersionId fxNfvcQ8KZE2iB5YYF64oMVyXZZcuRDe -- the 2026-10-07 01:28:18Z body")
    b_current = fetch(V_CURRENT)
    g2 = mod.grade_benchmark_series(b_current)
    print(f"       {shape(g2)}")
    print(f"       detail: {g2['detail']}")
    check("A2 result is CURRENT", g2["result"], "CURRENT")
    check("A2 10 of 10 series graded", g2["graded"], 10)
    check("A2 no series behind", g2["behind"], [])
    check("A2 no series ahead", g2["ahead"], [])
    check("A2 nothing not-measured", g2["not_measured"], [])

    print("\n[A3] PLANTED from the CURRENT body: benchmark_last_date removed from model[0]")
    planted = copy.deepcopy(b_current)
    dropped = planted["models"][0].get("code")
    planted["models"][0].pop("benchmark_last_date", None)
    g3 = mod.grade_benchmark_series(planted)
    print(f"       dropped the field from model {dropped}")
    print(f"       {shape(g3)}")
    print(f"       detail: {g3['detail']}")
    check("A3 result is SERIES-NOT-MEASURED", g3["result"], "SERIES-NOT-MEASURED")
    check("A3 is NOT a pass", g3["result"] == "CURRENT", False)
    check("A3 is NOT the series-behind result", g3["result"] == "SERIES-BEHIND", False)
    check("A3 names the ungradable model", g3["not_measured"],
          [f"{dropped}: no benchmark_last_date object"])
    check("A3 still graded the other 4 models' 8 series", g3["graded"], 8)

    print("\n[A4] PRECEDENCE -- planted from the BEHIND body (9 real behind), field dropped")
    planted2 = copy.deepcopy(b_behind)
    planted2["models"][0].pop("benchmark_last_date", None)
    g4 = mod.grade_benchmark_series(planted2)
    print(f"       {shape(g4)}")
    check("A4 not-measured outranks behind", g4["result"], "SERIES-NOT-MEASURED")
    check("A4 the behind series are STILL named in the detail",
          "2026-09-29" in g4["detail"], True)

    print("\n[A6] NEGATIVE CONTROL -- every series dated AFTER data_as_of must not read CURRENT")
    ahead = copy.deepcopy(b_current)
    for m in ahead["models"]:
        m["benchmark_last_date"] = {"index": "2026-12-31", "etf": "2026-12-31"}
    g6 = mod.grade_benchmark_series(ahead)
    print(f"       {shape(g6)}")
    check("A6 an all-ahead body does not read CURRENT", g6["result"] == "CURRENT", False)
    check("A6 it reads SERIES-BEHIND (the mismatch summons)", g6["result"], "SERIES-BEHIND")
    check("A6 all 10 counted as ahead, none as behind",
          (len(g6["ahead"]), len(g6["behind"])), (10, 0))
    check("A6 the detail says AHEAD, so direction is not misreported",
          "AHEAD" in g6["detail"], True)

    print("\n[A5] THE EXIT CONTRACT through the real main() -- S3, log, inbox and spawn all")
    print("     redirected; summon() recorded, never fired.")
    print("     ONE SUBSTITUTION, stated: expected_last_trading_day is pinned to each body's own")
    print("     data_as_of. Both archived bodies carry data_as_of 2026-10-05, so read on today's")
    print("     clock they are genuinely 2 trading days stale and the DATE check short-circuits")
    print("     to exit 2 before the series limb is ever reached -- which is the documented")
    print("     precedence working, not a defect. The series limb only runs on a FRESH date, so")
    print("     the proof puts the checker in that state: the state of the 07:30 run on the")
    print("     morning after a good pull. trading_days_behind itself is NOT substituted.")
    tmp = Path(tempfile.mkdtemp(prefix="guard3a_proof_"))
    recorded: list = []

    def fake_summon(kind, detail, test, dry_spawn, force_down):
        recorded.append((kind, detail))

    class FakeBody:
        def __init__(self, raw):
            self._raw = raw

        def read(self):
            return self._raw

    class FakeS3:
        def __init__(self, raw):
            self._raw = raw

        def get_object(self, **kw):
            return {"Body": FakeBody(self._raw)}

    class FakeBoto3:
        def __init__(self, raw):
            self._raw = raw

        def client(self, _name):
            return FakeS3(self._raw)

    mod.LOG = tmp / "proof_freshness_check.log"
    mod.ESCALATION = tmp / "proof_escalation.txt"
    mod.summon = fake_summon
    real_frontier = mod.expected_last_trading_day

    for label, body, want_rc, want_kind in (
        ("A1 body (9 behind)", b_behind, 4, "SERIES-BEHIND"),
        ("A2 body (all current)", b_current, 0, None),
        ("A3 planted (field dropped)", planted, 5, "SERIES-NOT-MEASURED"),
    ):
        recorded.clear()
        if mod.LOG.exists():
            mod.LOG.unlink()
        raw = json.dumps(body).encode("ascii")
        sys.modules["boto3"] = FakeBoto3(raw)
        as_of = __import__("datetime").date.fromisoformat(body["data_as_of"])
        mod.expected_last_trading_day = lambda _today, _a=as_of: _a
        try:
            rc = mod.main([])
        finally:
            mod.expected_last_trading_day = real_frontier
        kind = recorded[0][0] if recorded else None
        print(f"       {label}: main() rc={rc} summons={kind}")
        check(f"A5 {label} exits {want_rc}", rc, want_rc)
        check(f"A5 {label} summons {want_kind}", kind, want_kind)

    print("     And the UNPINNED read, to show the precedence is real rather than assumed:")
    recorded.clear()
    if mod.LOG.exists():
        mod.LOG.unlink()
    sys.modules["boto3"] = FakeBoto3(json.dumps(b_behind).encode("ascii"))
    rc_unpinned = mod.main([])
    kind_unpinned = recorded[0][0] if recorded else None
    print(f"       A1 body on today's real clock: main() rc={rc_unpinned} "
          f"summons={kind_unpinned}")
    check("A5 STALE still outranks the series limb when the date is genuinely behind",
          (rc_unpinned, kind_unpinned), (2, "STALE"))

    print("\n[A5b] entry_step() answers both new Kinds with their own text")
    generic = mod.entry_step("SOME-KIND-THAT-DOES-NOT-EXIST")
    for kind in ("SERIES-BEHIND", "SERIES-NOT-MEASURED"):
        txt = mod.entry_step(kind)
        check(f"A5b entry_step({kind}) is not the generic fallback", txt == generic, False)
        check(f"A5b entry_step({kind}) routes AWAY from Step 2 (no sign-in)",
              "DO NOT ENTER STEP 2" in txt, True)
    check("A5b the pre-existing STALE routing is unchanged",
          "independently confirm the data verdict" in mod.entry_step("STALE"), True)

    print(f"\nARMS: {6} | CHECKS: {len(failures)} failed")
    if failures:
        print("GUARD-3A: FAIL -- " + "; ".join(failures))
        return 1
    print("GUARD-3A: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
