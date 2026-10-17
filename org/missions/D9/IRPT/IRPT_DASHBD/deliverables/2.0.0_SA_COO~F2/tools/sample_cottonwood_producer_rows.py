"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY sampler for the Cottonwood J1 criterion (DBF130-1-J1), under the CTO's ruling (msg 9192).

  python <this file> <out.json> <hashed_out.json> [seed] [n]       defaults: seed 131, n 20 (round 131: the FRESH sample after the key fix)
  Round 138 (contract 0.5.1): TWO forced lines, one whose Action carries blank padding and one whose Trade Date is not a trading day (claim `inferred`); the hashed form
  also carries business_date_claim and whether business_date equals the Trade Date.

The comparison key is the source row's NATURAL KEY: account, trade date, transaction code, symbol, units and amount (`AccountID`, `Trade Date`,
the code = `Transaction Type | Transaction Sub Type | Action`, `Symbol`, `Units`, `Market Value`). The sample is drawn ONLY from rows whose natural key is
UNIQUE within its partition; a duplicate key is a finding and never a sample, and the tool first counts, over EVERY partition, the rows and keys
that are not unique (counts only). It then draws `n` rows with a fixed seed (one partition each; ONE of them is forced to be a row whose Action
carries blank padding, the case the CTO's round-130 ruling names), runs the PRODUCER
(`account_transaction_cottonwood.normalize_trn`, nothing is written: no S3 put, no upload) on each, and writes the producer's output beside the
source row's own values for every field the contract fills. Two files: `<out.json>` holds client figures and an account id (the git-ignored
`org/mcp/drive_ticks/`, never committed); `<hashed_out.json>` holds only the day, the sha256 of the natural key and the producer's non-figure
results, and is the form that is committed. No row locator is written. GET requests only.
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
import pandas as pd
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


cbd = load("cbd", "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py")
at = load("account_transaction_cottonwood", "data/assets/scripts/gold/irpt_reporting/account_transaction_cottonwood.py")
CONTRACT = json.loads((ROOT / "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json").read_text(encoding="utf-8"))
PREFIX = cbd.SILVER_ROOT + "fact_transactions/"
KEY_FIELDS = ["AccountID", "Trade Date", "Transaction Type", "Transaction Sub Type", "Action", "Symbol", "Units", "Market Value"]
NATURAL_KEY_LABELS = ["account", "trade date", "transaction code (type | sub type | action)", "symbol", "units", "amount (Market Value)"]
SOURCE_FIELDS = ["TransactionID", "AccountID", "Trade Date", "Settle Date", "Return Date", "Transaction Type", "Transaction Sub Type", "Action",
                 "External Flow", "Units", "Price", "Market Value", "Transaction Fee", "Account Fee", "Symbol", "Asset Name", "Custodian"]
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
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=cbd.BUCKET, Prefix="%sdate=%s/" % (PREFIX, day)):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                raw = s3.get_object(Bucket=cbd.BUCKET, Key=o["Key"])["Body"].read()
                tables.append(pq.read_table(io.BytesIO(raw), columns=columns))
    return pa.concat_tables(tables, promote_options="default").to_pandas() if tables else None


def keys_of(frame):
    cols = [frame[c].astype(str).tolist() for c in KEY_FIELDS]
    return [(a, b, "%s | %s | %s" % (t, st, ac), s, u, m) for a, b, t, st, ac, s, u, m in zip(*cols)]


def _is_rolled(trade_date_cell):
    """True when the producer's own reader gives a Trade Date that is not a trading day (the rows it rolls forward and stamps `inferred`)."""
    d = at._day_of(trade_date_cell)
    return d is not None and not tc.is_trading_day(d)


