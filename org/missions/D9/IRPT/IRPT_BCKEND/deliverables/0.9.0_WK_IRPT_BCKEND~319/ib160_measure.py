#!/usr/bin/env python3
"""IB-pr-464 (round 160): READ ONLY.  The performance route's reader, per window and per composed firm: accounts with an excluded day
and where in the account's window the excluded days fall.  Counts only: no account id, balance or holding is written; no security named.

  python -I ib160_measure.py fetch   <entry> <scratch>              # S3 list + get of the addresses the reader's own composition builds
  python -I ib160_measure.py measure <entry> <window> <scratch>     # the reader's calculate() per account, partitions served from the cache
  python -I ib160_measure.py verify  <entry> <window> <scratch> [n] # n=50 accounts: cached-source result == the reader's own HoldingsGoldSource.frame path
  python -I ib160_measure.py census  <entry> <scratch>              # status token row counts over every landed partition, and per window
  (then: python -I ib160_assemble.py <scratch> <out_dir> <base_commit>)

entry: "49F" (the 49F entry) or "orion".  window: SI, YTD, QTD, 1Y (the reader's windows, each at the latest landed day).
Reads from AWS here: S3 list/get only.  Nothing is written to AWS.  No Lambda, no sign-in, no Secrets Manager.
"""
from __future__ import annotations

import collections
import contextlib
import functools
import io
import json
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
L = ROOT / "infra/aws/lambda/investor-reporting"
sys.path[:0] = [str(ROOT / "lib"), str(ROOT), str(ROOT / "data/assets/scripts/silver"), str(ROOT / "data/assets/scripts/analysis"),
                str(ROOT / "data/assets/scripts/gold/irpt_reporting"), str(ROOT / "data/assets/scripts/gold/investor_reporting"),
                str(ROOT / "data/assets/scripts/gold/runners_49f"), str(L / "performance"), str(L / "reports"), str(L)]
import boto3  # noqa: E402
import pandas as pd  # noqa: E402

WINDOWS = ("SI", "YTD", "QTD", "1Y")
ENTRIES = ("49F", "orion")
KEEP = ["account_id", "business_date", "daily_return", "account_value", "excluded_count", "excluded_weight", "status",
        "prior_business_date", "span_trading_days"]


def firm_of(entry):
    import tenants
    return (tenants._CANONICAL_49F, tenants._LEGACY_SHORT_ID["49F"]) if entry == "49F" else (tenants._CANONICAL_INF, tenants._LEGACY_SHORT_ID["INF"])


def window_of(name, last):
    import parity_period_returns as ppr
    import holdings_gold as hg
    if name == "SI":
        return hg.SINCE_INCEPTION_START, last
    a, b = ppr.period_window(name, last)
    return a.isoformat(), b.isoformat()


# ----------------------------------------------------------------------------------------------------------- fetch
def fetch(entry, scratch):
    import installed
    from concurrent.futures import ThreadPoolExecutor
    s3 = boto3.client("s3", region_name="us-east-1")
    canonical, _ = firm_of(entry)
    src = installed._holdings_source_for(s3, canonical)          # the route's own composition (installed.py:75)
    avail = src.partition_dates()                                  # the reader's own listing
    d = Path(scratch) / entry
    d.mkdir(parents=True, exist_ok=True)
    (d / "avail.json").write_text(json.dumps(avail))
    todo = [x for x in avail if not (d / (x + ".parquet")).is_file()]
    t0 = time.time()

    def get(day):
        key = "%sdate=%s/data.parquet" % (src.prefix, day)
        raw = src.s3.get_object(Bucket=src.bucket, Key=key)["Body"].read()
        (d / (day + ".parquet")).write_bytes(raw)
        return len(raw)
    with ThreadPoolExecutor(16) as pool:
        total = sum(pool.map(get, todo))
    print("fetch %s: listed %d partitions, fetched %d now (%d bytes) in %.0fs" % (entry, len(avail), len(todo), total, time.time() - t0))


def load(entry, scratch):
    d = Path(scratch) / entry
    avail = json.loads((d / "avail.json").read_text())
    frames = {}
    for day in avail:
        fr = pd.read_parquet(d / (day + ".parquet"))
        if not {"account_id", "business_date", "daily_return", "account_value", "status"} <= set(fr.columns):
            raise SystemExit("schema changed at a partition")
        for c in KEEP:
            if c not in fr.columns:
                fr[c] = None if c in ("prior_business_date", "span_trading_days") else float("nan")
        frames[day] = fr[KEEP].assign(account_id=fr["account_id"].astype(str), _day=day)
    return avail, frames


