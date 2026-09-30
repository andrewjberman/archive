"""HVST-ac-2 AC2 (issuer, read-only): what the sa probe MEASURED, and the standing of row Z-W37-S4 (the 09-29 HTTP 402).

Prints the account status/class, the standing (`CLEARED` on an authorized 200; `402 PERSISTS` on a 402; else the class),
and, when the listing ran, its status, hits, dated hits and pre-floor hits. PASS requires a recorded account status and
class, and -- when the account read was an authorized 200 -- a recorded listing result (status and class). An honest
refusal passes when recorded with its class and (where the transport kept one) its body.
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
WK = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~85")


def main():
    failures = []
    with open(os.path.join(WK, "ac2_probe.json"), encoding="utf-8") as fh:
        probe = json.load(fh)
    acct, lst = probe.get("account") or {}, probe.get("listing")
    status, klass = acct.get("status"), acct.get("class")
    if status == 200 and acct.get("authorized"):
        standing = "CLEARED (the stored sa token reads the account)"
    elif status == 402:
        standing = "402 PERSISTS"
    else:
        standing = "NOT CLEARED: status %s class %s" % (status, klass)
    print("ACCOUNT: status %s class %s authorized %s" % (status, klass, acct.get("authorized")))
    print("Z-W37-S4 STANDING: %s" % standing)
    if status is None or not klass:
        failures.append("account status or class not recorded")
    if status == 200 and acct.get("authorized"):
        if not lst:
            failures.append("authorized account but no listing recorded")
        else:
            print("LISTING (Lenovo, %s): status %s class %s hits %s dated %s pre_floor %s"
                  % ((probe.get("security") or {}).get("sa_symbol"), lst.get("status"), lst.get("class"), lst.get("hits"),
                     lst.get("dated"), lst.get("pre_floor")))
            if lst.get("status") is None or not lst.get("class"):
                failures.append("listing status or class not recorded")
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
