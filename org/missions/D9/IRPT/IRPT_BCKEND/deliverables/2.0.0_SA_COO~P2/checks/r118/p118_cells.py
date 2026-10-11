"""IRPT_BCKEND round 118 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order:
  IB118-1  IB-pr-420  apply IB-pr-416's irpt-performance-adapter and irpt-narrative on 0.7.0_AE_CloudOps~IB2 under the pair
                      (COO half @c362f7e0fb, CTO half @1dc8d0a860), with the three candidate source-map entries landed first.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB118-1-AC1  the three functions' entries in infra/aws/lambda/ci/lambda-source-map.json equal the candidate map's
               apart from artifact_sha256, which for the two applied functions equals the built digest (AMENDMENT 1; row D2-W278-S2), and the after-reads file names the commit that landed them. Base: FAIL (entries differ).
  IB118-1-AC2  live irpt-performance-adapter CodeSha256 == 9kYLdR64...; its after-reads row: BUILD_ONLY digest matched,
               not rolled back, live-call status not 500, 0 TypeError lines. Base: FAIL (live == o/643qVE...).
  IB118-1-AC3  live irpt-narrative CodeSha256 == x0SqAx2U...; its after-reads row as AC2's; ledger CLOSED. Base: FAIL.
"""
import json
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
A1 = D + "0.7.0_AE_CloudOps~IB2/IB118-1_two_function_release_after_reads.json"
CAND = D + "0.9.0_WK_IRPT_BCKEND~278/candidate_source_map.json"
REAL = "infra/aws/lambda/ci/lambda-source-map.json"
BUILT = {"irpt-performance-adapter": "9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=",
         "irpt-narrative": "x0SqAx2US8UXLnn7Xqy5l3Ttd0Iv1TZQ2jlxgCQtflU="}
MAP_FUNCTIONS = ("irpt-performance-adapter", "irpt-narrative", "irpt-status")


def live(root, fn):
    p = subprocess.run(["bash", str(root / ".tools" / "aws"), "lambda", "get-function-configuration", "--function-name", fn,
                        "--query", "CodeSha256", "--output", "text"], capture_output=True, timeout=100)
    return p.stdout.decode("utf-8", "replace").strip() if p.returncode == 0 else ""


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB118"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    def function_row(fn):
        got = live(root, fn)
        if got != BUILT[fn]:
            fail("%s live %r != built" % (fn, got))
        rows = [r for r in load(A1).get("functions") or [] if r.get("function") == fn]
        if len(rows) != 1:
            fail("%d after-reads row(s) for %s" % (len(rows), fn))
        r = rows[0]
        if r.get("built_sha256") != BUILT[fn] or r.get("build_only_digest_matched") is not True or r.get("rolled_back") is not False:
            fail("%s row %r" % (fn, {k: r.get(k) for k in ("built_sha256", "build_only_digest_matched", "rolled_back")}))
        lc = r.get("live_call") or {}
        if not isinstance(lc.get("status"), int) or lc.get("status") >= 500 or lc.get("typeerror_lines") != 0:
            fail("%s live_call %r" % (fn, lc))
        if not r.get("rollback_version"):
            fail("%s names no rollback_version" % fn)
        return r

    if cid == "IB118-1-AC1":
        cand = load(CAND).get("functions") or {}
        real = load(REAL).get("functions") or {}
        # AMENDMENT 1 (row D2-S68): build-and-upload.sh rewrites `artifact_sha256` to the DEPLOYED digest at the apply, so the
        # entries are compared without that field; for an applied function the field must then equal the signed built digest.
        def strip(e):
            return {k: v for k, v in (e or {}).items() if k != "artifact_sha256"}
        for fn in MAP_FUNCTIONS:
            if fn not in cand or strip(real.get(fn)) != strip(cand[fn]):
                fail("source-map entry of %s differs from the candidate beyond artifact_sha256" % fn)
            if fn in BUILT and (real.get(fn) or {}).get("artifact_sha256") != BUILT[fn]:
                fail("source-map artifact_sha256 of %s is not the signed built digest" % fn)
        if not load(A1).get("source_map_commit"):
            fail("after-reads names no source_map_commit")
        print("OK: 3 of 3 source-map entries equal the candidate; landing commit named")
    elif cid == "IB118-1-AC2":
        function_row("irpt-performance-adapter")
        print("OK: adapter live == built; digest matched; live call typed; not rolled back")
    elif cid == "IB118-1-AC3":
        function_row("irpt-narrative")
        led = load(A1).get("ledger") or {}
        if led.get("state") != "CLOSED":
            fail("ledger %r" % led)
        print("OK: narrative live == built; digest matched; live call typed; ledger CLOSED")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
