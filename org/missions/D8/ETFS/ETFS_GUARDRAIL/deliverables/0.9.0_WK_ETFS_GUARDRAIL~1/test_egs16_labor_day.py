#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-16 S16-AC1 battery -- THE LEGITIMATELY-EMPTY DAY.

2026-09-07 is Labor Day, US market shut, inside the month EG-s-15 ran on REAL data.
Prints EGS16-LABOR-DAY-CLASS-A only when every arm (a)-(f) holds. READ-ONLY: no
invoke, no write, no deploy. Every S3 read via s3api in UTC; every list with its
denominator.

Run from the worktree root:
  timeout 300 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/test_egs16_labor_day.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "..", "..", ".."))
AWS = os.path.join(ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")
BUCKET = "opal-data-etfs"
MONTH = "2026-09"
PREFIX = "platinum/reports/%s/" % MONTH
VERDICT_KEY = PREFIX + "coverage_verdict.json"
TARGET = "2026-09-07"          # Labor Day, the legitimately-empty day
CONTROL = "2026-09-08"         # the positive control: a trading day
ARM_D_PARTNERS = ["cottonwood", "49financial"]      # the face's arm (d) enumerates these
ALL_PARTNERS = ["cottonwood", "49financial", "inflection"]
PRODUCERS = ["bd-49f-etf-ownership-daily", "cot-etf-ownership-daily"]
# EG-s-15's run, which this order READS and never re-fires.
EGS15_REQUEST_ID = "9fbc33e0-174c-4c82-b392-2b1dafe4a835"
EGS15_START_UTC = "2026-09-10T01:19:02Z"
EGS15_END_UTC = "2026-09-10T01:20:28Z"

ARMS: list[tuple[str, bool, str]] = []


def arm(name: str, ok: bool, detail: str) -> bool:
    ARMS.append((name, ok, detail))
    print("ARM %-3s %-4s %s" % (name, "PASS" if ok else "FAIL", detail))
    return ok


def aws(args: list[str], timeout: int = 120) -> tuple[int, str]:
    p = subprocess.run([AWS] + args, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", "replace").replace("\r", "")


def aws_json(args: list[str], timeout: int = 120):
    rc, out = aws(args + ["--output", "json"], timeout=timeout)
    try:
        return rc, json.loads(out) if out.strip() else None
    except Exception:  # noqa: BLE001
        return rc, None


def list_prefix(prefix: str):
    rc, doc = aws_json(["s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", prefix])
    return (doc or {}).get("Contents", [])


def main() -> int:
    print("EG-s-16 -- the legitimately-empty day that has already happened: %s (Labor Day)" % TARGET)
    print("READ-ONLY. This order reads EG-s-15's run and runs nothing.\n")

    # ------------------------------------------------------------------ arm (a)
    sys.path.insert(0, ROOT)
    from lib.trading_calendar import is_trading_day  # READ, never edited

    t_target = is_trading_day(dt.date(2026, 9, 7))
    t_control = is_trading_day(dt.date(2026, 9, 8))
    print("(a) lib/trading_calendar.py")
    print("    is_trading_day(date(2026, 9, 7))  -> %s   (the target: Labor Day)" % t_target)
    print("    is_trading_day(date(2026, 9, 8))  -> %s   (POSITIVE CONTROL: a trading day)"
          % t_control)
    nontrading = [dt.date(2026, 9, d).isoformat() for d in range(1, 10)
                  if not is_trading_day(dt.date(2026, 9, d))]
    print("    every non-trading day 2026-09-01..09-09: %s -> %d of 9 day(s)"
          % (nontrading, len(nontrading)))
    print("    (09-05 Sat, 09-06 Sun, 09-07 Labor Day -- THREE, not one; the count matters for (b))")
    arm("a", (t_target is False) and (t_control is True),
        "the calendar says %s is NOT a trading day (%s) and the control %s IS (%s)"
        % (TARGET, t_target, CONTROL, t_control))

    # ------------------------------------------------------------------ arm (b)
    rc, head = aws_json(["s3api", "head-object", "--bucket", BUCKET, "--key", VERDICT_KEY])
    v_utc = (head or {}).get("LastModified")
    v_size = (head or {}).get("ContentLength")
    dest = os.path.join(ROOT, ".scratch", "egs16_coverage_verdict.json")
    rc2, _ = aws(["s3api", "get-object", "--bucket", BUCKET, "--key", VERDICT_KEY, dest])
    vdoc = json.load(open(dest, encoding="utf-8")) if rc2 == 0 else None
    print("\n(b) THE OBJECT EG-s-15's RUN WROTE: s3://%s/%s" % (BUCKET, VERDICT_KEY))
    print("    LastModified(UTC)=%s Size=%s verdict=%r"
          % (v_utc, v_size, (vdoc or {}).get("verdict")))

    per = (vdoc or {}).get("per_partner", {})
    holes_ok = 0
    for p, d in per.items():
        h = d.get("holes", [])
        inh = TARGET in h
        holes_ok += 0 if inh else 1
        print("    %-12s A=%s COVERED=%s B=%s C=%s D=%s UNKNOWN=%s | holes=%s | %s in holes -> %s"
              % (p, d["summary"].get("A"), d["summary"].get("COVERED"), d["summary"].get("B"),
                 d["summary"].get("C"), d["summary"].get("D"), d["summary"].get("UNKNOWN"),
                 h, TARGET, inh))
    print("    %s appears in NO partner's holes: %d of %d partner(s)" % (TARGET, holes_ok, len(per)))

    a_counts = {p: d["summary"].get("A") for p, d in per.items()}
    a_matches = sum(1 for p, n in a_counts.items() if n == len(nontrading))
    print("    class A count per partner: %s -- the calendar has %d non-trading day(s); "
          "matching partners: %d of %d" % (a_counts, len(nontrading), a_matches, len(per)))

    # THE GRAIN QUESTION THE ARM TURNS ON: does the object CLASSIFY the date, or only COUNT?
    blob = json.dumps(vdoc)
    occurrences = blob.count(TARGET)
    has_date_class_map = occurrences > 0
    print("    DOES THE OBJECT NAME %s AT ALL? occurrences of the literal date in the whole "
          "document = %d" % (TARGET, occurrences))
    print("    per_partner entry keys: %s"
          % (sorted(next(iter(per.values())).keys()) if per else []))
    print("    summary keys: %s"
          % (sorted(next(iter(per.values()))["summary"].keys()) if per else []))
    print("    => the served verdict carries PER-CLASS COUNTS plus a `holes` DATE LIST. It carries "
          "NO per-date class map, so 'this object classifies %s as A' is NOT READABLE FROM IT; "
          "only the NEGATIVE (not a hole) and the COUNT (A=%s == %d non-trading days) are."
          % (TARGET, a_counts.get("49financial"), len(nontrading)))
    arm("b", holes_ok == len(per) and len(per) > 0 and a_matches == len(per)
        and has_date_class_map,
        "%s in NO partner's holes (%d of %d) and class A count == the calendar's %d non-trading "
        "days for %d of %d partners -- BUT the object contains the literal date %d time(s), so it "
        "carries no per-date class map and the 'classifies %s as class A' limb is UNREADABLE from "
        "the named artifact (row W1-S30)"
        % (TARGET, holes_ok, len(per), len(nontrading), a_matches, len(per), occurrences, TARGET))

    # ------------------------------------------------------------------ arm (c)
    print("\n(c) THE `expected_empty` FIELD")
    print("    classifier.py:168-170 @c866edd324 -- summarize()'s own docstring: 'Counts per class "
          "plus trading_days, covered, holes (= C + UNKNOWN + D; B is NOT a hole), expected_empty "
          "(= B).'")
    print("    classifier.py:176-178 @c866edd324 -- expected_empty = counts[\"B\"]")
    ee = {p: d["summary"].get("expected_empty") for p, d in per.items()}
    bb = {p: d["summary"].get("B") for p, d in per.items()}
    print("    expected_empty per partner: %s ; class B per partner: %s -- identical, as the "
          "source says" % (ee, bb))
    print("    So `expected_empty` counts class B (upstream present, priced == 0). %s is class A "
          "(market closed). A class-A date CANNOT appear in expected_empty by construction."
          % TARGET)
    # the equivalent-field hunt the face allows
    carriers = [k for k in (next(iter(per.values())).keys() if per else [])
                if isinstance(next(iter(per.values())).get(k), list)]
    print("    EQUIVALENT-FIELD HUNT (the face allows naming one): fields in a per_partner entry "
          "that carry DATES at all: %s -- and %s is in none of them." % (carriers, TARGET))
    # the hole list with and without the date -- the limb that IS satisfiable
    equal = 0
    for p, d in per.items():
        h = list(d.get("holes", []))
        without = [x for x in h if x != TARGET]
        same = (h == without)
        equal += 1 if same else 0
        print("    %-12s holes WITH %s removed: %s | holes as written: %s | EQUAL -> %s"
              % (p, TARGET, without, h, same))
    print("    => the hole counts are UNAFFECTED by %s for %d of %d partners (that limb HOLDS)."
          % (TARGET, equal, len(per)))
    ee_carries = any(v for v in ee.values())
    arm("c", ee_carries and equal == len(per),
        "the hole counts are UNAFFECTED by %s (%d of %d partners) -- but `expected_empty` is the "
        "class B count (=%s) and CANNOT carry a class-A date, and no other per_partner field "
        "carries dates except `holes`; the 'expected_empty carries %s' limb is unsatisfiable "
        "against this artifact (row W1-S30)"
        % (TARGET, equal, len(per), list(ee.values()), TARGET))

    # ------------------------------------------------------------------ arm (d)
    print("\n(d) NO DAILY SLICE FOR %s (the face enumerates: %s)" % (TARGET, ARM_D_PARTNERS))
    d_ok = 0
    for p in ARM_D_PARTNERS:
        keys = list_prefix("daily/%s/" % p)
        hit = [c for c in keys if TARGET in c["Key"]]
        ctl = [c for c in keys if CONTROL in c["Key"]]
        d_ok += 1 if len(hit) == 0 else 0
        print("    daily/%s/ -> %d key(s) naming %s, of %d key(s) under the prefix (denominator)"
              % (p, len(hit), TARGET, len(keys)))
        for c in ctl:
            print("      POSITIVE CONTROL %s -> %d B, LastModified(UTC)=%s"
                  % (c["Key"], c["Size"], c["LastModified"]))
        if not ctl:
            print("      POSITIVE CONTROL: no %s slice under this prefix" % CONTROL)
    # THE UNCOVERED MEMBER, printed though the face's arm does not grade it.
    inf_keys = list_prefix("daily/inflection/")
    inf_hit = [c for c in inf_keys if TARGET in c["Key"]]
    print("    UNCOVERED MEMBER, printed not graded -- the face's arm (d) enumerates 2 of 3 "
          "partners:")
    print("      daily/inflection/ -> %d key(s) naming %s, of %d key(s) (denominator)"
          % (len(inf_hit), TARGET, len(inf_keys)))
    for c in inf_hit:
        print("        %s  %d B  LastModified(UTC)=%s  <- A SLICE EXISTS ON A CLOSED-MARKET DAY "
              "(row W1-S31)" % (c["Key"], c["Size"], c["LastModified"]))
    arm("d", d_ok == len(ARM_D_PARTNERS),
        "0 daily slices for %s for %d of %d enumerated partner(s) (%s), each with its prefix "
        "denominator and a %s positive control"
        % (TARGET, d_ok, len(ARM_D_PARTNERS), ", ".join(ARM_D_PARTNERS), CONTROL))

    # ------------------------------------------------------------------ arm (e)
    print("\n(e) NOTHING WAS WRITTEN AGAINST %s ACROSS EG-s-15's RUN WINDOW" % TARGET)
    print("    COVERAGE-ABSENT: no data-event selector covers opal-data-etfs (the served-key trail "
          "names only platinum/firm/ on inf/bd/cot; versioning on opal-data-etfs is DISABLED, "
          "W1-S12) -- so a CloudTrail PutObject read is neither a pass nor a fail here, and the "
          "write is read from the OBJECTS and the producers' own logs instead.")
    e_ok = 0
    for p in ARM_D_PARTNERS:
        keys = list_prefix("daily/%s/" % p)
        hit = [c for c in keys if TARGET in c["Key"]]
        in_window = [c for c in keys
                     if str(c["LastModified"]).startswith("2026-09-10T01:")]
        ok = (len(hit) == 0 and len(in_window) == 0)
        e_ok += 1 if ok else 0
        print("    daily/%s/ AFTER the run: %d key(s) naming %s of %d (denominator); keys with "
              "LastModified INSIDE the run window: %d of %d"
              % (p, len(hit), TARGET, len(keys), len(in_window), len(keys)))
    print("    THE 'BEFORE' LIMB, and its LIMIT stated: no listing of these prefixes was taken "
          "before EG-s-15's run, and a prefix listing is not retrospective. What IS measured: 0 "
          "keys name %s now, AND no key under either prefix carries a LastModified inside the run "
          "window -- so nothing under them was created or modified during the run. With no delete "
          "performed by any actor and versioning disabled, the AFTER state equals the BEFORE state "
          "for this date. That is an INFERENCE from two measurements, not a retrospective read."
          % TARGET)
    start_ms = int(dt.datetime(2026, 9, 10, 1, 19, 0, tzinfo=dt.timezone.utc).timestamp() * 1000)
    end_ms = int(dt.datetime(2026, 9, 10, 1, 21, 0, tzinfo=dt.timezone.utc).timestamp() * 1000)
    log_ok = 0
    for g in PRODUCERS:
        rc, doc = aws_json(["logs", "filter-log-events", "--log-group-name", "/aws/lambda/" + g,
                            "--start-time", str(start_ms), "--end-time", str(end_ms)], timeout=180)
        ev = (doc or {}).get("events", [])
        named = [e for e in ev if TARGET in e["message"]]
        wrote = [e for e in ev if "wrote" in e["message"].lower()]
        log_ok += 1 if not named and not wrote else 0
        print("    /aws/lambda/%-30s %d line(s) scanned (denominator), nextToken=%s | lines naming "
              "%s: %d | lines containing 'wrote': %d"
              % (g, len(ev), bool((doc or {}).get("nextToken")), TARGET, len(named), len(wrote)))
    arm("e", e_ok == len(ARM_D_PARTNERS) and log_ok == len(PRODUCERS),
        "0 keys for %s under %d of %d prefixes with no key modified in the run window, and %d of "
        "%d producer log groups carry no line naming %s and no 'wrote' line"
        % (TARGET, e_ok, len(ARM_D_PARTNERS), log_ok, len(PRODUCERS), TARGET))

    # ------------------------------------------------------------------ arm (f)
    print("\n(f) THE RUN THIS READS IS EG-s-15's")
    print("    EG-s-15 request id: %s (from that order's egs15_invoke_record.json)"
          % EGS15_REQUEST_ID)
    print("    that run's window: %s -> %s" % (EGS15_START_UTC, EGS15_END_UTC))
    print("    the verdict object's LastModified(UTC): %s" % v_utc)
    # NOTE, an instrument difference worth stating: s3api head-object renders
    # LastModified in RFC-1123 ("Thu, 10 Sep 2026 01:20:20 GMT") while list-objects-v2
    # renders ISO-8601 ("2026-09-10T01:20:20.000Z"). Both are UTC. Parse either.
    def _parse_utc(v):
        if not v:
            return None
        v = str(v).strip()
        # Discriminate on SHAPE, not on the letter 'T' -- "Thu, ..." contains a 'T'
        # and an `if "T" in v` test silently truncates the RFC-1123 form.
        if len(v) >= 19 and v[4] == "-" and v[7] == "-" and v[10] == "T":
            try:
                return dt.datetime.strptime(v[:19], "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                return None
        for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S"):
            try:
                return dt.datetime.strptime(v.replace(" GMT", ""), fmt.replace(" %Z", ""))
            except ValueError:
                continue
        return None

    v_dt = _parse_utc(v_utc)
    print("    (that LastModified is s3api head-object's RFC-1123 rendering; list-objects-v2 "
          "renders the SAME instant as 2026-09-10T01:20:20.000Z -- both UTC)")
    s_dt = dt.datetime(2026, 9, 10, 1, 19, 2)
    e_dt = dt.datetime(2026, 9, 10, 1, 20, 28)
    inside = bool(v_dt and s_dt <= v_dt <= e_dt)
    print("    is the verdict object's UTC inside that run's window? -> %s" % inside)
    arm("f", inside, "the verdict object read by arms (b)/(c) was written at %s, inside EG-s-15's "
                     "run window %s -> %s, whose request id is %s"
        % (v_utc, EGS15_START_UTC, EGS15_END_UTC, EGS15_REQUEST_ID))

    # ------------------------------------------------------------------ verdict
    npass = sum(1 for _, ok, _ in ARMS if ok)
    print("\nARMS %d of %d PASS" % (npass, len(ARMS)))
    if npass == len(ARMS):
        print("EGS16-LABOR-DAY-CLASS-A")
        return 0
    print("EGS16-NOT-ESTABLISHED -- failing arms: %s"
          % ", ".join(n for n, ok, _ in ARMS if not ok))
    return 1


if __name__ == "__main__":
    sys.exit(main())
