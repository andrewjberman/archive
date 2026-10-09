"""IRPT_BCKEND round 100 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of apply order IB-pr-395: release IB-pr-390 (_authz served.py:
IB-pr-385 + IB-pr-387 + ALL never admits) on 6 of 8 hosts by 0.7.0_AE_CloudOps~IB2 (MSTR msg 2725), under COO half @567612e686 and CTO
half @b97ebb6b98 (msg 2726); Andrew's release-now (~V2 msg 2536).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB100-1-AC1  every artifact in IB-pr-390's census reads live (CodeSha256, now) equal to its built_sha256; the after-reads file A records
               ledger "CLOSED" with the pin and all six sha256 stated, and rolled_back false. Base: FAIL (live == live_before).
  IB100-1-AC2  A's replay_rerun_before_ledger has >= 10 arms, each "identical" or "expected-diff", with >= 1 negative control; and
               held_hosts_unchanged: irpt-holdings and irpt-narrative read live equal to their pre-apply CodeSha256. Base: FAIL (no A).
"""
import json
import subprocess
import sys
from pathlib import Path

CENSUS = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~201/IB97-3_release_census.json"
A = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/IB100-1_authz_release_after_reads.json"


def live(root, fn):
    p = subprocess.run(["bash", str(root / ".tools" / "aws"), "lambda", "get-function-configuration", "--function-name", fn,
                        "--query", "CodeSha256", "--output", "text"], capture_output=True, timeout=120)
    return p.returncode, p.stdout.decode("utf-8", "replace").strip()


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB100-1"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB100-1-AC1":
        arts = load(CENSUS).get("artifacts") or []
        if len(arts) != 6:
            fail("census has %d artifacts, want 6" % len(arts))
        for a in arts:
            rc, v = live(root, a["name"])
            if rc != 0 or v != a.get("built_sha256"):
                fail("%s live %r != built %r" % (a["name"], v, a.get("built_sha256")))
        d = load(A)
        led = d.get("ledger") or {}
        if led.get("state") != "CLOSED" or not led.get("pin") or len(led.get("sha256") or []) != 6 or d.get("rolled_back") is not False:
            fail("ledger %r rolled_back %r" % (led, d.get("rolled_back")))
        print("OK: 6 of 6 live == built; ledger CLOSED with pin + six sha256")
    elif cid == "IB100-1-AC2":
        d = load(A)
        arms = d.get("replay_rerun_before_ledger") or []
        if len(arms) < 10 or any(x.get("verdict") not in ("identical", "expected-diff") for x in arms) \
                or not any(x.get("negative_control") for x in arms):
            fail("replay_rerun_before_ledger %d arms %r" % (len(arms), arms[:2]))
        held = d.get("held_hosts_unchanged") or {}
        for fn in ("irpt-holdings", "irpt-narrative"):
            want = held.get(fn)
            rc, v = live(root, fn)
            if not want or rc != 0 or v != want:
                fail("%s live %r vs recorded pre-apply %r" % (fn, v, want))
        print("OK: %d replay arms before the ledger; both held hosts unchanged" % len(arms))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
