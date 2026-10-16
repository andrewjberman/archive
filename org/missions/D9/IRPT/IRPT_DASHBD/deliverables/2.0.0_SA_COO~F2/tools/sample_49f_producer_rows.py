"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY sampler for the CVO's judgment criterion DBF129-1-J1, as the CTO ruled it (msg 9192).

  python <this file> <out.json> [seed] [n]       defaults: seed 129, n 20

The comparison key is the source row's NATURAL KEY: account, trade date, transaction code, symbol, quantity and amount (`account_id`,
`trade_date`, `tran_srcde`, `ticker_symbol`, `quantity`, `gross_amount`); the source's own identifier is used only where it is non-null AND
unique. The sample is drawn ONLY from rows whose natural key is UNIQUE within its partition; a row with a duplicate key is a finding and never a
sample. The tool first counts, over EVERY partition, the rows and keys that are not unique (counts only, printed and written), then draws `n` rows
with a fixed seed -- one partition per row -- runs the PRODUCER (`account_transaction.normalize_trn`, nothing is written: no S3 put, no upload)
on each, and writes the producer's output beside the source row's own values for every field the contract fills. No row locator is written (row
order is not a stable identity).

The output file holds client figures and an account id: it is written ONLY to the path given (use the git-ignored `org/mcp/drive_ticks/`),
never committed. This tool holds no data. GET requests only.
"""
import json
import random
import sys
import datetime as dt
import importlib.util
from decimal import Decimal
from pathlib import Path

import boto3
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
import account_return_daily as ard  # noqa: E402

spec = importlib.util.spec_from_file_location("account_transaction", ROOT / "data/assets/scripts/gold/irpt_reporting/account_transaction.py")
at = importlib.util.module_from_spec(spec)
spec.loader.exec_module(at)

CONTRACT = json.loads((ROOT / "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json").read_text(encoding="utf-8"))
FEE_COLUMNS = CONTRACT["fee_basis"]["49financial"]["columns"]
NATURAL_KEY = ["account_id", "trade_date", "tran_srcde", "ticker_symbol", "quantity", "gross_amount"]
ID_FIELD = "cashiering_transaction_identifier"
SOURCE_FIELDS = [ID_FIELD, "account_id", "business_date", "trade_date", "settlmnt_date", "tran_srcde", "tr_cd", "sb_cd", "ticker_symbol",
                 "quantity", "price", "gross_amount", "debit_credit"] + list(FEE_COLUMNS)


def plain(v):
    if v is None:
        return None
    if isinstance(v, Decimal):
        return str(v)
    if hasattr(v, "isoformat"):
        return v.isoformat()
    try:
        if v != v:  # NaN
            return None
    except Exception:  # noqa: BLE001
        pass
    return v.item() if hasattr(v, "item") else v


def key_series(frame):
    """One hashable natural key per row (a missing value is its own value)."""
    cols = [frame[c].astype(str) if c in frame.columns else None for c in NATURAL_KEY]
    return list(zip(*[(c if c is not None else [""] * len(frame)) for c in cols]))


def main(out_path, seed=129, n=20):
    src = json.load(open(ROOT / "data/assets/scripts/gold/irpt_reporting/sources.json", encoding="utf-8"))["schwab_08335338"]
    s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))
    days = ard.partition_days(s3, src["bucket"], src["transactions_prefix"])
    # 1. the duplicate census over every partition (counts only)
    rows_total = dup_rows = dup_keys = 0
    unique_by_day = {}
    for day in days:
        frame = ard.read_partition(s3, src["bucket"], src["transactions_prefix"], day, columns=NATURAL_KEY + [ID_FIELD])
        if frame is None or not len(frame):
            continue
        keys = key_series(frame)
        counts = {}
        for k in keys:
            counts[k] = counts.get(k, 0) + 1
        rows_total += len(keys)
        dup_keys += sum(1 for c in counts.values() if c > 1)
        dup_rows += sum(c for c in counts.values() if c > 1)
        unique_by_day[day] = sum(1 for c in counts.values() if c == 1)
    census = {"partitions": len(days), "rows": rows_total, "rows_in_non_unique_keys": dup_rows, "non_unique_keys": dup_keys,
              "share_of_rows_non_unique": round(dup_rows / rows_total, 6) if rows_total else None,
              "partitions_with_a_unique_row": sum(1 for v in unique_by_day.values() if v)}
    print("duplicate census:", census, flush=True)
    # 2. the sample: only rows whose natural key is unique within the partition
    rng = random.Random(seed)
    eligible = sorted(d for d, v in unique_by_day.items() if v)
    picked_days = sorted(rng.sample(eligible, n))
    out = {"seed": seed, "n": n, "drawn_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "contract_version": CONTRACT["contract_version"], "natural_key": NATURAL_KEY, "id_field": ID_FIELD,
           "rule": "CTO msg 9192: compare by the natural key; the id only where non-null and unique; sample only from rows whose key is "
                   "unique within the partition; a duplicate key is a finding, never a sample; no row locator",
           "duplicate_census_49financial": census, "rows": []}
    for day in picked_days:
        frame = ard.read_partition(s3, src["bucket"], src["transactions_prefix"], day)
        keys = key_series(frame)
        counts = {}
        for k in keys:
            counts[k] = counts.get(k, 0) + 1
        candidates = [i for i, k in enumerate(keys) if counts[k] == 1]
        i = candidates[rng.randrange(len(candidates))]
        one = frame.iloc[[i]].reset_index(drop=True)
        produced = at.normalize_trn(one, "49financial")[0]
        id_value = plain(one.iloc[0].get(ID_FIELD))
        out["rows"].append({
            "day": day,
            "natural_key_values": {c: plain(one.iloc[0].get(c)) for c in NATURAL_KEY},
            "id_usable": bool(id_value),
            "source": {k: plain(one.iloc[0].get(k)) for k in SOURCE_FIELDS},
            "producer_output": {k: plain(v) for k, v in produced.items()},
        })
        print("sampled", day, flush=True)
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print("wrote", len(out["rows"]), "rows to", out_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 129, int(sys.argv[3]) if len(sys.argv) > 3 else 20)
