"""IRPT_BCKEND round 64 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-342 (directory-coverage census).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s and reads only the committed census file.

  IB64-1-AC1  IB64-1_directory_coverage.json: granted_total and not_in_directory_total are numbers with their sources named;
              len(accounts) == not_in_directory_total; every account carries a firm, a reason from the file's own declared
              reason set, and the evidence that placed it there; by_reason sums to not_in_directory_total; UNEXPLAINED (if
              declared) is counted, never hidden. Base: FAIL (no file).
  IB64-G-144  A GUARD: worker ~144's commits touch only its grant. Base: PASS.
"""
import json
import subprocess
import sys
from pathlib import Path

BASE = "33949e002d"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
OUT = P + "/deliverables/0.9.0_WK_IRPT_BCKEND~144/IB64-1_directory_coverage.json"
GRANT = (P + "/surprise-channel/investigations/INVESTIGATION_v1.md", P + "/task-orders/IRPT_BCKEND.TO-IB-pr-342.",
         P + "/deliverables/0.9.0_WK_IRPT_BCKEND~144/")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB64"))
        sys.exit(1)

    if cid == "IB64-1-AC1":
        f = root / OUT
        if not f.is_file():
            fail("no %s" % OUT)
        d = json.loads(f.read_text(encoding="utf-8"))
        for k in ("granted_total", "not_in_directory_total"):
            if not isinstance(d.get(k), int):
                fail("%s is not a number" % k)
        if not d.get("sources"):
            fail("no sources named")
        reasons = d.get("reason_set") or []
        accts = d.get("accounts") or []
        if not reasons:
            fail("no declared reason_set")
        if len(accts) != d["not_in_directory_total"]:
            fail("accounts listed %d != not_in_directory_total %d" % (len(accts), d["not_in_directory_total"]))
        for a in accts:
            if not a.get("firm") or a.get("reason") not in reasons or not a.get("evidence"):
                fail("account %r lacks firm / declared reason / evidence" % (a.get("account") or a)[:80])
        by = d.get("by_reason") or {}
        if sum(by.values()) != d["not_in_directory_total"] or set(by) - set(reasons):
            fail("by_reason %r does not sum to %d over the declared set" % (by, d["not_in_directory_total"]))
        print("OK: %d of %d granted not in directory; by_reason %s" % (d["not_in_directory_total"], d["granted_total"], by))
    elif cid == "IB64-G-144":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~144", "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(GRANT)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~144's grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
