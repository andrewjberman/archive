"""m2_ac2_fwd7_rank.py -- HVST-m-2 AC2: FWD-7 re-grade from the served store (READ-ONLY, MEASURES, GRADES NOTHING).

WHAT IT MEASURES
  1. THE PAGE'S CHATTER RANK AS SERVED. The page reads the scoped API route
        GET /api/scoped/amgt/lead-panel/rankings/{movement}/{subject}
     (lib/research/api/scoped_amgt.py: handler -> read_rankings; line numbers looked up and printed below), which
     serves the committed generation of the DynamoDB table `opal-harvest-security-metrics` written by the Lambda
     `amgt-resapp-chatter-axis` (lib/research/metrics/chatter_axis.py: compute_chatter_axis; the source is chosen by
     the env var CHATTER_AXIS_SOURCE read in infra/aws/terraform/harvest/lambda_src/lambda_function.py select_source).
     WHY THIS ROUTE: it is the only path from the ranking producer to the page; `amgt-resapp-chatter-axis` itself
     has no read route (it is a scheduled writer), so its OUTPUT is read through the API route. The route is invoked
     read-only (a GET event, opal-amgt-scoped-api, lead-panel/rankings, TRENDING and BREAKOUT x CHATTER) and the
     Lambda's CHATTER_AXIS_SOURCE is read with GetFunctionConfiguration. Nothing is written.
  2. THE INPUT that rank is computed from, read from CHATTER_AXIS_SOURCE and chatter_axis.SOURCE_COUNT_FNS:
        legacy -> default_daily_article_counts (raw article counts per day from the pool publication links)
        gold   -> gold_daily_mention_scores    (graded chatter_daily mention_score per day)
  3. AN INDEPENDENT RECOMPUTE from the served graded gold `chatter_daily` newest part (key printed), over the same
     30-day window ending on the served as_of_date (window = as_of - 29 days .. as_of, chatter_gate.WINDOW_DAYS = 30):
        graded  TRENDING measure = mention_score ON the as-of day (movement_gate ABSOLUTE_COUNT_ON_AS_OF_DAY);
                                   names with a zero window total are dropped first (chatter_axis no-signal rule);
                                   ordered by score descending, ties broken by security_key ascending.
        graded  WINDOW measure   = sum of mention_score over the 30 days (printed beside it because the as-of day
                                   alone can be all-zero).
        raw     WINDOW measure   = sum of mention_count_total (names, not strength) over the same 30 days.
     A RANK POSITION = 1 + the number of companies with a strictly greater value (competition ranking, ties share the
     best position), over the companies with a non-zero window total on that measure.
  4. RANK CORRELATION: Spearman rho (average ranks), own implementation, with n printed. Printed for
        (i)  served rank vs the recomputed graded rank, over the companies on BOTH lists;
        (ii) raw-count window rank vs graded window rank, over all companies with signal.
     A correlation over fewer than 3 companies is printed as NOT MEASURABLE HERE with n, never estimated.
  5. PASSING-MENTION TEST: every company whose raw-count window rank is better (numerically lower) than its graded
     window rank by 5 or more places (graded_rank - raw_rank >= 5), listed with both ranks, raw count, graded score
     and tier split; the same test on the as-of-day measure is printed too.
  6. CONSISTENCY: chatter_daily's window mention_score per company recomputed from the newest article_security_mention
     part's pairs (sum of signal_weight by published day) against the chatter_daily figure -- a line of agreement.

NOT MEASURABLE HERE: the RENDERED page (client-side; the portal is not fetched), the DynamoDB table by direct call
(the route is used instead), any state the API does not serve.
Reads only. Writes only m2_ac2_* files beside this script's parent folder.
"""
import collections
import datetime
import io
import json
import math
import os
import re
import sys

import boto3
import pyarrow.parquet as pq

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * 8)))
sys.path.insert(0, REPO)

import lib.research.harvest.store as store  # noqa: E402

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BUCKET = store.HARVEST_BUCKET
WINDOW_DAYS = 30
s3 = boto3.client("s3", region_name="us-east-1")
lam = boto3.client("lambda", region_name="us-east-1")


