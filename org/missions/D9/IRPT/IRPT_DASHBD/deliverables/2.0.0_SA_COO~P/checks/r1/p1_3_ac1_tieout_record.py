"""IRPT_DASHBD round 1 AC (DB-b-3, FWD-8 / ADDENDUM ruling 11 / C-TIEOUT / C-FLOWTIME) -- the tie-out MEASUREMENT exists, was read
from the LANDED Black Diamond pulls, and every number in it RECOMPUTES from the returns it states. Rewritten
counterexample-first (TO-DB-b-3 issuer amendment 3; rows IRPT_DASHBD-S4 limb c, S6 limb d, S7).

Usage: python p1_3_ac1_tieout_record.py <worktree root>
       python p1_3_ac1_tieout_record.py --self-test      (no AWS: the counterexamples must each FAIL, the good record PASS)

Reads org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/tieout/TIEOUT_49F_BLACKDIAMOND_R1.json. `grade_record`
is the whole rule for the record's CONTENT and is what --self-test exercises:
  vendor_calls is 0, or above 0 only beside overlap_before_pull below 5 (amendment 1);
  periods: at least 5 DISTINCT (account, start, end) rows -- a repeated period is a defect, not an observation -- each with account,
    bd_account, start, end, bd_twr, opal_twr_start, opal_twr_end, opal_twr_mid, abs_diff, reasons, gap_days;
  flow_convention_ran is END; flow_convention_preferred is one of START, END, MIDPOINT;
  per_convention_summary is present and NON-EMPTY for all three, and each one's median, p90 and max recompute from
    |opal_twr_<convention> - bd_twr| over the rows (1e-12);
  flow_convention_preferred IS the convention with the lowest recomputed median (ties to END);
  every row's abs_diff equals |opal_twr_<preferred> - bd_twr| recomputed from the row's own stated returns (1e-12) -- an asserted
    difference is never taken on trust;
  summary.median, .p90, .max recompute from those recomputed differences; proposed_tieout_tolerance is a number above 0.
Then, on S3: every oracle key sits under blackdiamond/49f/bronze/reporting_performance/ and answers HeadObject.
Pass line: DB-3-AC1 PASS. Base (at the cut): FAIL -- no record.
"""
import json
import statistics
import sys
from pathlib import Path

ORACLE_PREFIX = "blackdiamond/49f/bronze/reporting_performance/"
CONVENTIONS = ("START", "END", "MIDPOINT")
FIELD = {"START": "opal_twr_start", "END": "opal_twr_end", "MIDPOINT": "opal_twr_mid"}
NEED = {"account", "bd_account", "start", "end", "bd_twr", "opal_twr_start", "opal_twr_end", "opal_twr_mid", "abs_diff", "reasons",
        "gap_days"}


def _stats(values):
    ordered = sorted(values)
    return {"median": statistics.median(ordered),
            "p90": ordered[min(len(ordered) - 1, int(round(0.9 * (len(ordered) - 1))))],
            "max": ordered[-1]}


def grade_record(d):
    """Failures of the record's content; empty = it holds. No IO."""
    out = []
    vc = d.get("vendor_calls")
    if not isinstance(vc, int) or vc < 0:
        return ["vendor_calls absent or not a count: %r" % vc]
    if vc > 0:
        ov = d.get("overlap_before_pull")
        if not isinstance(ov, int) or ov >= 5:
            out.append("vendor_calls = %d without an overlap_before_pull below 5 (got %r)" % (vc, ov))
    keys = d.get("oracle_keys") or []
    if not keys or any(not str(k).startswith(ORACLE_PREFIX) for k in keys):
        out.append("oracle_keys empty or outside %s" % ORACLE_PREFIX)
    periods = d.get("periods") or []
    for p in periods:
        miss = NEED - set(p)
        if miss:
            return out + ["period row lacks %s" % sorted(miss)]
    identities = [(str(p["account"]), str(p["start"]), str(p["end"])) for p in periods]
    if len(set(identities)) != len(identities):
        out.append("%d period rows but %d distinct (account, start, end): a repeated period is not an observation"
                   % (len(identities), len(set(identities))))
    if len(set(identities)) < 5:
        out.append("only %d distinct periods (need >= 5)" % len(set(identities)))
    if out:
        return out
    if d.get("flow_convention_ran") != "END":
        out.append("flow_convention_ran %r (the emitted gold is computed END)" % d.get("flow_convention_ran"))
    preferred = d.get("flow_convention_preferred")
    if preferred not in CONVENTIONS:
        return out + ["flow_convention_preferred %r" % preferred]

    recomputed = {}
    for conv in CONVENTIONS:
        try:
            recomputed[conv] = _stats([abs(float(p[FIELD[conv]]) - float(p["bd_twr"])) for p in periods])
        except (TypeError, ValueError):
            return out + ["a period row carries a non-numeric return for %s" % conv]
    per = d.get("per_convention_summary") or {}
    for conv in CONVENTIONS:
        got = per.get(conv)
        if not isinstance(got, dict) or not got:
            out.append("per_convention_summary[%s] is absent or empty" % conv)
            continue
        for name, val in recomputed[conv].items():
            if name not in got or abs(float(got[name]) - val) > 1e-12:
                out.append("per_convention_summary[%s].%s %r != recomputed %.12g" % (conv, name, got.get(name), val))
    lowest = min(CONVENTIONS, key=lambda c: (recomputed[c]["median"], 0 if c == "END" else 1))
    if preferred != lowest:
        out.append("flow_convention_preferred %s but the lowest recomputed median is %s (%.6g against %.6g)"
                   % (preferred, lowest, recomputed[preferred]["median"], recomputed[lowest]["median"]))

    diffs = []
    for p in periods:
        want = abs(float(p[FIELD[preferred]]) - float(p["bd_twr"]))
        diffs.append(want)
        if abs(float(p["abs_diff"]) - want) > 1e-12:
            out.append("account %s %s..%s: abs_diff %r != |%s - bd_twr| = %.12g recomputed from the row"
                       % (p["account"], p["start"], p["end"], p["abs_diff"], FIELD[preferred], want))
    summary = d.get("summary") or {}
    for name, val in _stats(diffs).items():
        if name not in summary or abs(float(summary[name]) - val) > 1e-12:
            out.append("summary.%s %r != recomputed %.12g" % (name, summary.get(name), val))
    tol = d.get("proposed_tieout_tolerance")
    if isinstance(tol, bool) or not isinstance(tol, (int, float)) or tol <= 0:
        out.append("proposed_tieout_tolerance %r is not a positive number" % tol)
    return out


