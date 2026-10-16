"""ADVI_COTBKF CB-cw-1 (worker ~190): the FWD-3 one-account exercise, read by hand from the SERVED objects.

READ-ONLY. Two get_object calls at the pinned VersionIds (daily_returns, month_grades). Nothing is written to S3.
The account is picked BY RULE (most graded months = MATCH or DIFF rows of month_grades; ties to the smallest sha256
hex of the account id). The account id stays in memory: it is never printed or written; only its 8 hex digits are.

Strings each month of the account's daily returns the way commonwealth_monthly_grade.py does
((prod(1 + return) - 1) * 100 over the month's rows; absent when any day of the month has a null return), compares
with the served computed_pct (equal within 1e-6 percentage points) and with Commonwealth's reported_month_pct
(MATCH when abs(diff) <= 0.05 percentage points), and counts the reported and benchmark figures that are readable.

Prints counts only, and writes the numbers to the path given as argv[1] (a scratch file, never committed).
  python -I cw1_fwd3_exercise_read.py <numbers.json>
"""
import hashlib
import io
import json
import math
import re
import sys

import boto3
import pandas as pd
import pyarrow.parquet as pq

BUCKET = "opal-data-assets"
BASE = "commonwealth/cottonwood/silver/%s/date=2026-06-23/part-00000.parquet"
VERSIONS = {"daily_returns": "lNzQMjfx6uX2zdFdWKsDANboShtDUz2N", "month_grades": "nkTE.F82uFSboXr9PEamIENCwFL9cwcC"}
TOL = 0.05
MG_COLS = ["account", "month", "computed_pct", "reported_month_pct", "verdict", "reason", "reported_year_pct",
           "reported_itd_pct", "benchmark_month_pct", "benchmark_year_pct", "benchmark_itd_pct", "reported_note"]
DR_COLS = ["account", "date", "return", "blank_reason"]

s3 = boto3.client("s3", region_name="us-east-1")


def read(t, cols):
    resp = s3.get_object(Bucket=BUCKET, Key=BASE % t, VersionId=VERSIONS[t])
    df = pq.read_table(io.BytesIO(resp["Body"].read()), columns=cols).to_pandas()
    return df, resp.get("VersionId")


def h8(acct):
    return hashlib.sha256(str(acct).encode("utf-8")).hexdigest()[:8]


def cat(text):
    """Category of a served reason text: digits collapsed, so counts and values do not split a category."""
    return re.sub(r"[-+]?\d+(\.\d+)?", "N", str(text)) if text is not None and text == text else "(null)"


mg, mg_v = read("month_grades", MG_COLS)
dr, dr_v = read("daily_returns", DR_COLS)
assert mg_v == VERSIONS["month_grades"] and dr_v == VERSIONS["daily_returns"], "served VersionId mismatch"

# ---- population (whole tables, counts only)
pop = dict(months=int(len(mg)), match=int((mg["verdict"] == "MATCH").sum()), diff=int((mg["verdict"] == "DIFF").sum()),
           ungradable=int((mg["verdict"] == "UNGRADABLE").sum()), days=int(len(dr)), blank_days=int(dr["return"].isna().sum()))
pop_other = int(len(mg) - pop["match"] - pop["diff"] - pop["ungradable"])

# ---- selection by rule
graded = mg[mg["verdict"].isin(["MATCH", "DIFF"])].groupby("account").size()
top = int(graded.max())
cands = sorted(graded[graded == top].index.astype(str), key=lambda a: hashlib.sha256(a.encode("utf-8")).hexdigest())
acct = cands[0]
hash8 = h8(acct)

# ---- the account's days
d = dr[dr["account"].astype(str) == acct].copy().sort_values("date")
d["mon"] = pd.to_datetime(d["date"]).dt.strftime("%Y-%m")
days = int(len(d))
first, last = str(d["date"].min()), str(d["date"].max())
blank = d[d["return"].isna()]
blank_by_reason = {str(k): int(v) for k, v in blank["blank_reason"].fillna("(none recorded)").value_counts().items()}

# ---- string the days into months
strung = {}
blank_reason_by_month = {}
for mon, g in d.groupby("mon"):
    r = g["return"]
    if r.isna().any():
        strung[mon] = None
        first_blank = g[g["return"].isna()].sort_values("date").iloc[0]["blank_reason"]
        blank_reason_by_month[mon] = str(first_blank) if first_blank is not None and first_blank == first_blank else "(none recorded)"
    else:
        strung[mon] = (math.prod(1.0 + float(x) for x in r.tolist()) - 1.0) * 100.0

