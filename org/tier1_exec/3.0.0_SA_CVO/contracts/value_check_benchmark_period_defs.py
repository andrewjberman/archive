#!/usr/bin/env python3
"""NFRA_GCONTR value-limb: the CVO-owned period_defs value-check for the benchmark contract.

The VALUE limb of the benchmark graph_contract (PRD 3.3): runs the SERVED benchmark column against
its period_defs -- a served number that does NOT reproduce from the source-of-truth via the DOCUMENTED
canonical transform is a violation, INDEPENDENT of who wrote it. This is the codified BMKAUD WS-2
(the SmartX-override incident: 1M=last-complete-calendar-month replaced the canonical trailing window).

Grounded on DS~B's 2026-06-01 reproduce harness (bmkaud_ws2_reproduce_harness~B.py): reproduce the
served values from the source PKL via the DEPLOYED yang lambda's OWN functions
(get_term_returns + calculate_period_returns), diff against served.

METHODOLOGY-OF-RECORD (Andrew ruling 2026-06-01, BMKAUD WS-3, directive 631d8d0d9): the canonical
1M / 1Q are TRAILING 30 / 91 CALENDAR DAYS -- deliberately NOT calendar-month/quarter windows, and
NOT last-complete-calendar-period. See docs/briefs/bmkaud-ws3-methodology-walkthrough-20260601.md.

DETECTION-POWER GATE (added 2026-07-09 after the live exercise -- the reason this file changed):
the trailing-Nd window and the last-complete-calendar-period window COINCIDE EXACTLY at certain
as-of dates -- measured, not assumed:
  * 1M: as-of = month-end of a 30-day month (Apr/Jun/Sep/Nov). e.g. as-of 2026-06-30,
        (05-31, 06-30] == June -> canonical and violation differ by 0.00 on all 5 models.
  * 1Q: as-of = quarter-end whose quarter spans exactly 91 days (Q2 = 30+31+30).
        e.g. as-of 2026-06-30, (03-31, 06-30] == Q2 -> delta 0.00 on all 5 models.
At such an as-of a BMKAUD-class override is INDISTINGUISHABLE from canonical, so a "clean" result on
that column is NOT evidence of no-violation. The check MUST say so out loud rather than report CLEAN
(TO-3 acceptance: an unreviewable surface reads LOUD, never silently "fine"). Exit 4 covers this.

READ-ONLY. Source PKL is resolved the way the PRODUCER resolves it (benchmarks/LATEST.json ->
data_pkl), not by an ls-sort -- an ls-sort picks model_*.pkl over data_*.pkl (m > d) and cannot see a
pointer that names a version the listing filter excludes.

VACUITY GATE (added 2026-07-09 after feeding this check its own degenerate input -- it FAILED):
**A gate whose checks pass VACUOUSLY on the degenerate input is not a gate.** An assertion over a set is
vacuously TRUE on the empty set. Fed a served artifact with `periods: []`, this script reported
`CHECKED 0 cells | VIOLATIONS 0` and printed "every served cell reproduces" -- a clean bill for an artifact
containing nothing. Every conformance limb agreed, because there was nothing to disagree about.
This is the same defect as `C_02:310` (existence, not rows), `A_00:337` (`sorted()[-1]` onto a 0-row stub),
and the bd/49F `QTD entry_count = 0` outage that served an empty window for 39.8h while `mtime`, `size`,
`generated_at` and `data_as_of` all advanced correctly. **Always pair a conformance limb with a
NON-EMPTINESS limb, and run the non-emptiness limb FIRST.** Exit 5 covers this.

Usage: value_check_benchmark_period_defs.py [--pkl <s3|local>] [--served <s3|local>] [--tol 0.01]
Exit 0 = all served cells reproduce AND every rolling window is discriminating at this as-of.
Exit 2 = VIOLATION (loud).
Exit 3 = VINTAGE-SKEW: served as-of != reproduced as-of, so a diff would be meaningless. Undecidable.
Exit 4 = cells reproduce, but >=1 rolling window is UNDISCRIMINATING at this as-of (partial coverage).
Exit 5 = VACUOUS: the served artifact carried nothing to check. NEVER a pass.
"""
from __future__ import annotations
import argparse
import json
import os
import pickle
import shutil
import subprocess
import sys
import tempfile

