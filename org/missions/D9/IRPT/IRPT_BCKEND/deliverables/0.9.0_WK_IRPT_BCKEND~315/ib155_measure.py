#!/usr/bin/env python3
"""IB-pr-459 (round 155): READ ONLY, two measurements.  Counts only: no account id, balance or holding of an account is written; no security is named.

  python -I ib155_measure.py <scratch_dir> <out.json>

<scratch_dir> holds what the ~308 / ~310 scripts rebuilt (cache of S3 partitions, tx.pkl, phase1.pkl, prep.pkl, tickers.json, yahoo/ cache, calls.json); this script
never fetches Yahoo (ib150_fetch_yahoo.py of ~310 did, ONE pass, logged in calls.json).  Reads from AWS here: S3 get/head/list only.

Measurement 1: the landed prices store (the parquet commonwealth_price_basis_census.py:159 reads) against the unadjusted Close the reader returned, for the 878 tickers.
Measurement 2: the performance route's reader (HoldingsGoldSource + holdings_gold.calculate, imported from the repo at this base) run locally over the SERVED holdings
gold read from S3 for one entry the route composes today.  NOT the deployed function's answer.
"""
from __future__ import annotations

import collections
import datetime as dt
import io
import json
import sys
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
import commonwealth_daily_valuation as dv  # noqa: E402
import commonwealth_price_basis_census as cen  # noqa: E402
import commonwealth_price_census as pc  # noqa: E402
import trading_calendar as tc  # noqa: E402

EPOCH = dt.date(1970, 1, 1)
EQ_TOL = cen.EQ_TOL            # 1e-4 relative, the module's tolerance (commonwealth_price_basis_census.py:73)
LOOKBACK = 40                  # trading days before the first graded day (the grading window)
SMALL = 5e-3                   # "within half a percent": the census's own TOL