class CachedSource:
    """Stands in for HoldingsGoldSource's S3 transport only: same methods the reader calls, rows served from memory.
    Everything the reader computes from the rows (map_account, the filter at holdings_gold.py:246, the chain, days_excluded, claim) is the reader's own."""

    def __init__(self, avail, frames):
        self.avail = avail
        self.receipts, self.timings = [], []
        self.keys_by_day = {}
        big = pd.concat([frames[x] for x in avail], ignore_index=True)
        self.groups = {k: g.sort_values("_day", kind="stable") for k, g in big.groupby("account_id", sort=False)}
        for x in avail:
            self.keys_by_day[x] = sorted(set(frames[x]["account_id"]))
        self.big = big

    def describe(self):
        return {"bucket": "cache", "prefix": "cache/", "table": "holdings_performance_daily"}

    def partition_dates(self):
        return list(self.avail)

    def account_keys(self, day):
        return self.keys_by_day[day]

    def frame(self, days, account_key):
        g = self.groups.get(account_key)
        cols = ["account_id", "business_date", "daily_return", "account_value", "excluded_count", "excluded_weight", "status"]
        if g is None:
            return pd.DataFrame(columns=cols)
        return g[g["_day"].isin(set(days))].drop(columns=["_day"]).reset_index(drop=True)

    def _read(self, day, account_key):
        fr = self.big[self.big["_day"] == day]
        if account_key is not None:
            fr = fr[fr["account_id"] == account_key]
        return {}, fr.drop(columns=["_day"])


def find(o, key):
    if isinstance(o, dict):
        if key in o:
            return o
        for v in o.values():
            r = find(v, key)
            if r:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, key)
            if r:
                return r
    return None


def read_one(hg, ids, src, entry, key, a, b):
    """The reader's calculate() for one account; returns (outcome, days_excluded, claim, absences)."""
    canonical, legacy = firm_of(entry)
    cid = ids.opaque_account(canonical, key)
    scope = {"resolved_scope": {"scope_ids": [cid]}, "permitted_account_set": [cid], "verified_request_firm_id": legacy}
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            ans = hg.calculate(scope, a, b, src)
    except hg.HoldingsGoldRefused as exc:
        return ("refused", str(exc), None, None)
    vf = find(ans["report"], "days_excluded") or {}
    return ("figure", vf.get("days_excluded"), ans["claim"], sorted((x.get("fact"), x.get("status")) for x in ans["absences"]))


def classify(sts):
    """sts: the account's statuses in the window, ordered by business_date. Returns the position class (account has >=1 OK and >=1 non-OK)."""
    ok = [i for i, s in enumerate(sts) if s == "OK"]
    bad = [i for i, s in enumerate(sts) if s != "OK"]
    if sts[-1] != "OK":
        return "last_day_involved"
    first_ok = ok[0]
    lead = [i for i in bad if i < first_ok]
    inter = [i for i in bad if i > first_ok]
    if lead and not inter:
        return "first_day_only"
    if inter and not lead:
        return "interior_only"
    return "first_and_interior"


def bucket(n):
    return "1" if n == 1 else "2" if n == 2 else "3-5" if n <= 5 else "6-20" if n <= 20 else "more"


def setup():
    import holdings_gold as hg
    import ids
    orig = ids.opaque_account
    ids.opaque_account = functools.lru_cache(maxsize=None)(orig)   # memoise the reader's own function (same outputs); map_account imports it at call time
    return hg, ids


