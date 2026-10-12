"""IRPT_BCKEND round 168 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one apply order:
  IB168-1  IB-pr-487  apply IB-pr-482's irpt-performance-adapter (the claim-by-status reader change, C-CHAINCLAIM) on 0.7.0_AE_CloudOps~IB2 under the
                      pair (COO half signed 2026-10-12T21:03:15Z, CTO half msg 6557), the one source-map re-pin landed first.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. Base: every criterion FAILs.
  IB168-1-AC1  the function's entry in infra/aws/lambda/ci/lambda-source-map.json equals the candidate map's entry apart from the keys a deploy record writes, and its
               artifact_sha256 equals the built digest; the after-reads file names the source-map commit, which touched only that file.
  IB168-1-AC2  the LIVE CodeSha256 of irpt-performance-adapter, read now, equals the built digest (so the apply landed and was not rolled back).
  IB168-1-AC3  the after-reads record: ledger CLOSED; the rollback S3 version named BEFORE the upload; BUILD_ONLY digest matched; plan 1 change 0 destroy; re-plan 0;
               not rolled back; 0 TypeError lines; the four direct-invoke arms with each figure's sha256 unchanged and the claim as stated, arm 4 allowed UNEXERCISED with its
               reason; the persisted retained revisions COUNTED; no account id in the record.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
A1 = D + "0.7.0_AE_CloudOps~IB2/IB168-1_release_after_reads.json"
CAND = D + "0.9.0_WK_IRPT_BCKEND~337/candidate_source_map_482.json"
REAL = "infra/aws/lambda/ci/lambda-source-map.json"
FN = "irpt-performance-adapter"
BUILT = "abep4h7RngMS9JomQUdkcOT3EZ+W953OdxeK0HkdzFo="
LIVE_BEFORE = "kMB8xCI93/9QLUnzglVIs0EIRY07SSLBiU5ln8iJwUc="
DEPLOY_KEYS = {"artifact_sha256", "last_deployed_commit", "last_deployed_at", "recorded_by", "deploy_ledger", "deployed_code_sha256", "_deploy_note"}
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB168"))
    sys.exit(1)


def run(cmd, timeout=120):
    try:
        p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        fail("timeout: %s" % " ".join(cmd)[:100])
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def live():
    rc, out = run(["bash", str(ROOT / ".tools" / "aws"), "lambda", "get-function-configuration", "--function-name", FN, "--query", "CodeSha256", "--output", "text"])
    return out.strip() if rc == 0 else ""


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    arm = CID[8:]
    if arm == "AC1":
        real = load(REAL)["functions"].get(FN) or {}
        cand = load(CAND)["functions"].get(FN) or {}
        if not real or not cand:
            fail("the function entry is missing from the real or the candidate map")
        diff = [k for k in set(real) | set(cand) if k not in DEPLOY_KEYS and real.get(k) != cand.get(k)]
        if diff:
            fail("the real entry differs from the candidate entry in %s (the one re-pin has not landed, or more than it did)" % sorted(diff)[:4])
        if real.get("artifact_sha256") != BUILT:
            fail("artifact_sha256 %r != the built digest %s" % (real.get("artifact_sha256"), BUILT))
        a = load(A1)
        sc = str(a.get("source_map_commit", ""))
        if not re.fullmatch(r"[0-9a-f]{7,40}", sc):
            fail("source_map_commit")
        rc, out = run(["git", "show", "--name-only", "--format=", sc])
        names = [n for n in out.split() if n.strip()]
        if rc != 0 or names != [REAL]:
            fail("the source-map commit %s must touch only %s, touched %s" % (sc, REAL, names[:3]))
        print("OK: the entry equals the candidate apart from deploy-record keys; artifact_sha256 = the built digest; commit %s touched only the map" % sc[:10])
    elif arm == "AC2":
        got = live()
        if got != BUILT:
            fail("live CodeSha256 %r != the built %s (live before the apply was %s)" % (got, BUILT, LIVE_BEFORE))
        print("OK: live CodeSha256 equals the built digest")
    elif arm == "AC3":
        a = load(A1)
        led = a.get("ledger") or {}
        if led.get("state") != "CLOSED" or not led.get("slug"):
            fail("ledger %r" % led)
        if a.get("live_before") != LIVE_BEFORE or a.get("live_after") != BUILT:
            fail("live_before/live_after must read %s / %s" % (LIVE_BEFORE, BUILT))
        if not a.get("rollback_version") or a.get("rollback_version_named_before_upload") is not True:
            fail("the rollback S3 version must be named, and named BEFORE the upload")
        if a.get("build_only_digest_matched") is not True or a.get("build_only_digest") != BUILT:
            fail("build_only_digest_matched true with build_only_digest = the built digest")
        pl = a.get("plan") or {}
        if pl.get("changes") != 1 or pl.get("destroys") != 0 or a.get("re_plan_changes") != 0:
            fail("plan must read 1 change 0 destroy and the re-plan 0 changes")
        if a.get("rolled_back") is not False:
            fail("rolled_back must be false")
        lg = a.get("log") or {}
        if lg.get("typeerror_lines") != 0 or not lg.get("window_start"):
            fail("log.typeerror_lines must be 0 over a stated window_start")
        arms = a.get("direct_invoke_arms") or []
        names = {x.get("arm") for x in arms}
        if names != {1, 2, 3, 4}:
            fail("direct_invoke_arms must hold arms 1, 2, 3 and 4, holds %s" % sorted(map(str, names)))
        want = {1: "measured", 2: "inferred", 3: "inferred", 4: "inferred"}
        for x in arms:
            n = x["arm"]
            if x.get("exercised") is False:
                if n != 4 or not x.get("unexercised_reason"):
                    fail("only arm 4 may be UNEXERCISED, and with its reason")
                continue
            if x.get("figure_sha256_before") != x.get("figure_sha256_after") or not re.fullmatch(r"[0-9a-f]{64}", str(x.get("figure_sha256_after", ""))):
                fail("arm %s: the figure's sha256 must be equal before and after" % n)
            if x.get("claim_after") != want[n]:
                fail("arm %s: claim_after %r != %s" % (n, x.get("claim_after"), want[n]))
        if n_arms_ex(arms) < 3:
            fail("at least arms 1, 2 and 3 must be exercised")
        if not isinstance(a.get("persisted_retained_revisions"), int):
            fail("persisted_retained_revisions (the count of retained reports the invokes wrote) must be an integer")
        if not a.get("read_operation") or a.get("read_operation") != "performance-report":
            fail("read_operation must name performance-report, the function's one operation")
        raw = json.dumps(a)
        if re.search(r"(?<![0-9a-fA-F])\d{10,}(?![0-9a-fA-F])", raw):
            fail("the record carries a long digit run (an account id or a figure?)")
        print("OK: ledger CLOSED, rollback version named before upload, digest matched, plan 1/0, re-plan 0, %d arms, %d retained revision(s) counted" % (len(arms), a["persisted_retained_revisions"]))
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


def n_arms_ex(arms):
    return sum(1 for x in arms if x.get("exercised") is not False)


if __name__ == "__main__":
    main()