# ---- the account's graded months, compared
m = mg[mg["account"].astype(str) == acct].copy().sort_values("month")
months = int(len(m))
eq_present = eq_both_absent = match = differ = ungr = agree_served_verdict = 0
served_verdicts = {}
diffs, ungr_rows = [], []
for _, row in m.iterrows():
    mon = str(row["month"])
    s = strung.get(mon)
    s_present = s is not None
    comp = row["computed_pct"]
    comp_present = comp == comp
    rep = row["reported_month_pct"]
    rep_ok = rep == rep and math.isfinite(rep)
    if s_present and comp_present and abs(s - float(comp)) <= 1e-6:
        eq_present += 1
    if (not s_present) and (not comp_present):
        eq_both_absent += 1
    if (not s_present) or (not rep_ok):
        verdict = "UNGRADABLE"
        ungr += 1
        if mon not in strung:
            why = "no daily returns for the month"
        elif not s_present:
            why = "blank day: %s" % blank_reason_by_month.get(mon, "(none recorded)")
        else:
            why = "reported value null"
        ungr_rows.append({"month": mon, "kind": "UNGRADABLE", "reason": why, "served_reason_category": cat(row["reason"])})
    elif abs(s - float(rep)) <= TOL:
        verdict = "MATCH"
        match += 1
    else:
        verdict = "DIFF"
        differ += 1
    sv = str(row["verdict"])
    served_verdicts[sv] = served_verdicts.get(sv, 0) + 1
    if sv == verdict:
        agree_served_verdict += 1

months_with_days_no_grade = sorted(set(strung) - set(m["month"].astype(str)))
months_grade_no_days = sorted(set(m["month"].astype(str)) - set(strung))

# ---- readable reported and benchmark figures
readable = {
    "reported_month": int(m["reported_month_pct"].notna().sum()),
    "reported_year": int(m["reported_year_pct"].notna().sum()),
    "reported_itd": int(m["reported_itd_pct"].notna().sum()),
    "benchmark_month": int(m["benchmark_month_pct"].notna().sum()),
    "benchmark_year": int(m["benchmark_year_pct"].notna().sum()),
    "benchmark_itd": int(m["benchmark_itd_pct"].notna().sum()),
}
note_counts = {str(k): int(v) for k, v in m["reported_note"].fillna("(null)").map(cat).value_counts().items()}
absent_by_field = {f: int(months - int(m[f].notna().sum())) for f in
                   ["reported_month_pct", "reported_year_pct", "reported_itd_pct",
                    "benchmark_month_pct", "benchmark_year_pct", "benchmark_itd_pct"]}

out = dict(
    served=dict(daily_returns_version=dr_v, month_grades_version=mg_v, rows_read_daily=int(len(dr)), rows_read_months=int(len(mg))),
    account_hash8=hash8, selected_hash8_check=h8(cands[0]), tie_count=int(len(cands)), top_graded=top,
    span=dict(first=first, last=last), days=days,
    blank_days=dict(count=int(len(blank)), by_reason=blank_by_reason),
    months=months, strung_equals_served_computed=eq_present, strung_eq_incl_both_absent=eq_present + eq_both_absent,
    both_absent_months=eq_both_absent, matches_reported=match, differ=differ, ungradable=ungr,
    recomputed_grade_eq_served_verdict=agree_served_verdict, served_verdict_counts_account=served_verdicts,
    months_with_days_no_grade=months_with_days_no_grade, months_grade_no_days=months_grade_no_days,
    differences=ungr_rows, readable=readable, absent_by_field=absent_by_field, reported_note_category_counts=note_counts,
    population=pop, population_other_verdicts=pop_other,
)

text = json.dumps(out, indent=1, sort_keys=True, default=str)
assert acct not in text, "account id leaked into output"
with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as fh:
    fh.write(text + "\n")

print("SERVED daily_returns=%s month_grades=%s rows_daily=%d rows_months=%d" % (dr_v, mg_v, len(dr), len(mg)))
print("SELECT account_hash8=%s ties=%d top_graded=%d" % (hash8, len(cands), top))
print("SPAN first=%s last=%s days=%d blank_days=%d by_reason=%s" % (first, last, days, len(blank), json.dumps(blank_by_reason, sort_keys=True)))
print("MONTHS total=%d strung_equals_served=%d (both_absent=%d) matched=%d differ=%d ungradable=%d recomputed_eq_served_verdict=%d"
      % (months, eq_present, eq_both_absent, match, differ, ungr, agree_served_verdict))
print("MONTHS_WITH_DAYS_NO_GRADE=%d MONTHS_GRADE_NO_DAYS=%d" % (len(months_with_days_no_grade), len(months_grade_no_days)))
print("SERVED_VERDICTS_ACCOUNT %s" % json.dumps(served_verdicts, sort_keys=True))
print("UNGRADABLE_BY_CATEGORY %s" % json.dumps(
    {k: sum(1 for r in ungr_rows if r["reason"] == k) for k in sorted(set(r["reason"] for r in ungr_rows))}, sort_keys=True))
print("UNGRADABLE_MONTHS %s" % json.dumps([r["month"] for r in ungr_rows]))
print("UNGRADABLE_SERVED_REASON_CATEGORY %s" % json.dumps(
    {k: sum(1 for r in ungr_rows if r["served_reason_category"] == k) for k in sorted(set(r["served_reason_category"] for r in ungr_rows))}, sort_keys=True))
print("READABLE %s" % json.dumps(readable, sort_keys=True))
print("ABSENT_BY_FIELD %s" % json.dumps(absent_by_field, sort_keys=True))
print("REPORTED_NOTE_CATEGORY %s" % json.dumps(note_counts, sort_keys=True))
print("POPULATION %s other_verdicts=%d" % (json.dumps(pop, sort_keys=True), pop_other))
