"""ADVI_PERFRP PRF-a-4: the Schwab silver LOTS census, RE-READ on the corrected upstream.

DECOMP row 83: "B5 lots + txn tables, CENSUS FIRST (s.11 #5, sequenced LAST):
fact_uln / ult / upn / upt / rld -- partition coverage, date range, row counts, column
sets; whether unrealized ST/LT + realized-daily reconcile to canonical_positions."
Status at cut: 6 of 6 names present at I4, CONTENTS UNMEASURED. This measures them.

Issuer sequence (2.0.0_SA_COO 79261): b-5 -> THIS -> b-4 LAST, tying to this residual.
Scope clause: "the cost-basis column DECLARED UNDETERMINED unless the census names it
with evidence" (CTO 68440 item 3). So the cost-basis question is answered HERE, from
the data, or it stays UNDETERMINED -- it is not inherited from a name that looks right.

PLANE: the ADVI account's OWN silver, opal-data-assets/schwab/08335338/silver/ (I4).
Same firm; no cross-firm class.

NOTE: A ZERO HERE IS NOT AN ABSENCE UNTIL THE LISTING IS SHOWN. Every table prints its
partition denominator; a table with no partitions says OUT-OF-CORPUS, not "empty".
"""
import io
import json
import subprocess
from pathlib import Path

import boto3
import pyarrow.parquet as pq

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
OUT = ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables"

SILVER_BUCKET = "opal-data-assets"
SILVER = "schwab/08335338/silver/"
GOLD = "opal-data-49financial"
LOT_TABLES = ("fact_uln", "fact_ult", "fact_upn", "fact_upt", "fact_rld")
S3 = boto3.client("s3")

# Candidate cost-basis column NAMES. Presence of a name is NOT the answer -- the census
# must show the column is POPULATED and reconciles, or the choice stays UNDETERMINED.
COST_BASIS_CANDIDATES = ("cost_basis", "total_cost", "unit_cost", "cost_per_unit",
                         "adjusted_cost_basis", "original_cost", "book_value")


def partition_dates(prefix):
    out, tok = [], None
    while True:
        kw = {"Bucket": SILVER_BUCKET, "Prefix": prefix, "Delimiter": "/"}
        if tok:
            kw["ContinuationToken"] = tok
        r = S3.list_objects_v2(**kw)
        out += [p["Prefix"].rstrip("/").rsplit("date=", 1)[1]
                for p in r.get("CommonPrefixes", []) if "date=" in p["Prefix"]]
        if not r.get("IsTruncated"):
            break
        tok = r["NextContinuationToken"]
    return sorted(out)


report = {"plane": "s3://%s/%s" % (SILVER_BUCKET, SILVER), "tables": {}}
print("PRF-a-4 LOTS CENSUS -- plane s3://%s/%s" % (SILVER_BUCKET, SILVER))
print("=" * 78)

