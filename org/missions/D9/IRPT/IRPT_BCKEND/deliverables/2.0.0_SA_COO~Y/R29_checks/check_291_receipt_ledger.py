#!/usr/bin/env python3
"""IB-yr-291 AC1 -- the job's receipt.json carries the vendor endpoint ledger (shapes, never values).

Runs one OVERVIEW generation through the offline replay (no socket, netguard installed by the
suite module) and reads the receipt the job wrote. PASS iff the receipt carries `vendor_requests`
as a list whose length equals the transport's evidence length, every record's key set equals the
transport's own record shape, and no record carries a value-bearing key.

Base run (CLOUD HEAD before the cut): FAIL -- the receipt has no `vendor_requests` key.
Issuer 2.0.0_SA_COO~Y, round 29. ASCII only.
"""
import json
import os
import sys

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # parents[0] is R29_checks itself; the repo root is parents[8]
TESTS = os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting", "ycharts", "generate", "tests")
sys.path.insert(0, TESTS)

import run_offline_suite as suite  # noqa: E402  (installs netguard; offline by construction)

SHAPE = {"method", "path", "status", "content_type", "bytes", "set_cookie_count", "waf_action",
         "login_destination", "final_url_path", "body_complete"}
FORBIDDEN = {"cookie", "cookies", "set_cookie", "authorization", "body", "value", "password",
             "token", "headers", "csrf"}


def main():
    name, _fp = suite.owned_name()
    blobs = suite.jobmod.MemoryBlobs()
    job, _opener = suite.make_job(suite.base_script(collection_owned_name=name), blobs=blobs)
    run = job.run(suite.JOB_ID, suite.REQUEST_ID, suite.REVISION, suite.HOLDINGS, "OVERVIEW",
                  cover=suite.COVER)
    receipts = [k for k in blobs.objects if k[1].endswith("receipt.json")]
    print("run ok:", run.get("ok"), "| receipts written:", len(receipts),
          "| transport evidence records:", len(job.tx.evidence))
    if run.get("ok") is not True or len(receipts) != 1:
        print("FAIL: no single receipt from a READY run")
        return 1
    receipt = json.loads(blobs.objects[receipts[0]].decode("utf-8"))
    print("receipt keys:", sorted(receipt))
    ledger = receipt.get("vendor_requests")
    if not isinstance(ledger, list):
        print("FAIL: receipt.vendor_requests is %s, not a list" % type(ledger).__name__)
        return 1
    print("ledger records:", len(ledger), "| denominator (tx.evidence):", len(job.tx.evidence))
    if len(ledger) != len(job.tx.evidence) or len(ledger) < 4:
        print("FAIL: ledger length %d != evidence %d (or < 4)" % (len(ledger), len(job.tx.evidence)))
        return 1
    bad_shape = [i for i, r in enumerate(ledger) if set(r) != SHAPE]
    leaks = [i for i, r in enumerate(ledger) if any(k.lower() in FORBIDDEN for k in r)]
    print("records off-shape:", len(bad_shape), "| records with a value-bearing key:", len(leaks))
    if bad_shape or leaks:
        print("FAIL: shape or leak")
        return 1
    print("shape-only records carried:", len(ledger))
    print("PASS: receipt vendor_requests carries every transport record on the ten-key shape")
    return 0


if __name__ == "__main__":
    sys.exit(main())
