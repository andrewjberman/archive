"""HARVST round 44 HVST-aq-4 (FWD-12), READ ONLY: grade limbs (a)-(d) from storage and code. No S3 write, no publisher
request, no Lambda.

(a) round-32 evidence (`round32/ae1_wrong_object_cut.json`): wrong-object rows counted against rows checked; the newest sa
    quarantine object in S3 (`publication_gold.sa_quarantined_keys`) holds exactly those article keys.
(b) code at HEAD: the sa leg makes no `/api/v3/articles/{id}` request and takes the body from the listing item.
(c) the sa page cap: the code default AND the value the backfill run path actually uses (worker.py sets
    `client.max_listing_pages` from config.json), plus the stored listing hits' `search_page` distribution.
(d) re-check over EVERY stored sa silver article row with the round-32 classifier (`round32/checks/ae1_common.classify`,
    independent of the collector): a listing-discovered row carrying an article `id` whose title is not the stored
    listing hit's title for the same id is a MISMATCH; quarantined keys are excluded. Printed for all rows and for rows
    published since 2026-01-01.
Writes `round44/aq-4.sa_integrity.json`.
"""
import collections
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)

import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

_spec = importlib.util.spec_from_file_location("ae1_common", os.path.join(DELIV, "round32", "checks", "ae1_common.py"))
ae1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ae1)

B = store.HARVEST_BUCKET
ART_COLS = ("article_id", "id", "discovered_for", "title", "published_utc")
HIT_COLS = ("article_id", "id", "title", "search_page", "query_sha256", "run_stamp", "retrieval_mode")
OUT = os.path.join(HERE, "aq-4.sa_integrity.json")


