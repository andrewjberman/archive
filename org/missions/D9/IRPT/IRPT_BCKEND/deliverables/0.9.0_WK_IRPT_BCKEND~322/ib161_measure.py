#!/usr/bin/env python3
"""IB-pr-467 (round 161): READ ONLY.  For the performance reader's INTERIOR and LAST-ROW excluded days: the status token, the base class
(zero / negative / positive / no_prior_row) and the zero run.  Counts only: no account id, balance or return is written.

  python -I ib161_measure.py fetch   <entry> <scratch>            # S3 list + get of the addresses the reader's own composition builds (days <= CAP)
  python -I ib161_measure.py measure <entry> <scratch>            # all four windows, the reader's calculate() per account, partitions served from the cache
  python -I ib161_measure.py control                              # in-memory control of the classifier (no data, no AWS)
  (then: python -I ib161_assemble.py <scratch> <out_dir> <base_commit>)

entry: "49F" (the 49F entry) or "orion".  Windows SI, YTD, QTD, 1Y, each at the latest landed day <= CAP (2026-10-08, the day IB-pr-464 read).
Reads from AWS here: S3 list/get only.  Nothing is written to AWS.  No Lambda, no sign-in, no Secrets Manager.
The arm, the cache, the window rule, the reader call and the position classifier are IB-pr-464's (ib160_measure.py), copied.
"""
from __future__ import annotations

import collections
import contextlib
import functools
import io
import json
import math
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
CAP = "2026-10-08"
PV = ("zero", "negative", "positive", "no_prior_row")
BINS = ("1", "2", "3-5", "6-20", "21-60", "more")
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


def fetch(entry, scratch):
    import installed
    from concurrent.futures import ThreadPoolExecutor
    s3 = boto3.client("s3", region_name="us-east-1")
    canonical, _ = firm_of(entry)
    src = installed._holdings_source_for(s3, canonical)          # the route's own composition (installed.py:75)
    avail_all = src.partition_dates()                              # the reader's own listing
    avail = [x for x in avail_all if x <= CAP]
    d = Path(scratch) / entry
    d.mkdir(parents=True, exist_ok=True)
    (d / "avail.json").write_text(json.dumps(avail))
    (d / "avail_all_count.json").write_text(json.dumps({"listed": len(avail_all), "last_listed": avail_all[-1], "used": len(avail)}))
    todo = [x for x in avail if not (d / (x + ".parquet")).is_file()]
    t0 = time.time()

    def get(day):
        key = "%sdate=%s/data.parquet" % (src.prefix, day)
        raw = src.s3.get_object(Bucket=src.bucket, Key=key)["Body"].read()
        (d / (day + ".parquet")).write_bytes(raw)
        return len(raw)
    with ThreadPoolExecutor(16) as pool:
        total = sum(pool.map(get, todo))
    print("fetch %s: listed %d partitions (last %s), used %d (<= %s), fetched %d now (%d bytes) in %.0fs" % (
        entry, len(avail_all), avail_all[-1], len(avail), CAP, len(todo), total, time.time() - t0))


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
    """Stands in for HoldingsGoldSource's S3 transport only (IB-pr-464's stand-in): rows served from memory."""

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
    """The reader's calculate() for one account; returns (outcome, days_excluded)."""
    canonical, legacy = firm_of(entry)
    cid = ids.opaque_account(canonical, key)
    scope = {"resolved_scope": {"scope_ids": [cid]}, "permitted_account_set": [cid], "verified_request_firm_id": legacy}
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            ans = hg.calculate(scope, a, b, src)
    except hg.HoldingsGoldRefused as exc:
        return ("refused", str(exc))
    vf = find(ans["report"], "days_excluded") or {}
    return ("figure", vf.get("days_excluded"))


def classify(sts):
    """IB-pr-464's position class (account has >=1 OK and >=1 non-OK), copied."""
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


def counted_days(sts):
    """Indexes (into the account's in-window rows, date order) of the days this cell counts: a non-OK row after the account's first OK
    row that is either between OK days (INTERIOR: some OK row follows it) or the account's LAST row (a non-OK last row).
    Returns (interior_idx, last_row_idx_or_None).  A non-OK row before the first OK row is a first-day exclusion and is not counted."""
    ok = [i for i, s in enumerate(sts) if s == "OK"]
    first_ok, last_ok = ok[0], ok[-1]
    interior = [i for i, s in enumerate(sts) if s != "OK" and first_ok < i < last_ok]
    last = len(sts) - 1 if sts[-1] != "OK" else None
    # non-OK rows after the last OK row and before the last row (a trailing run longer than one) are neither interior (no OK follows)
    # nor the last row: they are counted in `trailing_not_last` so the partition of the excluded days is complete and visible.
    trailing = [i for i, s in enumerate(sts) if s != "OK" and i > last_ok and i != len(sts) - 1]
    return interior, last, trailing