def _record(rows, preferred="END", **over):
    periods = []
    for i, (bd, s, e, m) in enumerate(rows):
        periods.append({"account": "00%08d" % i, "bd_account": "bd%d" % i, "start": "2026-01-01", "end": "2026-06-30", "bd_twr": bd,
                        "opal_twr_start": s, "opal_twr_end": e, "opal_twr_mid": m, "reasons": [], "gap_days": 0,
                        "abs_diff": abs({"START": s, "END": e, "MIDPOINT": m}[preferred] - bd)})
    per = {c: _stats([abs(p[FIELD[c]] - p["bd_twr"]) for p in periods]) for c in CONVENTIONS}
    rec = {"vendor_calls": 0, "overlap_before_pull": len(periods), "oracle_keys": [ORACLE_PREFIX + "2026-08-30/x.json"],
           "periods": periods, "flow_convention_ran": "END", "flow_convention_preferred": preferred,
           "per_convention_summary": per, "summary": _stats([p["abs_diff"] for p in periods]), "proposed_tieout_tolerance": 0.0005}
    rec.update(over)
    return rec


def self_test():
    rows = [(0.050, 0.0512, 0.0502, 0.0507), (0.031, 0.0325, 0.0313, 0.0318), (0.012, 0.0131, 0.0121, 0.0126),
            (-0.020, -0.0189, -0.0199, -0.0194), (0.044, 0.0452, 0.0441, 0.0447), (0.008, 0.0092, 0.0083, 0.0087)]
    good = _record(rows)
    five_copies = _record(rows[:1] * 5)
    for p in five_copies["periods"]:
        p.update({"account": "0000000000", "opal_twr_end": 0.55, "abs_diff": 0.0})
    asserted = _record(rows)
    asserted["periods"][2]["abs_diff"] = 0.0
    wrong_pref = _record(rows, preferred="START")
    cases = [
        ("good: six distinct periods, END preferred, everything recomputes", good, False),
        ("COUNTER: five copies of one period, abs_diff asserted 0 against a real 50-point difference (the old check passed it)",
         five_copies, True),
        ("COUNTER: one row's abs_diff asserted, not the difference of its stated returns", asserted, True),
        ("COUNTER: an empty per-convention summary", _record(rows, per_convention_summary={"START": {}, "END": {}, "MIDPOINT": {}}), True),
        ("COUNTER: the preferred convention is not the one with the lowest median", wrong_pref, True),
        ("COUNTER: the record says the gold ran START", _record(rows, flow_convention_ran="START"), True),
        ("COUNTER: a vendor pull beside an overlap of 9", _record(rows, vendor_calls=3, overlap_before_pull=9), True),
    ]
    bad = 0
    for name, rec, must_fail in cases:
        failures = grade_record(rec)
        verdict = bool(failures) == must_fail
        bad += not verdict
        print("  %s %-118s -> %s" % ("ok " if verdict else "BAD", name, failures[0] if failures else "holds"))
    print("SELF-TEST %s: %d of %d cases behave as declared (%d counterexamples must fail, %d good record must hold)"
          % ("PASS" if not bad else "FAIL", len(cases) - bad, len(cases), sum(c[2] for c in cases), sum(not c[2] for c in cases)))
    return 1 if bad else 0


def fail(msg):
    print("DB-3-AC1 FAIL: " + msg)
    sys.exit(1)


def main(root):
    rec = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/tieout/TIEOUT_49F_BLACKDIAMOND_R1.json"
    if not rec.exists():
        fail("record absent: %s" % rec)
    d = json.loads(rec.read_text(encoding="utf-8"))
    failures = grade_record(d)
    if failures:
        fail("; ".join(failures[:4]) + (" (+%d more)" % (len(failures) - 4) if len(failures) > 4 else ""))
    import boto3

    s3 = boto3.client("s3", region_name="us-east-1")
    for k in d["oracle_keys"]:
        try:
            s3.head_object(Bucket="opal-data-assets", Key=k)
        except Exception as exc:  # noqa: BLE001
            fail("oracle key not readable: %s (%s)" % (k, str(exc)[:80]))
    s = d["summary"]
    print("  distinct periods %d over %d oracle keys; median %.6g p90 %.6g max %.6g; proposed tolerance %s; ran %s, preferred %s"
          % (len(d["periods"]), len(d["oracle_keys"]), s["median"], s["p90"], s["max"], d["proposed_tieout_tolerance"],
             d["flow_convention_ran"], d["flow_convention_preferred"]))
    print("DB-3-AC1 PASS")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    main(Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve())
