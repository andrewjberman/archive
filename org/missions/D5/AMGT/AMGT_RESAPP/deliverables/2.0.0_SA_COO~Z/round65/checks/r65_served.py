"""AMGT_RESAPP round 65 -- FWD-38 (b) title case, the CTO's round-64 analysis ruling 1 (@504827836c).

  --cell c17 --where local|deployed

c17 C1: on /lead-panel/rankings/breakout/price and /lead-panel/timeseries/collected/chatter, 0 served display_name values are
        all-caps, except names made only of the DECLARED acronyms (scoped_amgt.DISPLAY_NAME_ACRONYMS, its source printed from
        scoped_amgt.DISPLAY_NAME_ACRONYMS_SOURCE). At the base, before the constant exists, every all-caps name counts.
c17 C2: the cut name the analysis names, "MITSUBISHI UFJ FINANCIAL GRO", is served whole ("Mitsubishi UFJ Financial Group", with
        any legal-form suffix after it) on both routes.
Verdict: R65 C17 SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
ROUTES = ("/lead-panel/rankings/breakout/price", "/lead-panel/timeseries/collected/chatter")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c17",), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    from lib.research.api import scoped_amgt

    acronyms = set(getattr(scoped_amgt, "DISPLAY_NAME_ACRONYMS", ()) or ())
    print(f"   declared acronyms: {len(acronyms)}; source: {getattr(scoped_amgt, 'DISPLAY_NAME_ACRONYMS_SOURCE', 'NOT DECLARED')}")

    if a.where == "deployed":
        import boto3

        cl = _load("capture_lib", CAPTURE_LIB)
        lam = boto3.client("lambda", region_name=cl.REGION)

        def call(path):
            body, meta = cl._invoke(lam, path)
            return (200, body) if body is not None else (meta.get("status"), None)
    else:
        def call(path):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "opal"}, "queryStringParameters": None})
            try:
                return r.get("statusCode"), json.loads(r.get("body") or "null")
            except ValueError:
                return r.get("statusCode"), None

    def acronym_only(name):
        words = [w.strip(".,&()-") for w in name.split()]
        return bool(words) and all((w in acronyms) or not any(ch.isalpha() for ch in w) for w in words)

    for route in ROUTES:
        st, body = call(PREFIX + route)
        rows = (body or {}).get("rows") or []
        names = [r.get("display_name") for r in rows if r.get("display_name")]
        caps = [n for n in names if n == n.upper() and any(ch.isalpha() for ch in n) and not acronym_only(n)]
        clause(f"C1 {route.rsplit('/', 2)[-2]}/{route.rsplit('/', 1)[-1]} serves 0 all-caps names (acronym-only excepted)",
               st == 200 and names and not caps, f"status {st} names {len(names)} all-caps {len(caps)}; e.g. {caps[:4]}")
        mufg = [n for n in names if n.upper().startswith("MITSUBISHI UFJ")]
        clause(f"C2 {route.rsplit('/', 1)[-1]} serves Mitsubishi UFJ Financial Group whole", mufg
               and all(n.startswith("Mitsubishi UFJ Financial Group") for n in mufg), f"served {mufg}")
    print(f"R65 {a.cell.upper()} SERVED: {'YES' if all(ok) else 'NO'}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
