"""HVST-n-5 AC1: the 2026-01-01 backfill PLAN for every covered name, printed before any run.

PLANS ONLY. No vendor call, no fetch, no backfill run, no S3 write, no deploy. The only AWS calls
are S3 LIST/GET on the harvest bucket (stored listing objects; silver article rows for the
watermark), through the collector's own read paths.

Planning code used (the collector's own, no new formula):
  - lib/opal_data_harvest/__main__.py:104-135  `plan` command, driven here by subprocess per name
    (pages per publisher = config max_listing_pages[publisher], fallback 25 at :122).
  - lib/opal_data_harvest/config.json:21-27    max_listing_pages, 25 for each of the five publishers.
  - lib/opal_data_harvest/harvest_grammar.py:157 backfill_bound (max(floor, watermark)), called
    in-process for the bound date.
  - lib/opal_data_harvest/publishers.py:142    DEFAULT_MAX_LISTING_PAGES (the publisher-side twin).

Refinement over the planner cap (stated, not hidden): where the collector already HOLDS a stored
listing whose payload states its total page count (Seeking Alpha meta.page.totalPages), the planned
pages for that (name, publisher) are min(planner cap, stored totalPages) with basis MEASURED. Every
other figure is the planner's cap with basis DEFAULT (the default named on the row).
"""

import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
sys.path.insert(0, str(ROOT))
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

import boto3  # noqa: E402

import lib.research.harvest.store as store  # noqa: E402
from lib.opal_data_harvest import harvest_grammar  # noqa: E402

DELIV = ROOT / "org/missions/D5/AMGT/AMGT_HARVST/deliverables"
UNIVERSE = DELIV / "0.9.0_WK_AMGT_HARVST~46/securities.universe.json"
LENOVO = DELIV / "0.9.0_WK_AMGT_HARVST~10/lenovo.security.json"
OUT = DELIV / "0.9.0_WK_AMGT_HARVST~59/n5_backfill_plan.json"
PUBS = ["sa", "bbg", "ft", "wsj", "barrons"]
SOURCE = harvest_grammar.SOURCE_FOR_PUBLISHER
FLOOR = dt.date(2026, 1, 1)
DEFAULT_NAME = "25 pages: config.json max_listing_pages[<publisher>] (planner fallback __main__.py:122)"
PLANNER_CODE = [
    "lib/opal_data_harvest/__main__.py:104-135 (plan command; pages = max_listing_pages[publisher], fallback 25 at :122)",
    "lib/opal_data_harvest/config.json:21-27 (max_listing_pages, 25 per publisher)",
    "lib/opal_data_harvest/harvest_grammar.py:157-165 (backfill_bound = max(floor, silver watermark))",
    "lib/opal_data_harvest/publishers.py:142 (DEFAULT_MAX_LISTING_PAGES twin)",
]


def sha(q):
    return hashlib.sha256(q.encode("utf-8")).hexdigest()


def planner_line(security, tmpdir):
    """Run the collector's own `plan` command for one security (zero network); return {pub: line}."""
    p = Path(tmpdir) / "sec.json"
    p.write_text(json.dumps(security), encoding="utf-8")
    cp = subprocess.run(
        [sys.executable, "-m", "lib.opal_data_harvest", "plan", "--publishers", *PUBS,
         "--security-json", str(p), "--retrieval-mode", "backfill"],
        cwd=str(ROOT), capture_output=True, text=True, timeout=120)
    if cp.returncode != 0:
        raise SystemExit("planner rc=%s: %s" % (cp.returncode, cp.stderr[-400:]))
    lines = [json.loads(x) for x in cp.stdout.splitlines() if x.strip()]
    return {ln["publisher"]: ln for ln in lines if "publisher" in ln}, lines[-1]