import pandas as pd

# Windows resolves `aws` to aws.CMD; a bare "aws" argv[0] raises WinError 2 under CreateProcess.
AWS = shutil.which("aws") or "aws"

# The deployed canonical transform -- the SAME functions the yang producer runs (not a re-implementation).
YANG_LAMBDA_DIR = ("infra/aws/lambda/v2_portal/yang_pipeline/portfolios/"
                   "yang-model-portfolio-benchmarks")
SRC_BUCKET = "opal-data-portal-v2"
LATEST_KEY = "benchmarks/LATEST.json"              # the PRODUCER's own pointer (get_latest_data_pkl_key)
SRC_PKL_PREFIX = f"s3://{SRC_BUCKET}/benchmarks/"
SERVED_DEFAULT = f"s3://{SRC_BUCKET}/json/benchmarks/model_portfolio_benchmarks.json"

# The ratified 1M/1Q semantics and the incident signature they must stay distinct from.
CONTRACT_PERIODS = {
    "1M": "trailing-30-calendar-days -> as-of (Andrew ruling 2026-06-01, 631d8d0d9)",
    "1Q": "trailing-91-calendar-days -> as-of (Andrew ruling 2026-06-01, 631d8d0d9)",
}
VIOLATION_SIGNATURE = "last-complete-calendar-period (the reverted SmartX override)"

EXIT_CLEAN, EXIT_VIOLATION, EXIT_VINTAGE_SKEW, EXIT_UNDISCRIMINATING, EXIT_VACUOUS = 0, 2, 3, 4, 5
FIELDS = ["model", "index_benchmark", "etf_benchmark", "index_spread", "etf_spread"]
LEGS = ["model", "index_benchmark", "etf_benchmark"]


def _fetch(loc: str) -> str:
    """Return a local path for an s3://... or local location (read-only pull to a temp file)."""
    if not loc.startswith("s3://"):
        return loc
    fd, path = tempfile.mkstemp(suffix=os.path.basename(loc) or ".bin")
    os.close(fd)
    subprocess.run([AWS, "s3", "cp", loc, path], check=True, capture_output=True)
    return path


def _exists(bucket: str, key: str) -> bool:
    r = subprocess.run([AWS, "s3api", "head-object", "--bucket", bucket, "--key", key],
                       capture_output=True)
    return r.returncode == 0


def _resolve_source_pkl(pkl_arg: str) -> str:
    """Resolve the source PKL the way the PRODUCER does: benchmarks/LATEST.json -> data_pkl.

    Falls back to the newest data_*.pkl by name if the pointer is dangling, and says so LOUDLY --
    a dangling canonical pointer is itself a finding, never a silent fallback.
    """
    if not pkl_arg.startswith("s3://"):
        return pkl_arg                                   # explicit local override (replay / fixture)
    if pkl_arg != SRC_PKL_PREFIX:
        return pkl_arg                                   # explicit s3 object override

    latest = json.load(open(_fetch(f"s3://{SRC_BUCKET}/{LATEST_KEY}")))
    key = latest.get("data_pkl") or latest.get("files", {}).get("data_pkl")
    if key and _exists(SRC_BUCKET, key):
        print(f"SOURCE: {key} (via {LATEST_KEY}, producer-parity)")
        return f"s3://{SRC_BUCKET}/{key}"

    print(f"WARN: canonical pointer {LATEST_KEY} is DANGLING -- data_pkl={key!r} does not exist "
          f"(version={latest.get('version')!r}). The producer's get_latest_data_pkl_key() fallback "
          f"path cannot resolve. Falling back to newest data_*.pkl by name; REPORT THIS.")
    out = subprocess.run([AWS, "s3", "ls", SRC_PKL_PREFIX], capture_output=True, text=True).stdout
    names = [ln.split()[-1] for ln in out.splitlines() if ln.strip()]
    # data_ prefix ONLY -- an unfiltered sort picks model_*.pkl (m > d), the wrong artifact entirely.
    data_pkls = sorted(n for n in names if n.startswith("data_") and n.endswith(".pkl"))
    if not data_pkls:
        raise SystemExit(f"ERROR: no data_*.pkl under {SRC_PKL_PREFIX}")
    print(f"SOURCE: benchmarks/{data_pkls[-1]} (ls-fallback -- pointer dangling)")
    return SRC_PKL_PREFIX + data_pkls[-1]