# ------------------------------------------------------------------------------------------------------------------ measurement 1
def measurement_1(scratch):
    scratch = Path(scratch)
    tickers = list(json.load(open(scratch / "tickers.json", encoding="utf-8"))["tickers"])
    assert len(tickers) == 878 and len(set(tickers)) == 878
    P1 = __import__("pickle").load(open(scratch / "phase1.pkl", "rb"))
    graded = P1["graded"]
    assert len(graded) == 85
    first = dt.date.fromisoformat(graded[0])
    d = first
    for _ in range(LOOKBACK):
        d = tc.prev_trading_day(d)
    window_days = sorted(set(graded) | {x.isoformat() for x in tc.trading_days_between(d, first)})

    s3 = boto3.client("s3", region_name="us-east-1")
    bucket, key = pc.split_uri(pc.legacy_uri(cen.SPEC["legacy"]))
    head = s3.head_object(Bucket=bucket, Key=key)
    raw = pc._get(s3, bucket, key)
    pf = pq.ParquetFile(io.BytesIO(raw))
    names = list(pf.schema_arrow.names)
    rows = int(pf.metadata.num_rows)
    store = pf.read(columns=["date", "ticker", "price", "source"]).to_pandas()
    store["date"] = pd.to_datetime(store["date"]).dt.strftime("%Y-%m-%d")
    labels = {str(k): int(v) for k, v in store["source"].value_counts().items()}
    store_max = store["date"].max()
    ystore = store[store["source"] == cen.YAHOO_LABEL]
    yahoo_store_max = ystore["date"].max()
    in_store = set(store["ticker"].astype(str))
    by_tk = {t: g for t, g in ystore.groupby(ystore["ticker"].astype(str))}

    out = {k: 0 for k in ("every_compared_day_equal", "some_days_not_equal", "no_yahoo_labelled_point_in_the_store", "not_in_the_store", "no_bar_from_the_reader")}
    compared = equal = 0
    causes = collections.Counter()
    cover_all = cover_gaps = cover_none = 0
    needed_total = covered_total = 0
    store_newest_behind = 0
    yahoo_points_but_none_in_window = 0
    reader_max = None
    n_with_bars = 0
    ratio_unequal_tickers = 0
    for tk in tickers:
        s, _ = dv.read_yahoo_close(str(scratch / "yahoo"), tk)
        if s is None or len(s) == 0:
            out["no_bar_from_the_reader"] += 1
            continue
        n_with_bars += 1
        close = {(EPOCH + dt.timedelta(days=int(k))).isoformat(): float(v) for k, v in s.items()}
        yh = cen.read_cache(str(scratch / "yahoo"), tk)[0]          # DataFrame(index iso date, Close, Adj Close)
        adj = {} if yh is None else {k: float(v) for k, v in yh["Adj Close"].items()}
        rmax = max(close)
        reader_max = rmax if reader_max is None or rmax > reader_max else reader_max
        if tk not in in_store:
            out["not_in_the_store"] += 1
            continue
        g = by_tk.get(tk)
        if g is None or not len(g):
            out["no_yahoo_labelled_point_in_the_store"] += 1
            continue
        sp = g.groupby("date")["price"].median().to_dict()
        # coverage of the needed days (the window days on which the reader has a bar)
        need = [x for x in window_days if x in close]
        have = [x for x in need if x in sp]
        needed_total += len(need)
        covered_total += len(have)
        if need and len(have) == len(need):
            cover_all += 1
        elif have:
            cover_gaps += 1
        else:
            cover_none += 1
        if max(sp) < rmax:
            store_newest_behind += 1
        both = [x for x in have]
        if not both:
            out["no_yahoo_labelled_point_in_the_store"] += 1
            yahoo_points_but_none_in_window += 1
            continue
        neq = 0
        cdays = sorted(close)
        bad = []                                              # (day, store price, reader Close) of this ticker's unequal ticker-days
        for x in both:
            c, v = close[x], float(sp[x])
            compared += 1
            if c > 0 and abs(v / c - 1.0) <= EQ_TOL:
                equal += 1
                continue
            neq += 1
            bad.append((x, v, c))
        if bad:
            # the ticker's own run of ratios store / Close on days that differ by more than half a percent: a constant ratio (within 1e-3) over three or more days
            big = [v / c for _x, v, c in bad if c > 0 and abs(v / c - 1.0) > SMALL]
            med = float(np.median(big)) if len(big) >= 3 else None
            for x, v, c in bad:
                i = cdays.index(x)
                a = adj.get(x)
                r = v / c if c > 0 else float("nan")
                if a is not None and a > 0 and abs(a / c - 1.0) > EQ_TOL and abs(v / a - 1.0) <= EQ_TOL:
                    causes["store_equals_adj_close_not_close (dividend-adjusted point)"] += 1
                elif med is not None and abs(r - 1.0) > SMALL and abs(r / med - 1.0) <= 1e-3:
                    k = max(med, 1.0 / med)
                    whole = abs(k - round(k)) <= 1e-3 * k
                    causes["constant_ratio_store_over_Close_whole_number_or_its_reciprocal (a different share basis: split-like)" if whole
                           else "constant_ratio_store_over_Close_not_a_whole_number (a different basis or unit)"] += 1
                elif any(0 <= j < len(cdays) and cdays[j] != x and abs(v / close[cdays[j]] - 1.0) <= EQ_TOL for j in (i - 1, i + 1)) and abs(r - 1.0) > SMALL:
                    causes["store_equals_close_of_an_adjacent_reader_day (a different day)"] += 1
                elif abs(r - 1.0) <= SMALL:
                    causes["within_half_percent_of_close_not_equal (rounding or small drift)"] += 1
                else:
                    causes["other (beyond half a percent, not a constant ratio, not Adj Close, not an adjacent day)"] += 1
        out["every_compared_day_equal" if neq == 0 else "some_days_not_equal"] += 1
        ratio_unequal_tickers += 1 if neq else 0
    assert sum(out.values()) == 878, out
    not_equal = compared - equal
    assert sum(causes.values()) == not_equal
    compared_tickers = out["every_compared_day_equal"] + out["some_days_not_equal"]
    if compared == 0:
        word = "CANNOT_BE_TOLD"
    elif out["some_days_not_equal"] == 0:
        word = "YES_FOR_EVERY_COMPARED_TICKER"
    elif out["every_compared_day_equal"] == 0:
        word = "NO"
    else:
        word = "FOR_SOME"
    return {
        "store_object": {"last_modified_utc": head["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"), "rows": rows, "columns": names,
                         "content_length": int(head.get("ContentLength") or 0), "source_label_row_counts": labels,
                         "store_newest_day_any_label": store_max, "store_newest_yahoo_labelled_day": yahoo_store_max,
                         "distinct_tickers_in_store": len(in_store)},
        "tickers": {"asked": 878, "outcomes": out, "with_a_bar_from_the_reader": n_with_bars},
        "ticker_days": {"compared": compared, "equal": equal, "not_equal": not_equal,
                        "equality_rule": "abs(store_price / reader_Close - 1) <= 1e-4 (relative; the module's EQ_TOL, commonwealth_price_basis_census.py:73); store price = median of the "
                                         "ticker's yahoo_finance-labelled rows for the date; reader Close = Yahoo Close with auto_adjust=False; compared only on dates in the window "
                                         "(85 graded days plus the 40 trading days before the first) where both exist"},
        "not_equal_by_cause": dict(causes),
        "store_coverage": {
            "window": {"graded_days": 85, "trading_days_before_them": LOOKBACK, "days": len(window_days), "first": window_days[0], "last": window_days[-1]},
            "needed_day_definition": "a window day on which the reader returned a bar for the ticker",
            "tickers_with_every_needed_day_in_the_store": cover_all, "tickers_with_gaps": cover_gaps,
            "tickers_in_store_with_yahoo_points_but_none_on_a_needed_day": cover_none,
            "needed_ticker_days": needed_total, "covered_ticker_days": covered_total,
            "newest_day_the_store_holds_yahoo_labelled": yahoo_store_max, "newest_day_the_reader_returns": reader_max,
            "tickers_whose_newest_store_day_is_before_their_newest_reader_day": store_newest_behind},
        "outcome_definitions": {
            "no_bar_from_the_reader": "the reader returned no bar for the ticker (checked first)",
            "not_in_the_store": "the ticker has a reader bar and no row of any label in the store",
            "no_yahoo_labelled_point_in_the_store": "has a reader bar and store rows, but no yahoo_finance-labelled point on a date where the reader has a bar inside the window "
                                                  "(%d of these hold yahoo-labelled points outside the window or on no reader day)" % yahoo_points_but_none_in_window,
            "every_compared_day_equal / some_days_not_equal": "one or more compared ticker-days, all equal / at least one not equal"},
        "word": word, "compared_tickers": compared_tickers,
    }


