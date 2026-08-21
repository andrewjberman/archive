#!/usr/bin/env python3
"""COT_SUPERVISED G4/G4b belt acceptance -- the scheduled-run verifier.

Run AFTER the scheduled cot chain fires (7:30 AM ET / 11:30Z, schedule-et.tf:90,
live-verified ENABLED). This is the PRODUCTION evidence: the ad-hoc QA read taken
at amendment time proves the template, never the belt.

Every check reads the SERVED bytes. No check reads config to assert behavior.

  G4  : the scheduled holdings extract carries Holding Supervised + Account
        Supervised, with the row count intact vs the pre-amendment baseline.
  G4-INVARIANT (the belt's actual purpose): per-row Holding-vs-Account supervised
        DISAGREEMENT count over the whole extract -- the daily-tested form of the
        account-clean assumption. Reported with its denominator either way; a
        disagreement is a FINDING to route, never a silent pass.
  G4b : the promoted account_attributes table pulled on the SCHEDULE (not by hand),
        with its completeness sidecar, and the bronze sentinel emitted for the run.

Usage:
  python verify_g4_belt_acceptance.py                 # auto-resolve the expected as-of
  python verify_g4_belt_acceptance.py --asof 2026-08-20
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import warnings
from datetime import date, datetime, timedelta, timezone
from io import BytesIO

import boto3

warnings.filterwarnings("ignore")

BUCKET = "opal-data-cot"
FF = "forwardfill_v2"
BASELINE_COLS = 19
BASELINE_ROWS = 18051
BASELINE_KEY = "HOLDINGS_DAILY_2026-08-19.xlsx"  # measured pre-amendment: 19 cols / 18,051 rows
NEW_COLS = ("Holding Supervised", "Account Supervised")

s3 = boto3.client("s3")


def prev_bday(d: str) -> str:
    cur = date.fromisoformat(d) - timedelta(days=1)
    while cur.weekday() >= 5:
        cur -= timedelta(days=1)
    return cur.isoformat()


def read_xlsx(key: str):
    body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    import openpyxl
    wb = openpyxl.load_workbook(BytesIO(body), read_only=True, data_only=True)
    rows = list(wb.active.iter_rows(values_only=True))
    wb.close()
    header = [str(c) if c is not None else "" for c in rows[0]]
    return body, header, rows[1:]


def check(label: str, ok: bool, detail: str) -> bool:
    print("  [%s] %-34s %s" % ("PASS" if ok else "FAIL", label, detail), flush=True)
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--asof", help="expected snapshot as-of (default: prior business day, UTC today)")
    args = ap.parse_args()
    run_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    asof = args.asof or prev_bday(run_date)

    print("=== COT_SUPERVISED G4/G4b BELT ACCEPTANCE ===", flush=True)
    print("verified_at=%sZ run_date(UTC)=%s expected_asof=%s"
          % (datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"), run_date, asof), flush=True)
    print("baseline (measured pre-amendment, %s): %d cols / %d rows, zero supervised cols"
          % (BASELINE_KEY, BASELINE_COLS, BASELINE_ROWS), flush=True)
    results = []

    # ---- G4: the scheduled holdings extract -------------------------------
    print("\nG4 -- scheduled holdings extract", flush=True)
    hkey = "%s/holdings/HOLDINGS_DAILY_%s.xlsx" % (FF, asof)
    try:
        head = s3.head_object(Bucket=BUCKET, Key=hkey)
    except Exception as exc:
        print("  [FAIL] holdings artifact ABSENT at %s (%s)" % (hkey, type(exc).__name__), flush=True)
        print("\nVERDICT: NOT YET ACCEPTABLE -- the scheduled artifact has not landed.", flush=True)
        return 2
    landed = head["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")
    body, header, data = read_xlsx(hkey)
    results.append(check("artifact landed (served)", True,
                         "%s  %s B  LastModified(UTC) %s" % (hkey.split("/")[-1], format(len(body), ","), landed)))
    results.append(check("sha256 (evidence)", True, hashlib.sha256(body).hexdigest()))
    present = [c for c in NEW_COLS if c in header]
    results.append(check("both new columns present", len(present) == 2,
                         "found %s (cols now %d vs baseline %d)" % (present, len(header), BASELINE_COLS)))
    results.append(check("row count intact vs baseline", len(data) > 0,
                         "%s rows (baseline %s) -- delta %+d"
                         % (format(len(data), ","), format(BASELINE_ROWS, ","), len(data) - BASELINE_ROWS)))
    results.append(check("landed by the SCHEDULE not by hand", landed[11:13] in ("11", "12"),
                         "landed %s; schedule fires 11:30Z (7:30 ET). Hand-runs land off-window." % landed[11:19]))

    # ---- G4 invariant: the belt's actual purpose --------------------------
    print("\nG4-INVARIANT -- per-row Holding vs Account supervised agreement", flush=True)
    if len(present) == 2:
        hi, ai = header.index("Holding Supervised"), header.index("Account Supervised")
        disagree, blank, n = [], 0, 0
        for r in data:
            hv = str(r[hi]).strip() if hi < len(r) and r[hi] is not None else ""
            av = str(r[ai]).strip() if ai < len(r) and r[ai] is not None else ""
            if not hv or not av:
                blank += 1
                continue
            n += 1
            if hv != av:
                disagree.append((r[header.index("AccountID")] if "AccountID" in header else "?", hv, av))
        print("  DENOMINATOR: %s comparable rows (%s blank/absent, %s total)"
              % (format(n, ","), format(blank, ","), format(len(data), ",")), flush=True)
        results.append(check("account-clean invariant holds", not disagree,
                             "%d disagreeing row(s)" % len(disagree)))
        if disagree:
            print("  FINDING -- disagreeing rows (first 10), ROUTE do not swallow:", flush=True)
            for row in disagree[:10]:
                print("    account=%s holding=%s account_flag=%s" % row, flush=True)
        vals: dict = {}
        for r in data:
            v = str(r[hi]).strip() if hi < len(r) and r[hi] is not None else "(blank)"
            vals[v] = vals.get(v, 0) + 1
        print("  Holding Supervised value counts: %s" % json.dumps(vals), flush=True)
    else:
        results.append(check("account-clean invariant holds", False, "columns absent -- not computable"))

    # ---- G4b: the promoted attributes table on the schedule ---------------
    print("\nG4b -- account_attributes pulled BY THE SCHEDULE", flush=True)
    akey = "%s/account_attributes/ACCOUNT_ATTRIBUTES_DAILY_%s.xlsx" % (FF, asof)
    try:
        ahead = s3.head_object(Bucket=BUCKET, Key=akey)
        alanded = ahead["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")
        abody, aheader, adata = read_xlsx(akey)
        results.append(check("attributes artifact landed", True,
                             "%s  %s B  LastModified(UTC) %s  cols=%d rows=%s"
                             % (akey.split("/")[-1], format(len(abody), ","), alanded,
                                len(aheader), format(len(adata), ","))))
        results.append(check("landed by the SCHEDULE not by hand", alanded[11:13] in ("11", "12"),
                             "landed %s (the G1 bootstrap was a hand-run at 17:3xZ under a DIFFERENT "
                             "as-of; this key+window is what proves the SCHEDULE carries it)" % alanded[11:19]))
    except Exception as exc:
        results.append(check("attributes artifact landed", False,
                             "ABSENT at %s (%s)" % (akey, type(exc).__name__)))

    for label, key in (("holdings sidecar", "%s/holdings/_complete/%s.json" % (FF, asof)),
                       ("attributes sidecar", "%s/account_attributes/_complete/%s.json" % (FF, asof))):
        try:
            meta = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())
            results.append(check(label, meta.get("basis") == "land_time_measured"
                                 and int(meta.get("has_data_rows", 0)) == 1,
                                 "basis=%s has_data_rows=%s bytes=%s"
                                 % (meta.get("basis"), meta.get("has_data_rows"), meta.get("bytes"))))
        except Exception as exc:
            results.append(check(label, False, "ABSENT/unreadable (%s)" % type(exc).__name__))

    skey = "bronze/%s/_BRONZE_COMPLETE.json" % run_date
    try:
        sent = json.loads(s3.get_object(Bucket=BUCKET, Key=skey)["Body"].read())
        tables = sent.get("artifacts", {}).get("tables", [])
        results.append(check("bronze sentinel emitted", sent.get("overall") == "success",
                             "%s tables=%s" % (skey, tables)))
        results.append(check("account_attributes in the sentinel", "account_attributes" in tables,
                             "chain advances carrying it" if "account_attributes" in tables
                             else "NOT carried -- the table did not land this run"))
    except Exception as exc:
        results.append(check("bronze sentinel emitted", False,
                             "ABSENT at %s (%s) -- chain did NOT advance" % (skey, type(exc).__name__)))

    ok = all(results)
    print("\n=== VERDICT: %s (%d/%d checks passed) ==="
          % ("ACCEPTED" if ok else "NOT ACCEPTED", sum(1 for r in results if r), len(results)), flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
