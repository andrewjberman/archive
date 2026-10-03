"""IRPT_DASHBD TO-DB-b-19 -- MEASURE what PRD v0.7 ruling 27 moves. READS ONLY (S3 get/list of the Schwab silver and the holdings
gold neighbour); writes only the two JSON files named in argv.

Base = the producer with `share_quantity_column` removed from the declaration (the code path is then exactly the pre-change one:
the extra column is not read and no DIV debit is admitted). Change = the producer as declared.

STAGE A (every one of the transaction partitions since the span start, every account):
  * row level: every DIV/FC/DV debit row is run through classify_and_sum alone, base vs change; admitted = its income differs.
  * day level: the whole partition is run through classify_and_sum base vs change; flow, unvalued and cash_unknown must be
    identical on every account, and income may differ only where an admitted row sits.
STAGE B (return): compute_range over the span's trading days, with the LIVE-shaped thresholds, for the accounts that carry any
  DIV debit row, base vs change; compares total_return_daily, return_basis, day_quality, guard_state and external_flow
  account-day by account-day, and counts the income_received / income_return account-days that moved.

Usage: python short_div_debit_measure_r11.py <repo_root> <out_json> <detail_json>
"""
import copy
import importlib.util
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pandas as pd
from botocore.config import Config

root = Path(sys.argv[1]).resolve()
out_path, detail_path = Path(sys.argv[2]), Path(sys.argv[3])
SPAN_START = "2026-01-02"
spec = importlib.util.spec_from_file_location("ard", root / "data/assets/scripts/gold/irpt_reporting/account_return_daily.py")
ard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ard)
s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
doc = ard.load_declaration()
src_new = ard.source_entry(doc, ard.declared_sources(doc)[0])
assert src_new.get("share_quantity_column") == "dividend_interest_share_quantity", "the declaration does not carry the column"
src_base = copy.deepcopy(src_new)
del src_base["share_quantity_column"]
firm = ard.firm_scope(src_new)
table, keycols = ard.load_classification(src_new)
days = [d for d in ard.partition_days(s3, src_new["bucket"], src_new["transactions_prefix"]) if d >= SPAN_START]
print("partitions in span:", len(days), days[0], days[-1], flush=True)
cols = ard.transaction_columns(src_new)
assert "dividend_interest_share_quantity" in cols

# a read cache so Stage B does not re-read what Stage A read
_cache = {}
_real_read = ard.read_partition


def cached_read(s3_, bucket, prefix, day, columns=None):
    k = (bucket, prefix, day, tuple(columns) if columns else None)
    if k not in _cache:
        _cache[k] = _real_read(s3_, bucket, prefix, day, columns=columns)
    v = _cache[k]
    return None if v is None else v.copy()


ard.read_partition = cached_read


def read_day(d):
    return d, cached_read(s3, src_new["bucket"], src_new["transactions_prefix"], d, cols)


with ThreadPoolExecutor(8) as ex:
    trn_by_day = dict(ex.map(read_day, days))
print("read", len(trn_by_day), "partitions", flush=True)

rows_detail = []
day_mismatch = []
income_moved = {}   # (account, day) -> delta
flow_mismatch = 0
for d in days:
    t = trn_by_day[d]
    if t is None or not len(t):
        continue
    key = list(zip(t["tran_srcde"].astype(str).str.strip(), t["tr_cd"].astype(str).str.strip(), t["sb_cd"].astype(str).str.strip()))
    is_div = pd.Series([k == ("DIV", "FC", "DV") for k in key], index=t.index) & (t["debit_credit"].astype(str).str.strip().str[:1].str.upper() == "D")
    # --- row level
    for idx in t.index[is_div]:
        one = t.loc[[idx]]
        _f, inc_b, *_ = ard.classify_and_sum(one, src_base, table, keycols)
        _f, inc_n, *_ = ard.classify_and_sum(one, src_new, table, keycols)
        a = str(one.iloc[0]["account_id"]).zfill(10)
        vb, vn = inc_b.get(a, 0.0), inc_n.get(a, 0.0)
        q = pd.to_numeric(one.iloc[0]["dividend_interest_share_quantity"], errors="coerce")
        rows_detail.append({"day": d, "account_id": a, "gross_amount": float(one.iloc[0]["gross_amount"]),
                            "share_quantity": (None if q != q else float(q)), "admitted": abs(vn - vb) > 1e-12,
                            "income_base": vb, "income_change": vn})
    # --- day level, whole partition
    fb, ib, ub, cb = ard.classify_and_sum(t, src_base, table, keycols)[:4]
    fn, i_n, un, cn = ard.classify_and_sum(t, src_new, table, keycols)[:4]
    if fb != fn or ub != un or cb != cn:
        flow_mismatch += 1
    for a in set(ib) | set(i_n):
        dl = i_n.get(a, 0.0) - ib.get(a, 0.0)
        if abs(dl) > 1e-9:
            income_moved[(a, d)] = round(dl, 6)
    print("  stage A", d, "rows", len(t), flush=True) if d[-2:] == "15" else None