# ------------------------------------------------------------------------------------------------------------------ measurement 2
def measurement_2():
    import tenants
    import holdings_gold as hg
    import installed
    import ids
    import parity_period_returns as ppr
    s3 = boto3.client("s3", region_name="us-east-1")
    firm = tenants._CANONICAL_INF
    src = installed._holdings_source_for(s3, firm)            # the route's own composition of the source (installed.py:75)
    avail = src.partition_dates()
    last = avail[-1]
    # every partition read once (S3 get only) for the status census: account key in memory only, never written
    from concurrent.futures import ThreadPoolExecutor

    def rd(day):
        _, fr = src._read(day, None)
        return fr[["account_id", "status"]].assign(day=day)
    with ThreadPoolExecutor(16) as pool:
        allf = pd.concat(list(pool.map(rd, avail)), ignore_index=True)
    windows = [("SI", "1970-01-01", last), ("1Y",) + tuple(x.isoformat() for x in ppr.period_window("1Y", last)),
               ("YTD",) + tuple(x.isoformat() for x in ppr.period_window("YTD", last))]
    chosen = None
    tried = []
    for name, a, b in windows:
        w = allf[(allf["day"] >= a) & (allf["day"] <= b)]
        g = w.groupby("account_id")
        n = g.size()
        nonok = g["status"].apply(lambda s: int((s != "OK").sum()))
        onlast = set(w[w["day"] == last]["account_id"])
        maxn = int(n.max())
        parts = int(w["day"].nunique())
        control = sorted(k for k in n.index if k in onlast and nonok[k] == 0 and int(n[k]) == maxn)
        cand = []
        for k in n.index:
            if k in onlast and 1 <= nonok[k] <= 5 and int(n[k]) >= 0.9 * maxn:
                st = w[(w["account_id"] == k)].sort_values("day")["status"].tolist()
                if st[0] == "OK" and st[-1] == "OK":          # a non-OK day strictly inside the window
                    cand.append(k)
        tried.append({"window": name, "start": a, "end": b, "partitions": parts, "accounts": int(len(n)), "max_rows_for_an_account": maxn,
                      "accounts_with_all_ok_and_a_full_window": len(control), "accounts_with_1_to_5_non_ok_inside": len(cand)})
        if control and cand and chosen is None:
            chosen = (name, a, b, cand, control, parts, maxn)
    if chosen is None:
        raise SystemExit("no window with both a non-OK account and a control")
    name, a, b, cand, control, parts, maxn = chosen
    si_ctl = tried[0]["accounts_with_all_ok_and_a_full_window"]
    w = allf[(allf["day"] >= a) & (allf["day"] <= b)]

    def status_of(k):
        return w[w["account_id"] == k].sort_values("day")["status"].tolist()
    prefer = [k for k in sorted(cand) if any(x not in ("OK", "NO-PRIOR-HOLDINGS") for x in status_of(k))]
    acct = (prefer or sorted(cand))[0]
    ctl = sorted(control)[0]
    allstatus = collections.Counter(allf["status"])

    def read(k):
        cid = ids.opaque_account(firm, k)
        scope = {"resolved_scope": {"scope_ids": [cid]}, "permitted_account_set": [cid], "verified_request_firm_id": tenants._LEGACY_SHORT_ID["INF"]}
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):                  # the reader prints one timing line (no id, no value)
            ans = hg.calculate(scope, a, b, src)
        st = status_of(k)
        vf = ans["report"]["returns"].get("value_facts") if isinstance(ans["report"].get("returns"), dict) else None
        vf = vf or _find(ans["report"], "days_excluded") or {}
        figure = bool(ans["report"]["returns"].get("account_detail")) and ans["report"]["returns"]["account_detail"][0].get("value") is not None
        return {
            "window": ("%s: %s to %s (a ruled period at the latest landed day; the route has no default window. The longest window the code offers is SI, which holds "
                       "%d accounts with every row OK across all its partitions, so no control: this is the longest window with both kinds of account)" % (name, a, b, si_ctl))
                      if name != "SI" else "SI (Since Inception): 1970-01-01 to %s (the longest the code offers)" % b,
            "days_in_window": len(st), "partitions_in_window": parts, "non_ok_days": int(sum(1 for x in st if x != "OK")),
            "non_ok_status_values": sorted({x for x in st if x != "OK"}),
            "days_excluded": ans["report"]["returns"] and vf.get("days_excluded"),
            "days_observed": vf.get("days_observed"), "days_linked": vf.get("days_linked"),
            "claim": ans["claim"], "value_facts_claim": vf.get("claim"), "claim_basis": "measured (the reader's own return; a figure was returned)",
            "absences": [{"fact": x.get("fact"), "status": x.get("status")} for x in ans["absences"]],
            "excluded_rows_absence_text": next((x.get("reason") for x in ans["absences"] if x.get("fact") == "excluded_rows"), None),
            "answer_keys": sorted(ans.keys()), "report_keys": sorted(ans["report"].keys()), "refusals": ans["refusals"],
            "a_figure_was_returned": figure,
        }
    r_non = read(acct)
    r_ctl = read(ctl)
    chained = (r_non["a_figure_was_returned"] and r_non["days_linked"] is not None and r_non["days_excluded"] is not None
               and r_non["days_linked"] == r_non["days_observed"] - r_non["days_excluded"] and r_non["days_excluded"] >= 1)
    return {
        "arm": "READER_CODE_OVER_SERVED_GOLD",
        "arm_in_words": "NOT the deployed route. This is the route reader's OWN code at the base commit (holdings_gold.HoldingsGoldSource and holdings_gold.calculate, the source "
                        "composed by installed._holdings_source_for) run locally over the SERVED holdings gold read from S3 (get/list only; no Lambda invoked, no sign-in, "
                        "no call to the API). What could differ from the deployed function: the deployed package's bytes (the packaged copy, the dependencies, "
                        "the mapping loader), the route's authorization, scope resolution and response envelope (the scope here is built in memory, one permitted account), "
                        "and the ruled period set it offers a caller; the reader's answer dict is read, not the route's HTTP body.",
        "entry": "orion", "entry_basis": "the sources.json key whose monolith is orion (sources.json:66-68), the Inflection holdings entry; the route composes this firm's gold at installed.py:68 "
                 "(tenants._CANONICAL_INF). The 49 Financial entry's key carries an eight-digit master number and is not written here (the check refuses such a token); not read.",
        "reader_code_line": "infra/aws/lambda/investor-reporting/performance/holdings_gold.py:246 (non-OK rows dropped), :254 (the chain over the remaining rows), :314-317 (the PARTIAL excluded_rows absence)",
        "windows_tried": tried,
        "status_values_in_the_served_gold_all_partitions": dict(allstatus),
        "with_a_non_ok_day": r_non, "control_all_ok": r_ctl,
        "chained_over_the_non_ok_day": chained, "planted": False,
    }


