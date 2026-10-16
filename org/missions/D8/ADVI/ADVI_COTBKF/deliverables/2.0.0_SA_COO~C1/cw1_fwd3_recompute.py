"""ADVI_COTBKF TO-CB-cw-1 (issuer's check): the FWD-3 one-account exercise, recomputed from the SERVED objects.

FWD-3 DONE WHEN: one account's daily returns read across the whole span and checked against the monthly figures Commonwealth reported.
Reads (read-only, one get each, at the pinned VersionIds) the served daily_returns and month_grades; picks the account BY RULE (the account
with the most GRADED months, that is rows of month_grades whose verdict is MATCH or DIFF; a tie goes to the smallest sha256 hex of the account id), strings its daily returns into a monthly return (a month with both sides absent counts as equal, as the order says)
the way commonwealth_monthly_grade.py does ((prod(1 + return) - 1) * 100 over the month's rows; UNGRADABLE when any day of the month has a null
return), and compares with the served computed_pct and with Commonwealth's reported_month_pct (MATCH when abs(diff) <= 0.05 percentage points).

  python cw1_fwd3_recompute.py                -> prints  FWD3-RECOMPUTE account_hash8=<8 hex> days=<n> months=<m> strung_equals_served=<a>
                                                          matches_reported=<b> differ=<c> ungradable=<u>
  python cw1_fwd3_recompute.py <record.json>  -> prints  FWD3-CROSS selected_by_rule=<bool> days_equal=<bool> months_equal=<bool>
                                                          strung_equal=<bool> matched_equal=<bool> differ_equal=<bool> ungradable_equal=<bool> population_equal=<bool>
                                                 comparing the worker's record (keys account_hash8, days, months, strung_equals_served_computed,
                                                 matches_reported, differ, ungradable, population {months, match, diff, ungradable, days, blank_days}) with this independent recompute.
Prints the account only as the first 8 hex digits of sha256(account id); no account id, name or dollar value is printed. Needs AWS read credentials.
"""
import hashlib
import io
import json
import math
import sys

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-assets"
BASE = "commonwealth/cottonwood/silver/%s/date=2026-06-23/part-00000.parquet"
VERSIONS = {"daily_returns": "lNzQMjfx6uX2zdFdWKsDANboShtDUz2N", "month_grades": "nkTE.F82uFSboXr9PEamIENCwFL9cwcC"}
TOL = 0.05


def read(s3, t, cols):
    body = s3.get_object(Bucket=BUCKET, Key=BASE % t, VersionId=VERSIONS[t])["Body"].read()
    return pq.read_table(io.BytesIO(body), columns=cols).to_pandas()


def h8(acct):
    return hashlib.sha256(str(acct).encode("utf-8")).hexdigest()[:8]


def recompute():
    s3 = boto3.client("s3", region_name="us-east-1")
    mg = read(s3, "month_grades", ["account", "month", "computed_pct", "reported_month_pct", "verdict"])
    dr = read(s3, "daily_returns", ["account", "date", "return"])
    counts = mg[mg["verdict"].isin(["MATCH", "DIFF"])].groupby("account").size()
    top = counts.max()
    cands = sorted(counts[counts == top].index.astype(str), key=lambda a: hashlib.sha256(a.encode("utf-8")).hexdigest())
    acct = cands[0]
    m = mg[mg["account"].astype(str) == acct].copy()
    d = dr[dr["account"].astype(str) == acct].copy()
    d["month"] = d["date"].astype(str).str.slice(0, 7)
    strung = {}
    for mon, g in d.groupby("month"):
        r = g["return"]
        strung[mon] = None if r.isna().any() else (math.prod(1.0 + x for x in r.tolist()) - 1.0) * 100.0
    eq = match = differ = ungr = 0
    for _, row in m.iterrows():
        s = strung.get(str(row["month"]))
        comp = row["computed_pct"]
        rep = row["reported_month_pct"]
        if s is not None and comp == comp and abs(s - float(comp)) <= 1e-6:
            eq += 1
        elif s is None and comp != comp:
            eq += 1  # both absent: the days could not be strung and the served table shows no figure (AMENDMENT 1: the order's "or both absent")
        if s is None or rep != rep:
            ungr += 1
        elif abs(s - float(rep)) <= TOL:
            match += 1
        else:
            differ += 1
    pop = dict(months=int(len(mg)), match=int((mg["verdict"] == "MATCH").sum()), diff=int((mg["verdict"] == "DIFF").sum()),
               ungradable=int((mg["verdict"] == "UNGRADABLE").sum()), days=int(len(dr)), blank_days=int(dr["return"].isna().sum()))
    return dict(population=pop, account_hash8=h8(acct), days=int(len(d)), months=int(len(m)), strung_equals_served=eq, matches_reported=match,
                differ=differ, ungradable=ungr, selected_hash8=h8(cands[0]), top_rows=int(top))


r = recompute()
if len(sys.argv) < 2:
    p = r["population"]
    print("FWD3-POPULATION months=%d match=%d diff=%d ungradable=%d days=%d blank_days=%d"
          % (p["months"], p["match"], p["diff"], p["ungradable"], p["days"], p["blank_days"]))
    print("FWD3-RECOMPUTE account_hash8=%s days=%d months=%d strung_equals_served=%d matches_reported=%d differ=%d ungradable=%d"
          % (r["account_hash8"], r["days"], r["months"], r["strung_equals_served"], r["matches_reported"], r["differ"], r["ungradable"]))
else:
    w = json.load(open(sys.argv[1], encoding="utf-8"))
    print("FWD3-CROSS selected_by_rule=%s days_equal=%s months_equal=%s strung_equal=%s matched_equal=%s differ_equal=%s ungradable_equal=%s population_equal=%s"
          % (w.get("account_hash8") == r["selected_hash8"], w.get("days") == r["days"], w.get("months") == r["months"],
             w.get("strung_equals_served_computed") == r["strung_equals_served"], w.get("matches_reported") == r["matches_reported"],
             w.get("differ") == r["differ"], w.get("ungradable") == r["ungradable"], w.get("population") == r["population"]))