def newest_part(table):
    prefix = store.table_prefix("amgt", "gold", table)
    keys = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            if obj["Key"].endswith(".parquet"):
                keys.append(obj["Key"])
    date_of = lambda k: re.search(r"date=(\d{4}-\d{2}-\d{2})", k).group(1)  # noqa: E731
    keys.sort(key=lambda k: (date_of(k), k))
    return keys[-1], len(keys)


def read_rows(key):
    return pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())).to_pylist()


def line_of(relpath, needle):
    with open(os.path.join(REPO, relpath), "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            if needle in line:
                return i
    return None


def positions(values):
    """{key: 1 + count of keys with a strictly greater value} (competition ranking)."""
    vs = list(values.values())
    return {k: 1 + sum(1 for v in vs if v > val) for k, val in values.items()}


def avg_ranks(values):
    """{key: average rank}, rank 1 = largest; ties share the mean of the positions they span."""
    order = sorted(values, key=lambda k: (-values[k], k))
    out = {}
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        mean = (i + 1 + j + 1) / 2.0
        for t in range(i, j + 1):
            out[order[t]] = mean
        i = j + 1
    return out


def spearman(a, b):
    """Spearman rho of two {key: value} maps over their common keys; returns (rho, n) or (None, n)."""
    common = sorted(set(a) & set(b))
    n = len(common)
    if n < 3:
        return None, n
    ra = avg_ranks({k: a[k] for k in common})
    rb = avg_ranks({k: b[k] for k in common})
    ma = sum(ra.values()) / n
    mb = sum(rb.values()) / n
    cov = sum((ra[k] - ma) * (rb[k] - mb) for k in common)
    va = math.sqrt(sum((ra[k] - ma) ** 2 for k in common))
    vb = math.sqrt(sum((rb[k] - mb) ** 2 for k in common))
    if va == 0 or vb == 0:
        return None, n
    return cov / (va * vb), n


def invoke_rankings(movement):
    path = "/api/scoped/amgt/lead-panel/rankings/%s/chatter" % movement
    event = {"rawPath": path, "headers": {"x-firm-id": "m2-readonly-probe"},
             "requestContext": {"http": {"method": "GET", "path": path}}}
    resp = lam.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(event).encode())
    out = json.loads(resp["Payload"].read())
    return out.get("statusCode"), json.loads(out["body"])


def fmt_rho(rho, n):
    if rho is None:
        return "NOT MEASURABLE HERE (n=%d companies in common; fewer than 3, or one side has no spread)" % n
    return "%.4f (n=%d)" % (rho, n)


