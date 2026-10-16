"""READ TOOL (issuer 2.0.0_SA_COO~D2, 2026-10-16): the Cottonwood series the NEW publisher (publisher.py 0.4.0 at the repo HEAD) would build from the rewritten gold,
compared with the series published now. Run from the workspace root with python -I. Reads S3 (gold, platinum reporting); writes NOTHING to S3 or the repo; prints COUNTS only,
never an account id. Used by the packet NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_HOP2_HISTORY_SCOPE_REPUBLISH.md to read its blast radius before the write."""
import collections
import gzip
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import boto3

WS = __import__("os").path.abspath(".").replace("\\", "/")
sys.path.insert(0, WS + "/infra/aws/lambda/investor-reporting")
sys.path.insert(0, WS + "/infra/aws/lambda/investor-reporting/reporting-publish")
sys.path.insert(0, WS)
import handler as h  # noqa: E402
import publisher  # noqa: E402

t0 = time.time()
s3 = boto3.client("s3", region_name="us-east-1")
bucket, by_date = h._gold_objects(s3, "cottonwood")
dates = sorted(by_date)
print("gold partitions", len(dates), "first", dates[0], "last", dates[-1], flush=True)
pb, mp, _u = h._published_map(s3, "cottonwood")
raws = set(mp.values())
print("published", len(raws), flush=True)


def read_date(d):
    return d, h._read_rows(s3, bucket, by_date[d], raws)


rows_by_acct = collections.defaultdict(list)
with ThreadPoolExecutor(16) as pool:
    for i, (d, rows) in enumerate(pool.map(read_date, dates)):
        for r in rows:
            rows_by_acct[str(r["account_id"])].append(r)
        if i % 500 == 0:
            print("read", i, "of", len(dates), round(time.time() - t0), "s", flush=True)
print("accounts with rows", len(rows_by_acct), round(time.time() - t0), "s", flush=True)
present = dates
cal = h.trading_calendar


def pub_series(raw):
    b, k = h._split(h.opal_naming.address("irpt", "cottonwood", h.TIER_PLATINUM, h.TABLE_PLATINUM, "account=%s" % raw, publisher.SERIES_OBJECT))
    return raw, json.loads(gzip.decompress(s3.get_object(Bucket=b, Key=k)["Body"].read()))


with ThreadPoolExecutor(16) as pool:
    old = dict(pool.map(pub_series, sorted(raws)))
res = collections.Counter()
fieldchg = collections.Counter()
scope_flip = collections.Counter()
overlap_chg = collections.Counter()
for raw in sorted(raws):
    rows = rows_by_acct.get(raw)
    if not rows:
        res["no_gold_rows"] += 1
        continue
    try:
        new = publisher.build_series(rows, present_dates=present, calendar=cal)
    except publisher.PublishRefused:
        res["new_refused"] += 1
        continue
    o = old[raw]
    changed = [f for f in sorted(set(o) | set(new)) if o.get(f) != new.get(f)]
    for f in changed:
        fieldchg[f] += 1
    if not changed:
        res["identical"] += 1
    elif set(changed) <= {"history_scope", "history_scope_claim"}:
        res["scope_only"] += 1
    else:
        res["other_fields_changed"] += 1
    scope_flip[(str(o.get("history_scope")), str(new.get("history_scope")))] += 1
    od, nd = o.get("date") or [], new.get("date") or []
    common = [d for d in od if d in set(nd)]
    oi = {d: i for i, d in enumerate(od)}
    ni = {d: i for i, d in enumerate(nd)}
    for fld in ("total_return_daily", "external_flow", "value", "income", "holdings_price_return", "day_quality", "return_basis"):
        ov, nv = o.get(fld), new.get(fld)
        if isinstance(ov, list) and isinstance(nv, list) and any(ov[oi[d]] != nv[ni[d]] for d in common):
            overlap_chg[fld] += 1
    if any(d not in oi for d in nd):
        res["new_days_added"] += 1
    if any(d not in ni for d in od):
        res["old_days_dropped"] += 1
print("RESULT total", sum(res.values()), dict(res))
print("scope flips (old,new):", dict(scope_flip))
print("fields changed (count of series):", dict(fieldchg))
print("series with a changed value on a day present in BOTH (by field):", dict(overlap_chg))
print("elapsed", round(time.time() - t0), "s")
