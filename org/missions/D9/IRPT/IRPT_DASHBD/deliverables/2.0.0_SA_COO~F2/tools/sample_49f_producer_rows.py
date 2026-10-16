"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY sampler for the CVO's judgment criterion DBF129-1-J1.

  python <this file> <out.json> [seed] [n]       defaults: seed 129, n 20

It draws `n` rows of 49 Financial's transaction silver (`fact_trn`) with a fixed seed -- one partition per row, the day and the row chosen by the
seed -- runs the PRODUCER (`account_transaction.normalize_trn`, nothing is written: no S3 put, no upload) on each, and writes, for each sampled
row, the producer's output beside the SOURCE row's own values for every field the contract fills, keyed by the source's own id
(`cashiering_transaction_identifier`), so the CVO can fetch the same source row by that id and compare field by field.

The output file holds client figures and an account id: it is written ONLY to the path given (use the git-ignored `org/mcp/drive_ticks/`),
never committed. This tool holds no data. GET requests only.
"""
import json
import random
import sys
import datetime as dt
import importlib.util
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
SOURCE_FIELDS = ["cashiering_transaction_identifier", "account_id", "business_date", "trade_date", "settlmnt_date", "tran_srcde", "tr_cd",
                 "sb_cd", "ticker_symbol", "quantity", "price", "gross_amount", "debit_credit"] + list(FEE_COLUMNS)


def plain(v):
    if v is None:
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    try:
        if v != v:  # NaN
            return None
    except Exception:  # noqa: BLE001
        pass
    return v.item() if hasattr(v, "item") else v


def main(out_path, seed=129, n=20):
    src = json.load(open(ROOT / "data/assets/scripts/gold/irpt_reporting/sources.json", encoding="utf-8"))["schwab_08335338"]
    s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))
    days = ard.partition_days(s3, src["bucket"], src["transactions_prefix"])
    rng = random.Random(seed)
    picked_days = sorted(rng.sample(days, n))
    out = {"seed": seed, "n": n, "drawn_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "id_field": "cashiering_transaction_identifier", "contract_version": CONTRACT["contract_version"], "rows": []}
    for day in picked_days:
        frame = ard.read_partition(s3, src["bucket"], src["transactions_prefix"], day)
        if frame is None or not len(frame):
            out["rows"].append({"day": day, "skipped": "empty partition"})
            continue
        i = rng.randrange(len(frame))
        one = frame.iloc[[i]].reset_index(drop=True)
        produced = at.normalize_trn(one, "49financial")[0]
        out["rows"].append({
            "day": day,
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
