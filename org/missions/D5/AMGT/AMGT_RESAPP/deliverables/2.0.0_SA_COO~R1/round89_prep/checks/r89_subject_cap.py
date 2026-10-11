"""AMGT_RESAPP round-89 PREP -- D1-S15: the peer set's subject market cap is on the vintage of the subject's own record.

  python r89_subject_cap.py [--where local|deployed]        (repo root, PYTHONPATH=<repo root>)

Measured 2026-10-11: the stored peers object for ASML_NA_Equity (as_of 2026-09-24T2252Z) carries subject.market_cap_musd
541,931.78 at cap_vintage 2026-09-19T07:53:19Z, while the subject's own newest model block (20261010T130156Z) reads
CUR_MKT_CAP 621,657.44 at 2026-10-10T13:01:55Z. The route serves the stored object with decorators and never rewrites it,
so the cell is a serve-time decorator that takes the subject's cap fields from the CURRENT model block with the SAME derivation
the producer used (engine._subject_from_model_block), or serves the stored figure with the plain reason it could not refresh.
    C1 the served subject's market_cap_musd, market_cap_vintage, cap_vintage and cap_source equal the values
       engine._subject_from_model_block derives from a fresh read of the subject's current model block (computed here).
    C2 every OTHER subject field and every member is byte-equal to the stored object's.
    C3 (local only) when the model block cannot be read, the stored cap fields are served unchanged and the subject
       carries `cap_refresh` with a `status` and a non-empty plain `reason` (nothing is invented, nothing is dropped silently).
Verdict: R89 SUBJECT CAP: YES|NO (exit 0|1). At the base (2026-10-11) C1 and C3 FAIL, C2 PASSes.
"""
from __future__ import annotations

import argparse
import json
import sys
from unittest import mock

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
SUBJECT = "ASML_NA_Equity"
CAP_FIELDS = ("market_cap_musd", "market_cap_vintage", "cap_vintage", "cap_source")
# Fields the refresh may set; everything else on the subject must equal the stored object's.
MAY_CHANGE = set(CAP_FIELDS) | {"cap_refresh", "market_cap_raw", "cap_stored_vintage"}


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def call(where, path):
    event = {
        "rawPath": "%s%s" % (PREFIX, path),
        "queryStringParameters": None,
        "requestContext": {"http": {"method": "GET"}},
        "headers": {"x-firm-id": "opal"},
    }
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        r = scoped_amgt.handler(event)
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", default="local", choices=["local", "deployed"])
    where = ap.parse_args().where

    from lib.research.api import scoped_amgt
    from lib.research.peers import engine

    stored, rec = scoped_amgt.read_pool_object(scoped_amgt.PEERS_PREFIX, SUBJECT)
    block, brec = scoped_amgt._read_model_block_pool(SUBJECT)
    fresh = engine._subject_from_model_block(SUBJECT, block)
    code, served = call(where, "/security/%s/peers" % SUBJECT)
    subject = served.get("subject") or {}
    print("   where=%s status=%s | stored cap %s @ %s | fresh block %s cap %s @ %s | served cap %s @ %s" % (
        where, code, stored["subject"].get("market_cap_musd"), stored["subject"].get("cap_vintage"),
        brec.get("object_key"), fresh.get("market_cap_musd"), fresh.get("cap_vintage"),
        subject.get("market_cap_musd"), subject.get("cap_vintage")))

    c1 = say(code == 200 and all(subject.get(k) == fresh.get(k) for k in CAP_FIELDS),
             "C1 the served subject's cap fields equal the subject's current model block's (%s)" % (
                 ", ".join("%s=%r" % (k, subject.get(k)) for k in ("market_cap_musd", "cap_vintage"))))

    other_same = all(subject.get(k) == v for k, v in stored["subject"].items() if k not in MAY_CHANGE)
    members_same = served.get("members") is not None and [
        {k: m.get(k) for k in ("ticker", "name", "price", "market_cap_musd", "cap_ratio_to_subject", "log_cap_distance")}
        for m in served["members"]
    ] == [
        {k: m.get(k) for k in ("ticker", "name", "price", "market_cap_musd", "cap_ratio_to_subject", "log_cap_distance")}
        for m in stored["members"]
    ]
    c2 = say(other_same and members_same,
             "C2 every other subject field and every member's ticker, name, price, cap, ratio, distance equal the stored object's")

    if where == "local":
        with mock.patch.object(scoped_amgt, "_read_model_block_pool", side_effect=RuntimeError("model block unreadable (probe)")):
            _code, held = call("local", "/security/%s/peers" % SUBJECT)
        hs = held.get("subject") or {}
        unchanged = all(hs.get(k) == stored["subject"].get(k) for k in CAP_FIELDS)
        said = isinstance(hs.get("cap_refresh"), dict) and bool(str(hs["cap_refresh"].get("status") or "").strip()) \
            and bool(str(hs["cap_refresh"].get("reason") or "").strip())
        c3 = say(unchanged and said,
                 "C3 an unreadable model block serves the stored cap unchanged and says why in cap_refresh (unchanged=%s said=%s)" % (
                     unchanged, said))
    else:
        c3 = True
        print("   C3 skipped: the unreadable-block arm needs the local handler")

    ok = c1 and c2 and c3
    print("R89 SUBJECT CAP: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