def main(out_path, hashed_path, seed=131, n=20):
    days = ard.partition_days(s3, cbd.BUCKET, PREFIX)
    rows_total = dup_rows = dup_keys = 0
    unique_by_day = {}
    padded_by_day = {}
    rolled_by_day = {}
    for day in days:
        frame = read_day(day, KEY_FIELDS)
        if frame is None or not len(frame):
            continue
        counts = {}
        for k in keys_of(frame):
            counts[k] = counts.get(k, 0) + 1
        rows_total += len(frame)
        dup_keys += sum(1 for c in counts.values() if c > 1)
        dup_rows += sum(c for c in counts.values() if c > 1)
        unique_by_day[day] = sum(1 for c in counts.values() if c == 1)
        actions = frame["Action"].astype(str).tolist()
        padded_by_day[day] = sum(1 for k, a in zip(keys_of(frame), actions) if a != a.strip() and counts[k] == 1)
        rolled_by_day[day] = sum(1 for k in keys_of(frame) if counts[k] == 1 and _is_rolled(k[1]))
    census = {"partitions": len(days), "rows": rows_total, "rows_in_non_unique_keys": dup_rows, "non_unique_keys": dup_keys,
              "share_of_rows_non_unique": round(dup_rows / rows_total, 6) if rows_total else None,
              "partitions_with_a_unique_row": sum(1 for v in unique_by_day.values() if v)}
    print("duplicate census:", census, flush=True)
    rng = random.Random(seed)
    pad_days = sorted(d for d, v in padded_by_day.items() if v)
    pad_day = rng.choice(pad_days)
    rolled_days = sorted(d for d, v in rolled_by_day.items() if v and d != pad_day)
    rolled_day = rng.choice(rolled_days)
    picked = sorted(rng.sample(sorted(d for d, v in unique_by_day.items() if v and d not in (pad_day, rolled_day)), n - 2) + [pad_day, rolled_day])
    census["partitions_with_a_unique_padded_action_row"] = len(pad_days)
    census["partitions_with_a_unique_rolled_row"] = len(rolled_days) + (1 if rolled_by_day.get(pad_day) else 0)
    out = {"seed": seed, "n": n, "drawn_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "contract_version": CONTRACT["contract_version"], "natural_key": NATURAL_KEY_LABELS, "id_field": "TransactionID",
           "rule": "CTO msg 9192: compare by the natural key; the id only where non-null and unique within the partition; sample only from "
                   "rows whose key is unique within the partition; a duplicate key is a finding, never a sample; no row locator",
           "duplicate_census_cottonwood": census, "rows": []}
    hashed = {"doc": ("The Cottonwood J1 sample (DBF131-1-J1), committed WITHOUT client data: per sampled row the partition day, the sha256 of the "
                      "natural key (the day and the six key values joined by '|', str()) and the producer's non-figure results. No account id, "
                      "units, amount or symbol is written. Re-run: regenerate the draw with the same seed on the same source "
                      "(tools/sample_cottonwood_producer_rows.py) and compare the hashes. The un-hashed file stays untracked."),
              "seed": seed, "n": n, "drawn_at_utc": out["drawn_at_utc"], "contract_version": CONTRACT["contract_version"],
              "natural_key": NATURAL_KEY_LABELS, "id_field": "TransactionID", "duplicate_census_cottonwood": census, "rows": []}
    for day in picked:
        frame = read_day(day)
        keys = keys_of(frame)
        counts = {}
        for k in keys:
            counts[k] = counts.get(k, 0) + 1
        cand = [i for i, k in enumerate(keys) if counts[k] == 1]
        if day == pad_day:
            acts = frame["Action"].astype(str).tolist()
            cand = [i for i in cand if acts[i] != acts[i].strip()]
        if day == rolled_day:
            cand = [i for i in cand if _is_rolled(keys[i][1])]
        i = cand[rng.randrange(len(cand))]
        one = frame.iloc[[i]].reset_index(drop=True)
        prod = at.normalize_trn(pd.DataFrame(one), "cottonwood")[0]
        tid = plain(one.iloc[0].get("TransactionID"))
        out["rows"].append({"day": day, "natural_key_values": dict(zip(NATURAL_KEY_LABELS, [str(x) for x in keys[i]])),
                            "id_usable": bool(tid), "source": {k: plain(one.iloc[0].get(k)) for k in SOURCE_FIELDS},
                            "producer_output": {k: plain(v) for k, v in prod.items()}})
        hashed["rows"].append({"day": day, "natural_key_sha256": hashlib.sha256("|".join([day] + [str(x) for x in keys[i]]).encode("utf-8")).hexdigest(),
                               "id_usable": bool(tid), "txn_type": prod["txn_type"], "action": prod["action"], "flow_class": prod["flow_class"],
                               "coverage": prod["coverage"], "settle_date_present": prod["settle_date"] is not None,
                               "business_date_claim": prod["business_date_claim"],
                               "business_date_is_trade_date": str(prod["business_date"])[:10] == str(prod["trade_date"])[:10],
                               "fee_present": prod["fee"] is not None, "source_txn_id_present": prod["source_txn_id"] is not None,
                               "source_action_raw_has_blank_padding": prod["source_action_raw"] is not None
                               and prod["source_action_raw"] != prod["source_action_raw"].strip(),
                               "source_action_raw_equals_source": prod["source_action_raw"] == plain(one.iloc[0]["Action"])})
        print("sampled", day, flush=True)
    assert any(r["source_action_raw_has_blank_padding"] for r in hashed["rows"]), "the sample must hold a row whose Action carries blank padding"
    assert any(r["business_date_claim"] == "inferred" for r in hashed["rows"]), "the sample must hold a rolled (inferred) line"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    text = json.dumps(hashed, indent=1)
    assert text.isascii()
    open(hashed_path, "w", encoding="utf-8", newline="\n").write(text + "\n")
    print("wrote", len(out["rows"]), "rows to", out_path, "and the hashed form to", hashed_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 131, int(sys.argv[4]) if len(sys.argv) > 4 else 20)
