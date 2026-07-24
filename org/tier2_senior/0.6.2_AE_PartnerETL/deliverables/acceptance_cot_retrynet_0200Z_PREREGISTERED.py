"""PRE-REGISTERED acceptance check for the cot retry-net generalization (545bde4e9).

Written 2026-07-24 ~1520Z, BEFORE the ~02:00Z run, deliberately: pre-registering the criteria means
the verdict cannot be rationalized after seeing the outcome. Run as-is; do not edit thresholds after
looking at results. If a criterion turns out to be wrong, say so explicitly and say WHY -- do not
quietly retune it (that is the acceptance-item-5 failure I already made once today).

Verifies TWO AXES per CTO/design, plus the mutant control and the coverage denominator.

Usage:  python acceptance_0200Z.py
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys

BUCKET = "opal-data-cot"
PREFIX = "forwardfill_v2"
TARGET_DATE = "2026-07-23"          # the date the net must recover unattended
TABLES = ("allocations", "unrealized")

# Neighbour class, measured 2026-07-24 from the landed 07-22 objects (the re-land I verified):
#   allocations 342,860 B / 1,521 rows   unrealized 4,802,196 B / 67,163 rows
# Gates are the SAME ones the nightly itself uses (>=50% of neighbour), stated here so the
# acceptance is not a softer test than production's own guard.
NEIGHBOUR = {
    "allocations": {"bytes": 342_860, "rows": 1_521, "row_gate": 760},
    "unrealized":  {"bytes": 4_802_196, "rows": 67_163, "row_gate": 33_603},
}
STUB_BYTES = {"allocations": 4_305, "unrealized": 3_744}   # max observed 0-row size


def sh(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def head(table: str, date: str):
    key = f"{PREFIX}/{table}/{table.upper()}_DAILY_{date}.xlsx"
    out = sh(["aws", "s3api", "head-object", "--bucket", BUCKET, "--key", key,
              "--query", "[ContentLength,LastModified,ETag]", "--output", "text"]).strip()
    if not out:
        return None
    parts = out.split("\t")
    return {"key": key, "bytes": int(parts[0]), "last_modified": parts[1], "etag": parts[2]}


def sidecar(table: str, date: str):
    key = f"{PREFIX}/{table}/_complete/{date}.json"
    out = sh(["aws", "s3", "cp", f"s3://{BUCKET}/{key}", "-"])
    try:
        return json.loads(out)
    except Exception:
        return None


def marker(run_date: str):
    out = sh(["aws", "s3", "cp", f"s3://{BUCKET}/{PREFIX}/_retry_net/{run_date}.json", "-"])
    try:
        return json.loads(out)
    except Exception:
        return None


def main() -> int:
    print("=" * 78)
    print("PRE-REGISTERED ACCEPTANCE -- cot retry-net generalization @545bde4e9")
    print(f"target as-of {TARGET_DATE}   checked {dt.datetime.now(dt.timezone.utc):%Y-%m-%dT%H:%M:%SZ}")
    print("=" * 78)
    results: dict[str, bool] = {}

    # ---- AXIS 1 + 2: the object landed, on BOTH size-class and row-count-proxy axes ----
    for t in TABLES:
        h = head(t, TARGET_DATE)
        if h is None:
            print(f"\n[{t}] NOT LANDED -- no object at as-of {TARGET_DATE}")
            results[f"{t}_landed"] = False
            results[f"{t}_size_class"] = False
            results[f"{t}_not_stub"] = False
            results[f"{t}_sidecar"] = False
            continue
        nb = NEIGHBOUR[t]
        ratio = h["bytes"] / nb["bytes"]
        print(f"\n[{t}] landed {h['last_modified']}  {h['bytes']:,} B  (neighbour {nb['bytes']:,} B, ratio {ratio:.3f})")
        results[f"{t}_landed"] = True
        # AXIS A -- object size-class vs the neighbour (>=50%, same shape as the row gate)
        results[f"{t}_size_class"] = ratio >= 0.50
        # AXIS B -- independent of size: it must not be a header-only stub
        results[f"{t}_not_stub"] = h["bytes"] > STUB_BYTES[t] * 1.5
        # sidecar must appear, and must be MEASURED (a heal-forward INFERRED one is NOT acceptance:
        # the point is that the net RE-PULLED the day, not that it inferred an old object was fine)
        sc = sidecar(t, TARGET_DATE)
        if sc is None:
            print("       sidecar: ABSENT")
            results[f"{t}_sidecar"] = False
        else:
            basis = sc.get("basis")
            rows = sc.get("has_data_rows")
            print(f"       sidecar: basis={basis} has_data_rows={rows} inferred={sc.get('inferred')}")
            results[f"{t}_sidecar"] = (rows == 1)
            results[f"{t}_sidecar_MEASURED"] = (basis != "content_probe_backfill")

    # ---- The run marker: three states, and the coverage denominator ----
    print("\n" + "-" * 78)
    for rd in (TARGET_DATE, "2026-07-24", "2026-07-25"):
        m = marker(rd)
        if m:
            print(f"retry_net marker {rd}: {json.dumps(m)[:600]}")
            results["marker_present"] = True
            break
    else:
        print("retry_net marker: ABSENT for 07-23/24/25 -- the sweep may not have written one")
        results["marker_present"] = False

    # ---- MUTANT CONTROL: a date OUTSIDE the 5-bday lookback must remain un-swept ----
    # 2026-07-08 is far outside; it is a known 0-row pre-guard date and must NOT have been re-landed.
    print("-" * 78)
    old = head("allocations", "2026-07-08")
    if old:
        is_stub = old["bytes"] <= STUB_BYTES["allocations"] * 1.5
        print(f"MUTANT CONTROL allocations@2026-07-08: {old['bytes']:,} B  modified {old['last_modified']}")
        print(f"  still the pre-guard stub (not re-landed): {is_stub}")
        results["mutant_old_date_unswept"] = is_stub
    else:
        results["mutant_old_date_unswept"] = False

    # ---- COVERAGE DENOMINATOR -- state what this verdict is OF ----
    print("-" * 78)
    print("COVERAGE DENOMINATOR: this verdict covers 2 tables x 1 as-of date (2026-07-23) in "
          "s3://opal-data-cot only. It does NOT cover holdings (already had a net), the bd tree "
          "(deliberately un-synced, CTO ruling), or any other as-of date.")

    print("=" * 78)
    for k, v in results.items():
        print(f"  {k:36s} {'PASS' if v else '*** FAIL ***'}")
    verdict = all(results.values())
    print(f"\nVERDICT: {'PASS' if verdict else 'NOT PASS'}")
    print("NOTE: a NOT-PASS caused by BD still not publishing 07-23 is NOT a defect in the net -- "
          "check the run log for a 0-row REJECT before concluding anything about the fix.")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
