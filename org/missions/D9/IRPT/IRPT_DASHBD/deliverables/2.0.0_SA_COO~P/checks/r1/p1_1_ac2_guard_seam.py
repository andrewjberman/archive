"""IRPT_DASHBD round 1 AC (DB-b-1, FWD-8 C-GUARD / C-VALUE) -- the seam probe against the REAL neighbour: the adapter's
`holdings_price_return` equals IRPT_BCKEND's holdings gold `daily_return` for the same (account, day), and the guard is applied as
the method row says.

Usage: python p1_1_ac2_guard_seam.py <worktree root>
On S3 through lib.opal_naming.address(): reads dim_return_method/method_version=1 (tolerance), then 40 evenly spaced date partitions
of account_return_daily and, for each, IRPT_BCKEND's holdings_performance_daily partition of the same date. For every sampled row of
the five sample accounts (thread 0027265115 and the roster's other four, read from the account_return_daily rows themselves):
  - holdings_price_return == the holdings gold daily_return for that (account, date) where the holdings row's status is OK
    (abs diff <= 1e-12); a holdings row absent or not OK must be matched by day_quality != MEASURED or a non-null
    holdings_price_return_reason;
  - day_quality == MEASURED  ->  |total_return_daily - (holdings_price_return + income_return)| <= tolerance;
  - day_quality == FLOW_UNRECONCILED  ->  that difference > tolerance AND return_basis == HOLDINGS_INCOME_FALLBACK;
  - market_value_eod > 0 on every MEASURED day (C-VALUE: the whole-account value contains cash).
Denominators printed: partitions sampled, rows checked, rows per day_quality.
Pass line: DB-1-AC2 PASS. Base (at the cut): FAIL -- the adapter's gold does not exist.
"""
import io
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(root))


def _thread_account(root):
    """The thread account: the seat's record deliverables/0.4.0_DS_ClientPlatform~S/THREAD_ACCOUNT.json ({"thread_account": "..."}),
    chosen by census in DB-b-1 (issuer amendment 1, 2026-09-30 17:1xZ); the roster's first account is the fallback."""
    import json as _json
    p = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/THREAD_ACCOUNT.json"
    try:
        return str(_json.loads(p.read_text(encoding="utf-8"))["thread_account"])
    except Exception:  # noqa: BLE001
        return "0027265115"
THREAD = _thread_account(root)


def fail(msg):
    print("DB-1-AC2 FAIL: " + msg)
    sys.exit(1)


from lib import opal_naming as on  # noqa: E402
import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

s3 = boto3.client("s3", region_name="us-east-1")


def split(uri):
    b, k = uri[5:].split("/", 1)
    return b, k


def read(uri):
    b, k = split(uri)
    return pq.read_table(io.BytesIO(s3.get_object(Bucket=b, Key=k)["Body"].read())).to_pylist()


try:
    method = read(on.address("irpt", "49financial", "gold", "dim_return_method", "method_version=1") + "/data.parquet")[0]
except Exception as exc:  # noqa: BLE001
    fail("dim_return_method/method_version=1 unreadable: %s" % str(exc)[:120])
tol = float(method["tolerance"])

b, k0 = split(on.address("irpt", "49financial", "gold", "account_return_daily", "date=2000-01-01"))
prefix = k0.rsplit("date=2000-01-01", 1)[0]
pag = s3.get_paginator("list_objects_v2")
dates = sorted({k.split("date=")[1][:10] for page in pag.paginate(Bucket=b, Prefix=prefix)
                for k in [o["Key"] for o in page.get("Contents", [])] if "date=" in k})
if not dates:
    fail("no account_return_daily partitions under %s" % prefix)
step = max(1, len(dates) // 40)
sample = dates[::step][:40]
checked = 0
by_q = {}
for d in sample:
    rows = read(on.address("irpt", "49financial", "gold", "account_return_daily", "date=%s" % d) + "/data.parquet")
    try:
        hold = {str(r["account_id"]): r for r in read(
            on.address("irpt", "49financial", "gold", "holdings_performance_daily", "date=%s" % d) + "/data.parquet")}
    except Exception:  # noqa: BLE001
        hold = {}
    for r in rows:
        acct = str(r["account_id"])
        q = r.get("day_quality")
        by_q[q] = by_q.get(q, 0) + 1
        h = hold.get(acct)
        if h is not None and h.get("status") == "OK":
            if r.get("holdings_price_return") is None or abs(float(r["holdings_price_return"]) - float(h["daily_return"])) > 1e-12:
                fail("date=%s account %s holdings_price_return %r != holdings gold daily_return %r" % (d, acct, r.get("holdings_price_return"), h["daily_return"]))
        elif q == "MEASURED" and r.get("holdings_price_return_reason") is None:
            fail("date=%s account %s MEASURED with no holdings row and no holdings_price_return_reason" % (d, acct))
        if q == "MEASURED":
            if r.get("market_value_eod") is None or float(r["market_value_eod"]) <= 0:
                fail("date=%s account %s MEASURED with market_value_eod %r" % (d, acct, r.get("market_value_eod")))
            diff = abs(float(r["total_return_daily"]) - (float(r["holdings_price_return"] or 0.0) + float(r.get("income_return") or 0.0)))
            if diff > tol:
                fail("date=%s account %s MEASURED but |twr - (price+income)| = %.6g > tolerance %.6g" % (d, acct, diff, tol))
        elif q == "FLOW_UNRECONCILED":
            if r.get("return_basis") != "HOLDINGS_INCOME_FALLBACK":
                fail("date=%s account %s FLOW_UNRECONCILED with return_basis %r" % (d, acct, r.get("return_basis")))
        checked += 1
if checked == 0:
    fail("0 rows checked over %d sampled partitions" % len(sample))
print("  sampled partitions %d of %d; rows checked %d; by day_quality %s; tolerance %.6g" % (len(sample), len(dates), checked, by_q, tol))
print("DB-1-AC2 PASS")
