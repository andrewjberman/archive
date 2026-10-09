"""AMGT_RESAPP round-85 PREP -- the name list carries a measured issuer identity (CTO~DELL1 round-84 analysis item 3; ruling ADDENDUM 2).

  python r85_crosswalk.py --crit AC1 [--path <local crosswalk JSON>]

Reads the name list -- the LATEST key under s3://opal-data-harvest/crosswalk/v1/ (what the live function reads at request time), or a
local file with --path (the build cell's offline list) -- and the PRIOR stored key (the newest one before the latest; with --path, the
latest stored key), read only:
    C1 no record dropped: every security_key of the prior list is in this list (count printed, denominator the prior list);
    C2 ASML_NA_Equity and ASML_US_Equity both carry `issuer.cik` 937966, each with a claim of `measured` and a named source;
    C3 no `issuer.cik` carries an inferred claim or a text source, and every value names its source (count with denominator);
    C4 the four other stored 20-F names carry their filer CIKs (BABA 1577552, NU 1691493, PBR 1119639, SAP 1000184).
Verdict: R85 CROSSWALK AC1: YES|NO (exit 0|1). At the base (2026-10-07.json, 243 records): NO -- no record carries `issuer`.
"""
from __future__ import annotations

import argparse
import json
import sys

BUCKET = "opal-data-harvest"
PREFIX = "crosswalk/v1/"
ASML = ("ASML_NA_Equity", "ASML_US_Equity")
ASML_CIK = "937966"
FILERS = {"BABA_US_Equity": "1577552", "NU_US_Equity": "1691493", "PBR_US_Equity": "1119639", "SAP_GY_Equity": "1000184"}


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def _keys():
    import boto3

    s3 = boto3.client("s3", region_name="us-east-1")
    keys = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        keys += [o["Key"] for o in page.get("Contents") or [] if o["Key"].endswith(".json")]
    return s3, sorted(keys)


def _records(doc):
    recs = doc.get("records") if isinstance(doc, dict) else doc
    if isinstance(recs, dict):
        recs = list(recs.values())
    return {r.get("security_key"): r for r in recs or [] if isinstance(r, dict) and r.get("security_key")}


def _issuer(rec):
    iss = rec.get("issuer") or {}
    return str(iss.get("cik") or "").lstrip("0"), iss.get("claim"), iss.get("source")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--path")
    a = ap.parse_args()
    s3, keys = _keys()
    print("   stored name lists under s3://%s/%s: %d (latest %s)" % (BUCKET, PREFIX, len(keys), keys[-1] if keys else None))
    if a.path:
        this, label = json.load(open(a.path, encoding="utf-8")), a.path
        prior_key = keys[-1]
    else:
        label = keys[-1]
        this = json.loads(s3.get_object(Bucket=BUCKET, Key=keys[-1])["Body"].read())
        prior_key = keys[-2] if len(keys) > 1 else keys[-1]
    prior = _records(json.loads(s3.get_object(Bucket=BUCKET, Key=prior_key)["Body"].read()))
    recs = _records(this)
    print("   this list %s: %d records; prior %s: %d records" % (label, len(recs), prior_key, len(prior)))
    missing = sorted(set(prior) - set(recs))
    c1 = say(not missing, "C1 no record dropped: %d of %d prior records present%s" % (
        len(prior) - len(missing), len(prior), (" (missing %s)" % missing[:5]) if missing else ""))
    asml = {k: _issuer(recs.get(k) or {}) for k in ASML}
    for k, v in asml.items():
        print("   %s issuer %s" % (k, v))
    c2 = say(all(v[0] == ASML_CIK and v[1] == "measured" and v[2] for v in asml.values()),
             "C2 both ASML listings carry measured issuer.cik %s with a named source" % ASML_CIK)
    with_cik = [(k, _issuer(r)) for k, r in recs.items() if _issuer(r)[0]]
    bad = [k for k, (cik, claim, src) in with_cik if claim != "measured" or not src or "text" in str(src).lower()]
    c3 = say(bool(with_cik) and not bad, "C3 every issuer.cik is measured with a named source: %d of %d carry one; %d bad%s" % (
        len(with_cik) - len(bad), len(recs), len(bad), (" %s" % bad[:5]) if bad else ""))
    wrong = [k for k, cik in FILERS.items() if _issuer(recs.get(k) or {})[0] != cik]
    c4 = say(not wrong, "C4 the four other stored 20-F names carry their filer CIKs: %d of 4%s" % (
        4 - len(wrong), (" (wrong %s)" % wrong) if wrong else ""))
    ok = c1 and c2 and c3 and c4
    print("R85 CROSSWALK AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
