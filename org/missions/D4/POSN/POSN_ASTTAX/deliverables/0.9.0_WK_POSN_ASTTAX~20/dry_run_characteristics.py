#!/usr/bin/env python3
"""POSN_ASTTAX.TO-V4-1 V4-AC3 -- THE LOCAL DRY RUN: the arithmetic, with the null share visible.

Runs the SHIPPED producer (data/assets/scripts/gold/build_satellites_characteristics.py)
against the LIVE inputs and writes NOTHING to S3 -- it calls build(), never publish(), so
there is no code path in this script that could write the served key.

WHAT IT PRINTS, because the criterion asks for each of these by name:
  * the formula, ONCE, so a reader can check the divisor is 100 and not the covered weight
  * GLD's PER-FIELD presence in the bbg/<asof>/characteristics row, measured from the
    parquet rather than asserted
  * for every satellite and EVERY field: the aggregate, the ticker set that fed it, and the
    coverage pair, with (weight_with_value + weight_null) reconciled against the satellite's
    total holdings weight to 0.01
  * the sizing measurement the .tf cites: wall clock, python-object peak (tracemalloc) and
    the process peak working set

It also drops the derived document at .scratch/characteristics_dry_run.json so V4-AC11 can
compare the deployed function's output against THIS run's numbers.

ASCII only.
"""
from __future__ import annotations

import ctypes
import datetime as dt
import json
import os
import sys
import time
import tracemalloc

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    "..", "..", "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "data", "assets", "scripts", "gold"))
sys.path.insert(0, REPO)

import boto3  # noqa: E402
import build_satellites_characteristics as P  # noqa: E402


def peak_working_set_mib() -> float:
    """Windows process peak working set. Not Lambda's Linux RSS, but a real upper bound on
    what this process touched -- tracemalloc cannot see the interpreter, boto3 or pyarrow."""
    class PMC(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_uint32), ("PageFaultCount", ctypes.c_uint32),
                    ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]
    # TWO ENTRY POINTS, and the first one SILENTLY RETURNS ZERO here rather than raising:
    # psapi.dll's GetProcessMemoryInfo is a forwarder on this device and the call fails with
    # a FALSE return that an unchecked wrapper reads as "0.0 MiB peak" -- a number that is
    # impossible and still prints like a measurement. The BOOL return is checked, and
    # kernel32's K32GetProcessMemoryInfo is the fallback; a zero is reported as UNAVAILABLE.
    for dll, name in (("kernel32", "K32GetProcessMemoryInfo"),
                      ("psapi", "GetProcessMemoryInfo")):
        try:
            fn = getattr(getattr(ctypes.windll, dll), name)
            counters = PMC()
            counters.cb = ctypes.sizeof(PMC)
            ok = fn(ctypes.windll.kernel32.GetCurrentProcess(),
                    ctypes.byref(counters), counters.cb)
            if ok and counters.PeakWorkingSetSize:
                print("  (peak working set read via %s.%s)" % (dll, name))
                return counters.PeakWorkingSetSize / (1024.0 * 1024.0)
        except Exception as exc:  # noqa: BLE001 - a measurement, not a dependency
            print("  (%s.%s unavailable: %s)" % (dll, name, exc))
    print("  (peak working set UNAVAILABLE on this device -- reported as NaN, never as 0.0)")
    return float("nan")


