"""ADVI_PERFRP PRF-b-5 / PRFR2DS-AC4: the paged transactions contract, EXERCISED on
REAL fact_trn rows, and a sample paged emission.

AC4: paged per-relationship key; a request without a relationship key REFUSES; page
size + hasMoreResults present; the sec-15 column set honoured with absent columns
declared. PINS as AC1.

WHY THERE IS NO WHOLE-FIRM LEAF HERE, and why that is the criterion being met rather
than dodged: build() REFUSES the perfrp_transactions family because s.11 #6 rules
transactions as a PER-RELATIONSHIP PAGED resource -- "never a firm-wide dump". Emitting
one file with every transaction in it would violate the very rule AC4 tests. So b-5's
product is the paged contract exercised against real upstream rows plus a SAMPLE paged
artifact, not a firm-wide leaf.
"""
import io
import json
import subprocess
import sys
from pathlib import Path

import boto3
import pyarrow.parquet as pq

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/runners_49f"))
EMIT = ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables/emissions"

from perfrp_contract import CONTRACT_VERSION  # noqa: E402
from perfrp_transactions import (  # noqa: E402
    DEFAULT_PAGE_SIZE,
    TXN_BUILD_SIDE_ONLY,
    TXN_CARD_COLUMNS,
    to_card_rows,
    MAX_PAGE_SIZE,
    TXN_SENSITIVE_MEASURED,
    TXN_SERVED_COLUMNS,
    MissingUpstreamColumn,
    TransactionsRefused,
    page_transactions,
    project_rows,
    sensitive_leak_check,
)

SILVER_BUCKET = "opal-data-assets"
TRN_PREFIX = "schwab/08335338/silver/fact_trn/"     # the ADVI account's OWN silver
GOLD = "opal-data-49financial"
S3 = boto3.client("s3")
FAILS = []

# The PRD s.6.2 Transactions row, transcribed from the PRD rather than from the
# allowlist -- transcribing from the implementation would score the implementation's
# blind spot as a pass. Struck-through entries are DECLARED ABSENT with their reason.
PRD_SERVED = ("Date", "Asset Name", "Trade Date", "Account", "Action", "Type",
              "Symbol", "Units", "Price", "Amount")
PRD_DECLARED_ABSENT = {"Description": "NO-SOURCE-TODAY",
                       "Notes": "PII-EXCLUDED-PERMANENT (s.15)"}
# The mapping from the PRD's card names to this projection's column names.
PRD_TO_COLUMN = {
    "Date": "business_date", "Asset Name": "transaction_detail_description",
    "Trade Date": "trade_date", "Account": "account_id",
    "Action": "transaction_source_code_description", "Type": "transaction_category",
    "Symbol": "ticker_symbol", "Units": "quantity", "Price": "price",
    "Amount": "gross_amount",
}


def check(name, cond, detail=""):
    print("  %-58s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


def partition_dates(bucket, prefix):
    out, tok = [], None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix, "Delimiter": "/"}
        if tok:
            kw["ContinuationToken"] = tok
        r = S3.list_objects_v2(**kw)
        out += [p["Prefix"].rstrip("/").rsplit("date=", 1)[1]
                for p in r.get("CommonPrefixes", []) if "date=" in p["Prefix"]]
        if not r.get("IsTruncated"):
            break
        tok = r["NextContinuationToken"]
    return sorted(out)


dates = partition_dates(SILVER_BUCKET, TRN_PREFIX)
asof = dates[-1]
o = S3.get_object(Bucket=SILVER_BUCKET, Key="%sdate=%s/data.parquet" % (TRN_PREFIX, asof))
trn = pq.read_table(io.BytesIO(o["Body"].read())).to_pandas()
trn_pin = {"max_last_modified_utc": o["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"),
           "n_partitions_read": 1, "n_partitions_requested": 1, "partitions_absent": [],
           "partition_date": asof, "bucket": SILVER_BUCKET, "prefix": TRN_PREFIX}
print("fact_trn: %d partitions (%s..%s); read date=%s, %d rows, %d columns"
      % (len(dates), dates[0], dates[-1], asof, len(trn), len(trn.columns)))

ro = S3.get_object(Bucket=GOLD,
                   Key="gold/advi/dimensions/dim_relationship/date=%s/data.parquet" % asof)
rel = pq.read_table(io.BytesIO(ro["Body"].read())).to_pandas()
a2r = rel.drop_duplicates(subset=["account_id"]).set_index(
    "account_id")["relationship_id"].to_dict()
rel_pin = {"max_last_modified_utc": ro["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"),
           "n_partitions_read": 1, "n_partitions_requested": 1, "partitions_absent": [],
           "partition_date": asof}

