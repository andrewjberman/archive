"""AMGT_RESAPP round-85 PREP -- machine sentences served once and separated by a space (CTO~DELL1 round-84 analysis item 1).

  python r85_sentences.py --crit AC1 [--where deployed|stored|local] [--keys K1,K2,...] [--write-base]
  python r85_sentences.py --crit AC1 --where file --keys <ONE KEY> --draft <local drafting JSON>
    (round 85, the issuer: grades an OFFLINE draft written with no store write; S3's floor there is the CURRENT stored drafting
     document's sentence count for that key, read only -- the same shape, `sections[].sentences[]`)
  --no-floor: S3 is printed but not graded (round 85 AMENDMENT 1 to AMGT-jj-1, CTO~DELL1 msg 2442: a fresh model draw's yield is
     not the join repair's to control -- row D1-W338-S1; the served floor is graded by AMGT-jj-2 on the live function).

Reads every served machine sentence (`drafted_sections[].sentences[].text`) for the five stored 20-F names (ASML NA -- capture 004's
key -- BABA, NU, PBR, SAP), from the live function (--where deployed, the default), the stored drafting documents (--where stored:
drafting/v1/<KEY>.json, read only), or the local handler (--where local). Each served text is split into sentences at a sentence end,
INCLUDING a glued junction (". " missing: "...in 2024.Total revenue ...").
    S1 no served text states one fact twice in a row: no two adjacent sentences are identical after normalisation, or share two or
       more figures (numbers carrying a decimal point, a thousands comma, or three or more digits) -- the round-83 NU shape is a
       paraphrase followed by the filing's verbatim sentence repeating the same figures;
    S2 no sentence boundary is glued: no lowercase letter, digit, '%' or ')' + [.!?] + an uppercase letter + a lowercase letter with no
       space between (abbreviations and decimals do not match the pattern);
    S3 (negative arm) per name, the count of served sentence objects is printed with its denominator and is not below the base count
       recorded in r85_sentences_base.json (`--write-base` records it; a repair must not drop a sentence to pass S1/S2).
Verdict: R85 SENTENCES AC1: YES|NO (exit 0|1). At the base (2026-10-09, live 66MDfT5i): NO -- NU 25 of 38 served texts glued and
restated; the other four names 0.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

KEYS = ("ASML_NA_Equity", "BABA_US_Equity", "NU_US_Equity", "PBR_US_Equity", "SAP_GY_Equity")
FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
BUCKET = "opal-data-harvest"
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "r85_sentences_base.json")
GLUE_RE = re.compile(r"[a-z0-9%)][.!?][A-Z][a-z]")
SPLIT_RE = re.compile(r"(?<=[a-z0-9%)][.!?])\s*(?=[A-Z][a-z])")
FIGURE_RE = re.compile(r"\d[\d,]*\.\d+|\d{1,3}(?:,\d{3})+|\d{3,}")


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _norm(text):
    return re.sub(r"\s+", " ", text).strip().rstrip(".!?").lower()


def _figures(text):
    return set(FIGURE_RE.findall(text))


def restated(text):
    parts = [p.strip() for p in SPLIT_RE.split(text or "") if p.strip()]
    for a, b in zip(parts, parts[1:]):
        if _norm(a) == _norm(b) or len(_figures(a) & _figures(b)) >= 2:
            return True
    return False


def _sentences_from_body(body):
    return [s.get("text") or "" for sec in body.get("drafted_sections") or [] for s in sec.get("sentences") or []]


def _stored_doc(key):
    import boto3

    obj = boto3.client("s3", region_name="us-east-1").get_object(Bucket=BUCKET, Key="drafting/v1/%s.json" % key)
    return json.loads(obj["Body"].read())


def _doc_sentences(doc):
    return [s.get("text") or "" for sec in doc.get("sections") or [] for s in sec.get("sentences") or []]


def _read(key, where, draft=None):
    if where == "file":
        return _doc_sentences(json.load(open(draft, encoding="utf-8")))
    if where == "stored":
        import boto3

        obj = boto3.client("s3", region_name="us-east-1").get_object(Bucket=BUCKET, Key="drafting/v1/%s.json" % key)
        doc = json.loads(obj["Body"].read())
        return [s.get("text") or "" for sec in doc.get("sections") or [] for s in sec.get("sentences") or []]
    event = {"rawPath": "%s/security/%s/thesis" % (PREFIX, key), "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        r = scoped_amgt.handler(event)
    return _sentences_from_body(json.loads(r.get("body") or "{}"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--where", choices=("deployed", "stored", "local", "file"), default="deployed")
    ap.add_argument("--draft")
    ap.add_argument("--no-floor", action="store_true")
    ap.add_argument("--keys", default=",".join(KEYS))
    ap.add_argument("--write-base", action="store_true")
    a = ap.parse_args()
    root = _root()
    if root and root not in sys.path:
        sys.path.insert(0, root)
    keys = [k.strip() for k in a.keys.split(",") if k.strip()]
    base = {}
    if a.where == "file":
        if not a.draft or len(keys) != 1:
            ap.error("--where file needs --draft and exactly one --keys")
        base = {keys[0]: len(_doc_sentences(_stored_doc(keys[0])))}
        print("   file arm: S3 floor = the current stored draft's sentence count for %s: %d" % (keys[0], base[keys[0]]))
    elif os.path.isfile(BASE):
        base = json.load(open(BASE, encoding="utf-8"))
    counts, dbl_total, glue_total, n_total, short = {}, 0, 0, 0, []
    for key in keys:
        sents = _read(key, a.where, a.draft)
        dbl = sum(1 for t in sents if restated(t))
        glued = sum(1 for t in sents if GLUE_RE.search(t or ""))
        counts[key] = len(sents)
        n_total += len(sents)
        dbl_total += dbl
        glue_total += glued
        floor = base.get(key)
        if floor is not None and len(sents) < floor:
            short.append(key)
        print("   %-15s served sentences %3d (base %s) | restated %2d of %d | glued %2d of %d" % (
            key, len(sents), floor if floor is not None else "-", dbl, len(sents), glued, len(sents)))
    if a.write_base:
        json.dump(counts, open(BASE, "w", encoding="utf-8", newline="\n"), indent=2, sort_keys=True)
        print("   base written: %s" % BASE)
    s1 = say(dbl_total == 0, "S1 no served text states one fact twice in a row: %d of %d restated" % (dbl_total, n_total))
    s2 = say(glue_total == 0, "S2 no glued sentence boundary: %d of %d served texts glued" % (glue_total, n_total))
    s3 = say(bool(base) and not short, "S3 no name serves fewer sentences than its base (%s)" % (
        "names below base: %s" % short if short else ("no base recorded" if not base else "%d names at or above base" % len(keys))))
    if a.no_floor:
        print("   --no-floor: S3 printed, not graded")
    ok = s1 and s2 and (s3 or a.no_floor)
    print("R85 SENTENCES AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
