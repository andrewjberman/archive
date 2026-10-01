#!/usr/bin/env python3
"""IB-yr-304 AC1 -- the etf-classifications half of the comparison catalogue is a real, paginated READ
(row IRPT_BCKEND-W88-S2), and a failed read is never an empty answer.

Three cases against `comparison_catalogue.classifications_reader`, all offline (a botocore Stubber on a
low-level DynamoDB client; no AWS call is made):
  1. TWO PAGES: the reader issues Scan on table `etf-classifications` projecting `ticker`, `name` and
     `identifier_namespace` only, follows LastEvaluatedKey with ExclusiveStartKey, and returns
     {TICKER: {"name": ...}} keyed by the UPPER-CASED ticker for the three ticker rows (one with no name
     attribute); the one CUSIP-keyed row (`identifier_namespace` CUSIP) is dropped, as the table's own client
     drops it. (The CUSIP arm was added when the build read that client; the first draft of this check
     projected two attributes and would have listed a CUSIP as a ticker.)
  2. WIRED: build_catalogue(tenant, read_classifications=<that reader>) LISTS SPY labelled by its
     etf-classifications name (`name_source` etf_classifications) and does NOT list the unnamed BIL (CTO
     rulings batch 61: the list serves named rows only); entry_for_ticker still answers BIL verbatim.
  3. A FAILED READ PROPAGATES: an AccessDeniedException from Scan raises ClientError out of the reader; it is
     never caught and turned into "no names" (an empty answer would serve every ticker verbatim and hide the
     missing grant).
PASS iff all three. Base run (before the cut): FAIL at case 1 -- the module has no `classifications_reader`;
the port is unwired and production serves every non-model ticker verbatim.
Issuer 2.0.0_SA_COO~Y, round 30. ASCII only.
"""
import os
import sys

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # parents[0] is R30_checks; the repo root is parents[8]
sys.path.insert(0, os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting", "ycharts", "generate"))

import boto3  # noqa: E402
from botocore.exceptions import ClientError  # noqa: E402
from botocore.stub import Stubber  # noqa: E402

import comparison_catalogue as cc  # noqa: E402

SCAN = {"TableName": "etf-classifications", "ProjectionExpression": "#t, #n, #ns",
        "ExpressionAttributeNames": {"#t": "ticker", "#n": "name", "#ns": "identifier_namespace"}}
PAGE_1 = {"Items": [{"ticker": {"S": "spy"}, "name": {"S": "SPDR S&P 500 ETF Trust"}}, {"ticker": {"S": "BIL"}}],
          "LastEvaluatedKey": {"ticker": {"S": "BIL"}}}
PAGE_2 = {"Items": [{"ticker": {"S": "VNQ"}, "name": {"S": "Vanguard Real Estate ETF"}},
                    {"ticker": {"S": "912828YK0"}, "name": {"S": "A CUSIP-keyed row"},
                     "identifier_namespace": {"S": "CUSIP"}}]}


def client():
    return boto3.client("dynamodb", region_name="us-east-1", aws_access_key_id="offline",
                        aws_secret_access_key="offline")


def two_pages():
    c = client()
    stub = Stubber(c)
    stub.add_response("scan", PAGE_1, SCAN)
    stub.add_response("scan", PAGE_2, dict(SCAN, ExclusiveStartKey={"ticker": {"S": "BIL"}}))
    stub.activate()
    return c, stub


def names(rows):
    return {k: ((v or {}).get("name") or "").strip() for k, v in rows.items()}


def main():
    held, first = 0, None

    def case(n, ok, detail):
        nonlocal held, first
        if ok:
            held += 1
        elif first is None:
            first = "case %d: %s" % (n, detail)

    try:
        c, stub = two_pages()
        rows = cc.classifications_reader(c)()
        stub.assert_no_pending_responses()
        case(1, names(rows) == {"SPY": "SPDR S&P 500 ETF Trust", "BIL": "", "VNQ": "Vanguard Real Estate ETF"},
             "the reader returned %r" % (rows,))
    except Exception as exc:
        case(1, False, "%s %s" % (type(exc).__name__, exc))
    try:
        c, stub = two_pages()
        rows = cc.classifications_reader(c)()
        entries = {e["key"]: e for e in cc.build_catalogue(
            tenant="cottonwood", read_classifications=lambda: rows)["entries"]}
        spy = entries.get("SPY") or {}
        bil = cc.entry_for_ticker("BIL", tenant="cottonwood", read_classifications=lambda: rows)
        case(2, spy.get("label") == "SPDR S&P 500 ETF Trust" and spy.get("name_source") == "etf_classifications"
             and "BIL" not in entries and bil.get("label") == "BIL" and bil.get("name_source") == "ticker_verbatim",
             "SPY %r BIL listed %s BIL typed %r" % (spy, "BIL" in entries, bil))
    except Exception as exc:
        case(2, False, "%s %s" % (type(exc).__name__, exc))
    try:
        c = client()
        stub = Stubber(c)
        stub.add_client_error("scan", service_error_code="AccessDeniedException", expected_params=SCAN)
        stub.activate()
        try:
            got = cc.classifications_reader(c)()
            case(3, False, "a denied Scan returned %r instead of raising" % (got,))
        except ClientError as exc:
            case(3, exc.response["Error"]["Code"] == "AccessDeniedException", "raised %s" % exc)
    except Exception as exc:
        case(3, False, "%s %s" % (type(exc).__name__, exc))
    if held == 3:
        print("PASS: 3 of 3 classifications-reader cases hold")
        return 0
    print("FAIL: %d of 3 classifications-reader cases hold -- %s" % (held, first))
    return 1


if __name__ == "__main__":
    sys.exit(main())
