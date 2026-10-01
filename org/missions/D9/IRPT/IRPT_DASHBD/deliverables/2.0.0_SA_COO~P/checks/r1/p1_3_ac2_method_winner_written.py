"""IRPT_DASHBD round 1 AC (DB-b-3, C-FLOWTIME) -- the served method row names the convention the emitted returns were COMPUTED
under, and carries the proposed tie-out tolerance. Rewritten counterexample-first (TO-DB-b-3 issuer amendment 3; rows
IRPT_DASHBD-S4 limb c, S6 limb d, S7). The file keeps its name; a "winner" is no longer written into the served row.

Usage: python p1_3_ac2_method_winner_written.py <worktree root>
       python p1_3_ac2_method_winner_written.py --self-test    (no AWS: the counterexamples must each FAIL, the good set PASS)

`grade_method` is the rule for the three documents agreeing, and `grade_arithmetic` is the rule that READS THE ARITHMETIC; both
are what --self-test exercises:
  the record's flow_convention_ran is END;
  the served dim_return_method row and the method contract's method_versions[0] both read flow_convention END (a convention is
    changed only by a new method_version with every return recomputed -- never by writing a preferred convention into version 1);
  the row and the contract both carry the record's proposed_tieout_tolerance (1e-12);
  ARITHMETIC: on sampled MEASURED days of the thread account whose window folded exactly one custodian day (carried_days == 1) and
    whose prior day's value is positive, total_return_daily equals END recomputed from the gold's own columns,
    (V_t - F_t) / V_(t-1) - 1, within 1e-9. A row that says END over returns computed any other way FAILS here. At least 10 such
    days must be found, or the check says it could not grade the arithmetic and FAILS.
Pass line: DB-3-AC2 PASS. Base (at the cut): FAIL -- no record.
"""
import io
import json
import math
import sys
from pathlib import Path


def grade_method(record, contract_version, served_row):
    out = []
    if record.get("flow_convention_ran") != "END":
        out.append("the record's flow_convention_ran is %r" % record.get("flow_convention_ran"))
    tol = record.get("proposed_tieout_tolerance")
    if isinstance(tol, bool) or not isinstance(tol, (int, float)) or tol <= 0:
        return out + ["the record's proposed_tieout_tolerance is %r" % tol]
    for name, doc in (("contract method_versions[0]", contract_version), ("served dim_return_method row", served_row)):
        if doc.get("flow_convention") != "END":
            out.append("%s reads flow_convention %r; version 1's returns are computed END" % (name, doc.get("flow_convention")))
        got = doc.get("tieout_tolerance_proposed")
        if got is None or abs(float(got) - float(tol)) > 1e-12:
            out.append("%s reads tieout_tolerance_proposed %r; the record proposes %r" % (name, got, tol))
    return out


def grade_arithmetic(days):
    """days: [(date, V_prev, V, F, emitted)] for MEASURED, carried_days == 1 days. Failures; empty = END is what was computed."""
    out = []
    if len(days) < 10:
        return ["only %d gradable day(s) found (need >= 10); the arithmetic could not be read" % len(days)]
    for date, v_prev, v, flow, emitted in days:
        if v_prev is None or v_prev <= 0 or emitted is None:
            out.append("%s is not gradable (V_(t-1) %r, emitted %r) and should not have been sampled" % (date, v_prev, emitted))
            continue
        end = (v - flow) / v_prev - 1.0
        if math.isnan(end) or abs(end - float(emitted)) > 1e-9:
            out.append("%s: emitted %.12f != END (V_t - F_t) / V_(t-1) - 1 = %.12f" % (date, float(emitted), end))
    return out


