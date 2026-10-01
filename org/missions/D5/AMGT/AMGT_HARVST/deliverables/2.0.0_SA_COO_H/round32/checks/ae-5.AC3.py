"""HVST-ae-5 AC3 (issuer, read-only): a deliberately stale session renews itself (FWD-11 DONE WHEN, the renewal half).

Reads `~91/ae5_renewal.json`, written by the worker's WORLD phase in the SAME run as AC2's record:
{"publisher", "staled_how", "before_sha256", "after_sha256", "written_to", "renewed_by": "browser",
 "operator_input_detected": bool, "post_renewal_status": int}

PASS requires: the stored session's hash changed (before != after); `renewed_by` is "browser" (no Python client wrote
it); `operator_input_detected` is false; and the first request after renewal returned 200.
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
RECORD = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~91/ae5_renewal.json")


def main():
    failures = []
    if not os.path.exists(RECORD):
        print("RECORD: absent (%s)" % RECORD)
        print("AC3 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no renewal record")
        return 1
    r = json.load(open(RECORD, encoding="utf-8"))
    print("RENEWAL: %s staled by %s; %s -> %s; written to %s; renewed_by %s; operator_input %s; status %s"
          % (r.get("publisher"), r.get("staled_how"), str(r.get("before_sha256"))[:12], str(r.get("after_sha256"))[:12],
             r.get("written_to"), r.get("renewed_by"), r.get("operator_input_detected"), r.get("post_renewal_status")))
    if not r.get("before_sha256") or r.get("before_sha256") == r.get("after_sha256"):
        failures.append("the stored session did not change")
    if r.get("renewed_by") != "browser":
        failures.append("renewed_by is %r, not the browser" % r.get("renewed_by"))
    if r.get("operator_input_detected") is not False:
        failures.append("operator input detected or unrecorded")
    if r.get("post_renewal_status") != 200:
        failures.append("the first request after renewal returned %r" % r.get("post_renewal_status"))
    print("AC3 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