print()
print("=" * 78)
print("ARM 1 -- a request WITHOUT a relationship key REFUSES (never a firm-wide dump)")
print("=" * 78)
sample = trn.head(5).to_dict("records")
for bad in (None, "", "   "):
    try:
        page_transactions(sample, relationship_id=bad)
        check("refuses relationship_id=%r" % bad, False, "it returned a page")
    except TransactionsRefused:
        check("refuses relationship_id=%r" % bad, True)
try:
    page_transactions(sample)
    check("relationship_id is REQUIRED (no default)", False, "it defaulted")
except TypeError:
    check("relationship_id is REQUIRED (keyword-only, no default)", True)
# POSITIVE CONTROL: a real key must WORK, or the refusals prove nothing.
ok = page_transactions(sample, relationship_id="rel_probe")
check("POSITIVE CONTROL: a real key returns a page", ok["returned"] == len(sample),
      "%d rows" % ok["returned"])

print("=" * 78)
print("ARM 2 -- page size + hasMoreResults, computed from the TOTAL not the page")
print("=" * 78)
rows20 = trn.head(20).to_dict("records")
p0 = page_transactions(rows20, relationship_id="r", page=0, page_size=10)
p1 = page_transactions(rows20, relationship_id="r", page=1, page_size=10)
p2 = page_transactions(rows20, relationship_id="r", page=2, page_size=10)
check("page 0 of 20 @10: returned 10, hasMoreResults True",
      p0["returned"] == 10 and p0["hasMoreResults"] is True)
check("page 1 (the LAST FULL page): hasMoreResults FALSE",
      p1["returned"] == 10 and p1["hasMoreResults"] is False,
      "returned=%d more=%s" % (p1["returned"], p1["hasMoreResults"]))
print("      ^ THE DISCRIMINATING CASE: a full last page. Inferring 'more' from a full")
print("        page would say True here and promise rows that do not exist.")
check("page past the end: 0 rows, hasMoreResults False",
      p2["returned"] == 0 and p2["hasMoreResults"] is False)
check("every page carries page, page_size, returned, total, hasMoreResults",
      all(k in p0 for k in ("page", "page_size", "returned", "total", "hasMoreResults")))
for bad_size in (0, -1, MAX_PAGE_SIZE + 1):
    try:
        page_transactions(rows20, relationship_id="r", page_size=bad_size)
        check("refuses page_size=%d" % bad_size, False)
    except TransactionsRefused:
        check("refuses page_size=%d (bounds 1..%d)" % (bad_size, MAX_PAGE_SIZE), True)
try:
    page_transactions(rows20, relationship_id="r", page=-1)
    check("refuses a negative page", False)
except TransactionsRefused:
    check("refuses a negative page", True)

print("=" * 78)
print("ARM 3 -- the PRD s.6.2 column set, and the DECLARED-ABSENT two")
print("=" * 78)
projected = project_rows(list(trn.columns), trn.head(200).to_dict("records"))
served = set(projected[0].keys()) if projected else set()
print("  PRD enumerated: %d  %s" % (len(PRD_SERVED), list(PRD_SERVED)))
print("  PRD declared absent: %s" % PRD_DECLARED_ABSENT)
missing_prd = [p for p, c in PRD_TO_COLUMN.items() if c not in served]
check("every PRD-enumerated column is served (via its mapped name)", not missing_prd,
      "missing %s" % missing_prd)
check("the BUILD-side projection carries exactly the allowlist",
      served == set(TXN_SERVED_COLUMNS), "%d columns" % len(served))
# THE TRIM, ruled by CTO 79452: the SERVED page is the PRD card ten; the seven
# crosswalk/secondary fields stay BUILD-side. My earlier run REPORTED the 17-vs-10 gap
# rather than closing it, and the ruling closed it.
card = to_card_rows(projected)
card_cols = set(card[0].keys())
check("the SERVED page carries EXACTLY the PRD card ten", card_cols == set(TXN_CARD_COLUMNS),
      "%d columns" % len(card_cols))
check("the card set maps 1:1 onto the PRD's enumerated ten",
      card_cols == {PRD_TO_COLUMN[p] for p in PRD_SERVED})
check("the seven build-side fields are ABSENT from the served page",
      not (card_cols & set(TXN_BUILD_SIDE_ONLY)), str(sorted(TXN_BUILD_SIDE_ONLY)))
check("...and are still PRESENT build-side (the trim narrows serving, not the build)",
      set(TXN_BUILD_SIDE_ONLY) <= served)
try:
    to_card_rows([{c: 1 for c in TXN_CARD_COLUMNS if c != "price"}])
    check("to_card_rows REFUSES a row missing a card column", False, "it returned")
