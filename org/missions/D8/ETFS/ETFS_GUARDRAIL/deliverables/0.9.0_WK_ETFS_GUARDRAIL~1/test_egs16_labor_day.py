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
import hashlib
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
    global is_trading_day
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
    # RE-CUT 2026-09-10 ~03:2xZ on row W1-S30. The artifact carries per-class COUNTS
    # and a `holes` DATE LIST and NO per-date class map, so "this object classifies
    # THAT DATE as class A" is not readable from it. What IS readable: the class-A
    # COUNT against a calendar this battery ENUMERATES (never a hand-list), and the
    # date's ABSENCE from every hole list.
    rc, head = aws_json(["s3api", "head-object", "--bucket", BUCKET, "--key", VERDICT_KEY])
    v_utc = (head or {}).get("LastModified")
    v_size = (head or {}).get("ContentLength")
    dest = os.path.join(ROOT, ".scratch", "egs16_coverage_verdict.json")
    rc2, _ = aws(["s3api", "get-object", "--bucket", BUCKET, "--key", VERDICT_KEY, dest])
    vdoc = json.load(open(dest, encoding="utf-8")) if rc2 == 0 else None
    print("\n(b) THE OBJECT EG-s-15's RUN WROTE: s3://%s/%s" % (BUCKET, VERDICT_KEY))
    print("    LastModified(UTC)=%s Size=%s verdict=%r"
          % (v_utc, v_size, (vdoc or {}).get("verdict")))

    # THE PARTNER LIST COMES FROM THE ARTIFACT, with its denominator.
    per = (vdoc or {}).get("per_partner", {})
    partners = sorted(per.keys())
    print("    PARTNERS TAKEN FROM THE ARTIFACT: %s -> %d partner(s) (denominator)"
          % (partners, len(partners)))

    # THE VERDICT'S OWN WINDOW, derived from the artifact, not hand-coded: the six
    # class counts partition the days the classifier iterated.
    CLASSES = ("A", "COVERED", "B", "C", "D", "UNKNOWN")
    spans = {p: sum(int(per[p]["summary"].get(k) or 0) for k in CLASSES) for p in partners}
    span_vals = sorted(set(spans.values()))
    n_days = span_vals[0] if len(span_vals) == 1 else max(span_vals)
    print("    THE VERDICT'S OWN WINDOW, derived from the artifact: the six class counts sum to "
          "%s per partner -> %d day(s) covered, i.e. %s-01 .. %s-%02d"
          % (spans, n_days, MONTH, MONTH, n_days))
    if len(span_vals) != 1:
        print("    WARN: partners disagree on the covered span %s -- using the maximum" % spans)

    # THE CALENDAR IS ENUMERATED BY THIS BATTERY over that window. NEVER a hand-list:
    # the issuer hand-listed two non-trading dates and there are three, and a
    # hand-list would have failed this arm against a CORRECT world.
    y, mo = int(MONTH[0:4]), int(MONTH[5:7])
    window = [dt.date(y, mo, 1) + dt.timedelta(days=k) for k in range(n_days)]
    nontrading = [d.isoformat() for d in window if not is_trading_day(d)]
    trading = [d.isoformat() for d in window if is_trading_day(d)]
    print("    CALENDAR ENUMERATED BY THIS BATTERY over %d day(s) (never hand-listed):"
          % len(window))
    for d in window:
        print("      %s  %-3s  is_trading_day=%s" % (d.isoformat(), d.strftime("%a"),
                                                     is_trading_day(d)))
    print("    -> %d non-trading day(s): %s" % (len(nontrading), nontrading))
    print("    -> %d trading day(s)" % len(trading))

    count_ok = 0
    holes_ok = 0
    for p in partners:
        sm = per[p]["summary"]
        h = per[p].get("holes", [])
        a_ok = int(sm.get("A") or 0) == len(nontrading)
        t_ok = int(sm.get("trading_days") or 0) == len(trading)
        count_ok += 1 if a_ok else 0
        holes_ok += 0 if TARGET in h else 1
        print("    %-12s A=%s vs %d enumerated non-trading -> %s | trading_days=%s vs %d -> %s | "
              "holes=%s | %s in holes -> %s"
              % (p, sm.get("A"), len(nontrading), a_ok, sm.get("trading_days"), len(trading), t_ok,
                 h, TARGET, TARGET in h))
    blob = json.dumps(vdoc)
    print("    THE LIMIT, RECORDED AND NOT WORKED AROUND: the artifact carries NO per-date "
          "classification -- the literal %s appears %d time(s) in the whole %s-byte document -- so "
          "this arm proves THE COUNT and THE ABSENCE, never the per-date label."
          % (TARGET, blob.count(TARGET), v_size))
    arm("b", len(partners) > 0 and count_ok == len(partners) and holes_ok == len(partners),
        "class-A count == the %d non-trading day(s) this battery enumerated from the calendar for "
        "%d of %d partner(s) taken from the artifact, and %s is in NO partner's holes (%d of %d); "
        "the per-date label itself is NOT readable from this artifact and is not claimed"
        % (len(nontrading), count_ok, len(partners), TARGET, holes_ok, len(partners)))

    # ------------------------------------------------------------------ arm (c)
    # RE-CUT on W1-S30. expected_empty is the class-B count -- a DIFFERENT AXIS from
    # class A -- so it is printed with its true meaning and NOT graded as a class-A
    # instrument. The substance moves to the hole lists.
    print("\n(c) `expected_empty`, PRINTED WITH ITS TRUE MEANING AND NOT GRADED AS A CLASS-A "
          "INSTRUMENT")
    print("    data/etfs/scripts/coverage/classifier.py:178 @c866edd324 --")
    print('      expected_empty = counts["B"]')
    print("    and :169-170 @c866edd324, the docstring: 'Counts per class plus trading_days, "
          "covered, holes (= C + UNKNOWN + D; B is NOT a hole), expected_empty (= B).'")
    print("    classifier.py:146-148 @c866edd324 class D / :152-156 class B ('upstream present, "
          "priced == 0') / :122-124 class A ('market closed (not a trading day)') -- so class B "
          "and class A are DIFFERENT AXES and a class-A date cannot appear in expected_empty by "
          "construction.")
    for p in partners:
        sm = per[p]["summary"]
        print("    %-12s expected_empty=%s  B=%s  (identical, as the source says) -- RECORDED, "
              "NOT GRADED" % (p, sm.get("expected_empty"), sm.get("B")))
    equal = 0
    for p in partners:
        h = list(per[p].get("holes", []))
        without = [x for x in h if x != TARGET]
        same = (h == without)
        equal += 1 if same else 0
        print("    %-12s holes as written: %-16s | holes with %s removed: %-16s | EQUAL -> %s"
              % (p, h, TARGET, without, same))
    arm("c", equal == len(partners) and len(partners) > 0,
        "each partner's hole list is IDENTICAL with and without %s (%d of %d partners), so the "
        "closed day inflates no hole count; expected_empty printed beside it as the class-B count "
        "it is (%s) and NOT graded as a class-A instrument"
        % (TARGET, equal, len(partners),
           [per[p]["summary"].get("expected_empty") for p in partners]))

    # ------------------------------------------------------------------ arm (d)
    # RE-CUT on W1-S31, and the widening is the point: EVERY partner the verdict
    # covers, from the artifact's own list. THE ACCEPT IS ABOUT THIS SYSTEM'S
    # BEHAVIOUR: a slice that PREDATES EG-s-15's run is an upstream producer fact --
    # printed and named, but it does NOT fail this arm.
    print("\n(d) EVERY PARTNER THE VERDICT COVERS (%d of %d, from the artifact's own list): does a "
          "slice exist at daily/<partner>/%s.json ?" % (len(partners), len(partners), TARGET))
    run_start = dt.datetime(2026, 9, 10, 1, 19, 2)
    run_end = dt.datetime(2026, 9, 10, 1, 20, 28)

    def _iso(v):
        v = str(v)
        return dt.datetime.strptime(v[:19], "%Y-%m-%dT%H:%M:%S")

    def _vhash(partner, date_str):
        dst = os.path.join(ROOT, ".scratch", "egs16_%s_%s.json" % (partner, date_str))
        r, _ = aws(["s3api", "get-object", "--bucket", BUCKET,
                    "--key", "daily/%s/%s.json" % (partner, date_str), dst])
        if r != 0:
            return None, None, None
        try:
            doc = json.load(open(dst, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return None, None, None
        tup = [(x.get("etf_ticker"), x.get("ownership_value"), x.get("account_count")) for x in doc]
        return len(doc), (doc[0].get("source_as_of") if doc else None), \
            hashlib.sha256(str(tup).encode()).hexdigest()[:12]

    d_ok = 0
    predating = []
    for p in partners:
        keys = list_prefix("daily/%s/" % p)
        hit = [c for c in keys if TARGET in c["Key"]]
        ctl = [c for c in keys if CONTROL in c["Key"]]
        print("    daily/%-12s -> %d key(s) naming %s, of %d key(s) under the prefix (denominator)"
              % (p + "/", len(hit), TARGET, len(keys)))
        for c in ctl:
            print("      POSITIVE CONTROL (nearest trading day) %s -> %d B, LastModified(UTC)=%s"
                  % (c["Key"], c["Size"], c["LastModified"]))
        if not hit:
            d_ok += 1
            continue
        # a slice EXISTS -- decide WHO wrote it, and when.
        for c in hit:
            lm = _iso(c["LastModified"])
            inside = run_start <= lm <= run_end
            n, sao, vh = _vhash(p, TARGET)
            print("      SLICE EXISTS: %s  %d B  LastModified(UTC)=%s  INSIDE EG-s-15's run window "
                  "(%s -> %s)? -> %s"
                  % (c["Key"], c["Size"], c["LastModified"], run_start.isoformat(),
                     run_end.isoformat(), inside))
            print("        rows=%s  source_as_of=%s  value-sha=%s" % (n, sao, vh))
            neigh = []
            for nd in ("2026-09-04", "2026-09-05", "2026-09-06", "2026-09-08"):
                nn, nsao, nvh = _vhash(p, nd)
                if nvh:
                    neigh.append("%s rows=%s source_as_of=%s value-sha=%s" % (nd, nn, nsao, nvh))
            for line in neigh:
                print("        NEIGHBOUR %s" % line)
            print("        UPSTREAM-PRODUCER FACT, NAMED NOT GRADED: this slice PREDATES EG-s-15's "
                  "run, so it is not this system repairing a closed day into a number -- which is "
                  "what FWD-4 forbids. Row W1-S31; carried out of this project by the issuer."
                  if not inside else
                  "        WRITTEN INSIDE THE RUN WINDOW -- this WOULD be this system backfilling "
                  "a closed day.")
            if not inside:
                d_ok += 1
                predating.append("%s (%s, rows=%s, value-sha=%s)" % (c["Key"], c["LastModified"],
                                                                     n, vh))
    arm("d", d_ok == len(partners),
        "%d of %d partner(s) from the artifact's own list carry NO slice for %s written by "
        "EG-s-15's run or by any backfill against it (every existing slice's LastModified lies "
        "OUTSIDE the run window); upstream-producer slices that PREDATE the run, printed and named "
        "not graded: %s"
        % (d_ok, len(partners), TARGET, predating if predating else "none"))

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