def measure(entry, window, scratch):
    hg, ids = setup()
    avail, frames = load(entry, scratch)
    src = CachedSource(avail, frames)
    last = avail[-1]
    a, b = window_of(window, last)
    days = [d for d in avail if a <= d <= b]
    w = src.big[src.big["_day"].isin(set(days))]
    w = w[w["business_date"].map(lambda v: str(v)[:10]).between(a, b)]
    keys = sorted(set(w["account_id"]))
    st_by = {k: g.sort_values("business_date")["status"].tolist() for k, g in w.groupby("account_id", sort=False)}
    cell = {"entry": "the 49F entry" if entry == "49F" else "orion", "window": window, "start": a, "end": b,
            "partitions_in_window": len(days), "partitions_landed": len(avail), "partitions_read_for_this_cell": len(days),
            "accounts_read": len(keys)}
    refusals = collections.Counter()
    pos = collections.Counter({"first_day_only": 0, "interior_only": 0, "first_and_interior": 0, "last_day_involved": 0})
    dist = collections.Counter()
    claim = collections.Counter()
    absn = collections.Counter()
    absn_none = collections.Counter()
    claim_none = collections.Counter()
    n_exc = n_none = n_ref = 0
    mismatch = 0
    control = None
    t0 = time.time()
    for i, k in enumerate(keys):
        kind, x, cl, ab = read_one(hg, ids, src, entry, k, a, b)
        sts = st_by[k]
        nonok = sum(1 for s in sts if s != "OK")
        if kind == "refused":
            n_ref += 1
            refusals[x] += 1
            continue
        if x != nonok:
            mismatch += 1
        if x >= 1:
            n_exc += 1
            pos[classify(sts)] += 1
            dist[bucket(x)] += 1
            claim[cl] += 1
            absn[json.dumps(ab)] += 1
        else:
            n_none += 1
            claim_none[cl] += 1
            absn_none[json.dumps(ab)] += 1
        if (i + 1) % 1000 == 0:
            print("  %s %s: %d of %d accounts, %.0fs" % (entry, window, i + 1, len(keys), time.time() - t0), flush=True)
    cell.update({"accounts_with_an_excluded_day": n_exc, "accounts_with_none": n_none, "accounts_the_reader_refuses": n_ref,
                 "refusals": dict(refusals), "position_of_the_excluded_days": dict(pos),
                 "excluded_days_per_account_distribution": {k: dist.get(k, 0) for k in ("1", "2", "3-5", "6-20", "more")},
                 "claim_the_reader_gives": dict(claim),
                 "absences_named": {"for_accounts_with_an_excluded_day": {k: v for k, v in absn.items()}},
                 "claim_the_reader_gives_accounts_with_none": dict(claim_none),
                 "absences_named_accounts_with_none": {k: v for k, v in absn_none.items()},
                 "reader_days_excluded_differs_from_status_count_of_rows": mismatch})
    # control: an account with none, read the same way; plus an in-memory mutant of the same account (one OK day set non-OK), never written anywhere
    full = max(len(v) for v in st_by.values())
    pool = [k for k in keys if all(s == "OK" for s in st_by[k]) and len(st_by[k]) == full] or [k for k in keys if all(s == "OK" for s in st_by[k])]
    control = pool[0] if pool else None
    if control is not None:
        c1 = read_one(hg, ids, src, entry, control, a, b)
        g = src.groups[control]
        idx = g.index[g["_day"].isin(set(days))][len(days) // 2 if len(g) > len(days) // 2 else 0]
        old = src.groups[control].at[idx, "status"]
        src.groups[control].at[idx, "status"] = "NON-POSITIVE-BASE"
        c2 = read_one(hg, ids, src, entry, control, a, b)
        src.groups[control].at[idx, "status"] = old
        cell["control"] = {"unmodified_account_with_no_excluded_day": {"outcome": c1[0], "days_excluded": c1[1], "claim": c1[2]},
                           "same_account_with_one_in_memory_day_set_non_OK": {"outcome": c2[0], "days_excluded": c2[1], "claim": c2[2]}}
    cell["seconds"] = round(time.time() - t0, 1)
    out = Path(scratch) / ("cell_%s_%s.json" % (entry, window))
    out.write_text(json.dumps(cell, sort_keys=True, indent=1))
    print("measure %s %s: read %d, excluded %d, none %d, refused %d, %.0fs" % (entry, window, len(keys), n_exc, n_none, n_ref, cell["seconds"]))


def verify(entry, window, scratch, n=50):
    """The same reader code twice over a sample of accounts: (1) CachedSource, (2) the reader's OWN HoldingsGoldSource class
    (partition_dates, frame, account_keys real) with only _read's S3 get + parquet parse replaced by the cached frame."""
    hg, ids = setup()
    avail, frames = load(entry, scratch)
    cs = CachedSource(avail, frames)
    s3 = boto3.client("s3", region_name="us-east-1")
    import installed
    canonical, _ = firm_of(entry)
    real = installed._holdings_source_for(s3, canonical)

    def _read(day, account_key):
        fr = frames[day]
        if account_key is not None:
            fr = fr[fr["account_id"].astype(str) == account_key]
        return {"key": day}, fr.drop(columns=["_day"])
    real._read = _read
    real.partition_dates = lambda: list(avail)                   # same list the one real listing returned at fetch time
    last = avail[-1]
    a, b = window_of(window, last)
    keys = sorted(set(frames[avail[-1]]["account_id"]))
    random.Random(160).shuffle(keys)
    sample = keys[:n]
    same = 0
    for k in sample:
        r1 = read_one(hg, ids, cs, entry, k, a, b)
        r2 = read_one(hg, ids, real, entry, k, a, b)
        same += int(r1 == r2)
    res = {"entry": entry, "window": window, "sampled": len(sample), "identical": same}
    (Path(scratch) / ("verify_%s_%s.json" % (entry, window))).write_text(json.dumps(res))
    print("verify", res)


def census(entry, scratch):
    """status token -> row count over EVERY landed partition of the entry; plus, per window, non-OK rows by token (rows, not accounts)."""
    avail, frames = load(entry, scratch)
    tot = collections.Counter()
    for x in avail:
        tot.update(frames[x]["status"].tolist())
    out = {"partitions": len(avail), "first_partition": avail[0], "last_partition": avail[-1], "rows": sum(tot.values()),
           "accounts_ever_seen": len(set().union(*[set(frames[x]["account_id"]) for x in avail])), "status_values": dict(tot), "by_window": {}}
    for w in WINDOWS:
        a, b = window_of(w, avail[-1])
        c = collections.Counter()
        n = 0
        for x in avail:
            if a <= x <= b:
                fr = frames[x]
                n += len(fr)
                c.update(fr.loc[fr["status"] != "OK", "status"].tolist())
        out["by_window"][w] = {"rows": n, "non_ok_rows_by_status": dict(c)}
    (Path(scratch) / ("census_%s.json" % entry)).write_text(json.dumps(out, sort_keys=True))
    print("census", entry, out["status_values"])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch":
        fetch(sys.argv[2], sys.argv[3])
    elif cmd == "measure":
        measure(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "census":
        census(sys.argv[2], sys.argv[3])
    elif cmd == "verify":
        verify(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 50)
    else:
        raise SystemExit("unknown command")
