#!/usr/bin/env python3
"""NFRA_GCONTR value-limb: the CVO-owned period_defs value-check for the benchmark contract.

The VALUE limb of the benchmark graph_contract (PRD 3.3): runs the SERVED benchmark column against
its period_defs -- a served number that does NOT reproduce from the source-of-truth via the DOCUMENTED
canonical transform is a violation, INDEPENDENT of who wrote it. This is the codified BMKAUD WS-2
(the SmartX-override incident: 1M=last-complete-calendar-month replaced the canonical trailing-1M).

Grounded on DS~B's 2026-06-01 reproduce harness (bmkaud_ws2_reproduce_harness~B.py): reproduce the
served values from the source PKL via the DEPLOYED yang lambda's OWN functions
(get_term_returns + calculate_period_returns), diff against served. The contract's period_defs are the
declared semantic; the deployed transform is the canonical realization of them; a served value that
matches NEITHER = a non-canonical write (e.g. the last-complete-month 1M signature).

READ-ONLY. Acceptance = a LIVE exercise (this run against the current source PKL + served) MUST reproduce
all cells, AND a Phase-3 replay (inject a last-complete-month 1M) MUST flag it -- joint with AE's Q2 JOIN.

Usage: value_check_benchmark_period_defs.py [--pkl <s3|local>] [--served <s3|local>] [--tol 0.01]
Exit 0 = all served cells reproduce (value-limb CLEAN). Exit 2 = a violation (LOUD, never silently fine).
"""
from __future__ import annotations
import argparse
import json
import os
import pickle
import subprocess
import sys
import tempfile

# The deployed canonical transform -- the SAME functions the yang producer runs (not a re-implementation).
YANG_LAMBDA_DIR = ("infra/aws/lambda/v2_portal/yang_pipeline/portfolios/"
                   "yang-model-portfolio-benchmarks")
SRC_PKL_DEFAULT = "s3://opal-data-portal-v2/benchmarks/"                       # latest data_YYYYMMDD_v1.pkl
SERVED_DEFAULT = "s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json"

# The contract's 1M semantic (benchmark-model-portfolios.period_defs["1M"]) and the incident signature.
CONTRACT_1M = "trailing-1-calendar-month -> as-of"
VIOLATION_1M_SIGNATURE = "last-complete-calendar-month"   # the SmartX override BMKAUD caught


def _fetch(loc: str) -> str:
    """Return a local path for an s3://... or local location (read-only pull to a temp file)."""
    if not loc.startswith("s3://"):
        return loc
    fd, path = tempfile.mkstemp(suffix=os.path.basename(loc) or ".bin")
    os.close(fd)
    subprocess.run(["aws", "s3", "cp", loc, path], check=True, capture_output=True)
    return path


def _latest_pkl(prefix: str) -> str:
    if not prefix.startswith("s3://"):
        return prefix
    out = subprocess.run(["aws", "s3", "ls", prefix], capture_output=True, text=True).stdout
    pkls = sorted(line.split()[-1] for line in out.splitlines() if line.strip().endswith("_v1.pkl"))
    if not pkls:
        raise SystemExit(f"ERROR: no data_*_v1.pkl under {prefix}")
    return prefix + pkls[-1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkl", default=SRC_PKL_DEFAULT)
    ap.add_argument("--served", default=SERVED_DEFAULT)
    ap.add_argument("--tol", type=float, default=0.01)
    a = ap.parse_args()

    sys.path.insert(0, YANG_LAMBDA_DIR)
    import lambda_function as lf  # the DEPLOYED canonical transform

    pkl_path = _fetch(_latest_pkl(a.pkl))
    served_path = _fetch(a.served)
    with open(pkl_path, "rb") as fh:
        data_pkl = pickle.load(fh)
    served = json.load(open(served_path))

    term = lf.get_term_returns(data_pkl)
    end_date = term.index.max()
    periods = served["periods"]
    served_models = {m["code"]: m["returns"] for m in served["models"]}
    print(f"VALUE-CHECK benchmark: repro_end={end_date.date()} served_as_of={served.get('data_as_of')} "
          f"periods={len(periods)} models={len(served_models)}")

    FIELDS = ["model", "index_benchmark", "etf_benchmark", "index_spread", "etf_spread"]
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

    print(f"CHECKED {checked} cells | VIOLATIONS {len(violations)}")
    if violations:
        print("VALUE-LIMB VIOLATION -- a served value does NOT reproduce from the source PKL via the "
              "canonical yang transform (period_defs breach, independent of writer):")
        print(f"  {'model':4} {'period':6} {'field':16} {'SERVED':>14} {'CANONICAL(PKL)':>16}")
        for code, period, f, s, r in violations:
            flag = "  <-- 1M-SIGNATURE (last-complete-month?)" if period == "1M" else ""
            print(f"  {code:4} {period:6} {f:16} {str(s):>14} {str(r):>16}{flag}")
        print(f"\nBMKAUD-class: the served number the contract's period_defs['1M']='{CONTRACT_1M}' does not "
              f"reproduce -> candidate '{VIOLATION_1M_SIGNATURE}' override. LOUD, exit 2.")
        return 2
    print("VALUE-LIMB CLEAN: every served cell reproduces from the source PKL via the canonical transform.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
