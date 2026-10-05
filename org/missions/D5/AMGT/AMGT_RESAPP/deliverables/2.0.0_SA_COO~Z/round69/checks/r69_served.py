"""AMGT_RESAPP round 69 -- the CTO's round-68 analysis @f54b52325e, ruling 1.

  --cell c29 --where local|deployed

c29 (plain words, the /ledger dedupe and the article nit):
    C1  over EVERY covered name (`covered_universe.covered_security_keys()`), /ledger answers 200, and no class `source_reason`
        repeats a clause: split on ": " and ", and " / "; ", and no normalized clause of 4 or more words appears twice;
    C2  DE_US_Equity /thesis serves no reason with the article-less phrase "for driver chart".
The denominators print: names read, classes read.
Verdict: R69 C29 SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
SPLIT = re.compile(r":\s+|;\s+|,\s+and\s+")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _strings(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _strings(v, path + "." + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _strings(v, path + "[%d]" % i)
    elif isinstance(obj, str):
        yield path, obj


def _repeats(reason):
    """Clauses of 4+ words that appear twice, or that sit inside another clause of the same reason."""
    parts = [" ".join(re.findall(r"[a-z0-9]+", p.lower())) for p in SPLIT.split(reason or "")]
    parts = [p for p in parts if len(p.split()) >= 4]
    dup = []
    for i, p in enumerate(parts):
        for j, q in enumerate(parts):
            if i != j and (p == q and i < j or (p != q and f" {p} " in f" {q} ")):
                dup.append(p)
    return dup


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c29",), required=True)
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

    from lib.research.coverage import covered_universe

    keys = sorted(covered_universe.covered_security_keys())
    rep, non200, classes = [], [], 0
    for key in keys:
        st, led = call(f"{PREFIX}/security/{key}/ledger")
        if st != 200:
            non200.append(f"{key}:{st}")
            continue
        for c, v in ((led or {}).get("classes") or {}).items():
            classes += 1
            d = _repeats(str((v or {}).get("source_reason") or ""))
            if d:
                rep.append(f"{key}/{c}: {d[0][:50]}")
    print(f"   population: names {len(keys)} classes {classes} non-200 {len(non200)} e.g. {non200[:3]}")
    clause("C1 no /ledger source_reason repeats a clause", keys and not rep and not non200,
           f"offenders {len(rep)} e.g. {rep[:4]}")
    st, body = call(f"{PREFIX}/security/DE_US_Equity/thesis")
    bad = [f"{p}: {v[:70]}" for p, v in _strings(body or {}) if "for driver chart" in v.lower()]
    clause("C2 DE /thesis has no article-less 'for driver chart'", st == 200 and not bad, f"status {st} hits {len(bad)} e.g. {bad[:2]}")

    verdict = "YES" if ok and all(ok) else "NO"
    print(f"R69 {a.cell.upper()} SERVED: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    raise SystemExit(main())
