"""AMGT_RESAPP round 68 -- the CTO's round-67 analysis @2db6fd3e3d, section 4 (rulings 1 and 3).

  --cell c27|c28 --where local|deployed

c27 (FWD-39, ruling 1), a CENSUS over EVERY name that serves a cloud. The population is the distinct security_key set of the
    latest `chatter_window` part (212 at the cut; 199 served a cloud on the deployed function, ADJUDICATION_v80), never the
    95-name chatter universe the round-67 c23 read. Each name's /security/<key>/timeline on the route's default range:
    C1  0 clouds carry an own-name word: `scoped_amgt._word_cloud_own_words(key)` UNION the MEASURED leaks below (an
        oracle fixed at the cut, so it does not move with the implementation);
    C2  0 clouds carry a MEASURED junk or boilerplate token (the accent-broken stems, the "hon"/"hai" split, the CTO's
        measured headline boilerplate);
    The denominators print: names read, names serving a cloud, terms read.
c28 (ruling 3, DSGN FWD-27), plain words:
    C1  DE_US_Equity /thesis answers 200, and every served string whose key ends in "reason" is free of the jargon list;
    C2  DE_US_Equity /peers answers 200 under the same rule;
    C3  on BA, AMD, VLO, NVDA, /ledger answers 200, every class names a `source` or a non-empty `source_reason`, and no
        `source_reason` carries "estate", "stage" or "input ledger".
Verdict: R68 <CELL> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import importlib.util
import json

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
# Measured on the deployed function, ADJUDICATION_v80 @69ce44def1 (3.0.0_SA_CVO~Z): the own-name forms the name source does not
# spell, per security key root.
MEASURED_OWN = {
    "XOM": {"exxon", "mobil"},
    "GOOGL": {"google"},
    "GOOG": {"google"},
    "NSRGY": {"nestl", "nestle"},
    "HESAY": {"herm", "hermes"},
    "AZN": {"astra"},
}
MEASURED_JUNK = {"nestl", "herm", "hon", "hai", "movers", "premarket", "sees", "estimates"}
JARGON = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block")
LEDGER_JARGON = ("estate", "stage", "input ledger")
LEDGER_NAMES = ("BA_US_Equity", "AMD_US_Equity", "VLO_US_Equity", "NVDA_US_Equity")


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c27", "c28"), required=True)
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

    if a.cell == "c27":
        from lib.research.harvest import publication_gold

        keys = sorted({t.get("security_key") for t in publication_gold._latest_gold_snapshot_rows("chatter_window")
                       if t.get("security_key")})
        own_hits, junk_hits, serving, terms_read, non200 = [], [], 0, 0, []
        for key in keys:
            st, tl = call(f"{PREFIX}/security/{key}/timeline")
            if st != 200:
                non200.append(f"{key}:{st}")
                continue
            terms = [str(t.get("term")).lower() for t in (((tl or {}).get("word_cloud") or {}).get("terms") or [])]
            if not terms:
                continue
            serving += 1
            terms_read += len(terms)
            root = key.split("_")[0].upper()
            own = {w.lower() for w in scoped_amgt._word_cloud_own_words(key)} | MEASURED_OWN.get(root, set())
            hit = sorted(set(terms) & own)
            if hit:
                own_hits.append(f"{key}:{','.join(hit[:3])}")
            junk = sorted(set(terms) & MEASURED_JUNK)
            if junk:
                junk_hits.append(f"{key}:{','.join(junk[:3])}")
        print(f"   population: names {len(keys)} serving a cloud {serving} terms read {terms_read} non-200 {len(non200)} "
              f"e.g. {non200[:3]}")
        clause("C1 0 clouds carry an own-name word (name source + measured leaks)", keys and not own_hits and not non200,
               f"offenders {len(own_hits)} e.g. {own_hits[:8]}")
        clause("C2 0 clouds carry a measured junk or boilerplate token", keys and not junk_hits and not non200,
               f"offenders {len(junk_hits)} e.g. {junk_hits[:8]}")
    elif a.cell == "c28":
        for leaf, label in (("thesis", "C1"), ("peers", "C2")):
            st, body = call(f"{PREFIX}/security/DE_US_Equity/{leaf}")
            bad = [f"{p}: {v[:70]}" for p, v in _strings(body or {})
                   if p.rsplit(".", 1)[-1].lower().endswith("reason") and any(j in v.lower() for j in JARGON)]
            clause(f"{label} DE_US_Equity /{leaf} serves its reasons in plain words", st == 200 and not bad,
                   f"status {st} jargon reasons {len(bad)} e.g. {bad[:3]}")
        led_bad, unsourced, non200 = [], [], []
        for key in LEDGER_NAMES:
            st, led = call(f"{PREFIX}/security/{key}/ledger")
            if st != 200:
                non200.append(f"{key}:{st}")
                continue
            for c, v in ((led or {}).get("classes") or {}).items():
                v = v or {}
                reason = str(v.get("source_reason") or "")
                if not v.get("source") and not reason.strip():
                    unsourced.append(f"{key}/{c}")
                if any(j in reason.lower() for j in LEDGER_JARGON):
                    led_bad.append(f"{key}/{c}: {reason[:60]}")
        clause("C3 /ledger reasons are plain and every class is sourced or reasoned",
               not led_bad and not unsourced and not non200,
               f"names {len(LEDGER_NAMES)} jargon {len(led_bad)} e.g. {led_bad[:3]} unsourced {unsourced[:3]} non-200 {non200}")

    verdict = "YES" if ok and all(ok) else "NO"
    print(f"R68 {a.cell.upper()} SERVED: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    raise SystemExit(main())
