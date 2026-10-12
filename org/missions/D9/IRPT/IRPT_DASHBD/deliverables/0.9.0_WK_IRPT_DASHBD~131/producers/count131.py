"""~131: the count, implementing RULE.md (commit 469d1fc868) as written. Private inputs; prints and writes counts only.
Usage: IRPT_PRIV_ROOT=<private root> IRPT_RERUN_DIR=<out dir> python -I count131.py <repo_root> copy|orig"""
import collections
import datetime as dt
import json
import os
import pickle
import re
import sys
repo, which = sys.argv[1], sys.argv[2]
sys.path.insert(0, repo)
from lib.trading_calendar import is_trading_day, trading_days_between  # noqa: E402
PRIV = os.environ["IRPT_PRIV_ROOT"].rstrip("/") + "/0.9.0_WK_IRPT_DASHBD~131/"
OUTD = os.environ["IRPT_RERUN_DIR"].rstrip("/") + "/"
days = pickle.load(open(PRIV + "days234.pkl", "rb"))
T = pickle.load(open(PRIV + "txn_%s.pkl" % which, "rb"))
SWEEP = re.compile(r"money market|sweep|fdic|insured deposit|cash reserve|cash management|cash & equivalents|cash and equivalents|government cash|treasury cash|bank deposit", re.I)
SUBX = re.compile(r"sweep|reinvest", re.I)


def dd(x):
    if x is None:
        return None
    try:
        if x != x:
            return None
    except Exception:
        pass
    if hasattr(x, "date"):
        return x.date()
    s = str(x)[:10]
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        return None


def fnum(x):
    try:
        v = float(x)
        return None if v != v else v
    except (TypeError, ValueError):
        return None


rows = T["rows"]
noid = sum(1 for r in rows if not r.get("transaction_id"))
seen, ded = set(), []
for r in rows:
    i = r.get("transaction_id")
    if not i:
        continue
    if i in seen:
        continue
    seen.add(i)
    ded.append(r)
by = collections.defaultdict(list)
for r in ded:
    by[str(r["account_number"]).strip().lstrip("0")].append(r)
has_asset = any(r.get("asset_id") for r in ded)
F = dt.date.fromisoformat(T["newest_nonempty"])
firm = F - dt.timedelta(days=7)


def is_buy(r):
    return str(r.get("transaction_type") or "").strip().lower() == "buy"


def swept(r):
    return bool(SUBX.search(str(r.get("transaction_sub_type") or "")) or SWEEP.search(str(r.get("asset_name") or "")) or SWEEP.search(str(r.get("asset_display_name") or "")))


def qual_buys(a):
    out, excl, nodate = [], set(), set()
    for r in by.get(a, []):
        if not is_buy(r):
            continue
        mv = fnum(r.get("market_value"))
        if mv is None or mv == 0:
            continue
        if swept(r):
            excl.add(r["transaction_id"])
            continue
        t = dd(r.get("trade_date"))
        if t is None:
            nodate.add(r["transaction_id"])
            continue
        out.append((t, abs(mv), r.get("asset_id")))
    return out, excl, nodate


flowdays_by_acct = collections.defaultdict(list)
for x in days:
    flowdays_by_acct[x["a"]].append(dt.date.fromisoformat(x["d"]))
