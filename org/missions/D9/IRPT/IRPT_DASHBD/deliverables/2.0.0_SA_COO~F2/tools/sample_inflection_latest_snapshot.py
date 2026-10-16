"""IRPT_DASHBD (workstream F-SHIP, ~F2): the READ-ONLY sampler for the Inflection J grade on the ONE LATEST SNAPSHOT (round 135; CTO msgs 9625, 9669).

  python <this file> <out.json> <hashed_out.json> [seed] [n]       defaults: seed 135, n 20 (ONE row is forced to be a ROLLED line)

The Orion silver fact_transactions table is CUMULATIVE SNAPSHOTS: every partition holds the whole history. So this sampler reads ONE partition, the newest, and
every denominator it prints is that snapshot's (never a sum over partitions). It then:
  1. counts, over the one snapshot, the rows per status, the Complete rows, and the Complete rows and keys whose NATURAL KEY (accountId, transDate,
     transactionDescription, ticker, noUnits, transAmount) is not unique (counts only);
  2. derives the Reversed keys from THAT snapshot (reversed_keys_of) and runs the PRODUCER on the whole snapshot (split_complete with those keys, then
     normalize_trn; nothing is written: no S3 put, no upload) to print the emitted-row count and the no-repeat check (no source line on two emitted days);
  3. draws `n` rows from the snapshot's Complete, key-unique, not-offset lines with a fixed seed (one forced rolled line) and writes the producer's output beside the
     source row's own values for every field the contract fills.
Two files: `<out.json>` holds client figures and an account id (the git-ignored `org/mcp/drive_ticks/`, never committed); `<hashed_out.json>` holds only the
snapshot day, the sha256 of the natural key and the producer's non-figure results, and is the form that is committed. No row locator is written. GET only.
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


def read_day(day):
    tables = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="%sdate=%s/" % (PREFIX, day)):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                raw = s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()
                tables.append(pq.read_table(io.BytesIO(raw)))
    return pa.concat_tables(tables, promote_options="default").to_pandas() if tables else None


_TRADING = {}


def non_trading(value):
    if value not in _TRADING:
        _TRADING[value] = not tc.is_trading_day(dt.date.fromisoformat(str(value)))
    return _TRADING[value]


def main(out_path, hashed_path, seed=135, n=20):
    days = ard.partition_days(s3, BUCKET, PREFIX)
    snap = sorted(days)[-1]
    frame = read_day(snap)
    per_status = {k: int(v) for k, v in frame["status"].value_counts().items()}
    complete = frame[frame["status"] == "Complete"].reset_index(drop=True)
    sizes = complete.groupby(KEY_FIELDS, dropna=False).size()
    dup_rows, dup_keys = int(sizes[sizes > 1].sum()), int((sizes > 1).sum())
    rkeys = at.reversed_keys_of(frame)
    kept, excluded = at.split_complete(frame, reversed_keys=rkeys)
    rows = at.normalize_trn(kept, "inflection")
    by_id = {}
    repeats = 0
    for r in rows:
        if r["source_txn_id"] in by_id and by_id[r["source_txn_id"]] != str(r["business_date"]):
            repeats += 1
        by_id[r["source_txn_id"]] = str(r["business_date"])
    census = {"snapshot": snap, "partitions_not_read": len(days) - 1, "rows": int(len(frame)), "rows_per_status": per_status, "rows_complete": int(len(complete)),
              "rows_in_non_unique_keys": dup_rows, "non_unique_keys": dup_keys,
              "share_of_complete_rows_non_unique": round(dup_rows / len(complete), 6) if len(complete) else None,
              "reversed_keys": len(rkeys), "excluded_by_the_producer": {k: int(v) for k, v in excluded.items()}, "producer_rows_out": len(rows),
              "source_lines_on_more_than_one_emitted_day": repeats,
              "rolled_rows_out": sum(1 for r in rows if str(r["business_date"]) != str(r["trade_date"]))}
    print("one-snapshot census:", census, flush=True)
    assert repeats == 0, "a source line is emitted on two days"
    emitted_ids = {r["source_txn_id"] for r in rows}
    keyed = complete[KEY_FIELDS]
    unique = ~keyed.duplicated(keep=False)
    id_ok = complete["id"].astype(str).isin(emitted_ids)
    rolled = complete["transDate"].map(non_trading)
    rng = random.Random(seed)
    pool_roll = [i for i in range(len(complete)) if bool(unique.iloc[i] and id_ok.iloc[i] and rolled.iloc[i])]
    pool_all = [i for i in range(len(complete)) if bool(unique.iloc[i] and id_ok.iloc[i] and not rolled.iloc[i])]
    picked = [rng.choice(pool_roll)] + rng.sample(pool_all, n - 1)
    out = {"seed": seed, "n": n, "drawn_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "contract_version": CONTRACT["contract_version"],
           "natural_key": NATURAL_KEY_LABELS, "id_field": "id", "snapshot": snap,
           "rule": "compare by the natural key; the sample is drawn from ONE snapshot (the newest), from Complete lines whose key is unique within it and which "
                   "the producer emits; a duplicate key is a finding, never a sample; no row locator",
           "one_snapshot_census": census, "rows": []}
    hashed = {"doc": ("The Inflection sample on the ONE latest snapshot, committed WITHOUT client data: per sampled row the snapshot day, the sha256 of the natural "
                      "key and the producer's non-figure results. No account id, units, amount or symbol is written. Re-run: tools/sample_inflection_latest_snapshot.py "
                      "with the same seed on the same snapshot and compare the hashes."),
              "seed": seed, "n": n, "drawn_at_utc": out["drawn_at_utc"], "contract_version": CONTRACT["contract_version"], "snapshot": snap,
              "natural_key": NATURAL_KEY_LABELS, "id_field": "id", "one_snapshot_census": census, "rows": []}
    for i in picked:
        one = complete.iloc[[i]].reset_index(drop=True)
        k1, _ex = at.split_complete(one)
        prod = at.normalize_trn(k1, "inflection")[0]
        key_values = [str(plain(one.iloc[0][k])) for k in KEY_FIELDS]
        day = str(prod["business_date"])
        out["rows"].append({"day": day, "natural_key_values": dict(zip(NATURAL_KEY_LABELS, key_values)), "source": {k: plain(one.iloc[0].get(k)) for k in SOURCE_FIELDS},
                            "producer_output": {k: plain(v) for k, v in prod.items()}})
        hashed["rows"].append({"day": day, "natural_key_sha256": hashlib.sha256("|".join([snap] + key_values).encode("utf-8")).hexdigest(),
                               "txn_type": prod["txn_type"], "action": prod["action"], "flow_class": prod["flow_class"], "coverage": prod["coverage"],
                               "settle_date_present": prod["settle_date"] is not None, "fee_present": prod["fee"] is not None, "price_present": prod["price"] is not None,
                               "rolled": str(prod["business_date"]) != str(prod["trade_date"]), "business_date_claim": prod["business_date_claim"],
                               "emitted_in_the_snapshot_run": str(one.iloc[0]["id"]) in emitted_ids,
                               "source_action_raw_equals_source": prod["source_action_raw"] == plain(one.iloc[0]["transactionDescription"])})
    assert any(r["rolled"] for r in hashed["rows"]) and any(not r["rolled"] for r in hashed["rows"]), "the sample must hold a rolled line and a measured line"
    assert all((r["business_date_claim"] == "inferred") == r["rolled"] for r in hashed["rows"]), "the claim must read inferred exactly on the rolled lines"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    text = json.dumps(hashed, indent=1)
    assert text.isascii()
    open(hashed_path, "w", encoding="utf-8", newline="\n").write(text + "\n")
    print("wrote", len(out["rows"]), "rows to", out_path, "and the hashed form to", hashed_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 135, int(sys.argv[4]) if len(sys.argv) > 4 else 20)
