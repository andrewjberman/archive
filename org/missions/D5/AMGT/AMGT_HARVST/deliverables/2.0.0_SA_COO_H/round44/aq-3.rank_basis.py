"""HARVST round 44 HVST-aq-3 -- FWD-7 read: what the SERVED chatter rank is computed from, and one planted pair.

FWD-7 DONE WHEN: "the chatter ranks on the page are computed from the graded daily table, and a company named once in passing
in many articles no longer outranks one that was the subject of a few". READ ONLY: no S3 write, no generation write, no
collection, no vendor call. The only invoke is the read-only `opal-amgt-scoped-api`; the producer's Lambda configuration is
read with `get_function_configuration` (a describe, not an invoke).

  (1) BASIS at HEAD: the exact source lines that choose the count function, quoted with file:line.
  (2) APPLIED: the live `amgt-resapp-chatter-axis` CHATTER_AXIS_SOURCE, and the served TRENDING/BREAKOUT chatter rankings.
  (3) PLANT through the producer's own `compute_chatter_axis` (write_fn=None, a dry run that builds and returns the
      generations): company A is named in passing (tier D, signal_weight 0.1) in 6 articles every day; company B is the
      subject (tier A, signal_weight 1.0) of 2 articles on the as-of day; 10 filler names carry one tier-B article on the
      as-of day. Run once with the LEGACY count function (raw article count per day, what the served producer selects)
      and once with the GOLD branch (the graded per-article signal_weight, declared set {sa}).
PASS iff the served rank is computed from the graded table AND, on that path, B outranks A.
Writes `round44/aq-3.rank_basis.json`. Verdict line: `AQ-3 FWD-7: PASS|FAIL`.
"""
import datetime
import json
import os
import subprocess
import sys
import tempfile

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "aq-3.rank_basis.json")
REGION = "us-east-1"

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.metrics import chatter_axis as ca  # noqa: E402

BASIS = [
    ("lib/research/metrics/chatter_axis.py", 'DEFAULT_SOURCE = "legacy"'),
    ("lib/research/metrics/chatter_axis.py", '"legacy": default_daily_article_counts,'),
    ("lib/research/metrics/chatter_axis.py", '"gold": gold_daily_mention_scores,'),
    ("lib/research/metrics/chatter_axis.py", "result = pool_reader.window_read(identity, start_date, end_date)"),
    ("lib/research/metrics/chatter_axis.py", "result = pool_reader.gold_window_read(identity, start_date, end_date)"),
    ("infra/aws/terraform/harvest/lambda_src/lambda_function.py", 'SOURCE_ENV = "CHATTER_AXIS_SOURCE"'),
    ("infra/aws/terraform/harvest/lambda_src/lambda_function.py", "return DEFAULT_SOURCE"),
    ("infra/aws/terraform/harvest/chatter-axis-schedule.tf", 'chatter_axis_source       = "legacy"'),
    ("infra/aws/terraform/harvest/chatter-axis-schedule.tf", "CHATTER_AXIS_SOURCE = local.chatter_axis_source"),
    ("lib/research/metrics/movement_gate.py", 'if measure == "ABSOLUTE_COUNT_ON_AS_OF_DAY":'),
    ("lib/research/api/scoped_amgt.py", "read_rankings(rest[2], rest[3], query.get(\"as_of\"), int(limit) if limit else None),"),
]


def quote_basis():
    out = []
    for rel, needle in BASIS:
        lines = open(os.path.join(ROOT, rel), encoding="utf-8").read().splitlines()
        hits = [i + 1 for i, line in enumerate(lines) if needle in line]
        out.append({"file": rel, "line": hits, "text": needle})
    return out


def applied():
    import boto3
    lam = boto3.client("lambda", region_name=REGION)
    cfg = lam.get_function_configuration(FunctionName="amgt-resapp-chatter-axis")
    served = {}
    for movement in ("trending", "breakout"):
        path = "/api/scoped/amgt/lead-panel/rankings/%s/chatter" % movement
        ev = {"rawPath": path, "headers": {"x-firm-id": "opal"}, "queryStringParameters": None,
              "requestContext": {"http": {"method": "GET", "path": path}}}
        r = lam.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(ev).encode("utf-8"))
        parsed = json.loads(r["Payload"].read())
        body = json.loads(parsed.get("body") or "null") or {}
        rows = body.get("rows") or []
        served[movement] = {
            "status": parsed.get("statusCode"), "axis": body.get("axis"), "ranking_status": body.get("ranking_status"),
            "as_of_date": body.get("as_of_date"), "generation_id": body.get("generation_id"),
            "coverage_vintage": body.get("coverage_vintage"), "row_count": body.get("row_count"),
            "population_present": "population" in body, "row_fields": sorted(rows[0]) if rows else [],
            "top3": [{k: row.get(k) for k in ("rank", "ticker", "score", "raw_count", "window_total_count",
                                               "movement_raw_score")} for row in rows[:3]],
        }
    return {"chatter_axis_source_live": (cfg.get("Environment") or {}).get("Variables", {}).get("CHATTER_AXIS_SOURCE"),
            "last_modified": cfg.get("LastModified"), "code_sha256": cfg.get("CodeSha256"), "served": served}


