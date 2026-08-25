"""PRF-b-5 EXERCISE (ADVI_PERFRP TO-R1-DS, AC10) -- the paged key and the PII boundary.

AC10: per-relationship paged key ; a no-key request REFUSES ; hasMoreResults present.
Plus the boundary this cell actually turns on: no served transaction row may carry a
client-sensitive column.

Exercised against LIVE fact_trn rows, so the allowlist is proven on the real schema
rather than on a hand-made fixture that happens to contain only safe columns.

NO REAL VALUE FROM A SENSITIVE COLUMN IS PRINTED OR COMMITTED BY THIS FILE.
fact_trn's account_title_line_1 holds real client names. This exercise reports COLUMN
NAMES and COUNTS only. An artifact that proved the PII boundary by displaying the PII
would be self-defeating, and it would be committed to a shared repo forever.

EVIDENCE VINTAGE: live plane read 2026-08-25; citations resolve at
23271aac6480f2ebd65a37247ae64dde4d68c199.
"""
from __future__ import annotations

import io
import sys

import boto3
import pyarrow.parquet as pq

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
from perfrp_transactions import (  # noqa: E402  IMPORTED, never copied
    TXN_SENSITIVE_MEASURED,
    TXN_SERVED_COLUMNS,
    MissingUpstreamColumn,
    TransactionsRefused,
    page_transactions,
    project_rows,
    sensitive_leak_check,
)

ASSETS = "opal-data-assets"
TRN = "schwab/08335338/silver/fact_trn/"
ASOF = "2026-08-21"

PASSED = 0
FAILED = 0


def check(label, ok, detail=""):
    global PASSED, FAILED
    if ok:
        PASSED += 1
    else:
        FAILED += 1
    print("  [%s] %-56s %s" % ("PASS" if ok else "FAIL", label, detail))


def main() -> int:
    s3 = boto3.client("s3")
    r = s3.list_objects_v2(Bucket=ASSETS, Prefix="%sdate=%s/" % (TRN, ASOF))
    key = [o["Key"] for o in r.get("Contents", []) if o["Key"].endswith(".parquet")][0]
    df = pq.read_table(io.BytesIO(s3.get_object(Bucket=ASSETS, Key=key)["Body"].read())).to_pandas()
    upstream = df.to_dict("records")

    print("PRF-b-5 EXERCISE -- ADVI_PERFRP TO-R1-DS (AC10)")
    print("source: s3://%s/%s" % (ASSETS, key))
    print("=" * 100)
    print("upstream fact_trn: %d rows, %d columns" % (len(df), len(df.columns)))
    print("allowlist: %d columns | measured-sensitive on this schema: %d columns"
          % (len(TXN_SERVED_COLUMNS), len(TXN_SENSITIVE_MEASURED)))

    print("\nAC10.1 -- the PII boundary, exercised on LIVE rows")
    served = project_rows(list(df.columns), upstream)
    leaked = sensitive_leak_check(served)
    check("no served row carries a measured-sensitive column", leaked == [],
          "leaked=%s" % (leaked or "none"))
    check("served rows carry exactly the allowlist",
          all(set(r.keys()) == set(TXN_SERVED_COLUMNS) for r in served),
          "%d columns per row" % len(served[0].keys()))
    present = [c for c in TXN_SENSITIVE_MEASURED if c in set(df.columns)]
    pop = sum(1 for c in present if df[c].notna().any())
    print("       upstream carries %d of the %d measured-sensitive columns, %d populated"
          % (len(present), len(TXN_SENSITIVE_MEASURED), pop))
    print("       (column names and counts only -- no value from any of them is printed)")

    print("\nAC10.2 -- THE LEAK CHECK MUST BE ABLE TO FIRE")
    print("        a boundary check that never fires proves nothing (the a-2 lesson)")
    tainted = [dict(served[0]) for _ in range(3)]
    for t in tainted:
        t["bank_aba"] = "REDACTED-SYNTHETIC"      # synthetic, never a real value
        t["account_title_line_1"] = "REDACTED-SYNTHETIC"
    caught = sensitive_leak_check(tainted)
    check("MUTANT: deliberately leaked rows ARE caught",
          set(caught) == {"bank_aba", "account_title_line_1"},
          "caught=%s" % caught)
    check("and the clean set still reads clean (control re-run)",
          sensitive_leak_check(served) == [])

    print("\nAC10.3 -- a no-key request REFUSES (s.11 #6)")
    for bad in (None, "", "   "):
        try:
            page_transactions(served, relationship_id=bad)
            check("no-key REFUSES for %r" % bad, False, "it returned a page")
        except TransactionsRefused:
            check("no-key REFUSES for %r" % bad, True)
    try:
        ok = page_transactions(served, relationship_id="rel_test", page=0, page_size=10)
        check("POSITIVE CONTROL: a keyed request still serves", ok["returned"] > 0,
              "returned=%d of total=%d" % (ok["returned"], ok["total"]))
    except TransactionsRefused:
        check("POSITIVE CONTROL: a keyed request still serves", False, "it refused everything")

    print("\nAC10.4 -- hasMoreResults, including the boundary that is usually wrong")
    total = len(served)
    p0 = page_transactions(served, relationship_id="rel_test", page=0, page_size=100)
    check("page 0 of %d rows -> hasMoreResults True" % total, p0["hasMoreResults"] is True,
          "returned=%d total=%d" % (p0["returned"], p0["total"]))
    last = (total - 1) // 100
    pl = page_transactions(served, relationship_id="rel_test", page=last, page_size=100)
    check("last page -> hasMoreResults False", pl["hasMoreResults"] is False,
          "page=%d returned=%d" % (last, pl["returned"]))
    # EXACT-FIT must be tested WITHIN the page-size cap, so it uses a bounded subset.
    # (My first version asked for a 1180-row page against MAX_PAGE_SIZE=500 and the
    # module correctly REFUSED it -- the test was malformed, not the module.)
    subset = served[:250]
    exact = page_transactions(subset, relationship_id="rel_test", page=0, page_size=250)
    check("EXACT-FIT page (page_size == total) -> hasMoreResults False",
          exact["hasMoreResults"] is False,
          "returned=%d total=%d -- a full page inferred as 'more' is the classic "
          "off-by-one; this is computed from total" % (exact["returned"], exact["total"]))
    try:
        page_transactions(served, relationship_id="rel_test", page=0, page_size=total)
        check("over-cap page_size REFUSES", False, "it served %d rows in one page" % total)
    except TransactionsRefused:
        check("over-cap page_size REFUSES (no firm-wide dump via page_size)", True,
              "page_size=%d rejected against the 500 cap" % total)
    beyond = page_transactions(served, relationship_id="rel_test", page=last + 5, page_size=100)
    check("page beyond the end -> empty, hasMoreResults False",
          beyond["returned"] == 0 and beyond["hasMoreResults"] is False)
    check("hasMoreResults present on every response",
          all("hasMoreResults" in p for p in (p0, pl, exact, beyond)))

    print("\nAC10.5 -- a missing allowlisted column REFUSES rather than emitting a short row")
    try:
        project_rows([c for c in df.columns if c != "gross_amount"], upstream[:2])
        check("missing upstream column REFUSES", False, "it emitted a short row")
    except MissingUpstreamColumn as e:
        check("missing upstream column REFUSES", True, str(e)[:56] + "...")

    print("\n" + "=" * 100)
    print("DENOMINATOR: %d checks, %d PASS, %d FAIL" % (PASSED + FAILED, PASSED, FAILED))
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