def vclass(v):
    """exact-zero rule: 0.0 is zero; a nonzero value is negative or positive by sign, however small; NaN/None is no_prior_row."""
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "no_prior_row"
    return "zero" if v == 0.0 else "negative" if v < 0.0 else "positive"


def run_back(vals, j):
    """Consecutive rows ending at index j (inclusive) whose value is exactly 0.0."""
    n = 0
    while j >= 0 and vals[j] == 0.0:
        n += 1
        j -= 1
    return n


def day_base(vals, i, mode):
    """vals: the account's account_value on its rows in the gold, ordered by day.  i: index of the counted day's row.
    mode 'own'     : the base the producer tested on this row = this row's own account_value (the t-1 basket); run counted back from this row.
    mode 'previous': the account_value on the account's previous row in the gold; run counted back from that previous row."""
    if mode == "own":
        c = vclass(vals[i])
        return c, (run_back(vals, i) if c == "zero" else 0)
    if i == 0:
        return "no_prior_row", 0
    c = vclass(vals[i - 1])
    return c, (run_back(vals, i - 1) if c == "zero" else 0)


def bin_of(n):
    return "1" if n == 1 else "2" if n == 2 else "3-5" if n <= 5 else "6-20" if n <= 20 else "21-60" if n <= 60 else "more"


def new_tables():
    return {"by": collections.defaultdict(lambda: {k: 0 for k in PV}), "run": {k: 0 for k in BINS}}


def setup():
    import holdings_gold as hg
    import ids
    orig = ids.opaque_account
    ids.opaque_account = functools.lru_cache(maxsize=None)(orig)
    return hg, ids


def measure(entry, scratch):
    hg, ids = setup()
    avail, frames = load(entry, scratch)
    src = CachedSource(avail, frames)
    last = avail[-1]
    pos_in_avail = {d: i for i, d in enumerate(avail)}
    for window in WINDOWS:
        a, b = window_of(window, last)
        days = [d for d in avail if a <= d <= b]
        w = src.big[src.big["_day"].isin(set(days))]
        w = w[w["business_date"].map(lambda v: str(v)[:10]).between(a, b)]
        keys = sorted(set(w["account_id"]))
        rows_by = {k: g.sort_values("_day", kind="stable") for k, g in w.groupby("account_id", sort=False)}
        cell = {"entry": "the 49F entry" if entry == "49F" else "orion", "window": window, "start": a, "end": b,
                "partitions_in_window": len(days), "partitions_landed_used": len(avail), "accounts_read": len(keys)}
        pos = collections.Counter()
        refused = 0
        mism = 0
        t0 = time.time()
        modes = {"own": {"int": new_tables(), "last": new_tables()}, "previous": {"int": new_tables(), "last": new_tables()}}
        n_int = n_last = trailing_n = 0
        acc_all_zero = {"own": 0, "previous": 0}
        acc_neg = {"own": 0, "previous": 0}
        acc_pos = {"own": 0, "previous": 0}
        near_cent = {"own": 0, "previous": 0}
        prior_not_prev_partition = 0
        prior_span_gt1 = 0
        counted_accounts = 0
        for i, k in enumerate(keys):
            kind, x = read_one(hg, ids, src, entry, k, a, b)
            if kind == "refused":
                refused += 1
                continue
            g = rows_by[k]
            sts = g["status"].tolist()
            nonok = sum(1 for s in sts if s != "OK")
            if x != nonok:
                mism += 1
            if x < 1:
                continue
            cls = classify(sts)
            pos[cls] += 1
            if cls == "first_day_only":
                continue
            counted_accounts += 1
            interior, lastrow, trailing = counted_days(sts)
            trailing_n += len(trailing)
            full = src.groups[k]
            fdays = full["_day"].tolist()
            fidx = {d: j for j, d in enumerate(fdays)}
            vals = full["account_value"].astype(float).tolist()
            gdays = g["_day"].tolist()
            spans = g["span_trading_days"].tolist()
            flags = {m: {"zero": 0, "neg": 0, "pos": 0, "n": 0} for m in modes}
            for part, idxs in (("int", interior), ("last", [lastrow] if lastrow is not None else [])):
                for ii in idxs:
                    day = gdays[ii]
                    j = fidx[day]
                    st = sts[ii]
                    if part == "int":
                        n_int += 1
                    else:
                        n_last += 1
                    if j >= 1 and pos_in_avail[fdays[j - 1]] != pos_in_avail[day] - 1:
                        prior_not_prev_partition += 1
                    sp = spans[ii]
                    if sp is not None and not (isinstance(sp, float) and math.isnan(sp)) and int(sp) > 1:
                        prior_span_gt1 += 1
                    for m in modes:
                        c, run = day_base(vals, j, m)
                        t = modes[m][part]
                        t["by"][st][c] += 1
                        if c == "zero":
                            t["run"][bin_of(run)] += 1
                        v = vals[j] if m == "own" else (vals[j - 1] if j >= 1 else float("nan"))
                        if v == v and v != 0.0 and abs(v) < 0.01:
                            near_cent[m] += 1
                        f = flags[m]
                        f["n"] += 1
                        f["zero"] += c == "zero"
                        f["neg"] += c == "negative"
                        f["pos"] += c == "positive"
            for m in modes:
                f = flags[m]
                if f["n"] and f["zero"] == f["n"]:
                    acc_all_zero[m] += 1
                acc_neg[m] += f["neg"] >= 1
                acc_pos[m] += f["pos"] >= 1
            if (i + 1) % 2000 == 0:
                print("  %s %s: %d of %d accounts, %.0fs" % (entry, window, i + 1, len(keys), time.time() - t0), flush=True)

        def out(m):
            r = {}
            for part, nm in (("int", "interior"), ("last", "last_row")):
                t = modes[m][part]
                r[nm + "_by_status_and_prior_value"] = {s: dict(v) for s, v in sorted(t["by"].items())}
                r[nm + "_zero_run_lengths"] = dict(t["run"])
            r["accounts_all_zero_base"] = acc_all_zero[m]
            r["accounts_with_a_negative_base"] = acc_neg[m]
            r["accounts_with_a_positive_flagged_base"] = acc_pos[m]
            r["days_within_a_cent_of_zero_but_not_zero"] = near_cent[m]
            return r
        cell.update({
            "accounts_with_an_interior_or_last_row_excluded_day": counted_accounts,
            "position_of_the_excluded_days": dict(pos), "accounts_the_reader_refuses": refused,
            "interior_days": n_int, "last_row_days": n_last, "days_counted": n_int + n_last,
            "trailing_nonok_days_neither_interior_nor_last_row": trailing_n,
            "counted_days_whose_previous_gold_row_is_not_the_previous_landed_partition": prior_not_prev_partition,
            "counted_days_with_span_trading_days_over_1": prior_span_gt1,
            "reader_days_excluded_differs_from_status_count_of_rows": mism,
            "primary_own_row_base": out("own"), "literal_previous_row": out("previous"), "seconds": round(time.time() - t0, 1)})
        (Path(scratch) / ("cell161_%s_%s.json" % (entry, window))).write_text(json.dumps(cell, sort_keys=True, indent=1))
        print("measure %s %s: read %d, accounts counted %d, interior days %d, last-row days %d, refused %d, %.0fs" % (
            entry, window, len(keys), counted_accounts, n_int, n_last, refused, cell["seconds"]), flush=True)