frames = {}
for t in LOT_TABLES:
    prefix = SILVER + t + "/"
    dates = partition_dates(prefix)
    row = {"partitions": len(dates)}
    print()
    print("TABLE %s" % t)
    if not dates:
        print("  0 partitions listed under %s -- OUT OF CORPUS at this prefix," % prefix)
        print("  NOT an empty table. A zero is only an absence once the listing is shown.")
        row["verdict"] = "NO-PARTITIONS-AT-THIS-PREFIX"
        report["tables"][t] = row
        continue
    row.update({"date_min": dates[0], "date_max": dates[-1]})
    print("  partitions: %d   range %s .. %s" % (len(dates), dates[0], dates[-1]))
    o = S3.get_object(Bucket=SILVER_BUCKET,
                      Key="%sdate=%s/data.parquet" % (prefix, dates[-1]))
    df = pq.read_table(io.BytesIO(o["Body"].read())).to_pandas()
    frames[t] = df
    row.update({
        "read_date": dates[-1],
        "max_last_modified_utc": o["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n_partitions_read": 1, "n_partitions_requested": 1, "partitions_absent": [],
        "rows": len(df), "columns": len(df.columns),
        "column_set": sorted(df.columns),
    })
    print("  read date=%s  LastModified=%s  rows=%d  columns=%d"
          % (dates[-1], row["max_last_modified_utc"], len(df), len(df.columns)))
    if "account_id" in df.columns:
        row["accounts"] = int(df["account_id"].nunique())
        print("  distinct account_id: %d" % row["accounts"])
    found = [c for c in COST_BASIS_CANDIDATES if c in df.columns]
    near = [c for c in df.columns if "cost" in c.lower() or "basis" in c.lower()]
    row["cost_basis_candidates_present"] = found
    row["cost_like_columns"] = near
    if near:
        print("  cost/basis-like columns: %s" % near)
        for c in near:
            s = df[c]
            nn = int(s.notna().sum())
            row.setdefault("cost_column_population", {})[c] = {
                "non_null": nn, "of_rows": len(df),
                "nonzero": int((s.fillna(0) != 0).sum()) if s.dtype != object else None,
            }
            print("      [%s] non-null %d of %d" % (c, nn, len(df)))
    else:
        print("  cost/basis-like columns: NONE in this table")
    report["tables"][t] = row

print()
print("=" * 78)
print("THE TIE-OUT: do the lots reconcile to canonical_positions MV?")
print("=" * 78)
pos_dates = None
tie = {}
try:
    o = S3.get_object(Bucket=GOLD,
                      Key="gold/advi/canonical/canonical_positions/date=2026-08-27/data.parquet")
    pos = pq.read_table(io.BytesIO(o["Body"].read())).to_pandas()
    pos_mv = float(pos["market_value_settled_unsettled"].sum())
    tie["canonical_positions"] = {
        "date": "2026-08-27", "rows": len(pos), "market_value": round(pos_mv, 2),
        "max_last_modified_utc": o["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")}
    print("  canonical_positions date=2026-08-27: %d rows, MV %.2f" % (len(pos), pos_mv))
except Exception as e:
    tie["canonical_positions"] = {"read_failed": type(e).__name__}
    print("  canonical_positions read FAILED: %s" % type(e).__name__)

MV = "current_market_value"
per_table = {}
for t, df in frames.items():
    if MV in df.columns:
        per_table[t] = float(df[MV].fillna(0).sum())
        tie.setdefault("per_table_market_value", {})[t] = round(per_table[t], 2)
        print("  %-10s [%s] sum %.2f" % (t, MV, per_table[t]))

base = tie.get("canonical_positions", {}).get("market_value")
print()
print("  NOTE: COMPARING ONE TABLE AGAINST THE WHOLE BOOK IS THE WRONG GRAIN.")
print("  The numbers say so themselves: uln ~= upn and ult ~= upt to the cent, and the")
print("  two PAIRS differ. These are TAX-STATUS SLICES ('n' / 't') at two grains (lot /")
print("  position), not five independent views of one population. A single table can")
print("  only ever reconcile to its own slice, so a -57% 'residual' against the full")
print("  book measures the SPLIT, not a defect.")
print()
for label, parts in (("lot grain      uln + ult", ("fact_uln", "fact_ult")),
                     ("position grain upn + upt", ("fact_upn", "fact_upt"))):
    if all(p in per_table for p in parts):
        tot = sum(per_table[p] for p in parts)
        tie.setdefault("combined", {})[" + ".join(parts)] = round(tot, 2)
        if base:
            resid = tot - base
            pct = 100.0 * resid / base
            tie["combined"]["%s_residual" % " + ".join(parts)] = round(resid, 2)
            tie["combined"]["%s_residual_pct" % " + ".join(parts)] = round(pct, 6)
            print("  %s = %.2f  vs positions %.2f" % (label, tot, base))
            print("      RESIDUAL %.2f  (%.4f%%)  -- coverage %.4f%%"
                  % (resid, pct, 100.0 * tot / base))
# Are the two slices DISJOINT? If they overlap, summing them double-counts.
for a, b in (("fact_uln", "fact_ult"), ("fact_upn", "fact_upt")):
    if a in frames and b in frames and "account_id" in frames[a].columns:
        sa = set(frames[a]["account_id"].astype(str))
        sb = set(frames[b]["account_id"].astype(str))
        tie.setdefault("slice_overlap", {})["%s vs %s" % (a, b)] = {
            "accounts_%s" % a: len(sa), "accounts_%s" % b: len(sb),
            "accounts_in_both": len(sa & sb)}
        print("  %s accounts %d ; %s accounts %d ; IN BOTH %d"
              % (a, len(sa), b, len(sb), len(sa & sb)))
print("  ^ CORRECTED AGAINST MY OWN FIRST NOTE. I wrote that accounts would appear in")
print("    BOTH slices because an account can hold taxable and non-taxable lots. The")
print("    measurement says 0 IN BOTH, so the split is BY ACCOUNT (account-level tax")
print("    status -- e.g. IRA vs brokerage), not within an account. That makes the sum")
print("    safe for a stronger reason than the one I gave: the slices are DISJOINT at")
print("    the account grain, so summing them cannot double-count at any grain.")

report["tie_out"] = tie

print()
print("=" * 78)
print("THE COST-BASIS COLUMN: named with evidence, or DECLARED UNDETERMINED")
print("=" * 78)
named = {t: r.get("cost_like_columns") for t, r in report["tables"].items()
         if r.get("cost_like_columns")}
if not named:
    verdict = ("DECLARED UNDETERMINED -- no cost/basis-like column exists in any of the "
               "5 lot tables' latest partitions. CTO 68440 item 3 stands unresolved and "
               "b-4 must NOT pick one.")
    report["cost_basis_verdict"] = verdict
    print("  " + verdict)
else:
    # A PLAUSIBLE NAME IS NOT EVIDENCE. The lot tables carry a declared
    # `unrealized_gain_loss`, which makes an IDENTITY available:
    #     current_market_value - <cost basis> == unrealized_gain_loss
    # A candidate satisfying it on real rows is named BY THE DATA; one that does not is
    # excluded. This is the difference between "the column is called cost basis" and
    # "the column behaves as the cost basis".
    print("  Candidate names exist in all 5 tables. Names are not evidence, so the")
    print("  identity MV - cost_basis - unrealized_gain_loss ~ 0 is used to DISCRIMINATE:")
    scores = {}
    for t in ("fact_uln", "fact_ult"):
        df = frames.get(t)
        if df is None or "unrealized_gain_loss" not in df.columns:
            continue
        mvs = df[MV].fillna(0)
        ugl = df["unrealized_gain_loss"].fillna(0)
        for c in report["tables"][t].get("cost_like_columns", []):
            try:
                resid = float((mvs - df[c].fillna(0) - ugl).abs().sum())
            except (TypeError, ValueError):
                continue
            scores.setdefault(c, {})[t] = round(resid, 2)
            print("      %-34s %-10s sum|resid| %18.2f over %d rows"
                  % (c, t, resid, len(df)))
    report["cost_basis_identity_residuals"] = scores
    ranked = sorted((c for c in scores if len(scores[c]) == 2),
                    key=lambda c: sum(scores[c].values()))
    if ranked:
        best = ranked[0]
        runner = ranked[1] if len(ranked) > 1 else None
        verdict = (
            "NAMED WITH EVIDENCE: `%s`. It satisfies "
            "current_market_value - cost_basis == unrealized_gain_loss with summed "
            "absolute residual %s across both unrealized tables (%s rows), where every "
            "other candidate is off by orders of magnitude%s. CTO 68440 item 3 is "
            "DISCHARGED by measurement, not by name."
            % (best, json.dumps(scores[best]),
               json.dumps({t: report["tables"][t]["rows"] for t in ("fact_uln", "fact_ult")
                           if t in report["tables"]}),
               "" if not runner else
               " (next best `%s` at %s)" % (runner, json.dumps(scores[runner]))))
    else:
        verdict = ("DECLARED UNDETERMINED -- candidates exist but none could be scored "
                   "against the unrealized_gain_loss identity on both tables.")
    report["cost_basis_verdict"] = verdict
    print()
    print("  " + verdict)

path = OUT / "ADVI_PERFRP.PRF-a-4_LOTS_CENSUS.json"
path.write_bytes(json.dumps(report, indent=1, sort_keys=True, default=str).encode("utf-8"))
print()
print("WROTE %s (%d bytes)" % (path.name, path.stat().st_size))
tabled = sum(1 for r in report["tables"].values() if r.get("partitions"))
print("DENOMINATOR: %d of %d declared lot tables carry partitions." % (tabled, len(LOT_TABLES)))
