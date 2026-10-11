#!/usr/bin/env python3
"""IB-pr-427: Cottonwood's lagged closes graded BY ACCOUNT and by every column that could name a custodian, source or feed.
Copied from and extending IB-pr-425's s252_all_partitions.py (deliverables/0.9.0_WK_IRPT_BCKEND~284/, untouched).  Read only; the S3
reads were done by ib427_fetch.py into a cache OUTSIDE the repo, where AccountID is already a 12-character one-way digest.

    python -I ib427_by_account.py <cache_dir> <out.json>        measure and write the output (counts only)
    python -I ib427_by_account.py --control                      run only the planted control and print it

COPIED UNCHANGED FROM IB-pr-425:
  * price of a source row = Market Value / Units, rows with Units > 0 and Market Value > 0 and a CUSIP only;
  * the anchor is the Schwab silver closing_price by CUSIP (an own-date close);
  * a security MOVED on D when anchor close(D) differs from anchor close(prior trading day) by more than the tolerance (1e-4 relative);
  * FIRST_DAY_NO_PRIOR (2026-06-09) is outside the totals; trading days from lib/trading_calendar.py.
CHANGED: the unit of grading is the ROW.  A moved row (its CUSIP moved) is `prior` if its price is at the prior trading day's anchor
close, else `own` if at D's anchor close, else `neither`.  Rows are then grouped by account (digest) and by each field's value.
ACCOUNT CLASSES (the face): always_own = 0 prior rows and at least one moved row; always_prior = every own-or-prior moved row is
prior (and at least one); mixed = both own and prior rows; no_moved_rows.  An account whose moved rows are all `neither` has 0 prior
rows, so it meets the always_own definition literally; it is counted there and reported separately (own_rows_zero).
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import pickle
import statistics
import sys
from pathlib import Path

TOL = 1e-4


def same(a, b):
    return abs(a - b) <= TOL * max(abs(a), abs(b), 1e-9)


# ---------------------------------------------------------------------------- the instrument (pure functions: the control runs them)

def price_rows(cusips, mvs, units):
    """[(row_index, cusip, price)] -- the existing row filter, every row kept."""
    out = []
    for i, (c, mv, u) in enumerate(zip(cusips, mvs, units)):
        try:
            mv, u = float(mv), float(u)
        except (TypeError, ValueError):
            continue
        if c and c.strip() and u > 0 and mv > 0:
            out.append((i, c.strip(), mv / u))
    return out


def grade_rows(priced, own, prev):
    """priced [(idx, cusip, price)]; own/prev {cusip: anchor close}.  Returns [(idx, cusip, state)] for the MOVED rows only,
    state in own|prior|neither (prior first, as IB-pr-425's precedence)."""
    out = []
    for idx, k, x in priced:
        if k not in own or k not in prev or same(own[k], prev[k]):
            continue
        if same(x, prev[k]):
            out.append((idx, k, "prior"))
        elif same(x, own[k]):
            out.append((idx, k, "own"))
        else:
            out.append((idx, k, "neither"))
    return out


def security_day_states(graded):
    """IB-pr-425's security-day rule over the graded rows: prior if ANY row prior, else own if ANY own, else neither."""
    sec = collections.defaultdict(set)
    for _, k, s in graded:
        sec[k].add(s)
    return {k: ("prior" if "prior" in v else "own" if "own" in v else "neither") for k, v in sec.items()}


def classify_account(own, prior, neither):
    if own + prior + neither == 0:
        return "no_moved_rows"
    if prior == 0:
        return "always_own"          # 0 prior rows, at least one moved row (own_rows_zero flags the all-neither ones)
    if own == 0:
        return "always_prior"        # every own-or-prior moved row is prior
    return "mixed"


def mixing_kind(days):
    """days: list of (own, prior) per day for a MIXED account.  by_day: a day behind (prior only) and a day current (own only) both
    exist and no day holds both; within_day: a day holds both own and prior rows and no pure behind/current pair; both: the two."""
    within = any(o > 0 and p > 0 for o, p in days)
    by_day = any(p > 0 and o == 0 for o, p in days) and any(o > 0 and p == 0 for o, p in days)
    return "both" if within and by_day else "within_day" if within else "by_day"


# ---------------------------------------------------------------------------- the planted control

def control():
    """Fixture: 3 trading days D1<D2<D3, 6 accounts all holding the same 5 moving securities (so a security-level read cannot see the
    account), ONE planted account (ACCT_PLANTED) at its own close on D1 and at the PRIOR close on D2 and D3.  Decoys, none reported:
    a security that did not move, one clean account's row at neither close, a row for a security the anchor does not carry.
    The clean copy is the same fixture with the planted account at its own close every day.  Runs grade_rows / classify_account."""
    secs = ["S1", "S2", "S3", "S4", "S5"]
    anchors = {"D0": {s: 10.0 * (i + 1) for i, s in enumerate(secs)}}
    anchors["D0"]["FLAT"] = 50.0
    for n, d in enumerate(("D1", "D2", "D3"), start=1):
        anchors[d] = {s: 10.0 * (i + 1) + n for i, s in enumerate(secs)}
        anchors[d]["FLAT"] = 50.0
    prev_of = {"D1": "D0", "D2": "D1", "D3": "D2"}
    accounts = ["ACCT_C1", "ACCT_C2", "ACCT_C3", "ACCT_C4", "ACCT_C5", "ACCT_PLANTED"]

    def run(lag_days):
        per = {a: [0, 0, 0] for a in accounts}
        for d in ("D1", "D2", "D3"):
            own, prev = anchors[d], anchors[prev_of[d]]
            rows = []  # (account, cusip, price)
            for a in accounts:
                for s in secs + ["FLAT"]:
                    px = prev[s] if (a == "ACCT_PLANTED" and d in lag_days and s != "FLAT") else own[s]
                    rows.append((a, s, px))
            rows.append(("ACCT_C2", "S4", own["S4"] * 1.07))      # decoy: a clean account's row at neither close
            rows.append(("ACCT_C3", "NOANCHOR", 5.0))             # decoy: a security the anchor does not carry
            priced = [(i, r[1], r[2]) for i, r in enumerate(rows)]
            for idx, _, st in grade_rows(priced, own, prev):
                per[rows[idx][0]][("own", "prior", "neither").index(st)] += 1
        cls = {a: classify_account(*v) for a, v in per.items()}
        return sorted(a for a, c in cls.items() if c in ("always_prior", "mixed")), cls

    reported, cls = run({"D2", "D3"})
    clean, _ = run(set())
    return {"planted_account_label": "ACCT_PLANTED", "reported": reported, "clean_fixture_reported": clean,
            "classes_in_planted_fixture": dict(collections.Counter(cls.values())),
            "fixture": "3 trading days, 6 accounts holding the same 5 moving securities plus one that does not move; ACCT_PLANTED at the prior close "
                       "on D2 and D3 (own on D1); decoys: the unmoved security, one clean account's row at neither close, a row the anchor does not carry"}


# ---------------------------------------------------------------------------- the measurement

FIELDS = [  # (column, taken?, reason)
    ("Account Supervised", True, "a category label (Supervised / Unsupervised) on the account: could track an account type or servicing line"),
    ("Holding Supervised", True, "a category label on the holding: could track a servicing line"),
    ("_source", True, "the pipeline's own source stamp: names the feed system"),
    ("_feed", True, "the pipeline's own feed stamp: names the feed"),
    ("_schema_version", True, "the pipeline's schema stamp: a layout change could carry a date change"),
    ("Relationship ID", False, "account-specific grouping id (hundreds of values, each an account family): not a category label"),
    ("PortfolioID", False, "account-specific grouping id (hundreds of values): not a category label"),
    ("Account Number", False, "account-specific identifier: not a category label"),
    ("_source_file", False, "one value per partition (the file name carries the date): it is the day, not a field; the day is read in the per-day table"),
    ("_source_as_of", False, "one value per partition (the as-of date): it is the day"),
    ("Cash Equivalent", False, "a security attribute (cash sweep or not), not a custodian, source, feed or account type"),
    ("Symbol / Ticker / Asset Name / Original Asset Name / Asset Display Name / Alternative Identifier / AssetID",
     False, "security descriptors, not custodian, source, feed or account type (security class was IB-pr-425's cut)"),
]
FIELD_COLS = [f for f, taken, _ in FIELDS if taken]
HEAVY = ["2026-10-01", "2026-09-03", "2026-07-02", "2026-07-31"]


def blk():
    return {"moved": 0, "own": 0, "prior": 0, "neither": 0}


def add(b, st):
    b["moved"] += 1
    b[st] += 1


def main():
    if sys.argv[1:] == ["--control"]:
        print(json.dumps(control(), indent=1))
        return 0
    cache, out = Path(sys.argv[1]), Path(sys.argv[2])
    root = Path(__file__).resolve().parents[7]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/gold/irpt_holdings_performance")]
    import trading_calendar as tc
    import holdings_performance as hp
    decl = json.load(open(root / "data/assets/scripts/gold/irpt_holdings_performance/sources.json", encoding="utf-8"))
    src = decl["blackdiamond_z09"]
    prefix_resolved = hp.resolved_prefix(src, "positions_prefix", hp.firm_scope(src))
    anchor_prefix = decl["schwab_08335338"]["positions_prefix"]

    def load(kind, day):
        f = cache / ("%s_%s.pkl" % (kind, day))
        return pickle.load(open(f, "rb")) if f.exists() else "UNREAD"

    listed = sorted(f.name[4:14] for f in cache.glob("src_*.pkl") if pickle.load(open(f, "rb")) is not None)
    tdays = [d for d in listed if tc.is_trading_day(d)]

    def anchor(day):
        t = load("anc", day)
        if t in (None, "UNREAD"):
            return t
        by = {}
        for c, p in zip(t["cusip"], t["closing_price"]):
            c = (c or "").strip()
            if c and p is not None and float(p) > 0:
                by[c] = float(p)
        return by

    acct_all = set()                                   # every account in a graded-day partition
    acct = collections.defaultdict(lambda: [0, 0, 0])  # account -> own, prior, neither
    acct_days = collections.defaultdict(list)          # account -> [(own, prior)] per day it had moved rows
    rows_tot = blk()
    graded_days = []
    ungradeable = []
    per_day_acct = {}                                  # day -> {account: [own, prior, neither]}
    field_acct = {f: collections.defaultdict(lambda: [blk(), set()]) for f in FIELD_COLS}  # field -> value -> [block, accounts]
    sec_day = {}                                       # day -> security-day counts (reconciliation)
    sup = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0]))  # account -> Account Supervised value -> [own, prior, neither]
    absent_cols = collections.defaultdict(list)
    for i, d in enumerate(tdays):
        p = tc.prev_trading_day(dt.date.fromisoformat(d)).isoformat()
        s = load("src", d)
        A, B = anchor(d), anchor(p)
        if s in (None, "UNREAD") or A in (None, "UNREAD") or B in (None, "UNREAD"):
            ungradeable.append(d)
            continue
        if i == 0 or tdays[i - 1] != p:
            continue  # FIRST_DAY_NO_PRIOR: outside the totals
        for c in s.get("_absent_columns", []):
            absent_cols[c].append(d)
        graded_days.append(d)
        priced = price_rows(s["CUSIP"], s["Market Value"], s["Units"])
        graded = grade_rows(priced, A, B)
        acct_all.update(s["AccountID"])
        sd = collections.Counter(security_day_states(graded).values())
        sec_day[d] = {"moved": sum(sd.values()), "own": sd["own"], "prior": sd["prior"], "neither": sd["neither"],
                      "rows_priced_moved": len(graded), "rows_prior": sum(1 for g in graded if g[2] == "prior")}
        pd = collections.defaultdict(lambda: [0, 0, 0])
        for idx, k, st in graded:
            a = s["AccountID"][idx]
            j = ("own", "prior", "neither").index(st)
            acct[a][j] += 1
            pd[a][j] += 1
            add(rows_tot, st)
            if "Account Supervised" not in s.get("_absent_columns", []):
                sup[a][str(s["Account Supervised"][idx])][j] += 1
            for f in FIELD_COLS:
                v = s[f][idx]
                v = "(column absent from this partition)" if f in s.get("_absent_columns", []) else "(null)" if v is None else str(v)
                cell = field_acct[f][v]
                add(cell[0], st)
                cell[1].add(a)
        per_day_acct[d] = pd
        for a, (o, pr, ne) in pd.items():
            acct_days[a].append((o, pr))

    # ---- classes
    cls = {a: classify_account(*acct[a]) if a in acct else "no_moved_rows" for a in acct_all}
    accounts = collections.Counter(cls.values())
    by_class = {k: blk() for k in ("always_own", "always_prior", "mixed")}
    for a, v in acct.items():
        c = cls[a]
        for st, n in zip(("own", "prior", "neither"), v):
            by_class[c][st] += n
            by_class[c]["moved"] += n
    only_neither = sum(1 for a, v in acct.items() if cls[a] == "always_own" and v[0] == 0)
    neither_by_class = {k: by_class[k]["neither"] for k in by_class}

    # ---- the share distribution (prior / (own + prior)); the alternative over all moved rows is beside it
    def bucket(sh):
        return ("zero" if sh == 0 else "above_0_to_1" if sh < 1 else "1_to_10" if sh < 10 else "10_to_50" if sh < 50
                else "50_to_99" if sh < 100 else "100")
    order = ["zero", "above_0_to_1", "1_to_10", "10_to_50", "50_to_99", "100"]
    dist, dist_moved = collections.Counter(), collections.Counter()
    undefined = 0
    for a, (o, pr, ne) in acct.items():
        if o + pr:
            dist[bucket(100.0 * pr / (o + pr))] += 1
        else:
            undefined += 1
        dist_moved[bucket(100.0 * pr / (o + pr + ne))] += 1
    share = {"basis": "per-account prior rows / (own + prior rows), percent; bounds: zero = exactly 0, above_0_to_1 = (0,1), 1_to_10 = [1,10), "
                      "10_to_50 = [10,50), 50_to_99 = [50,100), 100 = exactly 100",
             "accounts": {k: dist[k] for k in order}, "accounts_with_only_neither_rows_no_share": undefined,
             "alternative_over_all_moved_rows": {k: dist_moved[k] for k in order}}

    # ---- mixed accounts
    mix = collections.Counter(mixing_kind(acct_days[a]) for a, c in cls.items() if c == "mixed")
    mixed_accounts = {"by_day": mix["by_day"], "within_day": mix["within_day"], "both": mix["both"],
                      "definition": "by_day: the account has a day with prior rows and no own rows AND a day with own rows and no prior rows, and no "
                                    "day holds both; within_day: some day holds both own and prior rows and there is no such pure pair of days; "
                                    "both: both patterns occur. The three sum to the mixed accounts."}
    # day-level view of the mixed accounts' prior-day pattern
    mixed_set = [a for a, c in cls.items() if c == "mixed"]
    pure_behind = pure_current = within_days = 0
    for a in mixed_set:
        for o, pr in acct_days[a]:
            if pr and not o:
                pure_behind += 1
            elif o and not pr:
                pure_current += 1
            elif o and pr:
                within_days += 1
    mixed_accounts["account_days_of_mixed_accounts"] = {"behind_only": pure_behind, "current_only": pure_current, "both_own_and_prior": within_days}

    # ---- per account persistence
    behind_days = collections.Counter()
    for d in graded_days:
        for a, v in per_day_acct[d].items():
            if v[1]:
                behind_days[a] += 1
    per_day = []
    prev_set = None
    carry = []
    for d in graded_days:
        pd = per_day_acct[d]
        beh = {a for a, v in pd.items() if v[1]}
        per_day.append({"date": d, "accounts_behind": len(beh), "accounts_with_moved_rows": len(pd),
                        "rows_prior": sum(v[1] for v in pd.values()), "rows_moved": sum(sum(v) for v in pd.values())})
        if prev_set is not None and prev_set:
            carry.append((len(beh & prev_set), len(prev_set), len(beh)))
        prev_set = beh
    pb = [x["accounts_behind"] for x in per_day]
    ever = [a for a in behind_days]
    persistence = {
        "accounts_ever_behind": len(ever),
        "accounts_behind_on_k_or_more_days": {str(k): sum(1 for a in ever if behind_days[a] >= k) for k in (1, 2, 5, 10, 20, 40, 60, 80)},
        "per_day_accounts_behind": {"min": min(pb), "median": statistics.median(pb), "max": max(pb)},
        "days_with_zero_accounts_behind": sum(1 for x in pb if x == 0),
        "day_to_day": {"pairs": len(carry), "median_share_of_yesterdays_behind_accounts_still_behind":
                       round(statistics.median(100.0 * c / n for c, n, _ in carry), 2) if carry else None,
                       "median_share_of_todays_behind_accounts_also_behind_yesterday":
                       round(statistics.median(100.0 * c / m for c, _, m in carry if m), 2) if any(m for *_, m in carry) else None},
    }
    heavy = []
    heavy_sets = {}
    for d in HEAVY:
        if d in per_day_acct:
            pd = per_day_acct[d]
            beh = {a for a, v in pd.items() if v[1]}
            heavy_sets[d] = beh
            x = next(z for z in per_day if z["date"] == d)
            heavy.append({"date": d, "accounts_behind": x["accounts_behind"], "accounts_with_moved_rows": x["accounts_with_moved_rows"],
                          "share_of_accounts_behind_pct": round(100.0 * x["accounts_behind"] / x["accounts_with_moved_rows"], 2),
                          "rows_prior": x["rows_prior"], "median_prior_rows_per_behind_account":
                              statistics.median(pd[a][1] for a in beh) if beh else 0,
                          "accounts_in_class": dict(collections.Counter(cls[a] for a in beh))})
    inter = {}
    keys = list(heavy_sets)
    for i1 in range(len(keys)):
        for i2 in range(i1 + 1, len(keys)):
            inter["%s & %s" % (keys[i1], keys[i2])] = len(heavy_sets[keys[i1]] & heavy_sets[keys[i2]])
    all_heavy = set.intersection(*heavy_sets.values()) if heavy_sets else set()
    others = [x["accounts_behind"] for x in per_day if x["date"] not in HEAVY]
    persistence["heavy_days"] = {"days": heavy, "accounts_behind_on_both_days_of_each_pair": inter,
                                 "accounts_behind_on_all_four": len(all_heavy),
                                 "other_days_accounts_behind": {"median": statistics.median(others), "max": max(others)}}

    # ---- by field
    by_field = []
    for f in FIELD_COLS:
        vals = []
        for v, (b, accs) in sorted(field_acct[f].items(), key=lambda kv: kv[0]):
            vals.append(dict(value=v, accounts=len(accs), **b))
        by_field.append({"field": f, "values": vals})
    # ---- the one field that varies with the lag: Account Supervised, on the days the column is present
    present_days = len(graded_days) - len(absent_cols.get("Account Supervised", []))
    grp = collections.defaultdict(lambda: {"accounts": 0, "rows": blk(), "by_class": collections.Counter()})
    for a, vals in sup.items():
        key = "|".join(sorted(vals)) if len(vals) > 1 else next(iter(vals))
        g = grp["both_values_over_the_window" if len(vals) > 1 else key]
        g["accounts"] += 1
        g["by_class"][cls[a]] += 1
        for st, n in zip(("own", "prior", "neither"), (sum(v[0] for v in vals.values()), sum(v[1] for v in vals.values()), sum(v[2] for v in vals.values()))):
            g["rows"][st] += n
            g["rows"]["moved"] += n
    supervision_cross = {
        "days_with_the_column": present_days, "days_without": len(absent_cols.get("Account Supervised", [])),
        "basis": "only the days the column is present; an account is grouped by the Account Supervised value(s) it carries on its moved rows on those days",
        "groups": {k: {"accounts": g["accounts"], "rows": g["rows"], "accounts_by_class": dict(g["by_class"])} for k, g in sorted(grp.items())},
        "all_16_plus_unsupervised_accounts_are_mixed_or_lagged": None,
    }
    supervision_cross.pop("all_16_plus_unsupervised_accounts_are_mixed_or_lagged")
    mixed_with_status = sum(1 for a in mixed_set if a in sup)
    supervision_cross["mixed_accounts_seen_on_present_days"] = mixed_with_status
    supervision_cross["mixed_accounts_never_seen_with_unsupervised_rows"] = sum(
        1 for a in mixed_set if a in sup and "Unsupervised" not in sup[a])
    # ---- reconciliation with IB-pr-425
    old = json.load(open(root / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~284/IB123-1_s252_all_partitions.json", encoding="utf-8"))
    od = {x["date"]: x for x in old["days"] if x["state"] == "GRADED"}
    mism = [d for d in graded_days if d not in od or any(
        od[d][k1] != sec_day[d][k2] for k1, k2 in (("moved", "moved"), ("own_close", "own"), ("prior_close", "prior"), ("neither", "neither"),
                                                  ("rows_priced_moved", "rows_priced_moved"), ("rows_prior", "rows_prior")))]
    def tot(k):
        return sum(v[k] for v in sec_day.values())
    recon = {
        "ib_pr_425_security_days": {"moved": sum(x["moved"] for x in od.values()),
                                    "own": sum(x["own_close"] for x in od.values()), "prior": sum(x["prior_close"] for x in od.values()),
                                    "neither": sum(x["neither"] for x in od.values()),
                                    "rows_priced_moved": sum(x["rows_priced_moved"] for x in od.values()),
                                    "rows_prior": sum(x["rows_prior"] for x in od.values())},
        "this_cell_security_days_by_the_same_rule": {"moved": tot("moved"), "own": tot("own"), "prior": tot("prior"), "neither": tot("neither"),
                                                     "rows_priced_moved": tot("rows_priced_moved"), "rows_prior": tot("rows_prior")},
        "this_cell_rows": dict(rows_tot),
        "days_compared": len(graded_days), "days_where_any_of_the_six_counts_differs": len(mism), "days_that_differ": mism,
        "how": "A security-day with several rows is several rows here. IB-pr-425's security-day rule (prior if any row prior, else own if any row own, "
               "else neither) is re-applied to this cell's graded rows and compared with IB-pr-425's per-day counts on all graded days; the row "
               "totals are compared with its rows_priced_moved and rows_prior.",
        "rows_prior_equals_425_rows_prior": rows_tot["prior"] == sum(x["rows_prior"] for x in od.values()),
        "rows_moved_equals_425_rows_priced_moved": rows_tot["moved"] == sum(x["rows_priced_moved"] for x in od.values()),
    }
    ctrl = control()

    doc = {
        "source": {"bucket": src["bucket"], "entry": "blackdiamond_z09", "prefix_template": src["positions_prefix"] + "date=YYYY-MM-DD/",
                   "prefix_resolved_by": "holdings_performance.resolved_prefix(blackdiamond_z09, positions_prefix, firm_scope) -> %d characters, same as the gold script" % len(prefix_resolved),
                   "anchor": "%s%s (closing_price by cusip; the Schwab own-date close)" % (anchor_prefix, "date=YYYY-MM-DD/"),
                   "price": "Market Value / Units, rows with Units > 0 and Market Value > 0 and a CUSIP; every row graded",
                   "account_key": "AccountID, replaced at read time by a one-way digest; used only to group rows, never written"},
        "tolerance": {"kind": "relative", "value": TOL, "rule": "abs(a-b) <= 1e-4 * max(abs(a), abs(b), 1e-9)", "taken_from": "IB-pr-425 s252_all_partitions.py same()"},
        "days_graded": len(graded_days),
        "days_ungradeable": ungradeable,
        "range_graded": [graded_days[0], graded_days[-1]],
        "rows": dict(rows_tot),
        "accounts": {"read": len(acct_all), "always_own": accounts["always_own"], "always_prior": accounts["always_prior"],
                     "mixed": accounts["mixed"], "no_moved_rows": accounts["no_moved_rows"],
                     "always_own_with_zero_own_rows_all_neither": only_neither,
                     "read_means": "distinct AccountID values present in any graded-day partition (rows of any kind)"},
        "class_definitions": "always_own: 0 prior rows and at least one moved row; always_prior: every own-or-prior moved row is prior; mixed: both "
                             "own and prior rows; no_moved_rows: none. An account with moved rows that are all neither has 0 prior rows and meets "
                             "the always_own definition literally; it is counted there and shown in always_own_with_zero_own_rows_all_neither.",
        "rows_by_account_class": by_class,
        "account_share_distribution": share,
        "mixed_accounts": mixed_accounts,
        "persistence": persistence,
        "fields_considered": [{"column": f, "split": t, "reason": r} for f, t, r in FIELDS],
        "columns_absent_from_some_partitions": {c: {"days_absent": len(v), "first": v[0], "last": v[-1]} for c, v in absent_cols.items()},
        "by_field": by_field,
        "supervision_cross": supervision_cross,
        "by_field_absent_reason": "",
        "neither_by_account_class": neither_by_class,
        "accounts_behind_per_day": [{"date": x["date"], "accounts_behind": x["accounts_behind"],
                                     "accounts_with_moved_rows": x["accounts_with_moved_rows"], "rows_prior": x["rows_prior"]} for x in per_day],
        "control": ctrl,
        "reconciliation_with_IB_pr_425": recon,
    }
    out.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    print("wrote", out, "days", len(graded_days), "rows", rows_tot, "accounts", dict(accounts), "read", len(acct_all))
    return 0


if __name__ == "__main__":
    sys.exit(main())
