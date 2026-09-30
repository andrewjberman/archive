"""n3_ac2_legacy_vs_gold.py -- HVST-n-3 AC2 (READ-ONLY): THE `gold` RANK'S EXPECTED DIFF AGAINST `legacy`.

WHAT IT DOES (no env change, no S3/DynamoDB write, no vendor call)
  The producer's OWN compute path, chatter_axis.compute_chatter_axis(as_of, count_fn=..., write_fn=None), is run
  IN MEMORY on the SAME as-of and the SAME 30-day window three ways:
    LEGACY        count_fn = SOURCE_COUNT_FNS["legacy"]  (what is deployed: CHATTER_AXIS_SOURCE=legacy)
    GOLD-AS-RUN   count_fn = SOURCE_COUNT_FNS["gold"]    (the gold branch exactly as the producer runs it,
                  including its incomplete-input HOLD: chatter_axis.py `gold_input` / `unresolved` / `failure_reason`)
    GOLD-NO-HOLD  count_fn = a pass-through wrapper of gold_daily_mention_scores. Because compute_chatter_axis
                  tests `count_fn is gold_daily_mention_scores`, the wrapper takes the ordinary branch: the SAME
                  producer code ranks the SAME gold scores with the HOLD guard not engaged. This is a COUNTERFACTUAL
                  (what the gold numbers would rank to if the guard were absent), labelled as such -- it is NOT
                  what a flip publishes.
  A pass-through recorder keeps the per-day series each count function returned, so the FULL ordered list beyond
  TOP_N can be printed with the producer's own dense_series / movement_scores / normalize_scores / rank_top_n
  (and is asserted equal to the producer's own top-10 rows).
  Then: side-by-side lists with row counts, every company whose rank moves (old and new rank), and the
  passing-mention test.
NOT MEASURABLE HERE: the rendered page; the served result of a real flip (no write is permitted).
Writes only n3_ac2_result.json beside this script's parent folder.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _n3_common as C  # noqa: E402

from lib.research.coverage import pool_reader  # noqa: E402
from lib.research.harvest.publication_gold import GOLD_DAILY_TABLE  # noqa: E402
from lib.research.metrics import chatter_axis as ca  # noqa: E402
from lib.research.metrics import movement_gate as mg  # noqa: E402


def recorder(fn, sink):
    def wrapped(identity, start_date, end_date):
        out = fn(identity, start_date, end_date)
        sink[identity] = dict(out)
        return out
    return wrapped


def full_order(daily, identities, as_of, movement, identity_index):
    """The producer's own ordering over EVERY scored name (no TOP_N cut), from the recorded series."""
    dates = ca.window_dates(as_of, ca.WINDOW_DAYS)
    series = {k: ca.dense_series(daily.get(k, {}), dates) for k in identities}
    totals = {k: sum(v) for k, v in series.items()}
    signal_series = {k: v for k, v in series.items() if totals[k] != 0}
    raw, excluded = mg.movement_scores(signal_series, movement, ca.SUBJECT)
    normalized = ca.normalize_scores(raw, ca.SCORE_MIN, ca.SCORE_MAX)
    as_of_counts = {k: v[-1] for k, v in series.items()}
    ordered = ca.rank_top_n(normalized, as_of_counts, top_n=max(len(normalized), 1))
    for entry in ordered:
        entry["display"] = (identity_index.get(entry["ticker"]) or {}).get("ticker") or entry["ticker"]
        entry["window_total"] = totals[entry["ticker"]]
    return ordered, excluded, totals, as_of_counts


def fmt(x):
    return "-" if x is None else ("%g" % x if isinstance(x, float) else str(x))


