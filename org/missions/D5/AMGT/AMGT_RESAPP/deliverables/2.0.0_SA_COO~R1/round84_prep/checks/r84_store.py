"""AMGT_RESAPP round-84 PREP -- the store half for one 20-F name, generalised from round 81's r81_store.py (ASML NA only).

  python r84_store.py --key <KEY>[,<KEY>...] --crit AC1|AC2 [--where deployed|local]
  (several keys: every key must read YES; the last line is R84 STORE ACn ALL: YES|NO n of N)

AC1 (the stored source): the LATEST silver `filing_source` row for --key (vendor sec, read through
    lib.research.harvest.store.silver_latest, read only):
    S1 parser opal-filings-fetch/2.0.0; S2 its excerpt `item_keys` holds "business";
    S3 its stamped `language` is "en" (row AMGT_RESAPP-D1-W332-S1: BABA read pt, SAP es before round 84).
AC2 (what is served): GET /security/<KEY>/thesis (--where deployed: the live function, read only):
    T1 200; T2 at least one served `location` STARTS with the business item (Item 4.B / Business overview / Item 4
       Information on the Company / Our Business); T3 the served sentences are English: 80% or more of them carry an English
       function word (the, and, of, to, in, from, at, on, with, its, is, are, was, were, by, for, versus). Round 84 AMENDMENT 1 to
       AMGT-ii-3: the first set (the/and/of) read SAP's number-heavy English segment sentences as unmarked (26 of 34, 76%).
       A Portuguese or Spanish draft still reads near 0% (none of these words is Portuguese or Spanish).
Verdict: R84 STORE ACn <KEY>: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
BUSINESS_RE = re.compile(r"^\s*(item\s*4\b|business overview|our business)", re.I)  # anchored: row D1-W337-S1
ENGLISH_RE = re.compile(r"\s(the|and|of|to|in|from|at|on|with|its|is|are|was|were|by|for|versus)\s", re.I)


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def ac1(key):
    from lib.research.harvest import store as hs

    rows = hs.silver_latest("sec", "filing_source", ("security_key", "accession"))
    rows = list(rows.values()) if isinstance(rows, dict) else list(rows)
    mine = [r for r in rows if r.get("security_key") == key]
    print("   silver sec filing_source rows: %d, for %s: %d" % (len(rows), key, len(mine)))
    if not mine:
        return say(False, "S0 a stored row exists")
    row = max(mine, key=lambda r: str(r.get("fetched_at")))
    obj = json.loads(row["object_json"])
    ex = obj.get("excerpt") or {}
    lang = obj.get("language") or ex.get("language")
    print("   accession %s parser %s language %s fetched_at %s items %s" % (
        obj.get("accession"), obj.get("parser_version"), lang, row.get("fetched_at"), ex.get("items")))
    s1 = say(obj.get("parser_version") == "opal-filings-fetch/2.0.0", "S1 parser opal-filings-fetch/2.0.0")
    s2 = say("business" in (ex.get("item_keys") or []), "S2 excerpt item_keys holds business")
    s3 = say(lang == "en", "S3 the stamped language is en (read %r)" % lang)
    return s1 and s2 and s3


def walk(node, locs, sents):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "location" and isinstance(v, str):
                locs.append(v)
            elif k in ("sentence", "text") and isinstance(v, str) and len(v) > 40:
                sents.append(v)
            else:
                walk(v, locs, sents)
    elif isinstance(node, list):
        for v in node:
            walk(v, locs, sents)


def ac2(key, where):
    event = {"rawPath": "%s/security/%s/thesis" % (PREFIX, key), "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        r = scoped_amgt.handler(event)
    code, body = r.get("statusCode"), json.loads(r.get("body") or "{}")
    locs, sents = [], []
    walk(body, locs, sents)
    biz = [loc for loc in locs if BUSINESS_RE.search(loc)]
    eng = [s for s in sents if ENGLISH_RE.search(" %s " % s)]
    share = (100.0 * len(eng) / len(sents)) if sents else 0.0
    print("   status %s, served locations %d, business locations %d, sentences %d, English-marked %d (%.0f%%)" % (
        code, len(locs), len(biz), len(sents), len(eng), share))
    t1 = say(code == 200, "T1 the route answers 200")
    t2 = say(len(biz) > 0, "T2 a served passage is cited to the business item")
    t3 = say(bool(sents) and share >= 80.0, "T3 the served sentences are English (%.0f%%, floor 80%%)" % share)
    return t1 and t2 and t3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True)
    ap.add_argument("--crit", required=True, choices=["AC1", "AC2"])
    ap.add_argument("--where", choices=("deployed", "local"), default="deployed")
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if root and root not in sys.path:
        sys.path.insert(0, root)
    keys = [k.strip() for k in a.key.split(",") if k.strip()]
    good = 0
    for key in keys:
        print("== %s" % key)
        ok = ac1(key) if a.crit == "AC1" else ac2(key, a.where)
        print("R84 STORE %s %s: %s" % (a.crit, key, "YES" if ok else "NO"))
        good += ok
    if len(keys) > 1:
        print("R84 STORE %s ALL: %s %d of %d" % (a.crit, "YES" if good == len(keys) else "NO", good, len(keys)))
    return 0 if good == len(keys) else 1


if __name__ == "__main__":
    sys.exit(main())
