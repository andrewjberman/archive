#!/usr/bin/env python3
"""MX-s-2 probes -- READ ONLY.

  AC3   the acceptance probe: the latest gold/timeseries/holdings_lots partition
        carries ZERO null-cusip rows that are not cash.
  DIAG  the diagnostic behind it: whether a re-run of B_01 against TODAY'S bridge
        could resolve any of them, and how many assets BD itself supplies with no
        cusip at all.

  THE CASH RULE IS A STATED SUBSTITUTE, NOT B_01's OWN RULE, AND THE DIFFERENCE IS
  MEASURED RATHER THAN GLOSSED.
  B_01's rule keys on `asset_id == 4` / `cusip == 'CASH'`
  (data/black_diamond/scripts/gold/B_01.holdings_lots.py:284-292). The SERVED
  partition does not carry `asset_id` at all -- its columns are lot_id,
  snapshot_date, account_id, relationship_id, account_name, account_type,
  account_registration_type, tax_status, qualified_flag, asset_name, ticker, cusip,
  ... -- so B_01's rule is NOT COMPUTABLE from the artifact AC3 is pointed at. This
  probe substitutes a name-token rule over `asset_name`, prints the tokens it used
  and the residual it cannot classify, and never claims to be the original rule.
"""
import io
import re
import sys
from datetime import timezone

import boto3
import pandas as pd

BUCKET = "opal-data-bd"
GOLD_PREFIX = "gold/timeseries/holdings_lots/"
DIM_KEY = "silver/bd_assets_dim.parquet"

# The substitute cash rule, stated as data so a reader can argue with it.
CASH_TOKENS = ("FCASH", "CASH", "MONEY MARKET", "MONEY MKT", "MMKT",
               "TREASURY LIQUID", "GOVERNMENT LIQUID", "LIQUIDITY FUND",
               "SWEEP", "DEPOSIT")
CASH_RE = re.compile("|".join(re.escape(t) for t in CASH_TOKENS), re.IGNORECASE)
NULLISH = ("", "nan", "None", "CASH")

s3 = boto3.client("s3", region_name="us-east-1")


def latest_partition():
    pag = s3.get_paginator("list_objects_v2")
    ks = [o["Key"] for p in pag.paginate(Bucket=BUCKET, Prefix=GOLD_PREFIX)
          for o in p.get("Contents", []) if o["Key"].endswith(".parquet")]
    if not ks:
        print("OUT-OF-CORPUS: 0 objects under s3://%s/%s -- an absence, not a zero"
              % (BUCKET, GOLD_PREFIX))
        sys.exit(2)
    ks.sort()
    return ks[-1], len(ks)


def read(key, columns=None):
    return pd.read_parquet(
        io.BytesIO(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()),
        columns=columns)


def load():
    key, n = latest_partition()
    df = read(key, columns=["asset_name", "ticker", "cusip", "market_value"])
    cus = df["cusip"].astype(str).str.strip()
    isnull = df["cusip"].isna() | cus.isin(NULLISH)
    name = df["asset_name"].astype(str).fillna("")
    is_cash = name.str.contains(CASH_RE, na=False)
    return key, n, df, name, isnull, is_cash


def ac3():
    key, n, df, name, isnull, is_cash = load()
    total = len(df)
    n_null = int(isnull.sum())
    n_cash = int((isnull & is_cash).sum())
    n_bad = int((isnull & ~is_cash).sum())
    blank = int((isnull & ~is_cash & (name.str.strip() == "")).sum())

    print("instrument : latest of %d partition(s) under s3://%s/%s, read by key"
          % (n, BUCKET, GOLD_PREFIX))
    print("partition  : %s" % key)
    print("cash rule  : SUBSTITUTE (asset_name token match), because the served")
    print("             partition carries no asset_id -- B_01's own rule is not")
    print("             computable here. Tokens: %s" % ", ".join(CASH_TOKENS))
    print("DENOMINATOR: %d rows" % total)
    print("  null cusip (incl. literal CASH) : %d" % n_null)
    print("  of which cash by the substitute : %d" % n_cash)
    print("  NON-CASH null cusip             : %d   <- AC3 counts this" % n_bad)
    print("  ... of those, blank asset_name  : %d   (unclassifiable either way)" % blank)
    if n_bad == 0:
        print("VERDICT: PASS-MXS2-AC3")
        return 0
    print("VERDICT: FAIL-MXS2-AC3 (%d non-cash null-cusip row(s))" % n_bad)
    return 1


def diag():
    key, n, df, name, isnull, is_cash = load()
    bad = isnull & ~is_cash

    dim = read(DIM_KEY, columns=["asset_id", "cusip", "ticker", "asset_name"])
    dcus = dim["cusip"].astype(str).str.strip()
    has_cusip = ~dcus.isin(NULLISH) & dim["cusip"].notna()
    dh = s3.head_object(Bucket=BUCKET, Key=DIM_KEY)

    print("partition : %s" % key)
    print("bridge    : s3://%s/%s  LastModified %s"
          % (BUCKET, DIM_KEY, dh["LastModified"].astimezone(timezone.utc).isoformat()))
    print("DENOMINATOR: bridge carries %d asset_id(s)" % len(dim))
    print("  with a usable cusip    : %d" % int(has_cusip.sum()))
    print("  WITHOUT any cusip      : %d   <- BD supplies no cusip for these at all,"
          % int((~has_cusip).sum()))
    print("                               so no rebuild can ever resolve them")
    print()

    # Can TODAY'S bridge resolve the served nulls? Join on ticker, the only key both
    # the served partition and the bridge carry (the served side has no asset_id).
    dt_ok = dim[has_cusip]
    tick_to_cusip = {str(t).strip().upper(): c for t, c in
                     zip(dt_ok["ticker"], dt_ok["cusip"])
                     if str(t).strip().upper() not in ("", "NAN", "NONE")}
    bt = df.loc[bad, "ticker"].astype(str).str.strip().str.upper()
    resolvable = bt.isin(tick_to_cusip)
    print("DENOMINATOR: %d non-cash null-cusip row(s), %d distinct ticker(s)"
          % (int(bad.sum()), bt.nunique()))
    print("  rows whose TICKER today's bridge could resolve : %d" % int(resolvable.sum()))
    print("  rows it could not                              : %d"
          % int((~resolvable).sum()))
    print("  blank/absent ticker among them                 : %d"
          % int((bt.isin(("", "NAN", "NONE"))).sum()))
    print()
    print("NOTE ON THIS JOIN: B_01 joins on asset_id, not ticker. A ticker hit here is")
    print("evidence the ASSET is in the bridge, not that B_01's own join would resolve")
    print("it -- the two keys can disagree. It bounds the fixable set from ABOVE.")
    return 0


if __name__ == "__main__":
    arm = (sys.argv[1] if len(sys.argv) > 1 else "AC3").upper()
    sys.exit({"AC3": ac3, "DIAG": diag}[arm]())
