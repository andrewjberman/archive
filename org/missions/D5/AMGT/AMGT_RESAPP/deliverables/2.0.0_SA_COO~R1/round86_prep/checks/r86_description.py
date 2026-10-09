"""AMGT_RESAPP round-86 PREP -- company_description drawn from the business item only (CTO~DELL1 round-85 analysis R5).

  python r86_description.py --crit AC1 [--where deployed|local] [--keys K1,K2,...]

Reads each name's served /thesis `drafted_sections[company_description]` (--where deployed: the live function, read only; local: the
handler) and classifies every sentence by its evidence's `source.location` item label:
    BUSINESS = 20-F Item 4 (4.B Business Overview, Item 4 Information on the Company) or 10-K Item 1 (not 1A/1B/1C);
    BANNED   = Item 5 (20-F OFR), Item 3.D (20-F risk), 10-K Item 7 (MD&A), 10-K Item 1A (risk).
    D1 every non-empty company_description sentence cites the business item (each of its evidence locations is BUSINESS);
    D2 0 sentences cite a BANNED item;
    D3 a name with no business-cited sentence serves an EMPTY section (0 sentences) -- the names printed.
Per name the item mix (sentences per item label) is printed with its denominator.
Verdict: R86 DESCRIPTION AC1: YES|NO (exit 0|1). At the base (live HZoC2x, 2026-10-09): NO -- NU serves Item 5 lines.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys

KEYS = ("ASML_NA_Equity", "BABA_US_Equity", "NU_US_Equity", "PBR_US_Equity", "SAP_GY_Equity", "AMD_US_Equity", "NVDA_US_Equity")
FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
SECTION = "company_description"
ITEM_RE = re.compile(r"^\s*item\s*(\d+)\s*\.?\s*([a-z])?\b", re.I)


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def item_label(location):
    m = ITEM_RE.match(location or "")
    if not m:
        return "OTHER"
    return ("%s.%s" % (m.group(1), m.group(2).upper())) if m.group(2) else m.group(1)


def is_business(label, form):
    if form == "20-F":
        return label in ("4", "4.B")
    return label == "1"


def is_banned(label, form):
    if form == "20-F":
        return label == "5" or label == "3.D"
    return label in ("7", "1.A")


def _thesis(key, where):
    event = {"rawPath": "%s/security/%s/thesis" % (PREFIX, key), "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        r = scoped_amgt.handler(event)
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def _form(body):
    src = body.get("drafting_source") or {}
    form = src.get("form") if isinstance(src, dict) else None
    if form:
        return form
    text = json.dumps(body.get("drafted_sections") or [])
    return "20-F" if re.search(r"ITEM 4\.B|ITEM 5\. OPERATING", text, re.I) else "10-K"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--where", choices=("deployed", "local"), default="deployed")
    ap.add_argument("--keys", default=",".join(KEYS))
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if root and root not in sys.path:
        sys.path.insert(0, root)
    keys = [k.strip() for k in a.keys.split(",") if k.strip()]
    n_total = n_non_business = n_banned = 0
    not_empty_without_business = []
    empty = []
    for key in keys:
        code, body = _thesis(key, a.where)
        form = _form(body)
        secs = [s for s in body.get("drafted_sections") or [] if s.get("section_id") == SECTION]
        sents = secs[0].get("sentences") or [] if secs else []
        mix = collections.Counter()
        biz = 0
        for s in sents:
            labels = [item_label(((e.get("source") or {}).get("location"))) for e in s.get("evidence") or [] if isinstance(e, dict)]
            for lab in labels or ["NONE"]:
                mix[lab] += 1
            if labels and all(is_business(lab, form) for lab in labels):
                biz += 1
            else:
                n_non_business += 1
            if any(is_banned(lab, form) for lab in labels):
                n_banned += 1
        n_total += len(sents)
        if not sents:
            empty.append(key)
        elif biz == 0:
            not_empty_without_business.append(key)
        print("   %-15s %s status %s form %s: %d sentences, %d business-cited | item mix %s" % (
            key, SECTION, code, form, len(sents), biz, dict(sorted(mix.items()))))
    d1 = say(n_non_business == 0, "D1 every company_description sentence cites the business item: %d of %d do not" % (n_non_business, n_total))
    d2 = say(n_banned == 0, "D2 sentences citing Item 5 / 3.D (20-F) or Item 7 / 1A (10-K): %d of %d" % (n_banned, n_total))
    d3 = say(not not_empty_without_business, "D3 a name with no business-cited sentence serves an EMPTY section: offending %s; empty %s" % (
        not_empty_without_business, empty))
    ok = d1 and d2 and d3
    print("R86 DESCRIPTION AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