def control():
    """In memory only.  An account valued positive, zero, positive over three days.  Gold rows carry as account_value the t-1 basket:
    the closing values [5.0, 0.0, 7.0] on days d1..d3 give rows d2 -> 5.0 and d3 -> 0.0 and a row for the day after d3 -> 7.0."""
    closes = [5.0, 0.0, 7.0]
    literal_rows = closes                                   # three rows valued positive, zero, positive (the face's wording)
    c_prev, r_prev = day_base(literal_rows, 2, "previous")
    own_rows = [float("nan")] + closes                      # rows for d1 (no basis), d2, d3, d4: own account_value = close of the day before
    c_own, r_own = day_base(own_rows, 3, "own")             # the row for the day AFTER close d3 is 7.0; the row for d3 carries close d2 = 0.0
    c_own3, r_own3 = day_base(own_rows, 2, "own")
    extra = day_base([0.0, 0.0, 0.0, 4.0], 3, "previous")   # a longer run: three zeros then a positive -> zero, run 3
    cent = vclass(0.004)                                      # not exactly zero -> positive
    return {"what": "In memory only: an account valued positive, zero, positive over three days (5.0, 0.0, 7.0). Rule 'previous row' on three rows valued positive, zero, positive: the "
                    "third day's prior value is read; rule 'own row' (the producer's base: the row's own account_value is the close of the day before) on the rows for the "
                    "days after each close: the row that follows the zero close is read. A second plant, rows 0.0, 0.0, 0.0, 4.0, reads the fourth day's prior value; a value of 0.004 is read "
                    "by the exact-zero rule.",
            "reading": {"previous_row_rule_third_day": {"prior_value": c_prev, "zero_run": r_prev},
                        "own_row_rule_day_after_the_zero_close": {"base": c_own3, "zero_run": r_own3},
                        "own_row_rule_day_after_the_last_close": {"base": c_own, "zero_run": r_own},
                        "previous_row_rule_zero_zero_zero_then_positive": {"prior_value": extra[0], "zero_run": extra[1]},
                        "value_0.004_reads": cent,
                        "expected": "third day's prior value zero with run length 1: " + ("HELD" if (c_prev, r_prev) == ("zero", 1) and (c_own3, r_own3) == ("zero", 1) and extra == ("zero", 3) and cent == "positive" else "NOT HELD")}}


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch":
        fetch(sys.argv[2], sys.argv[3])
    elif cmd == "measure":
        measure(sys.argv[2], sys.argv[3])
    elif cmd == "control":
        print(json.dumps(control(), indent=1))
    else:
        raise SystemExit("unknown command")