def _find(o, key):
    if isinstance(o, dict):
        if key in o:
            return o
        for v in o.values():
            r = _find(v, key)
            if r:
                return r
    elif isinstance(o, list):
        for v in o:
            r = _find(v, key)
            if r:
                return r
    return None


def refresh_block(s3):
    bucket, key = pc.split_uri(pc.legacy_uri(cen.SPEC["legacy"]))
    vs, tok = [], {}
    while True:
        r = s3.list_object_versions(Bucket=bucket, Prefix=key, **tok)
        vs += [x for x in r.get("Versions", []) if x["Key"] == key]
        if r.get("IsTruncated"):
            tok = {"KeyMarker": r["NextKeyMarker"], "VersionIdMarker": r["NextVersionIdMarker"]}
        else:
            break
    hist = [x["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ") for x in vs[:30]]
    status = s3.get_bucket_versioning(Bucket=bucket).get("Status")
    return {
        "schedule_found": False,
        "writer": "data/cot/scripts/gold/build_canonical_prices_v2.py (silver-prep S_00 of the cot gold chain): upload_file at :907, output key from OUTPUT_KEY :174 "
                  "(_legacy_key of the same registry row), bucket :115 (BD_S3_BUCKET default). By the file's own header (:21, :30) and the dispatcher's chain table "
                  "(gold_dispatch.sh:78) it is the script that writes this object.",
        "schedule_or_trigger": "none found. The cot chain's daily anchor (schedule-et.tf:78-91, cron(30 7) America/New_York, then session -> bronze -> silver -> gold events, "
                               "eventbridge.tf:219-245) ends in the SSM document opal-cot-gold-run (ssm.tf:303-), whose run_gold list (ssm.tf:375-) never names "
                               "build_canonical_prices_v2.py / S_00; gold_dispatch.sh runs S_00 before its freshness gate only for `--chain full` (:1069-1083), and no cot "
                               "trigger of gold_dispatch.sh was found. The bd twin has a daily 04:00 UTC rule (bd-pipeline/eventbridge.tf:374-384) for ITS OWN object.",
        "searched": ["infra/aws/terraform/cot-pipeline (all .tf; search for build_canonical_prices, S_00, silver-prep, canonical_prices: 0 hits)",
                     "infra/aws/terraform/cot-pipeline/eventbridge.tf, schedule-et.tf, ssm.tf (read at the lines cited)",
                     "infra/aws (search gold_dispatch|gold-dispatch: 40 files shown, none under cot-pipeline or a cot EC2 dir; bd, inf and 49f dispatchers)",
                     "data/cot/scripts/gold/gold_dispatch.sh, gold_pipeline_deps.yaml, build_canonical_prices_v2.py (read)",
                     "data/mdpf/scripts/demque/land_cot.py (the lander of the writer's Tier 2 inputs, not a writer of this object)",
                     "comp-pipescript io on the writer: out of the curated graph (AST answer only, 9 call sites, 0 resolved)"],
        "last_modified_history": hist,
        "versions_kept": len(vs), "bucket_versioning": status,
        "history_note": "%d version(s) of the key are held; the bucket keeps versions (%s) but a lifecycle rule on non-current versions was not read, so the count is a floor, "
                        "not the write count" % (len(vs), status),
        "claim": "inferred",
    }