def plant(as_of):
    dates = ca.window_dates(as_of)
    rows = []

    def add(key, day, n, tier, co_mentions):
        for i in range(n):
            rows.append({"security_key": key, "article_key": "sa:%s-%s-%d" % (key, day, i), "publisher": "sa",
                         "published_utc": "%sT12:00:00Z" % day, "signal_tier": tier,
                         "signal_weight": pg.WEIGHTS[tier], "co_mention_count": co_mentions})

    for day in dates:
        add("A_PASSING", day, 6, "D", 6)        # named once in passing, in a roundup, in many articles, every day
    add("B_SUBJECT", dates[-1], 2, "A", 0)      # the subject (title/lead) of a few articles on the as-of day
    for d in (dates[-8], dates[-15], dates[-22]):
        add("B_SUBJECT", d, 1, "A", 0)
    fillers = ["F%02d" % i for i in range(1, 11)]
    for key in fillers:
        add(key, dates[-1], 1, "B", 1)
    names = ["A_PASSING", "B_SUBJECT"] + fillers
    universe = {"as_of": as_of, "names": [{"security_key": k, "ticker": k, "name": k} for k in names]}
    fh = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(universe, fh)
    fh.close()

    def raw_counts(identity, start, end):
        out = {}
        for r in rows:
            day = r["published_utc"][:10]
            if r["security_key"] == identity and start <= day <= end:
                out[day] = out.get(day, 0) + 1
        return out

    def gold_window_read(identity, start, end):
        # the graded daily table is DENSE (a row per security per day), so every window day reads, 0.0 when quiet
        counts = {d: 0.0 for d in dates if start <= d <= end}
        for r in rows:
            day = r["published_utc"][:10]
            if r["security_key"] == identity and start <= day <= end:
                counts[day] = counts.get(day, 0.0) + r["signal_weight"]
        return {"counts": counts, "items": [{"day": d, "publishers_covered_codes": ["sa"]} for d in dates],
                "store_item_count": len(dates), "items_in_window": len(dates), "bodies_read": 0, "duplicate_links": 0,
                "states": {}, "complete": True, "key_forms": [], "crosswalk_status": "GOLD-DIRECT"}

    def ranks(result):
        out = {}
        for gen in result.get("generations") or []:
            out[gen.get("axis")] = {"state": gen.get("state"),
                                    "rows": [[r.get("security_key") or r.get("ticker"), r.get("rank")]
                                             for r in gen.get("rows") or []]}
        return out

    try:
        legacy = ca.compute_chatter_axis(as_of_date=as_of, universe_path=fh.name, count_fn=raw_counts, write_fn=None)
        saved = ca.pool_reader.gold_window_read
        ca.pool_reader.gold_window_read = gold_window_read
        try:
            gold = ca.compute_chatter_axis(
                as_of_date=as_of, universe_path=fh.name, count_fn=ca.gold_daily_mention_scores, write_fn=None,
                declared_publishers=("sa",),
                declared_score_fn=lambda ids, declared, s, e: ca.declared_set_scores(rows, ids, declared, s, e))
        finally:
            ca.pool_reader.gold_window_read = saved
    finally:
        os.unlink(fh.name)
    return {"as_of": as_of, "window": [dates[0], dates[-1]], "legacy": ranks(legacy), "gold": ranks(gold)}


def position(ranked_rows, key):
    for name, rank in ranked_rows:
        if name == key:
            return rank
    return None


def main():
    as_of = "2026-10-02"
    out = {"read_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "basis": quote_basis(),
           "applied": applied(), "plant": plant(as_of)}
    for b in out["basis"]:
        print("BASIS %s:%s  %s" % (b["file"], ",".join(str(x) for x in b["line"]) or "NOT FOUND", b["text"]))
    ap = out["applied"]
    print("APPLIED amgt-resapp-chatter-axis CHATTER_AXIS_SOURCE=%s (LastModified %s)"
          % (ap["chatter_axis_source_live"], ap["last_modified"]))
    for movement, s in ap["served"].items():
        print("SERVED %s/chatter: status %s axis %s %s as_of %s rows %s population_field %s top3 %s"
              % (movement, s["status"], s["axis"], s["ranking_status"], s["as_of_date"], s["row_count"],
                 s["population_present"], s["top3"]))
    verdict_rows = {}
    for source in ("legacy", "gold"):
        for axis, g in out["plant"][source].items():
            a, b = position(g["rows"], "A_PASSING"), position(g["rows"], "B_SUBJECT")
            verdict_rows["%s|%s" % (source, axis)] = {"A_PASSING": a, "B_SUBJECT": b, "state": g["state"]}
            print("PLANT %-6s %-17s state %-9s rank A_PASSING=%s  B_SUBJECT=%s" % (source, axis, g["state"], a, b))
    out["plant_ranks"] = verdict_rows
    served_graded = ap["chatter_axis_source_live"] == "gold"
    trending = [k for k in verdict_rows if k.endswith("TRENDING_CHATTER") or "TRENDING" in k]
    served_key = "%s|%s" % ("gold" if served_graded else "legacy",
                            next((k.split("|")[1] for k in trending), "TRENDING_CHATTER"))
    s = verdict_rows.get(served_key, {})
    b_wins = s.get("B_SUBJECT") is not None and (s.get("A_PASSING") is None or s["B_SUBJECT"] < s["A_PASSING"])
    out["verdict"] = {"served_rank_from_graded_table": served_graded, "served_path_plant": served_key,
                      "served_path_B_outranks_A": b_wins, "pass": served_graded and b_wins}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    print("SERVED PATH %s: B outranks A = %s" % (served_key, b_wins))
    print("AQ-3 FWD-7: %s" % ("PASS" if out["verdict"]["pass"] else "FAIL"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
