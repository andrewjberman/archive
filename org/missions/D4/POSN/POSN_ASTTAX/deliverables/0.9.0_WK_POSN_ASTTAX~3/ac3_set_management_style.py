#!/usr/bin/env python3
"""
POSN_ASTTAX.TO-S5-1 / cell AT2-s-5 / S5-AC3 -- set `management_style` to the factually
correct value on the six rows AT2-s-2 will retag.

WHAT THIS IS NOT: a bulk set. Each ticker below carries its OWN factual determination and
its own one-sentence basis. The determinations are made against the field's DEFINED domain,
read from the consumer rather than assumed:

    infra/aws/lambda/v2_portal/_shared/etf_classification.py:298
    "# 'active' = Actively managed, 'passive' = Index/Beta tracking"

DISCRIMINATION (could this method return the other value?): yes. The same estate map marks
PDBC -- Invesco Optimum Yield Diversified Commodity Strategy No K-1 ETF -- 'active' at :337
while marking VIXY 'passive' at :328. A commodity fund is NOT automatically passive here;
DBC (index tracking) and PDBC (actively managed strategy) are the pair that proves it. USO
is the member of this write set that could have gone either way and its basis says why.

BOUNDS OBSERVED:
  - writes attribute `management_style` ONLY, via SET on that single name;
  - `asset_class` is read for evidence and NEVER written (AT2-s-2's field);
  - every write is conditional on the row still reading "unknown", so a row that moved
    underneath this order is REFUSED rather than silently overwritten;
  - `updated_by` / `last_updated` are deliberately NOT written -- the order restricts this
    write to one attribute. The resulting provenance gap is filed as a surprise row, not
    fixed here.
"""
import sys
import boto3
from botocore.exceptions import ClientError

TABLE = "etf-classifications"
EXPECTED_OLD = "unknown"

# ticker -> (new_value, one-sentence factual basis)
DETERMINATIONS = [
    ("DBC", "passive",
     "Invesco DB Commodity Index Tracking Fund tracks the rules-based DBIQ Optimum Yield "
     "Diversified Commodity Index Excess Return and selects nothing at a manager's discretion, "
     "so it is index tracking."),
    ("GLD", "passive",
     "SPDR Gold Shares is a grantor trust whose only asset is allocated physical gold bullion, "
     "sold solely to meet trust expenses, with no portfolio manager and no security selection."),
    ("GSG", "passive",
     "iShares S&P GSCI Commodity-Indexed Trust holds index futures for the sole purpose of "
     "tracking the S&P GSCI Total Return Index, which is index tracking, not active management."),
    ("IAU", "passive",
     "iShares Gold Trust is a grantor trust holding physical gold bullion with no manager "
     "discretion over what it holds."),
    ("SLV", "passive",
     "iShares Silver Trust is a grantor trust holding physical silver bullion with no manager "
     "discretion over what it holds."),
    ("USO", "passive",
     "United States Oil Fund LP tracks a published Benchmark Oil Futures Contract rather than "
     "taking discretionary positions, so under this field's definition it is beta tracking -- "
     "the sponsor's contingency latitude over contract months is a roll mechanic, not an alpha "
     "mandate, which is what separates it from an actively managed commodity fund such as PDBC."),
]

FORBIDDEN_FIELD = "asset_class"


def main():
    assert len(DETERMINATIONS) == 6, "write set must be exactly the six AT2-s-2 rows"
    tickers = [t for t, _, _ in DETERMINATIONS]
    assert "VIXY" not in tickers, "VIXY already reads 'passive' and is NOT in the write set"
    assert all(reason.strip() for _, _, reason in DETERMINATIONS), "no ticker without a reason"

    ddb = boto3.client("dynamodb", region_name="us-east-1")
    rc = 0
    wrote = 0

    print("TABLE=%s  WRITE-SET=%d ticker(s): %s" % (TABLE, len(tickers), ", ".join(tickers)))
    print("FIELD WRITTEN: management_style ONLY.  FIELD NEVER WRITTEN: %s" % FORBIDDEN_FIELD)
    print("-" * 100)

    for ticker, new_value, reason in DETERMINATIONS:
        before = ddb.get_item(TableName=TABLE, Key={"ticker": {"S": ticker}}).get("Item", {})
        old_value = before.get("management_style", {}).get("S", "<ABSENT>")
        old_asset = before.get(FORBIDDEN_FIELD, {}).get("S", "<ABSENT>")

        if old_value != EXPECTED_OLD:
            print("SKIP:  %-5s old=%-8s new=<not written>  asset_class=%s" % (ticker, old_value, old_asset))
            print("       REFUSED: row no longer reads %r; this order does not overwrite a value "
                  "it did not measure." % EXPECTED_OLD)
            rc = 1
            continue

        try:
            resp = ddb.update_item(
                TableName=TABLE,
                Key={"ticker": {"S": ticker}},
                UpdateExpression="SET management_style = :new",
                ConditionExpression="management_style = :old",
                ExpressionAttributeValues={":new": {"S": new_value}, ":old": {"S": EXPECTED_OLD}},
                ReturnValues="UPDATED_NEW",
            )
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            print("ERROR: %-5s old=%-8s new=<not written>  %s" % (ticker, old_value, code))
            print("       %s" % exc.response["Error"].get("Message", ""))
            rc = 1
            continue

        written = resp["Attributes"]["management_style"]["S"]
        wrote += 1
        print("OK:    %-5s old=%-8s new=%-8s (write returned %r)  asset_class untouched=%s"
              % (ticker, old_value, new_value, written, old_asset))
        print("       REASON: %s" % reason)

    print("-" * 100)
    print("WROTE %d of %d; asset_class appears in NO UpdateExpression in this script."
          % (wrote, len(DETERMINATIONS)))
    print("A write's return value is NOT evidence the value is served -- S5-AC4 reads the rows back.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