def parts(cl, prefix):
    out = []
    for page in cl.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=prefix):
        out += [o["Key"] for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet")]
    return sorted(out)


def read_rows(cl, prefix, cols):
    rows = []
    for k in parts(cl, prefix):
        t = pq.read_table(io.BytesIO(cl.get_object(Bucket=B, Key=k)["Body"].read()))
        use = [c for c in cols if c in t.schema.names]
        for r in t.select(use).to_pylist():
            r["_part"] = k
            rows.append(r)
    return rows


def code_limbs():
    src = open(os.path.join(ROOT, "lib", "opal_data_harvest", "publishers.py"), encoding="utf-8").read()
    start = src.index("    def seeking_alpha(self, security, limit):")
    end = src.index("\n    def ", start + 10)
    sa_src = src[start:end]
    requests_article = [m.group(0) for m in re.finditer(r"[^\n]*api/v3/articles/[^\n]*", sa_src)
                        if not m.group(0).lstrip().startswith("#")]
    default_cap = re.search(r'DEFAULT_MAX_LISTING_PAGES = \{"sa": (\d+)', src)
    cfg = json.load(open(os.path.join(ROOT, "lib", "opal_data_harvest", "config.json"), encoding="utf-8"))
    worker = open(os.path.join(ROOT, "lib", "opal_data_harvest", "worker.py"), encoding="utf-8").read()
    wire = [ln.strip() for ln in worker.splitlines() if "client.max_listing_pages =" in ln]
    return {"sa_article_request_lines_in_seeking_alpha": requests_article,
            "body_from_listing_comment": "HVST-ae-1: the body comes from the LISTING item" in sa_src,
            "default_cap_sa": int(default_cap.group(1)) if default_cap else None,
            "config_json_max_listing_pages_sa": (cfg.get("max_listing_pages") or {}).get("sa"),
            "worker_sets_cap_from_config": wire}


def main():
    cl = boto3.client("s3", region_name="us-east-1")
    out = {}
    # (a)
    ev = json.load(open(os.path.join(DELIV, "round32", "ae1_wrong_object_cut.json"), encoding="utf-8"))
    q = pg.sa_quarantined_keys()
    ev_keys = set(ev["distinct_article_keys"])
    out["a"] = {"round32_rows_checked": ev["rows_checked"], "round32_wrong_rows": ev["wrong_rows"],
                "round32_distinct_keys": len(ev_keys), "s3_quarantine_keys": len(q),
                "s3_equals_round32_keys": q == ev_keys, "in_round32_not_s3": sorted(ev_keys - q),
                "in_s3_not_round32": sorted(q - ev_keys)}
    # (b), (c) code
    out["code"] = code_limbs()
    # (c) stored listing pages
    hits = read_rows(cl, ae1.LISTING, HIT_COLS)
    pages = collections.Counter(int(h["search_page"]) for h in hits if h.get("search_page") is not None)
    per_query = collections.defaultdict(int)
    for h in hits:
        if h.get("search_page") is not None and h.get("query_sha256"):
            per_query[(h["query_sha256"], h.get("run_stamp"))] = max(per_query[(h["query_sha256"], h.get("run_stamp"))],
                                                                     int(h["search_page"]))
    out["c_stored"] = {"listing_hits": len(hits), "max_search_page": max(pages) if pages else None,
                       "hits_on_page_gt_25": sum(v for p, v in pages.items() if p > 25),
                       "queries_runs": len(per_query), "queries_runs_reaching_page_25": sum(1 for v in per_query.values() if v == 25),
                       "queries_runs_beyond_25": sum(1 for v in per_query.values() if v > 25)}
    # (d)
    silver = read_rows(cl, ae1.SILVER, ART_COLS)
    wrong = ae1.classify(silver, hits)
    outside = [r for r in wrong if ae1.article_key(r) not in q]
    since = [r for r in silver if str(r.get("published_utc") or "")[:10] >= ae1.FLOOR]
    outside_since = [r for r in outside if str(r.get("published_utc") or "")[:10] >= ae1.FLOOR]
    with_id = sum(1 for r in silver if ae1.listed(r.get("discovered_for")) and ae1.listed(r.get("id")))
    out["d"] = {"silver_rows": len(silver), "silver_parts": len({r["_part"] for r in silver}),
                "rows_since_2026_01_01": len(since), "listing_discovered_with_id": with_id,
                "wrong_object_total": len(wrong), "wrong_quarantined": len(wrong) - len(outside),
                "mismatches_outside_quarantine": len(outside), "mismatches_outside_quarantine_since_floor": len(outside_since),
                "sample": [{"key": ae1.article_key(r), "published": str(r.get("published_utc"))[:10],
                            "title": str(r.get("title"))[:80]} for r in outside[:10]]}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    a, c, cs, d = out["a"], out["code"], out["c_stored"], out["d"]
    print("(a) round32: %d wrong of %d checked (%d keys); S3 quarantine %d keys; equal %s"
          % (a["round32_wrong_rows"], a["round32_rows_checked"], a["round32_distinct_keys"], a["s3_quarantine_keys"],
             a["s3_equals_round32_keys"]))
    print("(b) /api/v3/articles request lines in seeking_alpha(): %d; body-from-listing marker %s"
          % (len(c["sa_article_request_lines_in_seeking_alpha"]), c["body_from_listing_comment"]))
    print("(c) code default sa cap %s; config.json sa cap %s; worker wiring %s"
          % (c["default_cap_sa"], c["config_json_max_listing_pages_sa"], c["worker_sets_cap_from_config"]))
    print("(c) stored sa listing hits %d; max search_page %s; hits on page > 25: %d; query-runs %d, reaching page 25: %d, beyond 25: %d"
          % (cs["listing_hits"], cs["max_search_page"], cs["hits_on_page_gt_25"], cs["queries_runs"],
             cs["queries_runs_reaching_page_25"], cs["queries_runs_beyond_25"]))
    print("(d) silver rows %d (%d parts; %d since 2026-01-01; %d listing-discovered with an article id); wrong-object %d, "
          "quarantined %d; MISMATCHES outside quarantine %d (since floor %d)"
          % (d["silver_rows"], d["silver_parts"], d["rows_since_2026_01_01"], d["listing_discovered_with_id"],
             d["wrong_object_total"], d["wrong_quarantined"], d["mismatches_outside_quarantine"],
             d["mismatches_outside_quarantine_since_floor"]))
    for s in d["sample"]:
        print("  MISMATCH %s %s %r" % (s["key"], s["published"], s["title"]))
    print("RECORD: %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
