"""TO-DB-b-160 step 1: merge the previous cell's private table with its served copy (private paths only)."""

import pickle
import pandas as pd

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~128/"
Q = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~129/"
t = pd.read_parquet(P + "account_day_table.parquet")
g = pickle.load(open(P + "gold_copy.pkl", "rb"))
df = pd.DataFrame(g["rows"], columns=g["columns"])
df.to_parquet(Q + "gold_rows.parquet")
keep = [
    "account_id",
    "business_date",
    "external_flow",
    "income_return",
    "holdings_price_return",
    "total_return_daily",
    "market_value_eod",
    "day_quality",
    "guard_state",
    "carried_days",
]
m = t.merge(
    df[keep],
    on=["account_id", "business_date"],
    suffixes=("", "_g"),
    how="outer",
    indicator=True,
)
assert (m._merge == "both").all()
m.to_parquet(Q + "merged.parquet")
