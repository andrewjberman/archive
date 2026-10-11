"""AMGT_RESAPP round-94 PREP -- the CTO's census (round-93 analysis item 1): every served subject whose display name differs from its crosswalk company.

  PYTHONPATH=<repo root> python r94_name_census.py [--where deployed|local]

For each of the 243 MEASURED crosswalk subjects the name the page serves (`--where deployed`: the live function's `/overlay` `display_name`; `--where local`: the
checkout's own overlay name path, `scoped_amgt._overlay_name`) is compared with the crosswalk's registered company name. The two AGREE when their cleaned name tokens
(`numeric_tickers.name_token`, legal endings stripped, then the generic words com, stk, cl, class, cos, holdings, holding, group, del, new, and, corp, co, inc, ltd
dropped) share at least one token of two or more letters; a pair that shares none is a DIFFERENT COMPANY.
    C1 the count of subjects whose served name is a different company from the registered one: must be 0 (the base reads 2: SAN_FP_Equity served as
       'Banco Santander S.A.' and CSL_AU_Equity served as 'Carlisle Cos Inc', both bare-ticker collisions in the classifications table).
    C2 control: the denominator is printed: 243 subjects; each judged against EVERY reference name it has -- the crosswalk's registered identity name, the
       record's `legal_name.value` where its status is MEASURED, the record's research folder name (`source_row.folder`, e.g. 'Sanofi SAN FP'), and the key's
       own model-block header NAME (`scoped_amgt._model_block_names`); a served name is a DIFFERENT company only when it shares no token with ANY of them;
       a subject with no reference at all is UNJUDGED (a count, not a pass); the spelling variants (the names differ, the company is the same) are LISTED,
       not counted as defects.
Verdict: R94 NAME CENSUS: YES|NO (exit 0|1).
"""
import argparse
import json
import sys

import boto3

from lib.research.api import scoped_amgt
from lib.research.identity import crosswalk
from lib.research.peers import numeric_tickers

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
GENERIC = {"com", "stk", "cl", "class", "cos", "holdings", "holding", "group", "del", "new", "and", "corp", "co", "inc", "ltd"}
_LAM = boto3.client("lambda", region_name="us-east-1")


def tokens(name):
    return {t for t in numeric_tickers.name_token(name).split() if len(t) >= 2 and t not in GENERIC}


def served_deployed(key):
    event = {"rawPath": "%s/security/%s/overlay" % (PREFIX, key), "queryStringParameters": None,
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    return (json.loads(r.get("body") or "{}")).get("display_name")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", default="deployed", choices=["deployed", "local"])
    args = ap.parse_args()
    doc, _i, _a = crosswalk.load_crosswalk()
    keys = [r["security_key"] for r in doc["records"] if r.get("resolution") == "MEASURED" and r.get("security_key")]
    registered = scoped_amgt._crosswalk_names()
    if args.where == "local":
        # the name the page HEADER serves: the overlay's own name path (`_overlay_name`), not the chatter chain (round 94 amendment 1)
        served = {}
        for k in keys:
            ident = scoped_amgt.resolve_identity(k) or {}
            served[k] = scoped_amgt._overlay_name(ident, k, ident.get("bloomberg")).get("display_name")
    else:
        served = {k: served_deployed(k) for k in keys}
    records = {r["security_key"]: r for r in doc["records"] if r.get("security_key")}
    block = {}
    for i in range(0, len(keys), 8):
        block.update(scoped_amgt._model_block_names(keys[i:i + 8]))
    judged = wrong = unjudged = 0
    by_source = {"registered": 0, "legal_name": 0, "folder": 0, "model block": 0}
    variants, different = [], []
    for k in keys:
        name = served.get(k)
        rec = records.get(k) or {}
        legal = rec.get("legal_name") if isinstance(rec.get("legal_name"), dict) else {}
        refs = [("registered", registered.get(k)),
                ("legal_name", legal.get("value") if legal.get("status") == "MEASURED" else None),
                ("folder", (rec.get("source_row") or {}).get("folder")),
                ("model block", block.get(k))]
        refs = [(src, str(v).strip()) for src, v in refs if v and str(v).strip()]
        if not refs or not name:
            unjudged += 1
            continue
        judged += 1
        for src, _v in refs:
            by_source[src] += 1
        cleans = [scoped_amgt._clean_display_name(v) for _src, v in refs]
        if any(str(name).strip().lower() == str(c).strip().lower() for c in cleans):
            continue
        if any(tokens(name) & tokens(c) for c in cleans):
            variants.append((k, name, refs[0][1]))
        else:
            wrong += 1
            different.append((k, name, "; ".join("%s=%r" % r for r in refs)))
    print("   where=%s subjects %d | judged %d (references held: %s) | UNJUDGED (no reference name at all) %d | same company, names differ "
          "(spelling variants) %d | DIFFERENT company %d" % (args.where, len(keys), judged,
                                                           ", ".join("%s %d" % kv for kv in by_source.items()), unjudged, len(variants), wrong))
    for v in variants:
        print("   variant   %-18s served=%r registered=%r" % v)
    for d in different:
        print("   DIFFERENT %-18s served=%r registered=%r" % d)
    ok = wrong == 0 and judged > 0
    print("%s C1 no served subject name is another company's (%d)" % ("PASS" if ok else "FAIL", wrong))
    print("R94 NAME CENSUS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
