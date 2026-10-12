#!/usr/bin/env python3
"""IB-pr-470 (round 164): READ ONLY.  The closed status set (counts over the served gold), the NON-POSITIVE-BASE days placed by what the
account held the prior day, and the accounts whose claim moves.  Counts only: no account id, balance, return or cash amount is written.

  python -I ib164_measure.py fetch   <entry> <scratch>   # S3 list + get of the addresses the reader's own composition builds (days <= CAP)
  python -I ib164_measure.py census  <entry> <scratch>   # status tokens over every landed partition read (rows, partitions, columns present)
  python -I ib164_measure.py measure <entry> <scratch>   # four windows: the reader's calculate() per account, then this cell's counts
  python -I ib164_measure.py control <scratch>            # in-memory control of the claim counter (no data, no AWS)
  (then: python -I ib164_assemble.py <scratch> <out_dir> <base_commit>)

entry: "49F" (the 49F entry) or "orion".  Latest landed day read: CAP = 2026-10-08, the day IB-pr-464 and IB-pr-467 read.
S3 list/get only.  Nothing is written to AWS.  No Lambda, no sign-in, no Secrets Manager.
The arm, the cache step, the window rule, the reader call and the day rule are IB-pr-467's (ib161_measure.py), copied.
"""
from __future__ import annotations

import collections
import contextlib
import functools
import io
import json
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
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

WINDOWS = ("SI", "YTD", "QTD", "1Y")
CAP = "2026-10-08"
HELD = ("held_none", "held_included_only_or_mixed", "held_only_excluded", "held_only_negative", "held_other", "not_determinable")
NPB, NOPRIOR, OK = "NON-POSITIVE-BASE", "NO-PRIOR-HOLDINGS", "OK"
HELDCOLS = ["held_count", "included_count", "negative_count", "cash_value"]
KEEP = ["account_id", "business_date", "daily_return", "account_value", "excluded_count", "excluded_weight", "status",
        "prior_business_date", "span_trading_days"] + HELDCOLS


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


def census(entry, scratch):
    """Status tokens over EVERY landed partition read (<= CAP): rows, partitions, and which partitions carry the four held columns."""
    d = Path(scratch) / entry
    avail = json.loads((d / "avail.json").read_text())
    by = collections.Counter()
    rows = 0
    lacking = 0
    empty = 0
    for day in avail:
        t = pq.read_table(d / (day + ".parquet"), columns=["status"])
        names = set(pq.read_schema(d / (day + ".parquet")).names)
        if not set(HELDCOLS) <= names:
            lacking += 1
        if t.num_rows == 0:
            empty += 1
        rows += t.num_rows
        by.update(t.column("status").to_pylist())
    out = {"partitions_read": len(avail), "rows_read": rows, "by_token": dict(by), "first_partition": avail[0], "last_partition": avail[-1],
           "partitions_lacking_any_held_column": lacking, "partitions_with_zero_rows": empty}
    (Path(scratch) / ("census_%s.json" % entry)).write_text(json.dumps(out, sort_keys=True, indent=1))
    print("census %s: %d partitions, %d rows, tokens %s, partitions lacking a held column %d" % (entry, len(avail), rows, dict(by), lacking))


def hclass_series(fr):
    """The six prior-day-holdings classes, per row, from the gold's own columns (held_count, included_count, excluded_count, negative_count,
    cash_value).  The row for business_date D describes the account's positions on the base day (the prior trading day), producer
    holdings_performance.py:758-847 and :1065.  not_determinable: a count is null, or held_count != included+excluded+negative."""
    h = pd.to_numeric(fr["held_count"], errors="coerce")
    inc = pd.to_numeric(fr["included_count"], errors="coerce")
    neg = pd.to_numeric(fr["negative_count"], errors="coerce")
    exc = pd.to_numeric(fr["excluded_count"], errors="coerce")
    nd = h.isna() | inc.isna() | neg.isna() | exc.isna() | (h != inc + exc + neg)
    conds = [nd, h == 0, inc >= 1, neg == h, (inc == 0) & (neg == 0)]
    names = ["not_determinable", "held_none", "held_included_only_or_mixed", "held_only_negative", "held_only_excluded"]
    return np.select(conds, names, default="held_other")


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
        fr = fr[KEEP].assign(account_id=fr["account_id"].astype(str), _day=day)
        fr["_hc"] = hclass_series(fr)
        frames[day] = fr
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


