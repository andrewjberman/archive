#!/usr/bin/env python3
"""FAST item 2 (certifier comparisons) -- the ONE REAL RUN.

Read-only. For one served Analysis request it reads the REAL retained composition and the REAL retained vendor PDF
(irpt-requests rows and their versioned S3 blobs, through the live-walk Trace reader), derives the chosen comparison
names exactly as publisher._chosen_comparisons does (resolved.comparison_catalog by browser.comparison_keys), and
runs the NEW certify.missing_comparison_names on the real bytes:
  arm A  the request's own chosen names            -> expected: none missing
  arm B  the chosen names plus one the request did NOT choose (a control name) -> expected: exactly that one missing
Usage: python real_run_301.py <tenant> <REQ-id> <control name>
Prints one line per arm and a verdict line. No write, no vendor call. ASCII only.
"""
import hashlib
import json
import os
import sys

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # the worktree this file sits in
MAIN = os.environ.get("IRPT_LIVE_WALK") or os.path.join(
    ROOT, "org", "tier1_exec", "2.0.0_SA_COO", "deliverables", "IRPT_MVP_Y", "live_walk")
sys.path.insert(0, os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting", "ycharts", "extract"))
sys.path.insert(0, MAIN)

import case_trace  # noqa: E402
import certify  # noqa: E402


def main(argv):
    tenant, request_id, control = argv[1], argv[2], argv[3]
    t = case_trace.Trace(tenant)
    record = json.loads(t.req("analysis#%s#1" % request_id)["record"])
    comp_bytes, _ = t.blob(record["composition_ref"]["artifact_id"])
    bound = hashlib.sha256(comp_bytes).hexdigest() == record["composition_ref"]["sha256"]
    comp = json.loads(comp_bytes)
    chosen = [comp["resolved"]["comparison_catalog"][key]["name"] for key in comp["browser"]["comparison_keys"]]
    job = case_trace.item("irpt-jobs", {"tenant": {"S": tenant}, "job": {"S": request_id}})
    pdf_ref = json.loads(job["checkpoint_pdf"])["pdf_ref"]
    pdf_bytes, _ = t.blob(pdf_ref["artifact_id"])
    pdf_bound = hashlib.sha256(pdf_bytes).hexdigest() == pdf_ref["sha256"]
    arm_a = certify.missing_comparison_names(pdf_bytes, chosen)
    arm_b = certify.missing_comparison_names(pdf_bytes, chosen + [control])
    print("request %s tenant %s | composition bound %s | pdf sha256 %s bytes %d bound %s | chosen %r"
          % (request_id, tenant, bound, pdf_ref["sha256"][:16], len(pdf_bytes), pdf_bound, chosen))
    print("arm A chosen names        -> missing %r" % (arm_a,))
    print("arm B chosen plus control -> missing %r" % (arm_b,))
    ok = bound and pdf_bound and bool(chosen) and arm_a == [] and arm_b == [control]
    print("REAL RUN %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