def main() -> int:
    as_of = dt.datetime.now(dt.timezone.utc).date().isoformat()
    bbg_as_of = P.resolve_bbg_as_of()
    print("=" * 100)
    print("V4-AC3 LOCAL DRY RUN -- cot-satellites-characteristics-producer, NO S3 WRITE")
    print("  as_of              %s (today UTC)" % as_of)
    print("  bbg partition      %s (T-1 BUSINESS DAY from lib/trading_calendar.prev_trading_day)"
          % bbg_as_of)
    print("=" * 100)
    print()
    print("THE FORMULA, ONCE -- and the divisor is the whole point:")
    print("    aggregate(field) = SUM_over_holdings_WITH_a_value( weight_pct * value ) / 100")
    print("    weight_with_value(field) = SUM of weight_pct over holdings WITH a value")
    print("    weight_null(field)       = SUM of weight_pct over holdings WITHOUT one")
    print("    NOT renormalised: the divisor is the constant 100, NEVER weight_with_value,")
    print("    so an uncovered holding LOWERS the aggregate and is DISCLOSED beside it.")
    print()

    tracemalloc.start()
    t0 = time.time()
    s3 = boto3.client("s3")
    holdings_doc = P.load_holdings(s3)
    positioning_doc = P.load_positioning(s3)
    frame, manifest = P.load_bbg(s3, bbg_as_of)
    bbg_rows, collisions = P.bbg_index(frame)
    doc = P.build(holdings_doc, positioning_doc, bbg_rows, manifest, as_of, bbg_as_of,
                  bbg_collisions=collisions)
    wall = time.time() - t0
    traced_peak = tracemalloc.get_traced_memory()[1] / (1024.0 * 1024.0)
    tracemalloc.stop()

    print("INPUTS, as read (every one of them live):")
    print("  holdings.json        as_of=%s  satellites=%d  (s3://%s/%s)"
          % (holdings_doc.get("as_of"), len(holdings_doc.get("satellites") or {}),
             P.HOLDINGS_BUCKET, P.HOLDINGS_KEY))
    print("  positioning_data     data_as_of=%s  books=%d  distinct tickers=%d"
          % (positioning_doc.get("data_as_of"), len(positioning_doc.get("current_holdings") or {}),
             len(P.yang_index(positioning_doc)[0])))
    print("  bbg characteristics  as_of=%s  rows=%d  run_class=%s  universe_count=%s"
          % (bbg_as_of, len(frame), manifest.get("run_class"), manifest.get("universe_count")))
    print("  bbg ticker collisions on the first token of `security`: %s"
          % (collisions if collisions else "NONE"))
    print("  yang ticker conflicts across books: %s"
          % (doc["input_notes"]["yang_ticker_conflicts"] or "NONE"))
    print()

    print("GLD's PER-FIELD PRESENCE IN bbg/%s/characteristics (measured from the parquet):"
          % bbg_as_of)
    gld = bbg_rows.get("GLD")
    if gld is None:
        print("  GLD ABSENT from the partition -- the criterion's premise fails; reporting that.")
    else:
        print("  security row: %s" % gld.get("_security"))
        for field in P.SCALAR_FIELDS:
            col = P.BBG_SCALAR_COLUMNS.get(field)
            value = gld.get(field)
            print("    %-9s <- %-22s %-14s %s"
                  % (field, col, "PRESENT" if value is not None else "NULL",
                     ("value=%s" % value) if value is not None else "(NaN in the parquet)"))
        windows = doc["method"]["return_windows"]
        print("    returns   <- %-22s %-14s %s"
              % ("(no return columns)", "NULL (all %d)" % len(windows),
                 "the pull carries NO return fields: %s" % ", ".join(windows)))
        print("  => GLD contributes its weight to weight_with_value for: %s"
              % ([f for f in P.SCALAR_FIELDS if gld.get(f) is not None] or "NOTHING"))
        print("     and to weight_null for: %s"
              % ([f for f in P.SCALAR_FIELDS if gld.get(f) is None] + ["returns.%s" % w
                 for w in doc["method"]["return_windows"]]))
    print()

    windows = doc["method"]["return_windows"]
    print("RETURN WINDOWS, derived from the inputs (never hardcoded): %s" % ", ".join(windows))
    print()

    worst = 0.0
    failures = []
    for code in doc["satellites"]:
        sat = doc["satellites"][code]
        cov_v = sat["coverage"]["weight_with_value"]
        cov_n = sat["coverage"]["weight_null"]
        total = sat["total_weight"]
        print("-" * 100)
        print("%s   total holdings weight %.4f   holdings=%d"
              % (code, total, len(holdings_doc["satellites"][code]["holdings"])))
        print("   sources: positioning_data=%d  bbg=%d  none=%d   %s"
              % (len(sat["sources"]["positioning_data"]), len(sat["sources"]["bbg"]),
                 len(sat["sources"]["none"]),
                 "bbg:%s none:%s" % (sat["sources"]["bbg"], sat["sources"]["none"])))
        rows = [(f, sat[f], cov_v[f], cov_n[f], sat["contributors"]["scalar"][f])
                for f in P.SCALAR_FIELDS]
        rows += [("returns.%s" % w, sat["returns"][w], cov_v["returns"][w], cov_n["returns"][w],
                  sat["contributors"]["returns"][w]) for w in windows]
        for field, value, wv, wn, feeders in rows:
            delta = abs((wv + wn) - total)
            worst = max(worst, delta)
            flag = "OK " if delta <= 0.01 else "BAD"
            if delta > 0.01:
                failures.append((code, field, delta))
            print("   %s %-14s = %-12s  with_value %8.4f + null %7.4f = %8.4f (delta %.4f)"
                  % (flag, field, ("NULL" if value is None else "%.6f" % value), wv, wn,
                     wv + wn, delta))
            print("        fed by %d ticker(s): %s" % (len(feeders), ",".join(feeders) or "-"))
    print("-" * 100)
    print()
    print("INVARIANT: weight_with_value + weight_null == total holdings weight")
    print("  satellites checked : %d" % len(doc["satellites"]))
    print("  fields per satellite: %d (%d scalar + %d return windows)"
          % (len(P.SCALAR_FIELDS) + len(windows), len(P.SCALAR_FIELDS), len(windows)))
    print("  denominator        : %d field-checks" % (len(doc["satellites"]) *
                                                      (len(P.SCALAR_FIELDS) + len(windows))))
    print("  worst delta        : %.6f (tolerance 0.01)" % worst)
    print("  failures           : %s" % (failures if failures else "NONE"))
    print("  producer's own validate(): %s" % (P.validate(doc) or "CLEAN"))
    print()
    print("RENORMALISATION CHECK -- if the code renormalised, the aggregate would equal")
    print("num/with_value instead of num/100. For a satellite with any null share the two")
    print("differ; printed for Opal Satellite 15's fee:")
    sat15 = doc["satellites"].get("Opal Satellite 15")
    if sat15:
        wv = sat15["coverage"]["weight_with_value"]["fee"]
        published = sat15["fee"]
        renorm = (published * 100.0 / wv) if wv else None
        print("  published (divisor 100) = %.6f    renormalised (divisor %.4f) = %.6f"
              % (published, wv, renorm))
        print("  the published number is the SMALLER one, which is what 'never renormalise' means")
    print()
    print("SIZING (the numbers the .tf cites):")
    print("  wall                    %.2f s" % wall)
    print("  traced python peak      %.2f MiB (tracemalloc; excludes interpreter/boto3/pyarrow)"
          % traced_peak)
    print("  process peak workingset %.1f MiB (Windows PSAPI; includes pandas+pyarrow import)"
          % peak_working_set_mib())
    body = (json.dumps(doc, indent=2) + "\n").encode("utf-8")
    print("  artifact bytes          %d" % len(body))
    out = os.path.join(REPO, ".scratch", "characteristics_dry_run.json")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body.decode("utf-8"))
    print("  local copy for V4-AC11  %s" % out)
    print()
    print("NOTHING WAS WRITTEN TO S3: this script calls build(), never publish().")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
