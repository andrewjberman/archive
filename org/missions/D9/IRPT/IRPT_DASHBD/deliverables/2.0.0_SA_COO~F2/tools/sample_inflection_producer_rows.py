"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY sampler for the Inflection J2 criterion (DBF131-1-J2), under the CTO's natural-key ruling (msg 9192).

  python <this file> <out.json> <hashed_out.json> [seed] [n]       defaults: seed 132, n 20 (round 132: ONE row is forced to be a ROLLED line)

The comparison key is the source row's NATURAL KEY: account, trade date, transaction description, symbol, units and amount (`accountId`, `transDate`,
`transactionDescription`, `ticker`, `noUnits`, `transAmount`). Only rows whose status is Complete are candidates (the producer's own row filter), and
the sample is drawn ONLY from rows whose natural key is UNIQUE within its partition; a duplicate key is a finding and never a sample. The tool first
counts, over EVERY partition, the Complete rows and keys that are not unique (counts only). It then draws `n` partitions with a fixed seed (one row
each), runs the PRODUCER (`account_transaction_inflection.split_complete` then `normalize_trn`; nothing is written: no S3 put, no upload) on each, and
writes the producer's output beside the source row's own values for every field the contract fills. Two files: `<out.json>` holds client figures and
an account id (the git-ignored `org/mcp/drive_ticks/`, never committed); `<hashed_out.json>` holds only the day, the sha256 of the natural key and the
producer's non-figure results, and is the form that is committed. No row locator is written. GET requests only.
"""
import datetime as dt
import hashlib
import importlib.util
import io
import json
import random
import sys
from decimal import Decimal
from pathlib import Path

import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"))
import account_return_daily as ard  # noqa: E402
import trading_calendar as tc  # noqa: E402


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


iar = load("iar", "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
at = load("account_transaction_inflection", "data/assets/scripts/gold/irpt_reporting/account_transaction_inflection.py")
CONTRACT = json.loads((ROOT / "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json").read_text(encoding="utf-8"))
BUCKET, _, REST = iar.ORION_SILVER[len("s3://"):].partition("/")
PREFIX = REST + "fact_transactions/"
KEY_FIELDS = ["accountId", "transDate", "transactionDescription", "ticker", "noUnits", "transAmount"]
NATURAL_KEY_LABELS = ["account", "trade date", "transaction description", "symbol", "units", "amount (transAmount)"]
SOURCE_FIELDS = ["id", "accountId", "transDate", "status", "transactionDescription", "ticker", "productName", "custodianName", "noUnits", "navPrice",
                 "transAmount"]
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def plain(v):
    if v is None:
        return None
    if isinstance(v, Decimal):
        return str(v)
    if hasattr(v, "isoformat"):
        return v.isoformat()
    try:
        if v != v:
            return None
    except Exception:  # noqa: BLE001
        pass
    return v.item() if hasattr(v, "item") else v


def read_day(day, columns=None):
    tables = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="%sdate=%s/" % (PREFIX, day)):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                raw = s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()
                tables.append(pq.read_table(io.BytesIO(raw), columns=columns))
    return pa.concat_tables(tables, promote_options="default").to_pandas() if tables else None


_TRADING = {}


def non_trading(value):
    """True when the transDate is a non-trading day (the one business-date rule rolls it forward)."""
    if value not in _TRADING:
        _TRADING[value] = not tc.is_trading_day(dt.date.fromisoformat(str(value)))
    return _TRADING[value]


def rolled_mask(frame):
    return frame["transDate"].map(non_trading)


def complete_only(frame):
    return frame[frame["status"] == "Complete"].reset_index(drop=True)


def main(out_path, hashed_path, seed=132, n=20):
    days = ard.partition_days(s3, BUCKET, PREFIX)
    rows_total = dup_rows = dup_keys = 0
    unique_by_day = {}
    rolled_by_day = {}
    for day in days:
        frame = read_day(day, KEY_FIELDS + ["status"])
        if frame is None or not len(frame):
            continue
        frame = complete_only(frame)
        if not len(frame):
            continue
        sizes = frame.groupby(KEY_FIELDS, dropna=False).size()
        rows_total += len(frame)
        dup_keys += int((sizes > 1).sum())
        dup_rows += int(sizes[sizes > 1].sum())
        unique_by_day[day] = int((sizes == 1).sum())
        rolled_by_day[day] = int((rolled_mask(frame) & ~frame.duplicated(KEY_FIELDS, keep=False)).sum())
    census = {"partitions": len(days), "rows_complete": rows_total, "rows_in_non_unique_keys": dup_rows, "non_unique_keys": dup_keys,
              "share_of_rows_non_unique": round(dup_rows / rows_total, 6) if rows_total else None,
              "partitions_with_a_unique_row": sum(1 for v in unique_by_day.values() if v),
              "unique_rolled_rows": sum(rolled_by_day.values()), "partitions_with_a_unique_rolled_row": sum(1 for v in rolled_by_day.values() if v)}
    print("duplicate census:", census, flush=True)
    rng = random.Random(seed)
    roll_day = rng.choice(sorted(d for d, v in rolled_by_day.items() if v))
    picked = sorted(rng.sample(sorted(d for d, v in unique_by_day.items() if v and d != roll_day), n - 1) + [roll_day])
    out = {"seed": seed, "n": n, "drawn_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "contract_version": CONTRACT["contract_version"], "natural_key": NATURAL_KEY_LABELS, "id_field": "id",
           "rule": "CTO msg 9192: compare by the natural key; the id only where non-null and unique within the partition; sample only from "
                   "Complete rows whose key is unique within the partition; a duplicate key is a finding, never a sample; no row locator",
           "duplicate_census_inflection": census, "rows": []}
    hashed = {"doc": ("The Inflection J1 sample (DBF132-1-J1), committed WITHOUT client data: per sampled row the partition day, the sha256 of the "
                      "natural key (the day and the six key values joined by '|', str()) and the producer's non-figure results. No account id, "
                      "units, amount or symbol is written. Re-run: regenerate the draw with the same seed on the same source "
                      "(tools/sample_inflection_producer_rows.py) and compare the hashes. The un-hashed file stays untracked."),
              "seed": seed, "n": n, "drawn_at_utc": out["drawn_at_utc"], "contract_version": CONTRACT["contract_version"],
              "natural_key": NATURAL_KEY_LABELS, "id_field": "id", "duplicate_census_inflection": census, "rows": []}
    for day in picked:
        frame = complete_only(read_day(day))
        keyed = frame[KEY_FIELDS]
        mask = ~keyed.duplicated(keep=False)
        if day == roll_day:
            mask = mask & rolled_mask(frame).to_numpy()
        cand = [i for i in range(len(frame)) if bool(mask.iloc[i] if hasattr(mask, "iloc") else mask[i])]
        i = cand[rng.randrange(len(cand))]
        one = frame.iloc[[i]].reset_index(drop=True)
        kept, _excluded = at.split_complete(one)
        prod = at.normalize_trn(kept, "inflection")[0]
        key_values = [str(plain(one.iloc[0][k])) for k in KEY_FIELDS]
        out["rows"].append({"day": day, "natural_key_values": dict(zip(NATURAL_KEY_LABELS, key_values)), "id_usable": True,
                            "source": {k: plain(one.iloc[0].get(k)) for k in SOURCE_FIELDS},
                            "producer_output": {k: plain(v) for k, v in prod.items()}})
        hashed["rows"].append({"day": day, "natural_key_sha256": hashlib.sha256("|".join([day] + key_values).encode("utf-8")).hexdigest(),
                               "id_usable": True, "txn_type": prod["txn_type"], "action": prod["action"], "flow_class": prod["flow_class"],
                               "coverage": prod["coverage"], "settle_date_present": prod["settle_date"] is not None,
                               "fee_present": prod["fee"] is not None, "price_present": prod["price"] is not None,
                               "rolled": str(prod["business_date"]) != str(prod["trade_date"]),
                               "source_txn_id_present": prod["source_txn_id"] is not None,
                               "source_action_raw_equals_source": prod["source_action_raw"] == plain(one.iloc[0]["transactionDescription"])})
        print("sampled", day, flush=True)
    assert any(r["rolled"] for r in hashed["rows"]), "the sample must hold a rolled line"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    text = json.dumps(hashed, indent=1)
    assert text.isascii()
    open(hashed_path, "w", encoding="utf-8", newline="\n").write(text + "\n")
    print("wrote", len(out["rows"]), "rows to", out_path, "and the hashed form to", hashed_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 132, int(sys.argv[4]) if len(sys.argv) > 4 else 20)
