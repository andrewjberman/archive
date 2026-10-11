"""ADVI_FIRMBKTS round 3 check for cell FB-f-5 (F4's own-firm admit exercised, row D1-W7-S1), issuer 2.0.0_SA_COO~B1.

--arms ownfirm --evidence FILE grades the evidence record written by r3_f4_send.py (4 arms):
  O1 the command ran on a named SSM-managed runner and reports Status Success
  O2 the principal that made the calls is an assumed `*-cot-*` role (its STS ARN is printed)
  O3 OWN: the role's GetObject of its own-grant key in opal-data-cottonwood SUCCEEDED (a byte count is printed), so
     the fence admits the own-firm role and the identity policy lets it through
  O4 the difference controls: the same role's read of opal-data-inflection was REFUSED with an explicit deny in a
     resource-based policy (the fence), and its GetObject of a key its identity policy does not grant in
     opal-data-cottonwood was refused by the identity side, NOT by that resource-policy deny
Never edit this file. Plain ASCII; the last line carries the arm count.
"""
import argparse
import fnmatch
import json
import re
import sys

RUNNER_INSTANCES = {"i-0167fd745ad906a66"}
ROLE_GLOB = "arn:aws:sts::313476888478:assumed-role/*-cot-*/*"
FENCE_DENY = "explicit deny in a resource-based policy"
IDENTITY_DENY = "no identity-based policy allows"


def ownfirm(path):
    with open(path, encoding="utf-8") as fh:
        rec = json.load(fh)
    inv = rec.get("invocation") or {}
    out = str(inv.get("StandardOutputContent", ""))
    res = []
    res.append(("O1 the command ran on a named SSM-managed runner and reports Status Success",
                inv.get("Status") == "Success" and inv.get("InstanceId") in RUNNER_INSTANCES
                and bool(rec.get("command_id"))))
    caller = re.search(r"^CALLER: (\S+)", out, re.M)
    res.append(("O2 the principal that made the calls is an assumed `*-cot-*` role (its STS ARN is printed)",
                bool(caller) and fnmatch.fnmatch(caller.group(1), ROLE_GLOB)))
    own = re.search(r"^OWN: (.*)$", out, re.M)
    res.append(("O3 the role's GetObject of its own-grant key in opal-data-cottonwood SUCCEEDED (a byte count is "
                "printed)", bool(own) and re.fullmatch(r"\s*[0-9]+\s*", own.group(1)) is not None
                and "Denied" not in own.group(1)))
    inf = re.search(r"^INF: (.*)$", out, re.M)
    outk = re.search(r"^OUT: (.*)$", out, re.M)
    res.append(("O4 the other firm's bucket refused the role by the fence's resource-policy deny, and an ungranted "
                "own-firm key was refused by the identity side, not by that deny",
                bool(inf) and FENCE_DENY in inf.group(1) and bool(outk) and IDENTITY_DENY in outk.group(1)
                and FENCE_DENY not in outk.group(1)))
    print("  caller=%s" % (caller.group(1) if caller else None))
    print("  OWN: %s" % (own.group(1)[:120] if own else None))
    print("  OUT: %s" % (outk.group(1)[:200] if outk else None))
    print("  INF: %s" % (inf.group(1)[:200] if inf else None))
    return res, 4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("ownfirm",), required=True)
    ap.add_argument("--evidence", required=True)
    a = ap.parse_args()
    try:
        res, total = ownfirm(a.evidence)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable evidence (%s: %s)" % (type(e).__name__, str(e)[:160]))
        res, total = [("the evidence this arm grades is present", False)], 4
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 3 F4 OWNFIRM: %d of %d arms" % (n, total))
    sys.exit(0 if n == total else 1)


if __name__ == "__main__":
    main()
