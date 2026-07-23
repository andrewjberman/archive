"""Excusals evidence sweep -- orion accounts_v2 roster departures 609/1225/703/560.

The committed evidence record behind lib/nna_coverage_excusals.json entry "609"
(CTO ruling 20260723T150205Z) and the Saarinen 560/703/1225 package routed to
Andrew via COO. Re-runnable; every scan prints its denominator (Rule 22 /
VERIFICATION LAW 10). Findings as of 2026-07-23:

  1. accounts_v2 snapshots 07-18 vs 07-19 are IDENTICAL (873=873) -- the guard's
     07-19 firing date is the RUN axis, not the roster axis. Actual last-present:
     1225/703/560 = 2026-07-08; 609 = 2026-07-16 (80-snapshot sweep 04-28..07-23).
  2. 609 "Ronald Moir Estate": funded 2024-11-06 $1,111,495.49; distributions
     -$100,000.00 @2025-02-07, -$981,513.14 @2026-07-08; current_value $152.54
     (07-12..14) -> $0.00 (07-15/16) -> dropped. Vendor-evidenced estate closure.
  3. 560/703/1225: one household (Saarinen, TOD x3, rep Scanlan), all last present
     07-08 still valued ($68,029.12 combined), status Normal/active, NO closure
     marker; transactions sharpener over the last snapshots carrying them: final
     transDate 2026-06-26 (routine), transfer/journal/ACAT/withdrawal rows EVER: 0.
  4. Served NNA (1,416 gold/canonical partitions swept): 560 +$15,661.86/38,
     703 +$17,511.03/36, 1225 +$19,431.91/39, 609 -$94,561.08/11; net -$41,956.28
     (guard's -$44,206.28 is the rewritten-partition-set denominator, not all-history).
"""
from __future__ import annotations

import io
from concurrent.futures import ThreadPoolExecutor

import boto3
import pandas as pd

BUCKET = "opal-data-inf"
ROSTER_PREFIX = "silver/api_dims/accounts_v2/"
NNA_PREFIX = "gold/canonical/"
TXN_PREFIX = "silver/transactions/"
ACCOUNTS = (609, 1225, 703, 560)
SAARINEN = (560, 703, 1225)
TRANSFER_PAT = "transfer|journal|acat|deliver|withdraw"


def _s3():
    return boto3.client("s3")


def _keys(s3, prefix, want=None):
    pag = s3.get_paginator("list_objects_v2")
    out = []
    for page in pag.paginate(Bucket=BUCKET, Prefix=prefix):
        for o in page.get("Contents", []):
            if want is None or want(o["Key"]):
                out.append(o["Key"])
    return sorted(out)


def _parquet(s3, key, columns=None):
    body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    return pd.read_parquet(io.BytesIO(body), columns=columns)


def roster_presence(s3):
    """Per-account presence across every accounts_v2 snapshot. Prints denominator."""
    keys = _keys(s3, ROSTER_PREFIX, lambda k: k.endswith("data.parquet"))
    seen = {a: [] for a in ACCOUNTS}

    def one(key):
        df = _parquet(s3, key, columns=["account_id"])
        ids = set(pd.to_numeric(df["account_id"], errors="coerce").dropna().astype(int))
        day = key.split("snapshot_date=")[1].split("/")[0]
        return day, ids

    with ThreadPoolExecutor(16) as ex:
        for day, ids in ex.map(one, keys):
            for a in ACCOUNTS:
                if a in ids:
                    seen[a].append(day)
    print(f"roster sweep: {len(keys)} snapshots")
    for a in ACCOUNTS:
        s = sorted(seen[a])
        tail = f"first={s[0]} last={s[-1]}" if s else "NEVER present"
        print(f"  account {a}: {len(s)} snapshot(s), {tail}")
    return seen


def served_nna(s3):
    """Per-account served NNA across ALL gold/canonical partitions. Prints denominator."""
    keys = _keys(s3, NNA_PREFIX, lambda k: "canonical_nna_" in k)
    accts = set(ACCOUNTS)

    def one(key):
        df = _parquet(s3, key, columns=["date", "account_id", "net_nna"])
        df["account_id"] = pd.to_numeric(df["account_id"], errors="coerce")
        hit = df[df["account_id"].isin(accts)]
        return hit if len(hit) else None

    frames = []
    with ThreadPoolExecutor(24) as ex:
        for r in ex.map(one, keys):
            if r is not None:
                frames.append(r)
    all4 = pd.concat(frames)
    all4["net_nna"] = pd.to_numeric(all4["net_nna"], errors="coerce")
    print(f"NNA sweep: {len(keys)} partitions; rows for the 4: {len(all4)}")
    print(all4.groupby("account_id").agg(
        total_nna=("net_nna", "sum"), n_part=("date", "nunique"),
        first=("date", "min"), last=("date", "max")).to_string())
    print(f"  NET across 4 = {all4['net_nna'].sum():,.2f}")
    return all4


def transactions_sharpener(s3, snapshot="2026-07-08"):
    """Saarinen trio: last transactions + transfer-type census in the last
    snapshot that still carried them (the feed is roster-scoped -- later
    snapshots drop their history entirely, which is itself the guard's premise)."""
    df = _parquet(s3, f"{TXN_PREFIX}{snapshot}.parquet")
    df["accountId"] = pd.to_numeric(df["accountId"], errors="coerce")
    sub = df[df["accountId"].isin(SAARINEN)].copy()
    sub["transDate"] = pd.to_datetime(sub["transDate"], errors="coerce")
    print(f"sharpener snapshot {snapshot}: {len(sub)} rows for the trio "
          f"(of {len(df)} total)")
    print("  max transDate per account:")
    for a, d in sub.groupby("accountId")["transDate"].max().items():
        print(f"    {int(a)}: {d.date()}")
    ttypes = sub["trans_type_desc"].astype(str).str.lower()
    xfer = sub[ttypes.str.contains(TRANSFER_PAT, regex=True)]
    print(f"  transfer/journal/ACAT/withdrawal rows EVER: {len(xfer)}")
    return sub, xfer


if __name__ == "__main__":
    s3 = _s3()
    roster_presence(s3)
    served_nna(s3)
    transactions_sharpener(s3)
