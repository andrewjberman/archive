#!/usr/bin/env python3
"""IB-pr-468 (round 162): rebuild the 878-ticker list and write the demand-queue request file.  READ ONLY: S3 list/get through the earlier cells' own drivers;
NO price is fetched, NO vendor is called, no function is invoked, no sign-in, no AWS write.  Security identifiers only (symbol, cusip); the account column the
earlier phase-1 driver reads is already a one-way digest in the cache and nothing of it leaves the scratch folder.

Steps run (the earlier workers' drivers, unchanged, in their own folders; only the steps that derive the ticker list):
  1. ~308/ib433_fetch.py   <cache> 2026-06-09 2026-10-09   S3 list+get of the holdings (src) and anchor (anc) partitions, one per calendar day
  2. ~308/ib441_fetch_tx.py <tx.pkl>                         S3 list+get of every fact_transactions partition
  3. ~308/ib442_phase1.py  <cache> <phase1.pkl> <t442.json>  securities behind an OUTSIDE_ANCHOR row under the cash rule
  4. ~308/ib442_prepare.py <phase1.pkl> <tx.pkl> <prep.pkl> <t442b.json>   type of each; classes
  5. ~308/ib452_tickers.py <prep.pkl> <t452.json> <m452.json>              the 303 of IB-pr-452
  6. ~310/ib150_overlap_tickers.py <cache> <phase1> <prep> <tx> <t452> <tickers.json> <overlap.pkl> <meta.json>   the 878
Then this driver pairs each ticker with its cusip(s) from the same pickles and writes the request and the derivation record.

    python -I ib162_derive.py <scratch_dir> <base_commit> [--skip-fetch]
"""
import collections
import datetime as dt
import json
import os
import pickle
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
DELIV = HERE.parent
D308, D310 = DELIV / "0.9.0_WK_IRPT_BCKEND~308", DELIV / "0.9.0_WK_IRPT_BCKEND~310"
END_DAY, N_DAYS = "2026-10-09", 125
NINE_CLASSES = ("admitted_type", "left_out_type_inst", "left_out_type_ric_not_available")
CACHE_FIRST, CACHE_LAST = "2026-06-09", "2026-10-09"       # 85 graded days 2026-06-10..2026-10-09 each need their prior trading day


def run(label, folder, script, args, timeout):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-I", script] + [str(a) for a in args], cwd=str(folder), env=env, capture_output=True, text=True, timeout=timeout)
    tail = (r.stdout or "").strip().splitlines()[-3:]
    print("STEP", label, "rc", r.returncode, "|", " / ".join(t[:300] for t in tail), flush=True)
    if r.returncode:
        print((r.stderr or "")[-1500:])
        sys.exit(1)