def stored_listings(client):
    """{(publisher, query_hash): {page: {key, size, meta}}} from an S3 LIST + GET of the stored listing objects."""
    held = {}
    for pub in PUBS:
        prefix = store.table_prefix(SOURCE[pub], "bronze", "news_listing")
        for pg in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            for o in pg.get("Contents", []) or []:
                base = o["Key"].rsplit("/", 1)[-1]
                qh, page = base.split("_")[0], int(base.split("_")[1][1:])
                rec = {"key": o["Key"], "size_bytes": o["Size"], "sa_meta": None}
                if pub == "sa":
                    body = json.loads(client.get_object(Bucket=store.HARVEST_BUCKET, Key=o["Key"])["Body"].read())
                    mp = (body.get("meta") or {}).get("page") or {}
                    rec["sa_meta"] = {"title": mp.get("title"), "size": mp.get("size"),
                                      "totalPages": mp.get("totalPages"), "total": mp.get("total")}
                held.setdefault((pub, qh), {})[page] = rec
    return held


def candidate_queries(pub, sec):
    company = sec["company"]
    if pub == "sa":
        out = []
        if sec.get("sa_symbol"):
            out.append(("sa_symbol", sec["sa_symbol"]))
        first = sec["ticker"].split()[0].split("_")[0]
        out.append(("ticker_first_token_upper", first.upper()))
        return out
    if pub == "bbg":
        return [("company_quoted", '"' + company.replace('"', '') + '"')]
    return [("company", company)]


