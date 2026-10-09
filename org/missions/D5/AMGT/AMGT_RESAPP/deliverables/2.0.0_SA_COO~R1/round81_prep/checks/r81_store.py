"""AMGT_RESAPP round-81 PREP (DRAFT, not issued) -- R1's store half for ASML NA (row AMGT_RESAPP-D1-S3).

  python r81_store.py --crit AC1|AC2 [--where deployed|local]

AC1 (the stored source): the LATEST silver `filing_source` row for ASML_NA_Equity (vendor sec, read through
    lib.research.harvest.store.silver_latest, read only) carries a business section cut from its own heading:
    S1 its excerpt `item_keys` holds "business"; S2 its excerpt `items` holds "Item 4.B. Business Overview";
    S3 the excerpt text carries the heading "Item 4.B. Business Overview" in any case and spacing, and the 400 characters
       after it are body prose: no other "Item <n>" heading inside them (a contents entry is followed by the next item).
       Round 83 (row AMGT_RESAPP-D1-W324-S2): the round-81 S3 searched the label case-sensitively and then looked for the
       heading again AFTER itself, so a correct ASML cut ("ITEM 4.B. BUSINESS OVERVIEW") could never pass.
  python r81_store.py --self-test   runs S3 on planted texts: a true heading (YES), a contents-entry mis-cut (NO),
       no heading (NO). Exit 0 only when all three read as planted.
AC2 (what is served): GET /security/ASML_NA_Equity/thesis (--where deployed: the live function, read only):
    T1 200; T2 the share-capital refusal sentence ("shares or describes its share capital") appears 0 times;
    T3 at least one served `location` starts with an Item 4.B / Business overview item.
Verdict: R81 STORE ACn SERVED: YES|NO (exit 0|1). At the base (2026-10-09) both read NO.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

KEY = "ASML_NA_Equity"
FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
REFUSAL = "shares or describes its share capital"
LABEL = "Item 4.B. Business Overview"
HEADING_RE = re.compile(r"item\s+4\s*\.?\s*b\s*\.?\s*business\s+overview", re.I)
NEXT_ITEM_RE = re.compile(r"\bitem\s+\d+\s*\.?\s*[a-z]?\s*\.", re.I)


def s3_heading(text):
    """(ok, why): the business heading is in the text and opens body prose, not a contents line."""
    m = HEADING_RE.search(text or "")
    if not m:
        return False, "no Item 4.B Business Overview heading in the excerpt text"
    after = text[m.end():m.end() + 400]
    nxt = NEXT_ITEM_RE.search(after)
    if nxt:
        return False, "heading at %d is followed within 400 chars by %r (a contents entry)" % (m.start(), nxt.group(0))
    return True, "heading at %d (%r) opens %d chars of prose" % (m.start(), m.group(0), len(after))


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def ac1():
    from lib.research.harvest import store as hs

    rows = hs.silver_latest("sec", "filing_source", ("security_key", "accession"))
    rows = list(rows.values()) if isinstance(rows, dict) else list(rows)
    mine = [r for r in rows if r.get("security_key") == KEY]
    print("   silver sec filing_source rows: %d, for %s: %d" % (len(rows), KEY, len(mine)))
    if not mine:
        return say(False, "S0 a stored row exists")
    row = max(mine, key=lambda r: str(r.get("fetched_at")))
    obj = json.loads(row["object_json"])
    ex = obj.get("excerpt") or {}
    print("   accession %s parser %s fetched_at %s items %s" % (
        obj.get("accession"), obj.get("parser_version"), row.get("fetched_at"), ex.get("items")))
    s1 = say("business" in (ex.get("item_keys") or []), "S1 excerpt item_keys holds business")
    s2 = say(LABEL in (ex.get("items") or []), "S2 excerpt items holds %r" % LABEL)
    ok, why = s3_heading(ex.get("text") or "")
    s3 = say(ok, "S3 the business section opens on its own heading: %s" % why)
    return s1 and s2 and s3


def self_test():
    prose = " ASML is a supplier to the semiconductor industry. " * 12
    planted = [
        ("true heading, upper case", "ITEM 4.B. BUSINESS OVERVIEW" + prose, True),
        ("contents-entry mis-cut", "Item 4.B. Business Overview 23 Item 4.C. Organizational Structure 41" + prose, False),
        ("no heading", "About us" + prose, False),
    ]
    good = 0
    for name, text, want in planted:
        ok, why = s3_heading(text)
        good += say(ok == want, "planted %s reads %s (want %s): %s" % (name, ok, want, why))
    print("R81 STORE S3 SELF-TEST: %s %d of %d" % ("YES" if good == len(planted) else "NO", good, len(planted)))
    return good == len(planted)


def walk(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "location" and isinstance(v, str):
                out.append(v)
            else:
                walk(v, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, out)


def ac2(where):
    event = {"rawPath": "%s/security/%s/thesis" % (PREFIX, KEY), "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        r = scoped_amgt.handler(event)
    code, body = r.get("statusCode"), json.loads(r.get("body") or "{}")
    text = json.dumps(body)
    locs = []
    walk(body, locs)
    biz = [loc for loc in locs if re.match(r"^\s*item\s*4\.?\s*b\b|business overview", loc, re.I)]
    print("   status %s, served locations %d, Item 4.B locations %d, refusal sentence x%d" % (
        code, len(locs), len(biz), text.count(REFUSAL)))
    t1 = say(code == 200, "T1 the route answers 200")
    t2 = say(text.count(REFUSAL) == 0, "T2 no share-capital refusal sentence is served")
    t3 = say(len(biz) > 0, "T3 a served passage is cited to Item 4.B Business overview")
    return t1 and t2 and t3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=["AC1", "AC2"])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--where", choices=("deployed", "local"), default="deployed")
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if root and root not in sys.path:
        sys.path.insert(0, root)
    if a.self_test:
        return 0 if self_test() else 1
    if not a.crit:
        ap.error("--crit is required unless --self-test")
    ok = ac1() if a.crit == "AC1" else ac2(a.where)
    print("R81 STORE %s SERVED: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
