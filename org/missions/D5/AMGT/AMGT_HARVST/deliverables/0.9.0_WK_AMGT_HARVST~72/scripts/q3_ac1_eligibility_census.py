"""HVST-q-3 read-only census: FWD-7 eligibility under the declared set (bbg, wsj).
Reuses lib.research.metrics.chatter_axis.classify_eligibility / window_dates (merged HVST-q-4)."""
import os
import re
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *([".."] * 8)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from lib.research.coverage import pool_reader as pr  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.harvest.publication_gold import GOLD_DAILY_TABLE  # noqa: E402
from lib.research.metrics import chatter_axis as ca  # noqa: E402

DECLARED = ("bbg", "wsj")
UNIVERSE_N = 191

client = pr._client(None)
prefix = store.table_prefix("amgt", "gold", GOLD_DAILY_TABLE)
keys = []
for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
    keys += [o["Key"] for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet")]
date_re = re.compile(r"date=([0-9]{4}-[0-9]{2}-[0-9]{2})")
newest = sorted(keys, key=lambda k: (date_re.search(k).group(1) if date_re.search(k) else "", k))[-1]
rows = pr._gold_latest_snapshot_rows(GOLD_DAILY_TABLE, client=client)
days = sorted({(r["day"].isoformat() if hasattr(r["day"], "isoformat") else str(r["day"])) for r in rows})
as_of = days[-1]
print("served chatter_daily part: s3://%s/%s (%d parts listed, %d rows)" % (store.HARVEST_BUCKET, newest, len(keys), len(rows)))
print("part date= %s ; max day in rows = %s ; min day = %s ; AS-OF used = %s (max day in served part)"
      % (date_re.search(newest).group(1), as_of, days[0], as_of))
start, end = ca.window_bounds(as_of, ca.WINDOW_DAYS)
dates = ca.window_dates(as_of, ca.WINDOW_DAYS)
print("window: %s..%s (%d days, WINDOW_DAYS=%d)" % (start, end, len(dates), ca.WINDOW_DAYS))
entries, prov = ca.read_universe_names(None, as_of=as_of)
identities = [e["identity"] for e in entries]
print("universe: %d names (expected %d) source=%s" % (len(identities), UNIVERSE_N, prov.get("source")))
print("eligibility logic used: lib.research.metrics.chatter_axis.classify_eligibility + _coverage_by_day (merged HVST-q-4), reused not re-derived")

by_name = {i: {} for i in identities}
found_by_name = {i: {} for i in identities}
idset = set(identities)
seen = {}
for r in rows:
    k = r.get("security_key")
    if k not in idset:
        continue
    day = r["day"].isoformat() if hasattr(r["day"], "isoformat") else str(r["day"])
    if day < start or day > end:
        continue
    seen.setdefault(k, {}).setdefault(day, []).append(r)
for k, dd in seen.items():
    for day, rs in dd.items():
        if len(rs) == 1:  # a duplicated day carries no coverage claim (same rule as _coverage_by_day)
            by_name[k][day] = frozenset(rs[0].get("publishers_covered_codes") or ())
            found_by_name[k][day] = frozenset(rs[0].get("publishers_found_codes") or ())

eligible, excluded = ca.classify_eligibility(identities, by_name, dates, DECLARED)
n = len(identities)
print("ELIGIBLE UNDER (bbg, wsj): %d of %d" % (len(eligible), n))
print("excluded by reason: %s" % dict(Counter(excluded.values())))
print("  PARTIAL_COVERAGE=%d NOT_SEARCHED=%d (sum with eligible = %d)" % (
    sum(1 for v in excluded.values() if v == ca.REASON_PARTIAL_COVERAGE),
    sum(1 for v in excluded.values() if v == ca.REASON_NOT_SEARCHED), len(eligible) + len(excluded)))
per_pub = {p: sum(1 for i in identities if all(p in by_name[i].get(d, ()) for d in dates)) for p in DECLARED}
print("names covering every window day per declared publisher: %s" % per_pub)
print("eligible names: %s" % (", ".join(sorted(eligible)) or "<none>"))
for reason in (ca.REASON_PARTIAL_COVERAGE, ca.REASON_NOT_SEARCHED):
    print("excluded %s: %s" % (reason, ", ".join(sorted(k for k, v in excluded.items() if v == reason)) or "<none>"))

# NEGATIVE ARMS (NOT the contract): found-set read, and any-single-publisher coverage read
found_elig, _ = ca.classify_eligibility(identities, found_by_name, dates, DECLARED)
any_pub = sum(1 for i in identities if all(by_name[i].get(d) for d in dates))
print("NEGATIVE ARM (found-set read, publishers_found_codes, every declared pub every day): %d of %d" % (len(found_elig), n))
print("NEGATIVE ARM (any single publisher covering every day): %d of %d" % (any_pub, n))
print("FLOOR: %d against ELIGIBLE_FLOOR=%d -> %s" % (
    len(eligible), ca.ELIGIBLE_FLOOR, "AT/ABOVE FLOOR (no HOLD)" if len(eligible) >= ca.ELIGIBLE_FLOOR else "BELOW FLOOR (HOLD)"))
