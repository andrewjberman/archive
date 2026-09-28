"""IB-er-191 AC3 -- the daily return IS the holdings-based return of Andrew-direct call 3, recomputed independently.

Usage: python e19_ac3_holdings_method.py [s3 root, default the registry's served root]

The rule (record ANDREW_DIRECT_20260928_222xZ_OPEN_CALLS_1_2_APPROVED_3_HOLDINGS_BASED_PERFORMANCE.md): the account's
day-t return is the sum over the securities it held at the end of day t-1 of
    w_i = market_value_settled_unsettled(i, t-1) / fair_value(account, t-1)      (canonical_positions / canonical_valuation)
    r_i = closing_price(i, t) / closing_price(i, t-1) - 1                        (same cusip, both days, prices > 0)
with cash earning zero and NO inflow/outflow term. This check recomputes that for SAMPLE days that carry a cash flow
(cf_net != 0 in twr_daily) -- the days on which the flow-based rule and the holdings rule differ -- restricted to
(account, day) pairs where every t-1 security has a price on t. Pass: at least 20 such pairs checked and every one
within 1e-8 of twr_daily's r_net. Base (the flow-based engine): the pairs differ.
"""
import io
import sys

import boto3
import pandas as pd

BUCKET, ROOT = "opal-data-49financial", "gold/advi"
root = sys.argv[1] if len(sys.argv) > 1 else ROOT
base = root.rstrip("/") + "/canonical/"
s3 = boto3.client("s3")
PAIRS_DAYS = [("2026-09-23", "2026-09-24"), ("2026-09-24", "2026-09-25"), ("2026-08-27", "2026-08-28")]


def read(table, day, cols=None):
    key = "%s%s/date=%s/data.parquet" % (base, table, day)
    return pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()), columns=cols)


checked, worst, bad = 0, 0.0, 0
for prev, day in PAIRS_DAYS:
    twr = read("twr_daily", day, ["account_id", "status", "r_net", "cf_net"])
    flow = twr[(twr["status"] == "OK") & twr["r_net"].notna() & (twr["cf_net"].fillna(0.0) != 0.0)]
    pos0 = read("canonical_positions", prev, ["account_id", "cusip", "market_value_settled_unsettled", "closing_price"])
    pos1 = read("canonical_positions", day, ["account_id", "cusip", "closing_price"])
    val0 = read("canonical_valuation", prev, ["account_id", "fair_value"]).set_index("account_id")["fair_value"]
    for _, row in flow.head(40).iterrows():
        a = row["account_id"]
        # A cusip can sit on more than one row (lots, sides): one market value (summed) and one price per cusip.
        p0 = (pos0[pos0["account_id"] == a].groupby("cusip", as_index=False)
              .agg(market_value_settled_unsettled=("market_value_settled_unsettled", "sum"),
                   closing_price=("closing_price", "first")))
        p1 = pos1[pos1["account_id"] == a].groupby("cusip")["closing_price"].first()
        fv = float(val0.get(a, 0.0) or 0.0)
        if fv <= 0 or p0.empty or not all(c in p1.index for c in p0["cusip"]) or (p0["closing_price"] <= 0).any():
            continue
        r = sum(float(m) / fv * (float(p1[c]) / float(p) - 1.0)
                for c, m, p in zip(p0["cusip"], p0["market_value_settled_unsettled"], p0["closing_price"]))
        diff = abs(r - float(row["r_net"]))
        worst = max(worst, diff)
        checked += 1
        bad += diff > 1e-8
print("flow-day pairs checked: %d | outside 1e-8: %d | worst abs diff: %.3g" % (checked, bad, worst))
ok = checked >= 20 and bad == 0
if ok:
    print("E19-AC3 PASS")
else:
    print("E19-AC3 FAIL")
sys.exit(0 if ok else 1)
