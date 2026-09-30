"""~E round 4 AC3 -- PRD v0.21 ruling 18 (1.0.0_SA_CTO RULING S200, 102669): the trading day that FOLLOWS a NOT COMPUTABLE
(IMPLAUSIBLE-RETURN, ruling 16) day is itself NOT COMPUTABLE ("follows a price discontinuity"), in the 49F and the
Inflection gold, re-emitted.

Usage: python e4_ac3_ruling18_follow_day.py
For each firm (49financial 2024-07-09..2026-09-25, inflection 2020-04-27..2026-09-25): every (account, day d) row with
status IMPLAUSIBLE-RETURN is followed, on the next trading day that carries a row for that account, by a row whose
status is NOT 'OK'. Printed beside: the count of IMPLAUSIBLE-RETURN rows, the follow-day violations, and the 1Y
(2025-09-26..2026-09-25) chain of the 49F accounts ending ..0090 and ..4714 over their OK days.
"""
import io
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pandas as pd

ROOT = Path(__file__).resolve().parents[9]
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402
import trading_calendar  # noqa: E402

s3 = boto3.client("s3")


def read(firm, day):
    uri = opal_naming.address("irpt", firm, "gold", "holdings_performance_daily", "date=%s" % day)
    bucket, _, key = uri[len("s3://"):].partition("/")
    keys = [o["Key"] for o in s3.list_objects_v2(Bucket=bucket, Prefix=key.rstrip("/") + "/").get("Contents", []) if o["Key"].endswith(".parquet")]
    if not keys:
        return None
    f = pd.concat([pd.read_parquet(io.BytesIO(s3.get_object(Bucket=bucket, Key=k)["Body"].read()),
                                   columns=["account_id", "daily_return", "status"]) for k in keys])
    f["d"] = day
    return f


ok_all = True
for firm, first in (("49financial", "2024-07-09"), ("inflection", "2020-04-27")):
    days = [str(d) for d in trading_calendar.trading_days_between(pd.Timestamp(first).date(), pd.Timestamp("2026-09-25").date())]
    with ThreadPoolExecutor(32) as pool:
        g = pd.concat([f for f in pool.map(lambda d: read(firm, d), days) if f is not None])
    g["account_id"] = g["account_id"].astype(str)
    g = g.sort_values(["account_id", "d"])
    g["next_status"] = g.groupby("account_id")["status"].shift(-1)
    imp = g[g["status"].astype(str) == "IMPLAUSIBLE-RETURN"]
    bad = imp[imp["next_status"].astype(str) == "OK"]
    print("%s: IMPLAUSIBLE-RETURN rows %d | follow-day OK violations %d%s" % (
        firm, len(imp), len(bad), (" e.g. %s" % bad[["account_id", "d"]].head(3).values.tolist()) if len(bad) else ""))
    ok_all = ok_all and len(bad) == 0
    if firm == "49financial":
        okr = g[(g["status"].astype(str) == "OK") & (g["d"] >= "2025-09-26")]
        for suf in ("0090", "4714"):
            for a in sorted({x for x in okr["account_id"].unique() if x.endswith(suf)}):
                r = okr[okr["account_id"] == a]["daily_return"]
                print("  ..%s 1Y chain %.4f over %d OK days" % (a[-4:], float((1 + r).prod() - 1), len(r)))
print("E4-AC3 PASS" if ok_all else "E4-AC3 FAIL")
sys.exit(0 if ok_all else 1)