def main():
    result = {}
    # ---- 1/2. served rank + source ------------------------------------------------------------
    cfg = lam.get_function_configuration(FunctionName="amgt-resapp-chatter-axis")
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    source = env.get("CHATTER_AXIS_SOURCE")
    print("SERVED-RANK PRODUCER: Lambda amgt-resapp-chatter-axis  LastModified=%s  CodeSha256=%s"
          % (cfg.get("LastModified"), cfg.get("CodeSha256")))
    print("CHATTER_AXIS_SOURCE = %r   (raw env: %s)" % (source, json.dumps(env, sort_keys=True)))
    rel = {
        "route_table": "lib/research/api/scoped_amgt.py",
        "chatter": "lib/research/metrics/chatter_axis.py",
        "lam": "infra/aws/terraform/harvest/lambda_src/lambda_function.py",
    }
    print("ROUTE READ BY THE PAGE: GET /api/scoped/amgt/lead-panel/rankings/{movement}/{subject}")
    print("  handler branch  %s:%s  (rest[:2] == ['lead-panel','rankings'])"
          % (rel["route_table"], line_of(rel["route_table"], 'rest[:2] == ["lead-panel", "rankings"]')))
    print("  function        %s:%s  read_rankings(movement, subject, as_of_date, limit) -> pointer + generation rows"
          % (rel["route_table"], line_of(rel["route_table"], "def read_rankings(")))
    print("  producer        %s:%s  compute_chatter_axis(count_fn=SOURCE_COUNT_FNS[source])"
          % (rel["chatter"], line_of(rel["chatter"], "def compute_chatter_axis(")))
    print("  source map      %s:%s  SOURCE_COUNT_FNS = {legacy: default_daily_article_counts, gold: gold_daily_mention_scores}"
          % (rel["chatter"], line_of(rel["chatter"], "SOURCE_COUNT_FNS = {")))
    print("  env selection   %s:%s  select_source() reads CHATTER_AXIS_SOURCE (unset/empty -> legacy)"
          % (rel["lam"], line_of(rel["lam"], "def select_source(")))
    inp = {"legacy": "RAW ARTICLE COUNTS per day (pool publication links; default_daily_article_counts)",
           "gold": "GRADED chatter_daily mention_score per day (gold_daily_mention_scores)"}.get(
        source, "UNKNOWN source value %r" % (source,))
    print("INPUT THE SERVED RANK IS COMPUTED FROM (by CHATTER_AXIS_SOURCE=%s): %s" % (source, inp))

    served = {}
    for movement in ("trending", "breakout"):
        status, body = invoke_rankings(movement)
        served[movement] = body
        print("\nSERVED %s x CHATTER: http=%s axis=%s ranking_status=%s state=%s as_of_date=%s requested_as_of=%s dated=%s "
              "generation_id=%s row_count=%s movement_measure=%s"
              % (movement.upper(), status, body.get("axis"), body.get("ranking_status"), body.get("state"),
                 body.get("as_of_date"), body.get("requested_as_of"), body.get("dated"), body.get("generation_id"),
                 body.get("row_count"), (body.get("resolution") or {}).get("movement_measure")))
        for row in body.get("rows", []):
            print("   rank %-3s %-16s %-16s score=%s raw_chatter_count(as-of day)=%s window_total_count=%s movement_raw_score=%s"
                  % (row.get("rank"), row.get("ticker"), row.get("security_key"), row.get("score"),
                     row.get("raw_chatter_count"), row.get("window_total_count"), row.get("movement_raw_score")))
        if not body.get("rows"):
            print("   (no rows served: %s)" % body.get("ranking_reason"))
    result["chatter_axis_source"] = source
    result["served"] = {k: {kk: v.get(kk) for kk in ("axis", "as_of_date", "requested_as_of", "dated", "ranking_status",
                                                    "generation_id", "row_count", "rows")}
                        for k, v in served.items()}

    trending = served["trending"]
    as_of = trending.get("as_of_date") or datetime.date.today().isoformat()
    as_of_d = datetime.date.fromisoformat(as_of)
    start_d = as_of_d - datetime.timedelta(days=WINDOW_DAYS - 1)

    # ---- 3. independent recompute from chatter_daily ------------------------------------------
    dkey, dparts = newest_part("chatter_daily")
    daily = read_rows(dkey)
    print("\nNEWEST SERVED chatter_daily PART: s3://%s/%s  (%d part(s) under the prefix); %d rows, %d securities, days %s..%s"
          % (BUCKET, dkey, dparts, len(daily), len({r["security_key"] for r in daily}),
             min(r["day"] for r in daily), max(r["day"] for r in daily)))
    print("WINDOW: %s .. %s (%d days, the served generation's as_of_date %s minus 29 days)"
          % (start_d, as_of_d, WINDOW_DAYS, as_of))
    universe = sorted({r["security_key"] for r in daily})
    asof_score = {k: 0.0 for k in universe}
    win_score = {k: 0.0 for k in universe}
    win_raw = {k: 0 for k in universe}
    win_articles = {k: 0 for k in universe}
    win_tier = {k: collections.Counter() for k in universe}
    for r in daily:
        if start_d <= r["day"] <= as_of_d:
            k = r["security_key"]
            win_score[k] += r["mention_score"] or 0.0
            win_raw[k] += r["mention_count_total"] or 0
            win_articles[k] += r["articles_total"] or 0
            for t in "abcd":
                win_tier[k][t.upper()] += r["tier_" + t] or 0
            if r["day"] == as_of_d:
                asof_score[k] += r["mention_score"] or 0.0
    graded_win = {k: v for k, v in win_score.items() if v > 0}
    raw_win = {k: v for k, v in win_raw.items() if v > 0}
    signal = {k for k in universe if win_raw[k] > 0 or win_score[k] > 0}
    graded_asof_all = {k: asof_score[k] for k in signal}  # no-signal names dropped first, as chatter_axis does
    print("UNIVERSE (securities in chatter_daily): %d; companies with any window signal: %d; with an as-of-day score > 0: %d"
          % (len(universe), len(signal), sum(1 for k in signal if asof_score[k] > 0)))

    # recomputed graded TRENDING (as-of day) rank, tie-break security_key ascending
    order_asof = sorted(graded_asof_all, key=lambda k: (-graded_asof_all[k], k))
    rank_asof = {k: i + 1 for i, k in enumerate(order_asof)}
    order_win = sorted(graded_win, key=lambda k: (-graded_win[k], k))
    rank_win = {k: i + 1 for i, k in enumerate(order_win)}
    raw_pos = positions(raw_win)
    graded_pos = positions(graded_win)

    served_rows = trending.get("rows") or []
    served_rank = {r["security_key"]: r["rank"] for r in served_rows if r.get("security_key")}

    print("\nSIDE BY SIDE -- TRENDING x CHATTER, page as served vs recomputed from the graded chatter_daily part")
    print("  %-4s | %-28s | %-46s | %-46s" % ("rank", "SERVED (security_key score)", "RECOMPUTED graded, as-of-day mention_score",
                                              "RECOMPUTED graded, 30-day window mention_score"))
    n_rows = max(len(served_rows), 15)
    for i in range(n_rows):
        s = ("%s %s" % (served_rows[i]["security_key"], served_rows[i]["score"])) if i < len(served_rows) else "-"
        a = ("%s %.2f" % (order_asof[i], graded_asof_all[order_asof[i]])) if i < len(order_asof) else "-"
        w = ("%s %.2f (raw named %d)" % (order_win[i], graded_win[order_win[i]], win_raw[order_win[i]])) if i < len(order_win) else "-"
        print("  %-4d | %-28s | %-46s | %-46s" % (i + 1, s, a, w))

    rho_asof, n_asof = spearman({k: -v for k, v in served_rank.items()}, {k: -v for k, v in rank_asof.items()})
    rho_win, n_win = spearman({k: -v for k, v in served_rank.items()}, {k: -v for k, v in rank_win.items()})
    print("\nRANK CORRELATION (Spearman, own implementation)")
    print("  served TRENDING rank vs recomputed graded as-of-day rank : %s" % fmt_rho(rho_asof, n_asof))
    print("  served TRENDING rank vs recomputed graded 30-day-window rank: %s" % fmt_rho(rho_win, n_win))
    rho_rg, n_rg = spearman(raw_win, graded_win)
    print("  raw-count window measure vs graded window measure (all companies with signal, values not ranks): %s"
          % fmt_rho(rho_rg, n_rg))
    print("  served set vs recomputed windows: served %d companies %s; recomputed graded window set %d companies; overlap %d"
          % (len(served_rank), sorted(served_rank), len(graded_win), len(set(served_rank) & set(graded_win))))
    only_graded = sorted(set(graded_win) - set(served_rank))
    print("  companies with graded window signal that the served list does not carry: %d of %d" % (len(only_graded), len(graded_win)))

    # ---- 5. passing-mention test ----------------------------------------------------------------
    print("\nPASSING-MENTION TEST (raw-count window rank better than graded window rank by >= 5 places), competition ranks,")
    print("over the %d companies with a raw window count > 0 (%d with a graded window score > 0):" % (len(raw_win), len(graded_win)))
    print("  %-18s raw_rank graded_rank places raw_named articles graded_score tiers(A/B/C/D)" % "security_key")
    passing = []
    for k in sorted(signal, key=lambda k: (raw_pos.get(k, 10 ** 6), k)):
        rr = raw_pos.get(k)
        gr = graded_pos.get(k)
        if rr is None or gr is None:
            continue
        d = gr - rr
        if d >= 5:
            t = win_tier[k]
            passing.append({"security_key": k, "raw_rank": rr, "graded_rank": gr, "places": d, "raw_named": win_raw[k],
                            "articles": win_articles[k], "graded_score": round(win_score[k], 4),
                            "tiers": [t["A"], t["B"], t["C"], t["D"]]})
    for p in passing:
        print("  %-18s %8d %11d %6d %9d %8d %12.2f %s" % (p["security_key"], p["raw_rank"], p["graded_rank"], p["places"],
                                                         p["raw_named"], p["articles"], p["graded_score"],
                                                         "/".join(str(x) for x in p["tiers"])))
    print("  => %d company(ies) listed" % len(passing))
    # as-of-day version
    raw_asof = {k: 0 for k in signal}
    for r in daily:
        if r["day"] == as_of_d and r["security_key"] in raw_asof:
            raw_asof[r["security_key"]] += r["mention_count_total"] or 0
    ra_pos = positions({k: v for k, v in raw_asof.items() if v > 0})
    ga_pos = positions({k: v for k, v in asof_score.items() if v > 0 and k in signal})
    passing_asof = [k for k in ra_pos if k in ga_pos and ga_pos[k] - ra_pos[k] >= 5]
    print("  as-of-day version (%s): %d company(ies) with a raw as-of-day count > 0, %d with a graded as-of-day score > 0; listed: %s"
          % (as_of, len(ra_pos), len(ga_pos), passing_asof))
    if not ra_pos:
        print("  (the as-of day holds no mention in the graded table, so the as-of-day comparison is empty, not a pass)")
    # the top-10 by raw named count vs top-10 by graded score
    top_raw = sorted(raw_win, key=lambda k: (-raw_win[k], k))[:10]
    top_gr = sorted(graded_win, key=lambda k: (-graded_win[k], k))[:10]
    print("  top-10 by raw named count : %s" % top_raw)
    print("  top-10 by graded score    : %s" % top_gr)
    print("  in the raw top-10 but not the graded top-10: %s" % sorted(set(top_raw) - set(top_gr)))
    print("  in the graded top-10 but not the raw top-10: %s" % sorted(set(top_gr) - set(top_raw)))

    # ---- 6. consistency with the pair table ------------------------------------------------------
    mkey, _n = newest_part("article_security_mention")
    pairs = read_rows(mkey)
    from_pairs = collections.defaultdict(float)
    for p in pairs:
        pub = p.get("published_utc")
        if pub is None:
            continue
        day = pub.date() if hasattr(pub, "date") else pub
        if start_d <= day <= as_of_d:
            from_pairs[p["security_key"]] += p.get("signal_weight") or 0.0
    agree = sum(1 for k in universe if abs(from_pairs.get(k, 0.0) - win_score[k]) < 1e-9)
    print("\nCONSISTENCY: chatter_daily window mention_score vs the same sum recomputed from the newest pair table part"
          " (%s): agree for %d of %d securities" % (mkey.rsplit("/", 1)[-1], agree, len(universe)))
    disagree = [(k, round(from_pairs.get(k, 0.0), 4), round(win_score[k], 4)) for k in universe
                if abs(from_pairs.get(k, 0.0) - win_score[k]) >= 1e-9]
    if disagree:
        print("  disagreeing (security_key, from pair table, in chatter_daily): %s" % disagree)

    result.update({
        "chatter_daily_key": dkey, "window": [str(start_d), str(as_of_d)], "universe": len(universe),
        "signal_companies": len(signal), "served_rank_vs_graded_asof": {"rho": rho_asof, "n": n_asof},
        "served_rank_vs_graded_window": {"rho": rho_win, "n": n_win},
        "raw_vs_graded_window": {"rho": rho_rg, "n": n_rg}, "passing_mention": passing,
        "passing_mention_asof_day": passing_asof, "pair_table_key": mkey,
        "consistency_agree": [agree, len(universe)],
    })
    with open(os.path.join(OUT_DIR, "m2_ac2_result.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=2, sort_keys=True, default=str)
    print("\nwrote m2_ac2_result.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