NOT_ESTABLISHED = [
    "whether the constant store/Close ratios (whole-number multiples or reciprocals) are the store holding a pre-split price while the reader's Close is split-adjusted: "
    "not tested against a split calendar",
    "the ticker-days whose constant ratio is not a whole number: their basis (unit, share class, a different security under the ticker) was not identified",
    "why the store's yahoo-labelled points end 2026-06-05 and every point ends 2026-06-09 although the object was last written 2026-10-09: the writer's inputs were not read for that run",
    "the tickers not in the store: whether they are other firms' securities or tickers the store spells differently (a ticker was matched by exact string)",
    "any write or run history of the writer outside the object's own retained versions (a lifecycle rule on non-current versions, an EC2 cron, a manual run log): not read; "
    "schedule_found false is an absence in the places searched",
    "the tickers with no reader bar: the reason (delisted, renamed, a ticker Yahoo does not carry) was not classified",
    "the deployed route's answer: only the reader's code over served data was run; the deployed package's bytes, authorization and envelope were not read",
    "a second account with a different non-OK status: the served gold of this entry holds two status tokens (OK, NON-POSITIVE-BASE) and the reader's filter (holdings_gold.py:246) "
    "is status-agnostic by code, not tested per token",
    "the other entry the route composes (49 Financial's): not read; its sources.json key carries an eight-digit master number that the order's check refuses in the outputs",
]