def self_test():
    record = {"flow_convention_ran": "END", "flow_convention_preferred": "MIDPOINT", "proposed_tieout_tolerance": 0.0005}
    row_ok = {"flow_convention": "END", "tieout_tolerance_proposed": 0.0005}
    v_prev, flow = 100000.0, 5000.0
    v = 105400.0
    end_days = [("2026-06-%02d" % (i + 1), v_prev, v, flow, (v - flow) / v_prev - 1.0) for i in range(12)]
    start_days = [(d, vp, vv, f, (vv - vp - f) / (vp + f)) for d, vp, vv, f, _e in end_days]
    cases = [
        ("good: the three documents agree and END is what was computed", grade_method(record, row_ok, row_ok) + grade_arithmetic(end_days), False),
        ("COUNTER: the row names START while the returns are END (the old check passed a matching string)",
         grade_method(dict(record), {"flow_convention": "START", "tieout_tolerance_proposed": 0.0005},
                      {"flow_convention": "START", "tieout_tolerance_proposed": 0.0005}), True),
        ("COUNTER: the row says END over returns computed START", grade_method(record, row_ok, row_ok) + grade_arithmetic(start_days), True),
        ("COUNTER: the record says the gold ran START", grade_method(dict(record, flow_convention_ran="START"), row_ok, row_ok), True),
        ("COUNTER: the served row lacks the proposed tolerance",
         grade_method(record, row_ok, {"flow_convention": "END", "tieout_tolerance_proposed": None}), True),
        ("COUNTER: three gradable days only", grade_method(record, row_ok, row_ok) + grade_arithmetic(end_days[:3]), True),
    ]
    bad = 0
    for name, failures, must_fail in cases:
        verdict = bool(failures) == must_fail
        bad += not verdict
        print("  %s %-100s -> %s" % ("ok " if verdict else "BAD", name, failures[0] if failures else "holds"))
    print("SELF-TEST %s: %d of %d cases behave as declared (%d counterexamples must fail, %d good set must hold)"
          % ("PASS" if not bad else "FAIL", len(cases) - bad, len(cases), sum(c[2] for c in cases), sum(not c[2] for c in cases)))
    return 1 if bad else 0


def fail(msg):
    print("DB-3-AC2 FAIL: " + msg)
    sys.exit(1)


def main(root):
    sys.path.insert(0, str(root))
    rec_path = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/tieout/TIEOUT_49F_BLACKDIAMOND_R1.json"
    con_path = root / "org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json"
    thread_path = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/THREAD_ACCOUNT.json"
    if not rec_path.exists():
        fail("record absent: %s" % rec_path)
    if not con_path.exists():
        fail("method contract absent")
    record = json.loads(rec_path.read_text(encoding="utf-8"))
    versions = json.loads(con_path.read_text(encoding="utf-8")).get("method_versions") or []
    if not versions:
        fail("method contract carries no method_versions")
    try:
        thread = str(json.loads(thread_path.read_text(encoding="utf-8"))["thread_account"])
    except (OSError, ValueError, KeyError) as exc:
        fail("THREAD_ACCOUNT.json unreadable (%s)" % type(exc).__name__)

    from lib import opal_naming as on
    import boto3
    import pyarrow.parquet as pq

    s3 = boto3.client("s3", region_name="us-east-1")

    def read(uri):
        bucket, key = uri[5:].split("/", 1)
        return pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=key)["Body"].read())).to_pylist()

    served = read(on.address("irpt", "49financial", "gold", "dim_return_method", "method_version=1") + "/data.parquet")[0]
    failures = grade_method(record, versions[0], served)
    if failures:
        fail("; ".join(failures))

    bucket, k0 = on.address("irpt", "49financial", "gold", "account_return_daily", "date=2000-01-01")[5:].split("/", 1)
    prefix = k0.rsplit("date=2000-01-01", 1)[0]
    pag = s3.get_paginator("list_objects_v2")
    dates = sorted({k.split("date=")[1][:10] for page in pag.paginate(Bucket=bucket, Prefix=prefix)
                    for k in [o["Key"] for o in page.get("Contents", [])] if "date=" in k})
    step = max(1, len(dates) // 60)
    days, looked = [], 0
    for i in range(1, len(dates), step):
        looked += 1
        cur = next((r for r in read(on.address("irpt", "49financial", "gold", "account_return_daily", "date=%s" % dates[i]) + "/data.parquet")
                    if str(r["account_id"]) == thread), None)
        if cur is None or cur.get("day_quality") != "MEASURED" or cur.get("carried_days") != 1 or cur.get("total_return_daily") is None:
            continue
        prev = next((r for r in read(on.address("irpt", "49financial", "gold", "account_return_daily", "date=%s" % dates[i - 1]) + "/data.parquet")
                     if str(r["account_id"]) == thread), None)
        if prev is None or prev.get("market_value_eod") is None or float(prev["market_value_eod"]) <= 0:
            continue
        days.append((dates[i], float(prev["market_value_eod"]), float(cur["market_value_eod"]), float(cur["external_flow"]),
                     float(cur["total_return_daily"])))
    failures = grade_arithmetic(days)
    if failures:
        fail("; ".join(failures[:3]))
    print("  contract and served row read END and tieout_tolerance_proposed %s; END recomputed on %d gradable day(s) of %d sampled "
          "partition(s) for account %s; the record prefers %s" % (record["proposed_tieout_tolerance"], len(days), looked, thread,
                                                                  record.get("flow_convention_preferred")))
    print("DB-3-AC2 PASS")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    main(Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve())
