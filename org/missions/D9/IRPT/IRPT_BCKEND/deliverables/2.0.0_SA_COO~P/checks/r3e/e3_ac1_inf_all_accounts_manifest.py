"""~E round 3 AC1 -- on 2026-09-25 the Inflection holdings gold carries EVERY account that held positions on the prior
trading day, and the manifest reads complete (PRD v0.19 rulings 4, 9, 11; 1.0.0_SA_CTO round-19 analysis section 6).

Usage: python e3_ac1_inf_all_accounts_manifest.py [day, default 2026-09-25]
The accounts are the distinct accountId values (as strings) in Inflection's positions silver,
s3://opal-data-assets/orion/inflection/silver/fact_positions/date=<prior trading day>/ (PRD v0.19 ruling 1). Each must
have exactly one row in the gold at address("irpt", "inflection", "gold", "holdings_performance_daily", "date=<day>")
whose account_id is that accountId -- status OK or a named non-OK status. The manifest at
address(..., "holdings_performance_manifest", "date=<day>") carries accounts_with_prior_holdings, computable_count,
not_computable_count and complete, with computable + not_computable == accounts_with_prior_holdings == the silver
count, and complete true.
"""
import io
import sys
from pathlib import Path

import boto3
import pandas as pd

ROOT = Path(__file__).resolve().parents[9]
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402
import trading_calendar  # noqa: E402

DAY = sys.argv[1] if len(sys.argv) > 1 else "2026-09-25"
SILVER_BUCKET, SILVER_PREFIX = "opal-data-assets", "orion/inflection/silver/fact_positions/"
s3 = boto3.client("s3")


def frame(bucket, prefix):
    keys = [o["Key"] for o in s3.list_objects_v2(Bucket=bucket, Prefix=prefix).get("Contents", []) if o["Key"].endswith(".parquet")]
    if not keys:
        return None
    return pd.concat([pd.read_parquet(io.BytesIO(s3.get_object(Bucket=bucket, Key=k)["Body"].read())) for k in keys])


def split(uri):
    bucket, _, key = uri[len("s3://"):].partition("/")
    return bucket, key.rstrip("/") + "/"


prev = str(trading_calendar.prev_trading_day(pd.Timestamp(DAY).date()))
silver = frame(SILVER_BUCKET, "%sdate=%s/" % (SILVER_PREFIX, prev))
want = set(silver["accountId"].astype(str))
gold = frame(*split(opal_naming.address("irpt", "inflection", "gold", "holdings_performance_daily", "date=%s" % DAY)))
have = gold["account_id"].astype(str).value_counts() if gold is not None else pd.Series(dtype=int)
missing = sorted(want - set(have.index))
dupes = sorted(have[have > 1].index)
man = frame(*split(opal_naming.address("irpt", "inflection", "gold", "holdings_performance_manifest", "date=%s" % DAY)))
m = man.iloc[0].to_dict() if man is not None and len(man) else {}
counts_ok = (m.get("accounts_with_prior_holdings") == len(want)
             and (m.get("computable_count", -1) + m.get("not_computable_count", -1)) == len(want)
             and bool(m.get("complete")) is True)
print("silver accounts at %s: %d | gold rows at %s: %d | missing %d | duplicated %d | manifest %s" % (
    prev, len(want), DAY, int(have.sum()) if len(have) else 0, len(missing), len(dupes),
    {k: m.get(k) for k in ("accounts_with_prior_holdings", "computable_count", "not_computable_count", "complete")}))
ok = not missing and not dupes and counts_ok
if ok:
    print("E3-AC1 PASS")
else:
    print("E3-AC1 FAIL")
sys.exit(0 if ok else 1)