def place(sts):
    """For one account's in-window statuses in date order: the index sets of its NON-POSITIVE-BASE days by position.
    Returns (all_idx, interior_idx) where interior is IB-pr-467's rule: a non-OK row strictly between the first and the last OK row."""
    ok = [i for i, s in enumerate(sts) if s == OK]
    npb = [i for i, s in enumerate(sts) if s == NPB]
    if not ok:
        return npb, []
    f, la = ok[0], ok[-1]
    return npb, [i for i in npb if f < i < la]


def moves(sts, hcs):
    """The claim counter for ONE account that has a figure.  Returns (moves_under_contract_as_written, moves_if_npb_with_a_prior_position_also).
    As written: one or more excluded days (any position) whose status is neither NO-PRIOR-HOLDINGS nor NON-POSITIVE-BASE.
    Alternative: also a NON-POSITIVE-BASE day whose class is none of held_none, not_determinable."""
    under = any(s != OK and s not in (NOPRIOR, NPB) for s in sts)
    npb_prior = any(s == NPB and hcs[i] not in ("held_none", "not_determinable") for i, s in enumerate(sts))
    return under, (under or npb_prior)


def zero_tab():
    return {k: 0 for k in HELD}


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
    for window in WINDOWS:
        a, b = window_of(window, last)
        days = [d for d in avail if a <= d <= b]
        w = src.big[src.big["_day"].isin(set(days))]
        w = w[w["business_date"].map(lambda v: str(v)[:10]).between(a, b)]
        keys = sorted(set(w["account_id"]))
        rows_by = {k: g.sort_values("_day", kind="stable") for k, g in w.groupby("account_id", sort=False)}
        cell = {"entry": "the 49F entry" if entry == "49F" else "orion", "window": window, "start": a, "end": b,
                "partitions_in_window": len(days), "partitions_landed_used": len(avail), "accounts_read": len(keys)}
        t0 = time.time()
        refused = mism = 0
        fig = mv_under = mv_if = 0
        tab_int, tab_all = zero_tab(), zero_tab()
        tab_nofig = zero_tab()
        pos = {"before_first_ok": 0, "interior": 0, "after_last_ok": 0, "of_which_the_last_row": 0}
        cash_nz = 0
        status_days = collections.Counter()
        npb_accounts = 0
        for i, k in enumerate(keys):
            kind, x = read_one(hg, ids, src, entry, k, a, b)
            g = rows_by[k]
            sts = g["status"].tolist()
            hcs = g["_hc"].tolist()
            if kind == "refused":
                refused += 1
                for j, s in enumerate(sts):
                    if s == NPB:
                        tab_nofig[hcs[j]] += 1
                continue
            fig += 1
            if x != sum(1 for s in sts if s != OK):
                mism += 1
            status_days.update(s for s in sts if s != OK)
            under, alt = moves(sts, hcs)
            mv_under += under
            mv_if += alt
            all_idx, int_idx = place(sts)
            if all_idx:
                npb_accounts += 1
            ok = [j for j, s in enumerate(sts) if s == OK]
            cash = g["cash_value"].tolist()
            for j in all_idx:
                tab_all[hcs[j]] += 1
                c = cash[j]
                if c == c and c != 0.0:
                    cash_nz += 1
                if j < ok[0]:
                    pos["before_first_ok"] += 1
                elif j > ok[-1]:
                    pos["after_last_ok"] += 1
                    if j == len(sts) - 1:
                        pos["of_which_the_last_row"] += 1
                else:
                    pos["interior"] += 1
            for j in int_idx:
                tab_int[hcs[j]] += 1
            if (i + 1) % 2000 == 0:
                print("  %s %s: %d of %d accounts, %.0fs" % (entry, window, i + 1, len(keys), time.time() - t0), flush=True)
        cell.update({
            "accounts_the_reader_refuses": refused, "accounts_with_a_figure": fig,
            "reader_days_excluded_differs_from_status_count_of_rows": mism,
            "non_positive_base_days": {"interior": sum(tab_int.values()), "all_positions": sum(tab_all.values())},
            "non_positive_base_interior_by_prior_day_holdings": tab_int,
            "non_positive_base_all_positions_by_prior_day_holdings": tab_all,
            "non_positive_base_all_positions_by_position_in_window": pos,
            "non_positive_base_all_positions_with_nonzero_cash": cash_nz,
            "accounts_with_a_figure_and_a_non_positive_base_day": npb_accounts,
            "non_positive_base_days_in_accounts_without_a_figure_by_prior_day_holdings": tab_nofig,
            "excluded_days_in_accounts_with_a_figure_by_status": dict(sorted(status_days.items())),
            "accounts_whose_claim_moves": {"accounts_with_a_figure_saying_measured": fig, "under_the_contract_as_written": int(mv_under),
                                           "if_non_positive_base_with_a_prior_position_also_moves": int(mv_if)},
            "seconds": round(time.time() - t0, 1)})
        (Path(scratch) / ("cell164_%s_%s.json" % (entry, window))).write_text(json.dumps(cell, sort_keys=True, indent=1))
        print("measure %s %s: read %d, figure %d, refused %d, NPB all %d interior %d, moves %d / %d, %.0fs" % (
            entry, window, len(keys), fig, refused, cell["non_positive_base_days"]["all_positions"], cell["non_positive_base_days"]["interior"],
            mv_under, mv_if, cell["seconds"]), flush=True)


