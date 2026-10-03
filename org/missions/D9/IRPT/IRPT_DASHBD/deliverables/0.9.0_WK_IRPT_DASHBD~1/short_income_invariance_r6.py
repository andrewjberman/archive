"""IRPT_DASHBD TO-DB-b-13 -- MEASURE what the S22 income fix moves. READS ONLY (S3 get/list of the Schwab silver); writes one JSON file.

For every transaction partition since 2026-01-01, take the cash dividend DEBIT rows (tr_cd FC, sb_cd DV) on the producer's own
SHORT_PAID_DIVIDEND_KEYS (the rows the fix newly admits) and count, for each, whether the row's own share quantity is negative (a
short position) and whether the account's balance carries a short market value that day. A newly admitted row with neither signal
would be a row that moves a no-short account's income: its count is the proof the fix does not.

Usage: python short_income_invariance_r6.py <repo_root> <out_json>
"""
import importlib.util
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pandas as pd
from botocore.config import Config

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
spec = importlib.util.spec_from_file_location("ard", root / "data/assets/scripts/gold/irpt_reporting/account_return_daily.py")
ard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ard)
s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
doc = ard.load_declaration()
src = ard.source_entry(doc, ard.declared_sources(doc)[0])
days = [d for d in ard.partition_days(s3, src["bucket"], src["transactions_prefix"]) if d >= "2026-01-01"]
cols = ["account_id", "tran_srcde", "tr_cd", "sb_cd", "debit_credit", "gross_amount", "dividend_interest_share_quantity"]


def one(d):
    t = ard.read_partition(s3, src["bucket"], src["transactions_prefix"], d, columns=cols)
    if t is None or not len(t):
        return []
    t = t[(t["tr_cd"].astype(str).str.strip() == "FC") & (t["sb_cd"].astype(str).str.strip() == "DV")
          & (t["debit_credit"].astype(str).str[0].str.upper() == "D")]
    keys = list(zip(t["tran_srcde"].astype(str).str.strip(), t["tr_cd"].astype(str).str.strip(), t["sb_cd"].astype(str).str.strip()))
    t = t[[k in ard.SHORT_PAID_DIVIDEND_KEYS for k in keys]]
    if not len(t):
        return []
    b = ard.read_partition(s3, src["bucket"], src["balance_prefix"], d, columns=["account_id", "mkt_value_short"])
    sh = {}
    if b is not None and len(b):
        sh = dict(zip(b["account_id"].astype(str).str.zfill(10), pd.to_numeric(b["mkt_value_short"], errors="coerce").fillna(0.0)))
    out = []
    for _, r in t.iterrows():
        a = str(r["account_id"]).zfill(10)
        q = pd.to_numeric(r["dividend_interest_share_quantity"], errors="coerce")
        out.append({"day": d, "q_negative": bool(q == q and q < 0), "balance_short": (sh.get(a, 0.0) < 0),
                    "amount": float(r["gross_amount"])})
    return out


with ThreadPoolExecutor(8) as ex:
    rows = [x for part in ex.map(one, days) for x in part]
res = {
    "partitions_scanned": len(days), "span": [days[0], days[-1]],
    "newly_admitted_debit_rows": len(rows),
    "newly_admitted_amount_abs": round(sum(r["amount"] for r in rows), 2),
    "rows_with_negative_share_quantity": sum(1 for r in rows if r["q_negative"]),
    "rows_on_an_account_day_with_a_short_market_value": sum(1 for r in rows if r["balance_short"]),
    "rows_with_neither_signal": sum(1 for r in rows if not r["q_negative"] and not r["balance_short"]),
}
Path(sys.argv[2]).write_text(json.dumps(res, indent=1), encoding="utf-8")
print(json.dumps(res))
