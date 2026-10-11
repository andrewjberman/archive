"""TO-DB-b-160 step 2: add the prior value, flow share, price and income returns, and the three one-day returns."""

import pandas as pd

Q = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~129/"
m = pd.read_parquet(Q + "merged.parquet")
m = m.sort_values(["account_id", "business_date"]).reset_index(drop=True)
m["v0"] = m.groupby("account_id").market_value_eod.shift(1)
f = m.flow
v1 = m.market_value_eod
v0 = m.v0
m["base_ok"] = v0 > 0
m["share"] = f.abs() / v0
m["pr"] = m.holdings_price_return
m["ir"] = m.income_return
m["r_end_raw"] = (v1 - f) / v0 - 1
m["r_start_raw"] = v1 / (v0 + f) - 1
m["r_mid_raw"] = (v1 - f / 2) / (v0 + f / 2) - 1
m.to_parquet(Q + "work.parquet")
