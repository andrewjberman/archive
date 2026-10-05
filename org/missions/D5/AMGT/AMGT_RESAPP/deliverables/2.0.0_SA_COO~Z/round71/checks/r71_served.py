"""AMGT_RESAPP round 71 -- the CTO's round-70 analysis @21e6a2dc1c, section 4 items 1, 3, 4 (PRD v0.38 FWD-34, FWD-4, FWD-7).

  --cell c34|c35|c36 --where local|deployed

c34 (FWD-34, a price-movement score carries its unit): every object that carries `score` in
    /lead-panel/rankings/{trending,breakout}/price (default, ?days=90, ?days=365), /lead-panel/timeseries/{trending,breakout}/price
    (?security_key=BA_US_Equity) and the overlay `price` / `breakout_price` blocks of BA, AMD, VLO also carries
    `score_unit == "percent"`. C1: 0 objects without it; the denominator (objects carrying `score`) prints.
c35 (FWD-4, each feed item clickable to its original): over every covered name's /security/<key>/overlay `feed.items[]`, each item
    serves a non-empty `url`, or `url` null with a non-empty plain `url_reason`. C1: 0 items failing both; items read print.
    C2: every item whose publisher stores its link (bbg `url`, barrons `canonicalUrl`, sa `links.self`) serves a non-empty
    `url`, so a reason-only pass is refused; only ft and wsj, which store no link, may carry `url_reason`.
c36 (FWD-7, /freshness shows every covered company): /freshness `rows` carry a row for EVERY covered security key.
    C1: 0 covered keys missing; rows read print.
Population for c35/c36: `covered_universe.covered_security_keys()` (95 at the cut).
Verdict: R71 <CELL> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import importlib.util
import json

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
OVERLAY_NAMES = ("BA_US_Equity", "AMD_US_Equity", "VLO_US_Equity")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _scored(obj, path=""):
    if isinstance(obj, dict):
        if "score" in obj:
            yield path, obj
        for k, v in obj.items():
            yield from _scored(v, path + "." + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _scored(v, path + "[%d]" % i)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c34", "c35", "c36"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    from lib.research.api import scoped_amgt

    if a.where == "deployed":
        import boto3

        cl = _load("capture_lib", CAPTURE_LIB)
        lam = boto3.client("lambda", region_name=cl.REGION)

        def call(path, query=None):
            body, meta = cl._invoke(lam, path, query)
            return (200, body) if body is not None else (meta.get("status"), None)
    else:
        def call(path, query=None):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "opal"}, "queryStringParameters": query})
            try:
                return r.get("statusCode"), json.loads(r.get("body") or "null")
            except ValueError:
                return r.get("statusCode"), None

    non200 = []
    if a.cell == "c34":
        reads = []
        for mv in ("trending", "breakout"):
            for q in (None, {"days": "90"}, {"days": "365"}):
                reads.append((f"{PREFIX}/lead-panel/rankings/{mv}/price", q))
            reads.append((f"{PREFIX}/lead-panel/timeseries/{mv}/price", {"security_key": "BA_US_Equity"}))
        for key in OVERLAY_NAMES:
            reads.append((f"{PREFIX}/security/{key}/overlay", None))
        scored, bad = 0, []
        for path, q in reads:
            st, body = call(path, q)
            if st != 200:
                non200.append(f"{path}{q or ''}:{st}")
                continue
            for p, o in _scored(body):
                if "overlay" in path and not (p.startswith(".price") or p.startswith(".breakout_price")):
                    continue
                scored += 1
                if o.get("score_unit") != "percent":
                    bad.append(f"{path.rsplit('/amgt', 1)[-1]}{p}")
        print(f"   population: reads {len(reads)} objects carrying score {scored} non-200 {len(non200)} e.g. {non200[:3]}")
        clause("C1 every served score carries score_unit percent", scored and not bad and not non200,
               f"objects failing {len(bad)} e.g. {bad[:4]}")
    else:
        from lib.research.coverage import covered_universe

        keys = sorted(covered_universe.covered_security_keys())
        if a.cell == "c35":
            items, bad, with_url, linked, linked_bad = 0, [], 0, 0, []
            for key in keys:
                st, ov = call(f"{PREFIX}/security/{key}/overlay")
                if st != 200:
                    non200.append(f"{key}:{st}")
                    continue
                for it in (((ov or {}).get("feed") or {}).get("items") or []):
                    items += 1
                    url = str(it.get("url") or "").strip()
                    if it.get("publisher") in ("bbg", "barrons", "sa"):
                        linked += 1
                        if not url:
                            linked_bad.append(f"{key}/{it.get('publisher')}")
                    if url:
                        with_url += 1
                    elif not str(it.get("url_reason") or "").strip():
                        bad.append(f"{key}/{it.get('publisher')}")
            print(f"   population: names {len(keys)} items {items} with url {with_url} non-200 {len(non200)} e.g. {non200[:3]}")
            clause("C1 every feed item serves its url or a plain url_reason", keys and items and not bad and not non200,
                   f"items failing {len(bad)} e.g. {bad[:4]}")
            clause("C2 every bbg/barrons/sa item serves a url", linked and not linked_bad,
                   f"linked items {linked} without url {len(linked_bad)} e.g. {linked_bad[:4]}")
        elif a.cell == "c36":
            st, fr = call(f"{PREFIX}/freshness")
            rows = (fr or {}).get("rows") or []
            have = {r.get("security_key") for r in rows if isinstance(r, dict)}
            missing = [k for k in keys if k not in have]
            print(f"   population: covered {len(keys)} rows {len(rows)} status {st}")
            clause("C1 /freshness carries a row for every covered name", st == 200 and keys and not missing,
                   f"missing {len(missing)} e.g. {missing[:6]}")

    verdict = "YES" if ok and all(ok) else "NO"
    print(f"R71 {a.cell.upper()} SERVED: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    raise SystemExit(main())