def main():
    scratch, out = sys.argv[1], sys.argv[2]
    m1 = measurement_1(scratch)
    m2 = measurement_2()
    s3 = boto3.client("s3", region_name="us-east-1")
    calls = json.load(open(Path(scratch) / "calls.json"))
    asked = [t for c in calls for t in c["ticker_list"]]
    so = m1["store_object"]
    doc = {
        "schema": "IB155-1 two measurements (IB-pr-459)", "to_id": "IRPT_BCKEND.TO-IB-pr-459", "assignee": "0.9.0_WK_IRPT_BCKEND~315", "base_commit": "9f5ecc2f80",
        "read_only": True, "counts_only": "no account id, balance or holding of an account; no security is named",
        "landed_prices_store": {
            "address_built_by": "data/assets/scripts/silver/commonwealth_price_basis_census.py:161 (pc.legacy_uri(SPEC['legacy'])), through "
                                "data/assets/scripts/analysis/commonwealth_price_census.py:282-286 -> lib/opal_naming.py:2339 legacy_address, "
                                "row infra/logic/registry/legacy_addresses.json:11",
            "address_resolved_by_the_builder": pc.legacy_uri(cen.SPEC["legacy"]),
            "last_modified_utc": so["last_modified_utc"], "rows": so["rows"], "columns": so["columns"], "content_length_mb": round(so["content_length"] / 1048576.0, 1),
            "how_a_point_is_labelled_yahoo": "column `source` == 'yahoo_finance' (YAHOO_LABEL, commonwealth_price_basis_census.py:78); the store's other labels and their row "
                                             "counts are in source_label_row_counts",
            "source_label_row_counts": so["source_label_row_counts"], "distinct_tickers_in_store": so["distinct_tickers_in_store"],
            "newest_day_any_label": so["store_newest_day_any_label"], "newest_yahoo_labelled_day": so["store_newest_yahoo_labelled_day"],
            "refresh": refresh_block(s3),
        },
        "tickers": {"asked": m1["tickers"]["asked"], "outcomes": m1["tickers"]["outcomes"], "with_a_bar_from_the_reader": m1["tickers"]["with_a_bar_from_the_reader"],
                    "outcome_definitions": m1["outcome_definitions"]},
        "ticker_days": m1["ticker_days"], "not_equal_by_cause": m1["not_equal_by_cause"], "store_coverage": m1["store_coverage"],
        "the_store_holds_the_unadjusted_close": m1["word"],
        "route_read": m2,
        "fetch": {"call_count": len(calls), "distinct_tickers_asked": len(set(asked)), "tickers_asked_more_than_once": len(asked) - len(set(asked)), "counted_before_fetching": True,
                  "source": "Yahoo Finance through fetch_yahoo (commonwealth_price_basis_census.py:200), driver ib150_fetch_yahoo.py of ~310 run unchanged; start 2026-01-30, "
                            "end exclusive 2026-10-14; 50 a call, 8 s pause, none parallel",
                  "calls": [{"tickers": c["tickers"], "with_bars": c["with_bars"], "rate_limited": c["rate_limited_not_read"]} for c in calls]},
        "not_established": NOT_ESTABLISHED,
        "aws_writes_made": 0, "sign_ins_made": 0, "functions_invoked": 0, "product_files_edited": 0, "builds_proposed": 0, "other_sources_asked": 0,
    }
    json.dump(doc, open(out, "w"), indent=1, default=str)
    print(json.dumps({"tickers": m1["tickers"]["outcomes"], "ticker_days": {k: v for k, v in m1["ticker_days"].items() if k != "equality_rule"}, "word": m1["word"],
                      "fetch": {k: v for k, v in doc["fetch"].items() if k != "calls"}, "versions": doc["landed_prices_store"]["refresh"]["last_modified_history"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