def main():
    result = {}
    cfg, env = C.producer_config()
    print("DEPLOYED: amgt-resapp-chatter-axis CHATTER_AXIS_SOURCE=%r (unchanged by this cell)  LastModified=%s"
          % (env.get("CHATTER_AXIS_SOURCE"), cfg.get("LastModified")))
    status, trend_body = C.invoke_rankings("trending")
    as_of = trend_body.get("as_of_date")
    C.print_served("SERVED TRENDING (route default date)", status, trend_body)
    status_b, break_body = C.invoke_rankings("breakout", as_of=as_of)
    C.print_served("SERVED BREAKOUT (pinned as_of=%s)" % as_of, status_b, break_body)
    served_rank = {r["security_key"]: r["rank"] for r in trend_body.get("rows", [])}

    runs = {}
    daily = {}
    for label, count_fn in (
        ("LEGACY", ca.SOURCE_COUNT_FNS["legacy"]),
        ("GOLD-AS-RUN", ca.SOURCE_COUNT_FNS["gold"]),
        ("GOLD-NO-HOLD", ca.gold_daily_mention_scores),
    ):
        pool_reader.clear_caches()
        sink = {}
        fn = count_fn
        if label != "GOLD-AS-RUN":
            fn = recorder(count_fn, sink)
        summary = ca.compute_chatter_axis(as_of_date=as_of, count_fn=fn, write_fn=None)
        runs[label] = summary
        daily[label] = sink

    base = runs["LEGACY"]
    universe = base["universe"]
    win = base["window"]
    identities = [e["identity"] for e in ca.read_universe_names(as_of=as_of)[0]]
    identity_index = {e["identity"]: e for e in ca.read_universe_names(as_of=as_of)[0]}
    print("\nSAME WINDOW AND AS-OF FOR ALL THREE RUNS: as_of=%s window=%s..%s (%d days); universe=%s; covered names=%d "
          "(names_read=%d); write_fn=None (nothing written)"
          % (as_of, win["start_date"], win["end_date"], win["window_days"], universe["source"],
             base["tickers_considered"], universe["names_read"]))
    for label, s in runs.items():
        assert s["window"] == win and s["as_of_date"] == as_of and s["tickers_considered"] == len(identities)
    gold = runs["GOLD-AS-RUN"]
    cov = gold.get("input_coverage") or {}
    print("\nPRODUCT STATES (rows_ranked / state / reason):")
    for label, s in runs.items():
        for p in s["products"]:
            print("  %-13s %-17s rows=%-2d state=%-7s reason_code=%s candidates=%d excluded=%s  %s"
                  % (label, p["axis"], p["rows_ranked"], p["state"], p["reason_code"], p["candidates"],
                     json.dumps(dict(collections.Counter(p["excluded"].values())), sort_keys=True),
                     p.get("failure_reason") or ""))
    print("  GOLD-AS-RUN input_coverage: RESOLVED %s of %s %s (%s days each); unresolved names: %d; "
          "read-state totals over the run: %s"
          % (cov.get("resolved"), cov.get("required"), cov.get("unit"), cov.get("window_days"),
             len(cov.get("unresolved", [])), json.dumps(gold["states"], sort_keys=True)))
    state_shapes = collections.Counter(json.dumps(d["states"], sort_keys=True) for d in gold["read_detail"].values())
    print("  GOLD-AS-RUN per-name read-state shapes (%d names): %s" % (len(gold["read_detail"]), dict(state_shapes)))
    print("  guard code: %s ; %s"
          % (C.loc(C.REL_CHATTER, "unresolved = [key for key in identities"),
             C.loc(C.REL_CHATTER, "raw_scores = {}")))
    print("  => under the producer's own gold branch NEITHER movement publishes: FAILED / INCOMPLETE_GOLD_INPUT, zero "
          "rows, no pointer for the date (a _FAILED marker only); by CODE READING (not exercised: no write is permitted) "
          "the reader then serves the nearest earlier COMPLETE generation, dated (%s, lookback %s days)."
          % (C.loc(C.REL_ROUTE, "def _find_latest_served_pointer("),
             __import__("lib.research.api.scoped_amgt", fromlist=["x"])._DATED_FALLBACK_LOOKBACK_DAYS))

    result["as_of"] = as_of
    result["window"] = win
    result["products"] = {label: [{k: p.get(k) for k in ("axis", "rows_ranked", "state", "reason_code", "candidates",
                                                        "failure_reason")} for p in s["products"]]
                          for label, s in runs.items()}
    result["gold_input_coverage"] = {k: cov.get(k) for k in ("resolved", "required", "unit", "window_days")}

    # ---- full ordered lists (producer's own functions) ------------------------------------------
    orders = {}
    for label in ("LEGACY", "GOLD-NO-HOLD"):
        for movement in ("TRENDING", "BREAKOUT"):
            ordered, excluded, totals, as_of_counts = full_order(daily[label], identities, as_of, movement,
                                                                 identity_index)
            prod_rows = [r for r in runs[label]["rows"] if r["axis"] == "%s_CHATTER" % movement]
            got = [e["ticker"] for e in ordered[:ca.TOP_N]] if movement == "TRENDING" or prod_rows else []
            want = [(identity_index_key(r, identity_index)) for r in prod_rows]
            same = got[:len(want)] == want
            print("  CHECK %s %s: full-order top-%d equals the producer's own rows: %s (%d rows)"
                  % (label, movement, len(want), same, len(want)))
            assert same, (label, movement, got, want)
            orders[(label, movement)] = (ordered, excluded, totals, as_of_counts)

    # ---- side by side ---------------------------------------------------------------------------
    print("\n=== SIDE BY SIDE: TRENDING x CHATTER (score = as-of-day value; TOP_N=%d rows are what would be written) ==="
          % ca.TOP_N)
    leg_ord = orders[("LEGACY", "TRENDING")][0]
    gnh_ord = orders[("GOLD-NO-HOLD", "TRENDING")][0]
    leg_rows = {e["ticker"]: e["rank"] for e in leg_ord[:ca.TOP_N]}
    gnh_rows = {e["ticker"]: e["rank"] for e in gnh_ord[:ca.TOP_N]}
    print("  row counts written: SERVED-legacy=%d  LEGACY(in memory)=%d  GOLD-AS-RUN=%d  GOLD-NO-HOLD(counterfactual)=%d"
          % (len(served_rank), len(leg_rows), sum(p["rows_ranked"] for p in gold["products"] if p["movement"] == "TRENDING"),
             len(gnh_rows)))
    print("  %-4s | %-34s | %-14s | %-58s" % ("rank", "LEGACY (key score window_articles)", "GOLD-AS-RUN",
                                            "GOLD-NO-HOLD (key score window_mention_score)"))
    for i in range(max(len(leg_ord[:ca.TOP_N]), len(gnh_ord[:ca.TOP_N]), 1)):
        lg = leg_ord[i] if i < len(leg_ord[:ca.TOP_N]) else None
        g = gnh_ord[i] if i < len(gnh_ord[:ca.TOP_N]) else None
        print("  %-4d | %-34s | %-14s | %-58s" % (
            i + 1,
            ("%s %.1f %s" % (lg["ticker"], lg["score"], fmt(lg["window_total"]))) if lg else "-",
            "(no rows: HOLD)",
            ("%s %.1f %s" % (g["ticker"], g["score"], fmt(round(g["window_total"], 4)))) if g else "-"))

    print("\n=== SIDE BY SIDE: BREAKOUT x CHATTER ===")
    for label in ("LEGACY", "GOLD-AS-RUN", "GOLD-NO-HOLD"):
        p = [p for p in runs[label]["products"] if p["movement"] == "BREAKOUT"][0]
        print("  %-13s rows=%d state=%s candidates=%d excluded=%s empty_reason=%s"
              % (label, p["rows_ranked"], p["state"], p["candidates"],
                 json.dumps(dict(collections.Counter(p["excluded"].values())), sort_keys=True),
                 json.dumps(p.get("empty_reason"), sort_keys=True)))
    print("  SERVED BREAKOUT at as_of=%s: ranking_status=%s state=%s row_count=%s"
          % (as_of, break_body.get("ranking_status"), break_body.get("state"), break_body.get("row_count")))

    # ---- every rank move --------------------------------------------------------------------------
    print("\n=== EVERY COMPANY WHOSE RANK MOVES (TRENDING x CHATTER) ===")
    print("  old = LEGACY rank in the written top-%d (- = not in the list); new-as-run = GOLD-AS-RUN (HOLD: no list);"
          % ca.TOP_N)
    print("  new-no-hold = GOLD-NO-HOLD written top-%d rank, with the full-order position in [] where beyond TOP_N."
          % ca.TOP_N)
    gnh_full = {e["ticker"]: e["rank"] for e in gnh_ord}
    leg_full = {e["ticker"]: e["rank"] for e in leg_ord}
    keys = sorted(set(leg_rows) | set(gnh_rows) | set(leg_full) , key=lambda k: (leg_rows.get(k, 99), gnh_rows.get(k, 99), k))
    print("  %-16s %-8s %-10s %-22s %s" % ("company", "old", "new-as-run", "new-no-hold", "moved"))
    move_records = []
    for k in keys:
        old = leg_rows.get(k)
        new_nh = gnh_rows.get(k)
        nh_txt = fmt(new_nh) if new_nh else ("-[%s]" % gnh_full[k] if k in gnh_full else "-")
        moved = (old != new_nh)
        rec = {"security_key": k, "old_rank": old, "new_rank_as_run": None, "new_rank_no_hold": new_nh,
               "new_full_position_no_hold": gnh_full.get(k), "moved": moved}
        move_records.append(rec)
        print("  %-16s %-8s %-10s %-22s %s" % (k, fmt(old), "-(HOLD)", nh_txt, "MOVES" if moved else "same"))
    print("  gold-no-hold top-%d members not in legacy: %s" % (ca.TOP_N, sorted(set(gnh_rows) - set(leg_rows))))
    print("  legacy members not in gold-no-hold top-%d: %s (full-order position under gold-no-hold: %s)"
          % (ca.TOP_N, sorted(set(leg_rows) - set(gnh_rows)),
             {k: gnh_full.get(k) for k in sorted(set(leg_rows) - set(gnh_rows))}))
    result["rank_moves"] = move_records

    # ---- what the as-of-day measure looks like -----------------------------------------------------
    leg_asof = orders[("LEGACY", "TRENDING")][3]
    gnh_asof = orders[("GOLD-NO-HOLD", "TRENDING")][3]
    n_leg_asof = sum(1 for v in leg_asof.values() if v > 0)
    n_gold_asof = sum(1 for v in gnh_asof.values() if v > 0)
    print("\nAS-OF-DAY MEASURE (TRENDING's score): names with an as-of-day value > 0 -> LEGACY %d of %d, GOLD %d of %d. "
          "Where that is 0 the TRENDING order is decided by the key tie-break alone (chatter_axis.py:%s), under EITHER source."
          % (n_leg_asof, len(identities), n_gold_asof, len(identities), line_no("ordered = sorted(scores.keys()")))
    rows = pool_reader._gold_latest_snapshot_rows(GOLD_DAILY_TABLE)
    on_day = [r for r in rows if str(r.get("day")) == as_of]
    print("  gold chatter_daily on %s: %d rows; data_status %s; max day in the table %s"
          % (as_of, len(on_day), dict(collections.Counter(r.get("data_status") for r in on_day)),
             max(str(r.get("day")) for r in rows)))
    result["as_of_day_positive"] = {"legacy": n_leg_asof, "gold": n_gold_asof}

    # ---- passing-mention test -------------------------------------------------------------------------
    leg_tot = orders[("LEGACY", "TRENDING")][2]
    gld_tot = orders[("GOLD-NO-HOLD", "TRENDING")][2]
    named = sorted(k for k in identities if leg_tot.get(k, 0) > 0)
    scored = sorted(k for k in identities if gld_tot.get(k, 0) > 0)
    print("\n=== PASSING-MENTION TEST ===")
    print("  Rule: company X 'outranks a subject company' under LEGACY when its legacy 30-day article count is strictly "
          "greater than company Y's, and it does NOT outrank Y under GOLD when Y's graded 30-day mention_score is "
          "strictly greater than X's. X is listed with every such Y. Measure = the 30-day window total of each source "
          "(the as-of-day measure is all-zero under both sources, see above, so it cannot separate anyone).")
    print("  denominators: %d covered names; %d named by LEGACY (window article count > 0); %d with a GOLD window "
          "score > 0; the test compares each legacy-named X against all %d covered names." %
          (len(identities), len(named), len(scored), len(identities)))
    tier = {}
    for r in rows:
        k = r.get("security_key")
        if k in set(named) | set(scored) and str(r.get("day")) >= win["start_date"] and str(r.get("day")) <= win["end_date"]:
            t = tier.setdefault(k, {"A": 0, "B": 0, "C": 0, "D": 0, "articles": 0, "mentions": 0})
            for x in "abcd":
                t[x.upper()] += r.get("tier_" + x) or 0
            t["articles"] += r.get("articles_total") or 0
            t["mentions"] += r.get("mention_count_total") or 0
    listed = []
    for x in named:
        ys = sorted((y for y in identities if leg_tot.get(x, 0) > leg_tot.get(y, 0) and gld_tot.get(y, 0) > gld_tot.get(x, 0)),
                    key=lambda y: (-gld_tot.get(y, 0), y))
        t = tier.get(x, {})
        print("  X=%-14s legacy_articles=%s gold_score=%s gold_tiers(A/B/C/D)=%s articles=%s mentions=%s -> outranks %d "
              "company(ies) under legacy that outrank it under gold%s"
              % (x, leg_tot[x], fmt(round(gld_tot.get(x, 0), 4)),
                 "/".join(str(t.get(z, 0)) for z in "ABCD") if t else "n/a", t.get("articles", "n/a"),
                 t.get("mentions", "n/a"), len(ys),
                 (": " + ", ".join("%s(%s)" % (y, fmt(round(gld_tot[y], 4))) for y in ys)) if ys else ""))
        if ys:
            listed.append({"security_key": x, "legacy_articles": leg_tot[x], "gold_score": round(gld_tot.get(x, 0), 4),
                           "outranked_under_gold_by": [{"security_key": y, "gold_score": round(gld_tot[y], 4)} for y in ys]})
    print("  => PASSING-MENTION LIST (named by legacy, outranks subject companies under legacy but not under gold): %s"
          % ([e["security_key"] for e in listed] or "EMPTY"))
    not_listed = [x for x in named if x not in {e["security_key"] for e in listed}]
    print("  => named by legacy and NOT listed: %s" % not_listed)
    print("  rank of each legacy-named company by GOLD window score (competition rank over %d scored names): %s"
          % (len(scored), {x: 1 + sum(1 for y in scored if gld_tot[y] > gld_tot.get(x, 0)) for x in named}))
    print("  NOTE the legacy list cannot show the effect on its own: it names %d companies, so TOP_N=10 has no one to "
          "displace; the effect appears only against the %d companies gold scores that legacy never names."
          % (len(named), len(set(scored) - set(named))))
    result["passing_mention"] = listed
    result["denominators"] = {"covered": len(identities), "legacy_named": len(named), "gold_scored": len(scored)}

    print("\nDENOMINATORS: covered=%d legacy_signal=%d gold_signal=%d legacy_rows(T/B)=%d/%d gold_as_run_rows=0 "
          "gold_no_hold_rows(T/B)=%d/%d served_trending_rows=%d"
          % (len(identities), len(named), len(scored), len(leg_rows),
             sum(1 for r in runs["LEGACY"]["rows"] if r["axis"] == "BREAKOUT_CHATTER"), len(gnh_rows),
             sum(1 for r in runs["GOLD-NO-HOLD"]["rows"] if r["axis"] == "BREAKOUT_CHATTER"), len(served_rank)))
    with open(os.path.join(C.OUT_DIR, "n3_ac2_result.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=2, sort_keys=True, default=str)
    print("\nwrote n3_ac2_result.json")
    return 0


def identity_index_key(row, identity_index):
    for k, e in identity_index.items():
        if (e.get("ticker") or k) == row["ticker"] or k == row.get("security_key"):
            return k
    return row["ticker"]


def line_no(needle):
    return C.line_of(C.REL_CHATTER, needle)


if __name__ == "__main__":
    raise SystemExit(main())