cls_day = collections.Counter()
other_why = collections.Counter()
classes = collections.Counter()
bands = collections.Counter()
dep = []
n_plan = n_plan_same = beyond_next = 0
excl_all, nodate_all = set(), set()
QB = {}
for x in days:
    a = x["a"].strip().lstrip("0")
    d = dt.date.fromisoformat(x["d"])
    rs = [r for r in by.get(a, []) if dd(r.get("return_date")) == d and str(r.get("external_flow") or "").strip() in ("Contribution", "Withdrawal")]
    IN = [r for r in rs if r["external_flow"].strip() == "Contribution"]
    OUT = [r for r in rs if r["external_flow"].strip() == "Withdrawal"]
    fl = x["flow"]
    if not rs:
        k, why = "other", "no_ledger_row"
    elif IN and OUT:
        k, why = "other", "mixed"
    elif IN and all(str(r.get("transaction_type") or "").strip() == "Cash Deposit" for r in IN) and fl > 0:
        k, why = "deposit", None
    elif IN and all(str(r.get("transaction_type") or "").strip() == "Cash Deposit" for r in IN):
        k, why = "other", "sign_disagrees"
    elif IN:
        k, why = "other", "in_type_not_cash_deposit"
    elif OUT and fl < 0:
        k, why = "withdrawal", None
    else:
        k, why = "other", "sign_disagrees"
    cls_day[k] += 1
    if why:
        other_why[why] += 1
    if k != "deposit":
        continue
    amt = sum(abs(fnum(r.get("market_value")) or 0.0) for r in IN)
    seg_end = dt.date.fromisoformat(x["end"])
    if a not in QB:
        QB[a] = qual_buys(a)
        excl_all |= QB[a][1]
        nodate_all |= QB[a][2]
    buys = QB[a][0]
    eff_end = min(seg_end, firm)
    res = None
    if amt <= 0 or not by.get(a):
        res = "not_determinable"
    elif eff_end < d:
        res = "not_determinable"
    else:
        per = collections.defaultdict(float)
        for t, v, _ in buys:
            if d <= t <= eff_end:
                per[t] += v
        hit = sorted(t for t, v in per.items() if v >= 0.10 * amt)
        if hit:
            ts = hit[0]
            nxt = d + dt.timedelta(days=1)
            while not is_trading_day(nxt):
                nxt += dt.timedelta(days=1)
            if ts == d:
                res = "same_day"
            elif ts == nxt:
                res = "next_trading_day"
            else:
                res = "later"
                n = len(trading_days_between(d + dt.timedelta(days=1), ts))
                bands["2_to_5" if n <= 5 else "6_to_20" if n <= 20 else "over_20"] += 1
            later_flow = [f for f in flowdays_by_acct[x["a"]] if f > d]
            if later_flow and ts > min(later_flow):
                beyond_next += 1
        elif eff_end < seg_end:
            res = "not_determinable"
        else:
            res = "never_in_window"
    classes[res] += 1
    if has_asset:
        pb = collections.defaultdict(set)
        for t, v, aid in buys:
            if aid and d - dt.timedelta(days=90) <= t <= d - dt.timedelta(days=1):
                pb[aid].add(t)
        plan = False
        for aid, ts_ in pb.items():
            s = sorted(ts_)
            if len(s) >= 3 and max((s[i + 1] - s[i]).days for i in range(len(s) - 1)) <= 35:
                plan = True
                break
        if plan:
            n_plan += 1
            n_plan_same += res == "same_day"
CL = ("same_day", "next_trading_day", "later", "never_in_window", "not_determinable")
res = {"store": which, "flow_bearing_days": len(days), "accounts": len({x["a"] for x in days}),
       "deposit_days": cls_day["deposit"], "withdrawal_days": cls_day["withdrawal"], "other_days": cls_day["other"],
       "other_days_why": dict(other_why), "classes": {k: classes[k] for k in CL},
       "later_trading_days": {k: bands[k] for k in ("2_to_5", "6_to_20", "over_20")},
       "deposits_into_accounts_with_a_standing_purchase_plan": n_plan if has_asset else None, "plan_deposits_same_day": n_plan_same,
       "deposit_days_first_purchase_after_next_flow_day": beyond_next,
       "rows_no_transaction_id": noid, "buy_ids_excluded_as_sweep_or_reinvest": len(excl_all), "buy_ids_no_trade_date": len(nodate_all),
       "ids_kept": len(ded), "newest_nonempty_file_year_month": str(F)[:7], "coverage_firm_to_year_month": str(firm)[:7],
       "deposit_days_with_segment_end_past_coverage": sum(1 for x in days if dt.date.fromisoformat(x["end"]) > firm)}
print(json.dumps(res, indent=1))
json.dump(res, open(OUTD + "counts_%s.json" % which, "w"), indent=1)