def control(scratch):
    """In memory only.  Plants account A (OK, ALL-HOLDINGS-EXCLUDED, OK) and account B (OK, NO-PRIOR-HOLDINGS, OK) and runs the step-5
    counter.  Also plants C (OK, NON-POSITIVE-BASE with a prior included position, OK) and D (OK, NON-POSITIVE-BASE with no prior position, OK)
    to show the second reading moves C and not D.  Also checks the six-class function on planted count rows."""
    A = ["OK", "ALL-HOLDINGS-EXCLUDED", "OK"]
    B = ["OK", "NO-PRIOR-HOLDINGS", "OK"]
    C = ["OK", "NON-POSITIVE-BASE", "OK"]
    D = ["OK", "NON-POSITIVE-BASE", "OK"]
    hc_none = ["held_none"] * 3
    hc_inc = ["held_included_only_or_mixed"] * 3
    r = {"A_single_ALL-HOLDINGS-EXCLUDED": moves(A, hc_none), "B_single_NO-PRIOR-HOLDINGS": moves(B, hc_none),
         "C_single_NON-POSITIVE-BASE_prior_included_position": moves(C, hc_inc), "D_single_NON-POSITIVE-BASE_held_none": moves(D, hc_none)}
    fr = pd.DataFrame({"held_count": [0, 2, 1, 2, 3, None, 2], "included_count": [0, 1, 0, 0, 0, 0, 0], "negative_count": [0, 0, 1, 0, 1, 0, 0],
                       "excluded_count": [0, 1, 0, 2, 2, 0, 1]})
    cls = list(hclass_series(fr))
    want = ["held_none", "held_included_only_or_mixed", "held_only_negative", "held_only_excluded", "held_other", "not_determinable", "not_determinable"]
    held = (r["A_single_ALL-HOLDINGS-EXCLUDED"] == (True, True) and r["B_single_NO-PRIOR-HOLDINGS"] == (False, False)
            and r["C_single_NON-POSITIVE-BASE_prior_included_position"] == (False, True) and r["D_single_NON-POSITIVE-BASE_held_none"] == (False, False)
            and cls == want)
    out = {"what": "In memory only: plant account A with one ALL-HOLDINGS-EXCLUDED day and account B with one NO-PRIOR-HOLDINGS day (each between two OK days) and run the "
                   "step-5 counter (moves()) on each; plant C and D, each with one NON-POSITIVE-BASE day (C with a prior included position, D with no prior position), "
                   "to run the second reading; and run the six-class function on seven planted count rows.",
           "reading": {"moves_as_written_and_if_npb_prior_position_also": {k: list(v) for k, v in r.items()}, "six_classes_of_the_planted_rows": cls,
                       "expected": "A moves as written (True, True); B does not (False, False); C moves only under the second reading (False, True); D does not (False, False); "
                                   "classes " + ", ".join(want) + ": " + ("HELD" if held else "NOT HELD")}}
    (Path(scratch) / "control.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch":
        fetch(sys.argv[2], sys.argv[3])
    elif cmd == "census":
        census(sys.argv[2], sys.argv[3])
    elif cmd == "measure":
        measure(sys.argv[2], sys.argv[3])
    elif cmd == "control":
        control(sys.argv[2])
    else:
        raise SystemExit("unknown command")