def main():
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    lenovo = json.loads(LENOVO.read_text(encoding="utf-8"))
    order = sorted(range(len(universe)), key=lambda i: (universe[i]["key"] != lenovo["key"], i))
    universe = [universe[i] for i in order]
    assert universe[0]["key"] == lenovo["key"], "Lenovo must be first"
    universe[0] = dict(universe[0], sa_symbol=lenovo["sa_symbol"])  # the ~10 plan's own security object
    client = boto3.client("s3", region_name="us-east-1")

    held = stored_listings(client)
    # silver_latest memoised so backfill_bound (the collector's own function) scans each publisher once
    cache = {}
    real = store.silver_latest

    def memo(source, table, fields, client=None):
        k = (source, table, tuple(fields))
        if k not in cache:
            cache[k] = real(source, table, fields, client=client or boto3.client("s3", region_name="us-east-1"))
        return cache[k]

    store.silver_latest = memo

    names = []
    tmp = tempfile.mkdtemp()
    per_pub = {p: {"pages": 0, "measured": 0, "default": 0} for p in PUBS}
    cap_only_total = 0
    for sec in universe:
        lines, tail = planner_line({k: v for k, v in sec.items()}, tmp)
        row = {"key": sec["key"], "ticker": sec["ticker"], "company": sec["company"], "publishers": {}}
        name_total = 0
        for pub in PUBS:
            ln = lines[pub]
            cap = ln["planned_listing_pages"]
            cap_only_total += cap
            bound = harvest_grammar.backfill_bound(sec["key"], pub, FLOOR)
            entry = {"planner_pages": cap, "planner_line": ln, "bound_date": bound.isoformat(),
                     "bound_basis": "silver watermark" if bound > FLOOR else "floor (no silver watermark after floor)"}
            match = None
            for method, q in candidate_queries(pub, sec):
                h = held.get((pub, sha(q)))
                if h:
                    match = (method, q, h)
                    break
            if pub == "sa" and match:
                method, q, h = match
                meta = h[1]["sa_meta"]
                if meta and meta.get("totalPages"):
                    if method != "sa_symbol":
                        # inferred match by ticker token; confirm against the stored title
                        assert sec["company"].split()[0].lower() in (meta["title"] or "").lower(), (sec, meta)
                    pages = min(cap, int(meta["totalPages"]))
                    entry.update(pages=pages, basis="MEASURED",
                                 basis_detail="stored SA listing totalPages=%s (total=%s, size=%s) query=%r matched by %s%s"
                                 % (meta["totalPages"], meta["total"], meta["size"], q, method,
                                    "; capped at planner cap %d" % cap if int(meta["totalPages"]) > cap else ""),
                                 stored_listing_key=h[1]["key"])
            if "pages" not in entry:
                entry.update(pages=cap, basis="DEFAULT", basis_detail=DEFAULT_NAME.replace("<publisher>", pub))
                if match:
                    entry["stored_listing_note"] = "listing held for pages %s (%s) but states no total page count" % (
                        sorted(match[2]), match[0])
            if pub == "sa":
                entry["status"] = "WAITS-ON-RENEWAL"
                entry["sa_symbol_resolved"] = bool(sec.get("sa_symbol"))
            else:
                entry["status"] = "PLANNED"
            row["publishers"][pub] = entry
            name_total += entry["pages"]
            per_pub[pub]["pages"] += entry["pages"]
            per_pub[pub]["measured" if entry["basis"] == "MEASURED" else "default"] += 1
        row["name_total_pages"] = name_total
        names.append(row)

    grand = sum(v["pages"] for v in per_pub.values())
    n_measured = sum(v["measured"] for v in per_pub.values())
    n_default = sum(v["default"] for v in per_pub.values())
    doc = {
        "to_id": "AMGT_HARVST.TO-HVST-n-5.backfill-plan-for-every-covered-name",
        "floor": FLOOR.isoformat(),
        "run_state": "PLAN ONLY -- nothing fetched, no vendor call, no S3 write",
        "universe": str(UNIVERSE.relative_to(ROOT)).replace("\\", "/"),
        "planning_code": PLANNER_CODE,
        "default_named": DEFAULT_NAME,
        "seeking_alpha_leg": "WAITS-ON-RENEWAL (Andrew's renewal word given; account not yet renewed)",
        "names_count": len(names),
        "first_name": names[0]["key"],
        "per_publisher_totals": per_pub,
        "grand_total_pages": grand,
        "grand_total_excluding_sa": grand - per_pub["sa"]["pages"],
        "planner_cap_only_grand_total": cap_only_total,
        "figures_total": n_measured + n_default,
        "figures_measured": n_measured,
        "figures_default": n_default,
        "stored_listings_held": {"%s/%s" % k: sorted(v) for k, v in held.items()},
        "names": names,
    }
    OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8")

    print("PLAN (no vendor call, no fetch, no S3 write) floor=%s names=%d first=%s" % (FLOOR, len(names), names[0]["key"]))
    print("planning code:")
    for c in PLANNER_CODE:
        print("  " + c)
    print("default: " + DEFAULT_NAME)
    print("SA leg: WAITS-ON-RENEWAL")
    print("%-22s %5s %5s %5s %5s %7s %6s  basis" % ("name", "sa*", "bbg", "ft", "wsj", "barrons", "total"))
    for r in names:
        pp = r["publishers"]
        print("%-22s %5d %5d %5d %5d %7d %6d  %s" % (
            r["key"][:22], pp["sa"]["pages"], pp["bbg"]["pages"], pp["ft"]["pages"], pp["wsj"]["pages"],
            pp["barrons"]["pages"], r["name_total_pages"],
            ",".join(p + ":" + pp[p]["basis"][0] for p in PUBS)))
    print("per-publisher totals: " + json.dumps({p: v["pages"] for p, v in per_pub.items()}))
    print("GRAND TOTAL pages: %d (excluding SA: %d); planner cap-only grand total: %d" % (
        grand, grand - per_pub["sa"]["pages"], cap_only_total))
    print("figures: %d total, MEASURED=%d, DEFAULT=%d" % (n_measured + n_default, n_measured, n_default))
    measured = [(r["key"], p, r["publishers"][p]["basis_detail"]) for r in names for p in PUBS
                if r["publishers"][p]["basis"] == "MEASURED"]
    for m in measured:
        print("MEASURED: %s %s: %s" % m)
    ok = (len(names) == 191 and all("basis" in e for r in names for e in r["publishers"].values())
          and names[0]["key"] == lenovo["key"])
    print("all 191 names present, every page count carries its basis: %s" % ok)
    print("wrote " + str(OUT.relative_to(ROOT)).replace("\\", "/"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