def main():
    scratch, base = Path(sys.argv[1]), sys.argv[2]
    skip_fetch = "--skip-fetch" in sys.argv
    cache = scratch / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    p = {k: scratch / v for k, v in dict(tx="tx.pkl", p1="phase1.pkl", t442="t442.json", prep="prep.pkl", t442b="t442b.json", t452="tickers_452.json", m452="m452.json",
                                         t878="tickers.json", ov="overlap.pkl", m150="meta150.json").items()}
    if not skip_fetch:
        run("1 holdings+anchor partitions", D308, "ib433_fetch.py", [cache, CACHE_FIRST, CACHE_LAST], 1500)
        if not p["tx"].exists():
            run("2 transactions", D308, "ib441_fetch_tx.py", [p["tx"]], 900)
    run("3 phase1", D308, "ib442_phase1.py", [cache, p["p1"], p["t442"]], 1500)
    run("4 prepare", D308, "ib442_prepare.py", [p["p1"], p["tx"], p["prep"], p["t442b"]], 900)
    run("5 ib452 tickers", D308, "ib452_tickers.py", [p["prep"], p["t452"], p["m452"]], 300)
    run("6 overlap tickers", D310, "ib150_overlap_tickers.py", [cache, p["p1"], p["prep"], p["tx"], p["t452"], p["t878"], p["ov"], p["m150"]], 900)

    tickers = json.load(open(p["t878"], encoding="utf-8"))["tickers"]
    meta150 = json.load(open(p["m150"], encoding="utf-8"))
    B = pickle.load(open(p["prep"], "rb"))
    OV = pickle.load(open(p["ov"], "rb"))["overlap_nine"]
    P1 = pickle.load(open(p["p1"], "rb"))
    # cusip <-> symbol pairs exactly as the drivers formed them: ib442_prepare sec_ticker (ib442_prepare.py:81-82) for the nine classes (ib452_tickers.py:23-25),
    # and ib150_overlap_tickers.py:52-57 (overlap[c]["ticker"]) for the nine admitted pairs.
    pairs = set()
    for c, k in B["sec_cls"].items():
        if k in NINE_CLASSES and B["sec_ticker"][c]:
            pairs.add((c, B["sec_ticker"][c]))
    for c, v in OV.items():
        pairs.add((c, v["ticker"]))
    tset = set(tickers)
    pairs = {(c, t) for c, t in pairs if t in tset}
    cus_of, sym_of = collections.defaultdict(set), collections.defaultdict(set)
    for c, t in pairs:
        cus_of[t].add(c)
        sym_of[c].add(t)
    secs = []
    for t in sorted(tickers):
        cs = sorted(cus_of.get(t, ()))
        secs.append({"cusip": cs[0], "symbol": t} if cs else {"cusip_claim": "absent", "symbol": t})
    n_cus_multi_sym = sum(1 for c, s in sym_of.items() if len(s) > 1)
    n_sym_multi_cus = sum(1 for t, s in cus_of.items() if len(s) > 1)

    sys.path[:0] = [str(ROOT / "lib")]
    import trading_calendar as tc
    end = dt.date.fromisoformat(END_DAY)
    while not tc.is_trading_day(end):
        end -= dt.timedelta(days=1)
    start = end
    for _ in range(N_DAYS - 1):
        start = tc.prev_trading_day(start)
    n_td = len(tc.trading_days_between(start, end))

    src_n = sum(1 for f in cache.glob("src_*.pkl") if pickle.load(open(f, "rb")) is not None)
    anc_n = sum(1 for f in cache.glob("anc_*.pkl") if pickle.load(open(f, "rb")) is not None)
    T = pickle.load(open(p["tx"], "rb"))
    req = {"request_id": "IRPT_BCKEND-AS-TRADED-CLOSES-878", "standing": False, "tier": 2,
           "reason": "PRD v0.46 answer 1: the date-basis grading's second witness needs as-traded closes on landed bars; ruling CTO_RULING_DELL2_AS_TRADED_CLOSES_VIA_DEMQUE_20261012.md @479d6deba0",
           "page": "investor reporting (IRPT_BCKEND date-basis grading)", "vendor": "yahoo", "securities": secs, "fields": ["close"],
           "start": start.isoformat(), "end": end.isoformat(),
           "standing_enrolment": {"tier": 1, "in_words": "enrol the same 878 securities in the standing daily extension to the T-1 frontier after the history lands"},
           "filed_for": "IRPT_BCKEND", "requested_by": "2.0.0_SA_COO~P2",
           "authority": "1.0.0_SA_CTO~DELL2 msg 6362; 1.0.0_SA_CTO~DELL1 ruling @479d6deba0"}
    rec = {"base_commit": base, "tickers_derived": len(tickers), "with_a_cusip": sum(1 for s in secs if s.get("cusip")),
           "cusip_absent": sum(1 for s in secs if s.get("cusip_claim") == "absent"),
           "cusips_mapping_to_more_than_one_symbol": n_cus_multi_sym, "symbols_mapping_to_more_than_one_cusip": n_sym_multi_cus,
           "cusip_pair_in_words": "the pair is the one the drivers formed: ib442_prepare.py:81-82 sec_ticker[cusip] (most frequent ticker/symbol the holdings state that is not the cusip itself; "
                                  "built in ib442_phase1.py:97-99 from the Ticker and Symbol columns of rows whose CUSIP column is the security), restricted to the three nine-pair classes "
                                  "(ib452_tickers.py:23-25); plus ib150_overlap_tickers.py:52-57 overlap[cusip]['ticker'] for the nine admitted pairs.  Where a symbol has more than one "
                                  "cusip the request carries the lexicographically first and the count is stated.",
           "meta_of_the_overlap_step": meta150,
           "derivation_in_words": "Ran the earlier cells' own drivers unchanged, in their folders, each under its own timeout, with the cache outside the repo: "
                                  "(1) ~308/ib433_fetch.py over 2026-06-09..2026-10-09 (S3 list+get of holdings and anchor partitions; AccountID already a 12-character digest); "
                                  "(2) ~308/ib441_fetch_tx.py (every fact_transactions partition, de-duplicated on TransactionID); (3) ~308/ib442_phase1.py (graded days and securities behind OUTSIDE_ANCHOR under the cash rule); "
                                  "(4) ~308/ib442_prepare.py (type pair and class of each); (5) ~308/ib452_tickers.py (the 303 tickers of IB-pr-452); "
                                  "(6) ~310/ib150_overlap_tickers.py (the 303 plus the overlap securities of the nine pairs: the distinct tickers of IB-pr-454).  "
                                  "No fetch_yahoo / fetch_nav / ib441_fetch_yahoo step was run.  The driver then paired each ticker with its cusip and wrote the request.",
           "partitions_read": {"holdings_partitions_present": src_n, "anchor_partitions_present": anc_n, "calendar_days_asked": "%s..%s" % (CACHE_FIRST, CACHE_LAST),
                               "graded_days": len(P1["graded"]), "first_graded": P1["graded"][0], "last_graded": P1["graded"][-1],
                               "transactions_partitions": len(T["partitions"]), "transactions_objects": T["objects"], "transactions_rows_read": T["rows_read"],
                               "transactions_distinct_ids": len(T["rows"])},
           "start": start.isoformat(), "end": end.isoformat(), "trading_days_start_to_end_inclusive": n_td,
           "calendar_rule_in_words": "lib/trading_calendar.py: is_trading_day() to step end back to a trading day at or before 2026-10-09, prev_trading_day() 124 times for start, "
                                     "trading_days_between(start, end) (inclusive) to count; the module ran on its fallback NYSE holiday table (_USE_PMC False), not pandas_market_calendars.",
           "not_established": ["the window of calendar days the earlier cells fetched is read from their records (85 graded days 2026-06-10..2026-10-09, each needing its prior trading day), not from a stored command line",
                               "that Yahoo carries a bar for every one of the 878 symbols (the earlier pass found 871 with bars, 7 with none); nothing was asked of the vendor here",
                               "that the cusip chosen for a symbol with more than one cusip is the one the queue's quote should use",
                               "that the landed partitions are unchanged since the earlier cells read them (re-read live; the count is the test)",
                               "whether the as-traded close the queue lands equals the vendor's Close with later splits undone: the queue's own rule decides"],
           "prices_fetched": 0, "vendor_calls_made": 0, "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "accounts_written": 0, "values_written": 0}
    (HERE / "IRPT_BCKEND-AS-TRADED-CLOSES-878.json").write_text(json.dumps(req, indent=1, ensure_ascii=True) + "\n", encoding="utf-8")
    (HERE / "IB162-1_request_derivation.json").write_text(json.dumps(rec, indent=1, ensure_ascii=True) + "\n", encoding="utf-8")
    print("TICKERS", len(tickers), "distinct", len(tset), "with_cusip", rec["with_a_cusip"], "absent", rec["cusip_absent"], "cus>1sym", n_cus_multi_sym, "sym>1cus", n_sym_multi_cus,
          "start", start, "end", end, "td", n_td)


if __name__ == "__main__":
    main()
