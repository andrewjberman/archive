"""IRPT_BCKEND round 122 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one ROLLBACK order:
  IB122-1  IB-pr-424  the vendor performance release (IB-pr-421/422/423) rolled back on 0.7.0_AE_CloudOps~IB2, on CTO msg
                      4624: it served Cottonwood a vendor-calculated return against ratified FWD-3.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB122-1-AC1  live adapter CodeSha256 == 9kYLdR64...; after-reads: one fresh non-49F request refused, no vendor reached,
               ledger CLOSED. Base: FAIL (live == OF+8j4uc...).
  IB122-1-AC2  the live role holds 7 inline policies and neither session policy. Base: FAIL (9 policies).
  IB122-1-AC3  the tree is back: performance/ product source and retained.tf equal their content at fb3bae3b99 (the commit
               before the release's build), and the adapter's source-map entry equals its entry before f5d33c7aa9 apart from
               artifact_sha256, which equals 9kYLdR64.... Base: FAIL (tree and entry carry the release).
"""
import json
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
A1 = D + "0.7.0_AE_CloudOps~IB2/IB122-1_vendor_path_rollback_after_reads.json"
REAL = "infra/aws/lambda/ci/lambda-source-map.json"
FN = "irpt-performance-adapter"
ROLE = "irpt-performance-adapter-role"
BEFORE = "9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A="
SESSION = ("irpt-performance-approved-session-policy", "irpt-performance-approved-orion-session-policy")
BASE_COMMIT = "fb3bae3b99"
MAP_BEFORE = "f5d33c7aa9^"
RESTORED = ("infra/aws/lambda/investor-reporting/performance", "infra/aws/terraform/investor-reporting/performance/retained.tf")


def run(args, root, timeout=50):
    p = subprocess.run(args, cwd=str(root), capture_output=True, timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", "replace").strip()


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    aws = ["bash", str(root / ".tools" / "aws")]

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB122"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    if cid == "IB122-1-AC1":
        rc, got = run(aws + ["lambda", "get-function-configuration", "--function-name", FN, "--query", "CodeSha256", "--output",
                             "text"], root)
        if rc != 0 or got != BEFORE:
            fail("adapter live %r != the pre-release digest" % got)
        a = load(A1)
        fr = a.get("fresh_request") or {}
        if fr.get("refused") is not True or fr.get("vendor_reached") is not False or not fr.get("public_reason_code"):
            fail("fresh_request %r" % fr)
        if (a.get("ledger") or {}).get("state") != "CLOSED":
            fail("ledger %r" % a.get("ledger"))
        print("OK: adapter live == 9kYLdR64; one fresh non-49F request refused %s, no vendor reached; ledger CLOSED" % fr["public_reason_code"])
    elif cid == "IB122-1-AC2":
        rc, out = run(aws + ["iam", "list-role-policies", "--role-name", ROLE, "--query", "PolicyNames", "--output", "json"], root)
        if rc != 0:
            fail("list-role-policies rc %d" % rc)
        names = json.loads(out or "[]")
        left = [n for n in SESSION if n in names]
        if len(names) != 7 or left:
            fail("role holds %d inline policies; session policies still present: %r" % (len(names), left))
        print("OK: role holds 7 inline policies; 0 of 2 session policies present")
    elif cid == "IB122-1-AC3":
        rc, out = run(["git", "diff", "--name-only", BASE_COMMIT, "HEAD", "--"] + list(RESTORED), root)
        if rc != 0:
            fail("git diff rc %d" % rc)
        if out:
            fail("%d path(s) still differ from %s: %s" % (len(out.splitlines()), BASE_COMMIT, out.splitlines()[0]))
        rc, old = run(["git", "show", "%s:%s" % (MAP_BEFORE, REAL)], root)
        if rc != 0:
            fail("git show of the pre-release source map rc %d" % rc)
        before = (json.loads(old).get("functions") or {}).get(FN)
        real = (load(REAL).get("functions") or {}).get(FN)
        if not before or not real:
            fail("no %s entry" % FN)

        def strip(e):
            return {k: v for k, v in e.items() if k != "artifact_sha256"}
        if strip(real) != strip(before):
            fail("source-map entry differs from its pre-release entry beyond artifact_sha256")
        if real.get("artifact_sha256") != BEFORE:
            fail("source-map artifact_sha256 %r is not the pre-release digest" % real.get("artifact_sha256"))
        print("OK: performance/ and retained.tf equal %s; the adapter's source-map entry is its pre-release entry" % BASE_COMMIT)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
