"""n3_ac1_served_population.py -- HVST-n-3 AC1 (READ-ONLY): WHY THE SERVED CHATTER RANK HOLDS 2 ROWS.

WHAT IT DOES
  1. Reads CHATTER_AXIS_SOURCE from the deployed producer Lambda (GetFunctionConfiguration) and resolves
     it through the Lambda's OWN select_source (imported from its source file).
  2. Reads the served rankings route (read-only Invoke of opal-amgt-scoped-api): TRENDING and BREAKOUT x CHATTER,
     once with the route's own default date and once with as_of pinned to the as-of the TRENDING read served,
     printing as-of, requested as-of, generation id, state, row count.
  3. Runs the producer's OWN compute path (chatter_axis.compute_chatter_axis, count_fn =
     SOURCE_COUNT_FNS[<the deployed source>], write_fn=None so NOTHING is written) IN MEMORY at that as-of,
     and prints the population rule as a step-by-step count from the covered denominator down to the served
     rows, each dropping step named by file:line (line numbers looked up in the code at run time).
  4. Compares the in-memory rows with the served rows.
NOT MEASURABLE HERE: the rendered page (client side); a re-run of the 10:00Z scheduled fire itself (the
in-memory run reads the pool NOW; a difference from the served generation is printed, not hidden).
Writes only n3_ac1_result.json beside this script's parent folder.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _n3_common as C  # noqa: E402

from lib.research.coverage import pool_reader  # noqa: E402
from lib.research.metrics import chatter_axis as ca  # noqa: E402


def main():
    result = {}
    cfg, env = C.producer_config()
    lam_mod = C.load_lambda_module()
    source = lam_mod.select_source(env)
    print("PRODUCER: Lambda amgt-resapp-chatter-axis  LastModified=%s  CodeSha256=%s"
          % (cfg.get("LastModified"), cfg.get("CodeSha256")))
    print("CHATTER_AXIS_SOURCE = %r   (raw deployed env: %s)   select_source(env) -> %r   [%s]"
          % (env.get("CHATTER_AXIS_SOURCE"), json.dumps(env, sort_keys=True), source,
             C.loc(C.REL_LAMBDA, "def select_source(")))
    print("  Terraform pin: %s   (chatter_axis_source = \"legacy\")" % C.loc(C.REL_TF, "chatter_axis_source       ="))
    result["chatter_axis_source"] = source
    result["lambda"] = {"LastModified": cfg.get("LastModified"), "CodeSha256": cfg.get("CodeSha256"), "env": env}

    # ---------------------------------------------------------------- 1. the served route
    print("\nSERVED ROUTE: GET /api/scoped/amgt/lead-panel/rankings/{movement}/{subject}   handler branch %s ; "
          "function %s" % (C.loc(C.REL_ROUTE, 'rest[:2] == ["lead-panel", "rankings"]'),
                           C.loc(C.REL_ROUTE, "def read_rankings(")))
    served = {}
    for movement in ("trending", "breakout"):
        status, body = C.invoke_rankings(movement)
        served[movement] = body
        C.print_served("DEFAULT-DATE READ %s x CHATTER" % movement.upper(), status, body)
    as_of = served["trending"].get("as_of_date")
    print("\nAS-OF the TRENDING read served = %s (route's requested_as_of = %s, dated fallback = %s); "
          "pinning as_of=%s on both movements:"
          % (as_of, served["trending"].get("requested_as_of"), served["trending"].get("dated"), as_of))
    pinned = {}
    for movement in ("trending", "breakout"):
        status, body = C.invoke_rankings(movement, as_of=as_of)
        pinned[movement] = body
        C.print_served("PINNED as_of=%s READ %s x CHATTER" % (as_of, movement.upper()), status, body)
    result["served_default"] = {k: {kk: v.get(kk) for kk in ("axis", "as_of_date", "requested_as_of", "dated",
                                                            "ranking_status", "state", "generation_id", "row_count",
                                                            "coverage_vintage", "ranking_reason")}
                                for k, v in served.items()}
    result["served_pinned"] = {k: {kk: v.get(kk) for kk in ("axis", "as_of_date", "requested_as_of", "dated",
                                                           "ranking_status", "state", "generation_id", "row_count",
                                                           "coverage_vintage", "ranking_reason")}
                               for k, v in pinned.items()}
    result["served_rows_trending"] = [{k: r.get(k) for k in ("rank", "ticker", "security_key", "score",
                                                             "raw_chatter_count", "window_total_count")}
                                      for r in pinned["trending"].get("rows", [])]
    served_keys = [r["security_key"] for r in pinned["trending"].get("rows", [])]

    # ---------------------------------------------------------------- 2. the producer's own path, in memory
    pool_reader.clear_caches()
    summary = ca.compute_chatter_axis(as_of_date=as_of, count_fn=ca.SOURCE_COUNT_FNS[source], write_fn=None)
    universe = summary["universe"]
    detail = summary["read_detail"]
    totals = summary["window_totals"]
    win = summary["window"]
    n_considered = summary["tickers_considered"]
    with_links = sorted(k for k, d in detail.items() if d["store_item_count"] > 0)
    in_window = sorted(k for k, d in detail.items() if d["items_in_window"] > 0)
    signal = sorted(k for k in detail if totals.get(k, 0) > 0)
    trending = [p for p in summary["products"] if p["movement"] == "TRENDING"][0]
    breakout = [p for p in summary["products"] if p["movement"] == "BREAKOUT"][0]
    t_rows = [r for r in summary["rows"] if r["axis"] == trending["axis"]]
    b_rows = [r for r in summary["rows"] if r["axis"] == breakout["axis"]]
    states = summary["states"]

    print("\nPRODUCER'S OWN COMPUTE PATH, IN MEMORY (write_fn=None; source=%s; as_of=%s; window %s..%s = %d days)"
          % (source, summary["as_of_date"], win["start_date"], win["end_date"], win["window_days"]))
    print("  universe object: %s   read-failure states over the whole run: %s"
          % (universe["source"], json.dumps(states, sort_keys=True)))
    print("  crosswalk_status over %d reads: %s"
          % (len(detail), dict(collections.Counter(d["crosswalk_status"] for d in detail.values()))))

    print("\nPOPULATION RULE, STEP BY STEP (count remaining after each step; TRENDING and BREAKOUT shown separately "
          "where they diverge)")
    rows_out = []

    def step(n, name, remaining, dropped, where, why):
        rows_out.append({"step": n, "name": name, "remaining": remaining, "dropped": dropped, "where": where})
        print("  STEP %s  %-48s remaining=%-4s dropped=%-4s" % (n, name, remaining, dropped))
        print("           at %s" % where)
        print("           %s" % why)

    step(0, "universe object names (pool universe/v1)", universe["names_read"], 0,
         C.loc(C.REL_CHATTER, "def _read_pool_universe(") + " ; " + C.loc(C.REL_CHATTER, "names_read = len("),
         "the identity layer's union universe object %s (snapshot_date %s)" % (universe["source"],
                                                                                universe.get("snapshot_date")))
    step(1, "names carrying a canonical security_key = COVERED DENOMINATOR", n_considered,
         universe["names_read"] - n_considered,
         C.loc(C.REL_CHATTER, "if not identity:") + " (identity = security_key, union shape: "
         + C.loc(C.REL_CHATTER, "identity = security_key if union_shape") + ")",
         "a name with no security_key has nothing to query the store by and is not ranked "
         "(names_without_identifier=%s)" % universe.get("names_without_identifier"))
    step(2, "names with >=1 publication-links object in the pool, ANY date", len(with_links),
         n_considered - len(with_links),
         C.loc(C.REL_CHATTER, "result = pool_reader.window_read(") + " -> " + C.loc(C.REL_POOL, "links = list_links(")
         + " over " + C.loc(C.REL_POOL, "prefix = links_prefix(key_form)"),
         "legacy reads publication-links/v1/<alias>/ per identity (store_item_count); %d of %d identities have an empty "
         "store, so they can never score under legacy. Held: %s" % (n_considered - len(with_links), n_considered,
                                                                     ", ".join(with_links)))
    step(3, "names with >=1 article PUBLISHED inside the 30-day window", len(in_window),
         len(with_links) - len(in_window),
         C.loc(C.REL_POOL, "if day < start_date or day > end_date:"),
         "a link whose body `published` date is outside [%s, %s] is skipped, not counted; per-name "
         "store_item_count / items_in_window: %s"
         % (win["start_date"], win["end_date"],
            ", ".join("%s=%d/%d" % (k, detail[k]["store_item_count"], detail[k]["items_in_window"]) for k in with_links)))
    step(4, "names with window total > 0 (chatter signal test) = candidates of BOTH movements", len(signal),
         n_considered - len(signal),
         C.loc(C.REL_CHATTER, "no_signal_keys = sorted(") + " ; " + C.loc(C.REL_CHATTER, "signal_series = {"),
         "an all-zero 30-day series is dropped BEFORE either movement sees it (reason NO_SIGNAL_IN_WINDOW, "
         "excluded_no_signal=%d of candidates=%d); window totals: %s"
         % (trending["signal"]["excluded_no_signal"], trending["signal"]["candidates"],
            ", ".join("%s=%s" % (k, totals[k]) for k in signal)))
    t_cand = trending["candidates"]
    step("5-T", "TRENDING: movement_scores (score = as-of-day count)", t_cand, len(signal) - t_cand,
         C.loc(C.REL_MOVE, 'if movement == "TRENDING":'),
         "TRENDING scores every remaining name on the LAST day of the series (movement_gate.subject_level_score "
         "ABSOLUTE_COUNT_ON_AS_OF_DAY); it excludes nothing, and a name with a nonzero window but a zero as-of day "
         "is KEPT with score 0 (this is why BA and HD hold score 0)")
    step("6-T", "TRENDING: rank_top_n, TOP_N=10", len(t_rows), t_cand - len(t_rows),
         C.loc(C.REL_CHATTER, "top = ordered[:top_n]") + " ; TOP_N " + C.loc("lib/research/metrics/chatter_gate.py", "TOP_N = 10"),
         "no name dropped here: %d candidates < TOP_N 10; order = score desc, tie-break key asc "
         "(%s)" % (t_cand, C.loc(C.REL_CHATTER, "ordered = sorted(scores.keys()")))
    b_cand = breakout["candidates"]
    b_excl = collections.Counter(v for v in breakout["excluded"].values())
    step("5-B", "BREAKOUT: movement_scores / breakout_qualifies (min absolute jump 3.0)", b_cand,
         len(signal) - b_cand,
         C.loc(C.REL_MOVE, "if jump < float(floor):") + " ; floor " + C.loc(C.REL_MOVE, '"CHATTER": 3.0'),
         "a name qualifies only if as-of-day count minus trailing mean >= 3.0 articles; exclusion reasons over the run: %s"
         % json.dumps(dict(b_excl), sort_keys=True))
    step("6-B", "BREAKOUT: rows in the generation", len(b_rows), b_cand - len(b_rows),
         C.loc(C.REL_CHATTER, "STATE_COMPLETE if rows else STATE_EMPTY"),
         "zero rows -> the generation is committed EMPTY (state=%s, empty_reason=%s)"
         % (breakout["state"], json.dumps(breakout.get("empty_reason"), sort_keys=True)))
    step(7, "SERVED: read_rankings follows the _CURRENT pointer to the generation's rows",
         pinned["trending"].get("row_count"), 0,
         C.loc(C.REL_ROUTE, "read = read_generation_rows(axis, as_of_date, pointer)"),
         "the reader takes the generation whole (no filter, no re-sort); TRENDING served row_count=%s, BREAKOUT at the "
         "pinned as-of ranking_status=%s state=%s; at the route's own default date (%s) BREAKOUT is %s because "
         "the walk-back (%s) only accepts a COMPLETE pointer, and an EMPTY one is never promoted"
         % (pinned["trending"].get("row_count"), pinned["breakout"].get("ranking_status"),
            pinned["breakout"].get("state"), served["breakout"].get("requested_as_of"),
            served["breakout"].get("ranking_status"), C.loc(C.REL_ROUTE, "def _find_latest_served_pointer(")))

    # ---------------------------------------------------------------- 3. served vs in-memory
    mem_keys = [(r["security_key"] or r["ticker"]) for r in t_rows]
    print("\nIN-MEMORY TRENDING rows: %s" % [(r["rank"], r["ticker"], r["security_key"], r["score"], r["window_total_count"])
                                              for r in t_rows])
    print("SERVED    TRENDING rows: %s" % [(r["rank"], r["ticker"], r["security_key"], r["score"],
                                              r["window_total_count"]) for r in pinned["trending"].get("rows", [])])
    same = mem_keys == served_keys
    print("IN-MEMORY == SERVED (same keys, same order): %s   (in-memory %d rows, served %d rows)"
          % (same, len(mem_keys), len(served_keys)))
    print("IN-MEMORY BREAKOUT rows: %d state=%s   SERVED BREAKOUT (pinned) row_count=%s state=%s"
          % (len(b_rows), breakout["state"], pinned["breakout"].get("row_count"), pinned["breakout"].get("state")))

    # ---------------------------------------------------------------- 4. what the store holds, for the 3 names
    print("\nWHAT THE LEGACY STORE HOLDS FOR THE %d NAMES WITH LINKS (window_read over 2000-01-01..%s, read-only):"
          % (len(with_links), win["end_date"]))
    held = {}
    for key in with_links:
        r = pool_reader.window_read(key, "2000-01-01", win["end_date"])
        days = sorted(r["counts"])
        held[key] = {"links": r["store_item_count"], "published_days": days, "states": r["states"]}
        print("  %-14s links=%d published_days=%s states=%s" % (key, r["store_item_count"], days, json.dumps(r["states"])))

    print("\nANSWER: under CHATTER_AXIS_SOURCE=%s the ranked population is the set of the %d covered names whose "
          "pool store holds >=1 article PUBLISHED in the trailing 30 days; that set is %d (%s) out of %d, "
          "because only %d of %d identities have any publication-links object at all. TRENDING ranks them all "
          "(2 < TOP_N 10); BREAKOUT drops both at the 3.0 absolute-jump floor and commits EMPTY."
          % (source, n_considered, len(signal), ", ".join(signal), n_considered, len(with_links), n_considered))
    print("DENOMINATORS: names_read=%d  covered=%d  with_links=%d  in_window=%d  signal=%d  trending_rows=%d  "
          "breakout_rows=%d  served_trending_rows=%s" % (universe["names_read"], n_considered, len(with_links),
                                                         len(in_window), len(signal), len(t_rows), len(b_rows),
                                                         pinned["trending"].get("row_count")))

    result.update({"as_of": as_of, "window": win, "steps": rows_out, "in_memory_equals_served": same,
                   "with_links": with_links, "in_window": in_window, "signal": signal, "held_dates": held,
                   "read_states": states, "universe": {k: universe.get(k) for k in
                                                       ("source", "names_read", "names_considered",
                                                        "names_without_identifier", "snapshot_date")}})
    with open(os.path.join(C.OUT_DIR, "n3_ac1_result.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=2, sort_keys=True, default=str)
    print("\nwrote n3_ac1_result.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