def _last_complete_month(series, end_date):
    m_end = end_date if end_date == end_date + pd.offsets.MonthEnd(0) else \
        end_date.replace(day=1) - pd.Timedelta(days=1)
    return series[(series.index >= m_end.replace(day=1)) & (series.index <= m_end)]


def _last_complete_quarter(series, end_date):
    q_end = end_date if end_date == end_date + pd.offsets.QuarterEnd(0) else \
        end_date.replace(month=((end_date.month - 1) // 3) * 3 + 1, day=1) - pd.Timedelta(days=1)
    q_start = q_end.replace(month=((q_end.month - 1) // 3) * 3 + 1, day=1)
    return series[(series.index >= q_start) & (series.index <= q_end)]


def _discrimination(lf, term, end_date, tol):
    """Can this check TELL canonical apart from the BMKAUD violation semantic at this as-of?

    Returns {period: (discriminating, max_abs_delta)}. If the two windows coincide the check is
    structurally blind on that column and a 'clean' there says nothing.
    """
    windows = {"1M": _last_complete_month, "1Q": _last_complete_quarter}
    out = {}
    for period, viol_window in windows.items():
        worst = 0.0
        for code in lf.MODEL_CODES:
            for leg in LEGS:
                ser = term.get(lf.INDEX_NAME_MAP[code][leg])
                if ser is None:
                    continue
                canon = lf.calculate_period_returns(ser, end_date, period)["return"]
                viol = lf.compound_returns(viol_window(ser, end_date))
                if canon is None or viol is None:
                    continue
                worst = max(worst, abs(canon - viol))
        out[period] = (worst > tol, round(worst, 4))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkl", default=SRC_PKL_PREFIX)
    ap.add_argument("--served", default=SERVED_DEFAULT)
    ap.add_argument("--tol", type=float, default=0.01)
    a = ap.parse_args()

    sys.path.insert(0, YANG_LAMBDA_DIR)
    import lambda_function as lf  # the DEPLOYED canonical transform

    with open(_fetch(_resolve_source_pkl(a.pkl)), "rb") as fh:
        data_pkl = pickle.load(fh)
    served = json.load(open(_fetch(a.served)))

    term = lf.get_term_returns(data_pkl)
    end_date = term.index.max()
    periods = served["periods"]
    served_models = {m["code"]: m["returns"] for m in served["models"]}
    served_as_of = served.get("data_as_of")
    print(f"VALUE-CHECK benchmark: repro_end={end_date.date()} served_as_of={served_as_of} "
          f"periods={len(periods)} models={len(served_models)}")

    # --- Gate -1: VACUITY. Runs FIRST. An assertion over a set is vacuously true on the empty set,
    # so a conformance check on an artifact containing nothing reports a clean bill for nothing. ---
    expected_cells = len(lf.MODEL_CODES) * len(periods) * len(FIELDS)
    if not periods or not served_models or expected_cells == 0:
        print(f"VACUOUS: the served artifact carried nothing to check "
              f"(periods={len(periods)}, models={len(served_models)}, expected_cells={expected_cells}). "
              f"Every conformance limb would pass because there is nothing to disagree about. "
              f"A gate whose checks pass vacuously on the degenerate input is not a gate. "
              f"NEVER a pass. exit {EXIT_VACUOUS}.")
        return EXIT_VACUOUS

    # --- Gate 0: vintage. A diff across vintages measures data drift, not a period_defs breach. ---
    if served_as_of and str(end_date.date()) != str(served_as_of):
        print(f"VINTAGE-SKEW: served data_as_of={served_as_of} but source PKL reproduces to "
              f"{end_date.date()}. A cell diff here would measure DATA DRIFT, not a period_defs "
              f"breach. UNDECIDABLE -- re-run vintage-matched. exit {EXIT_VINTAGE_SKEW}.")
        return EXIT_VINTAGE_SKEW

    # --- Gate 1: detection power at this as-of (measured, per rolling window). ---
    disc = _discrimination(lf, term, end_date, a.tol)

    violations, checked = [], 0
    for code in lf.MODEL_CODES:
        mp = lf.INDEX_NAME_MAP[code]
        ms, ix, et = term.get(mp["model"]), term.get(mp["index_benchmark"]), term.get(mp["etf_benchmark"])
        for period in periods:
            mr = lf.calculate_period_returns(ms, end_date, period)["return"]
            ir = lf.calculate_period_returns(ix, end_date, period)["return"]
            er = lf.calculate_period_returns(et, end_date, period)["return"]
            repro = {"model": mr, "index_benchmark": ir, "etf_benchmark": er,
                     "index_spread": (round(mr - ir, 2) if mr is not None and ir is not None else None),
                     "etf_spread": (round(mr - er, 2) if mr is not None and er is not None else None)}
            srv = served_models.get(code, {}).get(period, {})
            for f in FIELDS:
                checked += 1
                a_, b_ = srv.get(f), repro[f]
                if a_ is None and b_ is None:
                    continue
                if a_ is None or b_ is None or abs(a_ - b_) > a.tol:
                    violations.append((code, period, f, a_, b_))

    if checked == 0:   # belt-and-braces: the loop compared nothing. Never report clean.
        print(f"VACUOUS: 0 cells compared. A clean result here is a clean bill for nothing. "
              f"NEVER a pass. exit {EXIT_VACUOUS}.")
        return EXIT_VACUOUS

    print(f"CHECKED {checked} cells (expected {expected_cells}) | VIOLATIONS {len(violations)}")
    print("DETECTION POWER (canonical vs '" + VIOLATION_SIGNATURE + "') at this as-of:")
    for period, (ok, delta) in sorted(disc.items()):
        verdict = "DISCRIMINATING" if ok else "UNDISCRIMINATING -- windows COINCIDE, check is BLIND"
        print(f"  {period}: max|canonical-violation| = {delta:.4f} (tol {a.tol}) -> {verdict}")

    if violations:
        print("VALUE-LIMB VIOLATION -- a served value does NOT reproduce from the source PKL via the "
              "canonical yang transform (period_defs breach, independent of writer):")
        print(f"  {'model':4} {'period':6} {'field':16} {'SERVED':>14} {'CANONICAL(PKL)':>16}")
        for code, period, f, s, r in violations:
            flag = "  <-- BMKAUD-SIGNATURE" if period in CONTRACT_PERIODS else ""
            print(f"  {code:4} {period:6} {f:16} {str(s):>14} {str(r):>16}{flag}")
        breached = sorted({p for _, p, _, _, _ in violations if p in CONTRACT_PERIODS})
        for p in breached:
            print(f"\nBMKAUD-class: served '{p}' does not reproduce under the contract's "
                  f"period_defs['{p}']='{CONTRACT_PERIODS[p]}' -> candidate {VIOLATION_SIGNATURE}.")
        print(f"LOUD, exit {EXIT_VIOLATION}.")
        return EXIT_VIOLATION

    blind = sorted(p for p, (ok, _) in disc.items() if not ok)
    if blind:
        print(f"\nCLEAN-BUT-UNDISCRIMINATING: every served cell reproduces, but {', '.join(blind)} "
              f"CANNOT be adjudicated at as-of {end_date.date()} -- the canonical trailing window and "
              f"the {VIOLATION_SIGNATURE} window are the SAME set of days, so a BMKAUD override would "
              f"reproduce identically. This is NOT a clean bill for those columns; it is no-coverage. "
              f"Re-exercise at a non-period-end as-of to adjudicate. exit {EXIT_UNDISCRIMINATING}.")
        return EXIT_UNDISCRIMINATING

    print("VALUE-LIMB CLEAN: every served cell reproduces from the source PKL via the canonical "
          "transform, and every rolling window is discriminating at this as-of.")
    return EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