except MissingUpstreamColumn:
    check("to_card_rows REFUSES a row missing a card column (fails CLOSED)", True)
for name, reason in PRD_DECLARED_ABSENT.items():
    check("DECLARED ABSENT and NOT emitted: %s (%s)" % (name, reason),
          name.lower() not in {c.lower() for c in served})
check("'transaction_memo' (the Notes source) is NOT served",
      "transaction_memo" not in served)

print("=" * 78)
print("ARM 4 -- the PII boundary holds on REAL rows (allowlist, not denylist)")
print("=" * 78)
leaked = sensitive_leak_check(projected)
card_leaked = sensitive_leak_check(to_card_rows(projected))
check("no leak on the TRIMMED SERVED page either (re-run per CTO 79452)",
      not card_leaked, "leaked %s" % card_leaked)
check("no served row carries any of the %d measured-sensitive columns"
      % len(TXN_SENSITIVE_MEASURED), not leaked, "leaked %s" % leaked)
present_upstream = [c for c in TXN_SENSITIVE_MEASURED if c in set(trn.columns)]
print("  sensitive columns PRESENT UPSTREAM in this partition: %d of %d"
      % (len(present_upstream), len(TXN_SENSITIVE_MEASURED)))
check("the leak check had something to find (it is not vacuous)",
      len(present_upstream) > 0, "%d present upstream" % len(present_upstream))
print("  ^ that count is the arm's own POSITIVE CONTROL: if the upstream carried none")
print("    of them, a clean leak check would prove nothing about the allowlist.")
# NEGATIVE CONTROL: the checker must FIRE on a row that does carry one.
if present_upstream:
    dirty = dict(projected[0])
    dirty[present_upstream[0]] = "LEAKED"
    check("NEGATIVE CONTROL: the leak check FIRES on a planted sensitive column",
          sensitive_leak_check([dirty]) == [present_upstream[0]],
          present_upstream[0])
try:
    project_rows([c for c in trn.columns if c != "ticker_symbol"],
                 trn.head(3).to_dict("records"))
    check("REFUSES when an allowlisted column is absent upstream", False, "it returned")
except MissingUpstreamColumn:
    check("REFUSES when an allowlisted column is absent upstream (fails CLOSED)", True)

print("=" * 78)
print("ARM 5 -- a REAL per-relationship page, emitted")
print("=" * 78)
trn["_rel"] = [str(a2r.get(str(a)) or "UNMAPPED-RELATIONSHIP:%s" % a)
               for a in trn["account_id"].astype(str)]
counts = trn["_rel"].value_counts()
target = counts.index[0]
sub = trn[trn["_rel"] == target]
build_rows = project_rows(list(trn.columns), sub.to_dict("records"))
rows = to_card_rows(build_rows)   # SERVE the card ten, not the build 17
page = page_transactions(rows, relationship_id=target, page=0, page_size=DEFAULT_PAGE_SIZE)
print("  relationship %s has %d transactions on date=%s" % (target, len(rows), asof))
print("  page 0 @%d -> returned %d, total %d, hasMoreResults %s"
      % (DEFAULT_PAGE_SIZE, page["returned"], page["total"], page["hasMoreResults"]))
check("the emitted page's rows carry exactly the CARD TEN",
      all(set(r.keys()) == set(TXN_CARD_COLUMNS) for r in page["rows"]))
check("no leak on the REAL emitted page", not sensitive_leak_check(page["rows"]))

artifact = {
    "contract_version": CONTRACT_VERSION,
    "family": "perfrp_transactions_relationship",
    "level": "relationship",
    "as_of": asof,
    "paged": True,
    "page": page,
    "declared_absent_columns": PRD_DECLARED_ABSENT,
    "served_columns": list(TXN_CARD_COLUMNS),
    "build_side_only_columns": list(TXN_BUILD_SIDE_ONLY),
    "prd_card_columns": list(PRD_SERVED),
    "window": {"upstream_pins": {"silver/fact_trn": trn_pin,
                                 "dimensions/dim_relationship": rel_pin}},
}
out = EMIT / "perfrp_transactions_relationship_sample.json"
out.write_bytes(json.dumps(artifact, indent=1, sort_keys=True, default=str).encode("utf-8"))
print("  WROTE %s (%d bytes)" % (out.name, out.stat().st_size))
print("  PINS: fact_trn %s ; dim_relationship %s"
      % (trn_pin["max_last_modified_utc"], rel_pin["max_last_modified_utc"]))

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d ARM(S) FAILED: %s" % (len(FAILS), FAILS))
    sys.exit(1)
print("RESULT: ALL ARMS PASS")