adm = [r for r in rows_detail if r["admitted"]]
zero = [r for r in rows_detail if (not r["admitted"]) and r["share_quantity"] == 0.0]
res = {
    "span": [days[0], days[-1]],
    "partitions_scanned": len(days),
    "newly_admitted_div_debit_rows": len(adm),
    "newly_admitted_amount_abs": round(sum(abs(r["gross_amount"]) for r in adm), 2),
    "admitted_with_nonnegative_share_quantity": sum(1 for r in adm if r["share_quantity"] is None or r["share_quantity"] >= 0),
    "zero_share_div_debit_rows_excluded": len(zero),
}
print("STAGE A:", json.dumps(res), "| whole-day flow/unvalued/cash_unknown mismatches:", flow_mismatch,
      "| account-partition-days where income moved:", len(income_moved), flush=True)

# ---------------- STAGE B
accts = sorted({r["account_id"] for r in rows_detail})
th = json.loads((root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/MEASURED_THRESHOLDS_R1.json").read_text(encoding="utf-8"))
assert not th.get("SUPERSEDED") and th.get("comparability_max_excluded_weight") is not None
tdays = [str(d) for d in ard.tc.trading_days_between(days[0], days[-1])]
trn_days = ard.partition_days(s3, src_new["bucket"], src_new["transactions_prefix"])
first_data = ard.first_data_dates(s3, src_new, tdays[-1], accounts=accts, workers=8)
bal_days = ard.partition_days(s3, src_new["bucket"], src_new["balance_prefix"])
caches = {}


def run(src):
    flows = ard.FlowCache(s3, src, table, keycols, accts)
    if not caches:
        caches["v"], caches["h"] = ard.prefetch(s3, src, firm, tdays, trn_days, accounts=accts, flows=flows, workers=8)
    else:
        for d in [x for x in trn_days if x >= min(caches["v"]) and x <= tdays[-1]]:
            flows.get(d)
    rows, _notes, _fs = ard.compute_range(s3, src, firm, tdays, trn_days, accounts=accts, thresholds=th, flows=flows,
                                          value_cache=caches["v"], holdings_cache=caches["h"], first_data=first_data,
                                          bal_days=bal_days)
    return {(r["account_id"], r["business_date"]): r for r in rows}


base = run(src_base)
new = run(src_new)
assert set(base) == set(new)


def same(x, y):
    if x is None or y is None:
        return x is None and y is None
    if isinstance(x, float) or isinstance(y, float):
        return abs(float(x) - float(y)) <= 1e-12
    return x == y


ret_fields = ("total_return_daily", "return_basis", "day_quality", "guard_state", "external_flow", "market_value_eod")
ret_delta = [k for k in base if not all(same(base[k].get(f), new[k].get(f)) for f in ret_fields)]
inc_delta = [k for k in base if not (same(base[k].get("income_received"), new[k].get("income_received"))
                                      and same(base[k].get("income_return"), new[k].get("income_return")))]
res.update({
    "account_days_compared": len(base),
    "return_delta_nonzero_account_days": len(ret_delta),
    "income_delta_nonzero_account_days": len(inc_delta),
})
print("STAGE B accounts", len(accts), "account-days", len(base), "return delta", len(ret_delta), "income delta", len(inc_delta), flush=True)
out_path.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
detail = {
    "note": "Detail behind SHORT_DIV_DEBIT_R11.json. Stage A = every account, every partition; Stage B = the accounts carrying any DIV debit row.",
    "stage_a_whole_day_flow_unvalued_cash_unknown_mismatching_partitions": flow_mismatch,
    "stage_a_account_partition_days_income_moved": len(income_moved),
    "stage_b_accounts": len(accts), "stage_b_return_fields_compared": list(ret_fields),
    "stage_b_thresholds": "deliverables/0.4.0_DS_ClientPlatform~S/MEASURED_THRESHOLDS_R1.json",
    "div_debit_rows": rows_detail,
    "stage_b_income_moved_account_days": [list(k) for k in sorted(inc_delta)],
    "stage_b_return_moved_account_days": [list(k) for k in sorted(ret_delta)],
}
detail_path.write_text(json.dumps(detail, indent=1) + "\n", encoding="utf-8")
print(json.dumps(res))
