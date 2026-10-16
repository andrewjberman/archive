"""ADVI_COTBKF TO-CB-cy-2, worker 0.9.0_WK_ADVI_COTBKF~193: an independent reproduction of the disjoint UNGRADABLE-month partition.

READ-ONLY. One get_object per served table at its pinned VersionId (daily_returns, month_grades). Recomputes, from the
definitions in the issuer's module docstring (2.0.0_SA_COO~C1/cy2_month_partition.py): the six disjoint categories, the
2x2x2 overlap matrix, the blank-reason sets of the blank-day months and the fill bound (= blank_only_unpriced). Also
counts three sensitivity checks the issuer's four-fragment list does not cover. Prints COUNTS only: no account id,
name or dollar value. With a path argument (default: MONTH_PARTITION_RECORD.json beside this file) it writes the record.

  python -I cy2_own_partition.py [record_path]
"""
import io
import json
import os
import re
import sys

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-assets"
BASE = "commonwealth/cottonwood/silver/%s/date=2026-06-23/part-00000.parquet"
VERSIONS = {"daily_returns": "lNzQMjfx6uX2zdFdWKsDANboShtDUz2N", "month_grades": "nkTE.F82uFSboXr9PEamIENCwFL9cwcC"}
REPORTED = ("no reported monthly return", "reported span", "reported rows disagree", "not finite")
# every reason clause the module commonwealth_monthly_grade.py emits (read at its lines 52-57, 81, 99, 104, 111, 118, 120)
KNOWN = [
    r"no daily returns for the month",
    r"\d+ blank day\(s\) of \d+; first blank reason: [A-Za-z_]+",
    r"no reported monthly return",
    r"reported span \S+\.\.\S+ is not one calendar month",
    r"\d+ reported rows disagree: \[.*\]",
    r"reported value is null",
    r"reported value \S+ is not finite",
]
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RECORD = os.path.join(HERE, "MONTH_PARTITION_RECORD.json")


def fetch(s3, t):
    resp = s3.get_object(Bucket=BUCKET, Key=BASE % t, VersionId=VERSIONS[t])
    if resp.get("VersionId") != VERSIONS[t]:
        raise SystemExit("refused: %s returned VersionId %r, pinned %r" % (t, resp.get("VersionId"), VERSIONS[t]))
    return pq.read_table(io.BytesIO(resp["Body"].read()), columns=COLS[t]).to_pandas(), resp["VersionId"]


COLS = {"daily_returns": ["account", "date", "return", "blank_reason"], "month_grades": ["account", "month", "verdict", "reason"]}


