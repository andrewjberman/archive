"""S4-AC3 -- per-row fill of blank sub_asset_class. One row at a time, each on its own basis.

Writes sub_asset_class ONLY. Never touches asset_class, management_style, name or last_updated.
Every write is conditional on the attribute still being absent or empty, so a row that is already
populated (by a person or by a concurrent worker) can never be overwritten by this script.

SHIPPED BYTES vs RUN BYTES: the run that produced the S4-AC3 acceptance evidence had the
value-set measurement loop at MODULE level. `.tools/ds-precommit-check.py` reports every name
bound inside a module-level `while` body as an undefined name (false positive, reproduced with a
negative control and filed as POSN_ASTTAX-Z-W8-S4), so the loop is wrapped in measure_value_set()
here. Behaviour is unchanged; re-running these bytes exercises the conditional guard, which now
refuses all three rows because they are populated.
"""
import boto3
from botocore.exceptions import ClientError

TABLE = "etf-classifications"
ddb = boto3.client("dynamodb", region_name="us-east-1")

# One entry per blank row found by S4-AC1. ticker -> (value, basis)
FILLS = [
    ("2602335D", "Financials",
     "TPG Inc is a US-listed alternative asset manager (GICS 40 Financials / Capital Markets -- "
     "Asset Management & Custody Banks), the same sector this registry already assigns to its "
     "asset-manager peers BEN (Franklin Templeton), AMP (Ameriprise) and BN (Brookfield Corp); "
     "the registry's own upstream served artifact carries 'Financials' for this exact ticker."),
    ("ICT", "Industrials",
     "International Container Terminal Services Inc is a Philippine-listed marine port terminal "
     "operator (GICS 20 Industrials / Transportation Infrastructure -- Marine Ports & Services), "
     "the same sector this registry already assigns to its transport-infrastructure peers OMAB "
     "(airport operator) and FER (Ferrovial); the upstream served artifact carries 'Industrials' "
     "for this exact ticker."),
    ("MER", "Utilities",
     "Manila Electric Co (Meralco) is a Philippine electric power distribution utility (GICS 55 "
     "Utilities / Electric Utilities), the same sector this registry already assigns to its "
     "regulated-utility peers ENLAY (Enel SpA) and IBDRY (Iberdrola SA); the upstream served "
     "artifact carries 'Utilities' for this exact ticker."),
]


def measure_value_set():
    """The registry's sub_asset_class value set, measured NOW and never inherited."""
    existing_vals = {}
    kw = {}
    scanned = 0
    while True:
        page = ddb.scan(TableName=TABLE, ProjectionExpression="ticker, sub_asset_class", **kw)
        for it in page["Items"]:
            scanned += 1
            v = it.get("sub_asset_class", {}).get("S")
            if v:
                existing_vals[v] = existing_vals.get(v, 0) + 1
        if "LastEvaluatedKey" not in page:
            break
        kw["ExclusiveStartKey"] = page["LastEvaluatedKey"]
    return scanned, existing_vals


def main():
    scanned, existing_vals = measure_value_set()
    print("PRE-FILL value set measured over %d row(s): %d distinct value(s) in use"
          % (scanned, len(existing_vals)))
    print("WRITE SURFACE: sub_asset_class ONLY -- asset_class, management_style, name, "
          "last_updated untouched.")
    print()

    wrote, skipped = 0, 0
    for ticker, value, basis in FILLS:
        already = value in existing_vals
        print("ROW %s" % ticker)
        print("   VALUE WRITTEN        : %r" % value)
        print("   ALREADY IN VALUE SET : %s (%d existing row(s) carry it) -- %s" % (
            already, existing_vals.get(value, 0),
            "NO vocabulary act" if already else "NEW VALUE -- WIDENS THE VOCABULARY"))
        print("   BASIS                : %s" % basis)
        try:
            r = ddb.update_item(
                TableName=TABLE,
                Key={"ticker": {"S": ticker}},
                UpdateExpression="SET sub_asset_class = :v",
                ConditionExpression="attribute_not_exists(sub_asset_class) OR sub_asset_class = :blank",
                ExpressionAttributeValues={":v": {"S": value}, ":blank": {"S": ""}},
                ReturnValues="ALL_NEW",
            )
            got = r["Attributes"].get("sub_asset_class", {}).get("S")
            print("   WRITE                : OK: update-item accepted, served sub_asset_class now %r" % got)
            wrote += 1
            print("   UNTOUCHED FIELDS NOW : asset_class=%r management_style=%r last_updated=%r" % (
                r["Attributes"].get("asset_class", {}).get("S"),
                r["Attributes"].get("management_style", {}).get("S"),
                r["Attributes"].get("last_updated", {}).get("S")))
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code == "ConditionalCheckFailedException":
                print("   WRITE                : SKIP: row is no longer blank -- NOT overwritten "
                      "(condition refused)")
                skipped += 1
            elif code in ("AccessDeniedException", "UnauthorizedOperation"):
                print("   WRITE                : BLOCKED: %s -- %s" % (code, e.response["Error"]["Message"]))
            else:
                print("   WRITE                : ERROR: %s -- %s" % (code, e.response["Error"]["Message"]))
        print()
    print("WROTE %d row(s) and SKIPPED %d of %d candidate(s), one at a time, each on its own "
          "factual basis." % (wrote, skipped, len(FILLS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