def main():
    s3 = boto3.client("s3", region_name="us-east-1")
    dr, dr_ver = fetch(s3, "daily_returns")
    mg, mg_ver = fetch(s3, "month_grades")
    dr["acct"] = dr["account"].astype(str)
    dr["month"] = dr["date"].astype(str).str.slice(0, 7)
    pairs = dr[["acct", "month"]].drop_duplicates()
    has_daily = set(zip(pairs["acct"], pairs["month"]))
    blank = dr[dr["return"].isna()]
    blank_rows = len(blank)
    blank_reason_null_rows = int(blank["blank_reason"].isna().sum())
    counts = {}
    for a, m in zip(blank["acct"], blank["month"]):
        counts[(a, m)] = counts.get((a, m), 0) + 1
    reasons = {}
    for a, m, r in zip(blank["acct"], blank["month"], blank["blank_reason"].astype(str)):
        reasons.setdefault((a, m), set()).add(r)

    ug = mg[mg["verdict"] == "UNGRADABLE"]
    n_ug = len(ug)
    part = dict(no_daily=0, blank_only_unpriced=0, blank_only_other=0, blank_and_reported=0, reported_only=0, other=0)
    overlap = {}
    blank_sets = dict(only_unpriced=0, unpriced_and_other=0, only_other=0)
    mismatch = unknown = null_rep = null_rep_in_bu = 0
    for a, m, reason in zip(ug["account"].astype(str), ug["month"].astype(str), ug["reason"].astype(str)):
        text = reason.lower()
        rep = any(k in text for k in REPORTED)
        nb = counts.get((a, m), 0)
        has_blank = nb > 0
        no_daily = (a, m) not in has_daily
        rs = reasons.get((a, m), set())
        all_unp = has_blank and rs == {"UNPRICED"}
        if ("blank day" in text) != has_blank:
            mismatch += 1
        if no_daily:
            part["no_daily"] += 1
        elif has_blank and rep:
            part["blank_and_reported"] += 1
        elif has_blank and all_unp:
            part["blank_only_unpriced"] += 1
        elif has_blank:
            part["blank_only_other"] += 1
        elif rep:
            part["reported_only"] += 1
        else:
            part["other"] += 1
        key = (has_blank, rep, no_daily)
        overlap[key] = overlap.get(key, 0) + 1
        if has_blank:
            if rs == {"UNPRICED"}:
                blank_sets["only_unpriced"] += 1
            elif "UNPRICED" in rs:
                blank_sets["unpriced_and_other"] += 1
            else:
                blank_sets["only_other"] += 1
        residue = reason
        for p in KNOWN:
            residue = re.sub(p, "", residue)
        if residue.replace(";", "").strip():
            unknown += 1
        if "reported value is null" in text:
            null_rep += 1
            if has_blank and all_unp and not rep:
                null_rep_in_bu += 1

    n_part = sum(part.values())
    blank_months_ug = sum(blank_sets.values())
    blank_months_total = len(counts)
    print("MONTH-PARTITION-OWN ungradable=%d no_daily=%d blank_only_unpriced=%d blank_only_other=%d blank_and_reported=%d "
          "reported_only=%d other=%d sum_equals=%s text_blank_mismatch=%d"
          % (n_ug, part["no_daily"], part["blank_only_unpriced"], part["blank_only_other"], part["blank_and_reported"],
             part["reported_only"], part["other"], n_part == n_ug, mismatch))
    print("VERSIONS daily_returns=%s month_grades=%s" % (dr_ver, mg_ver))
    print("BLANK-SIDE blank_rows=%d blank_months=%d blank_reason_null_rows=%d" % (blank_rows, len(counts), blank_reason_null_rows))
    for hb, rp, nd in [(False, False, False), (False, False, True), (False, True, False), (False, True, True),
                       (True, False, False), (True, False, True), (True, True, False), (True, True, True)]:
        print("OVERLAP has_blank_day=%s has_reported_clause=%s has_no_daily=%s months=%d"
              % (hb, rp, nd, overlap.get((hb, rp, nd), 0)))
    print("BLANK-REASON-SETS only_unpriced=%d unpriced_and_other=%d only_other=%d total=%d"
          % (blank_sets["only_unpriced"], blank_sets["unpriced_and_other"], blank_sets["only_other"], sum(blank_sets.values())))
    print("SENSITIVITY unknown_clause_months=%d reported_value_null_months=%d null_reported_in_blank_only_unpriced=%d"
          % (unknown, null_rep, null_rep_in_bu))

    if n_part != n_ug or mismatch:
        raise SystemExit("refused: partition does not sum to UNGRADABLE or text/blank mismatch; no record written")
    record_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RECORD
    rec = {
        "measured": True,
        "served": {"daily_returns_version": dr_ver, "month_grades_version": mg_ver},
        "ungradable": n_ug,
        "partition": part,
        "overlap_matrix": [
            {"has_blank_day": hb, "has_reported_clause": rp, "has_no_daily": nd, "months": overlap.get((hb, rp, nd), 0)}
            for hb, rp, nd in [(False, False, False), (False, False, True), (False, True, False), (False, True, True),
                               (True, False, False), (True, False, True), (True, True, False), (True, True, True)]],
        "blank_reason_sets": blank_sets,
        "fill_upper_bound": part["blank_only_unpriced"],
        "earlier_range": {"low": 70943, "high": 74791, "note": "row D1-S18 estimate"},
        "what_this_shows": (
            "Of %d UNGRADABLE months, %d carry at least one blank day and %d do not (%d have no daily_returns row and %d carry only a reported-side clause); "
            "the six disjoint categories sum to %d with no month in two categories. "
            "Of the %d blank-day months, %d also carry a reported-side clause and stay blocked after any fill, so the exact upper bound on months a full UNPRICED fill could make gradable is the %d of blank_only_unpriced, "
            "below the earlier UNPRICED-first count of 74,791 that the census in row D1-S18 gave."
            % (n_ug, blank_months_ug, n_ug - blank_months_ug, part["no_daily"], part["reported_only"], n_part,
               blank_months_ug, part["blank_and_reported"], part["blank_only_unpriced"])),
        "not_established": (
            "Not a promise that any of the %d blank_only_unpriced months would match after a fill, and not conditional on whether a vendor covers the securities "
            "(round 103 other cell measures that); the bound assumes every UNPRICED blank day is priced and nothing else changes. "
            "The month reason text names only the first blank reason in date order, so the blank-reason sets are taken from the daily rows. "
            "Sensitivity: %d UNGRADABLE months carry the clause 'reported value is null' (not one of the four fragments the partition uses), and %d unknown clauses appear outside the module's emitted texts; "
            "%d blank-day months in daily_returns are not UNGRADABLE months of month_grades and sit outside this census (their verdict was not read)."
            % (part["blank_only_unpriced"], null_rep, unknown, blank_months_total - blank_months_ug)),
    }
    with open(record_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rec, f, indent=2)
        f.write("\n")
    print("RECORD-WRITTEN %s" % os.path.basename(record_path))


if __name__ == "__main__":
    main()
