"""IRPT_BCKEND round 168 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one apply order:
  IB168-1  IB-pr-487  apply IB-pr-482's irpt-performance-adapter (the claim-by-status reader change, C-CHAINCLAIM) on 0.7.0_AE_CloudOps~IB2 under the
                      pair (COO half signed 2026-10-12T21:03:15Z, CTO half msg 6557), the one source-map re-pin landed first.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. Base: every criterion FAILs.
  IB168-1-AC1  the function's entry in infra/aws/lambda/ci/lambda-source-map.json equals the candidate map's entry apart from the keys a deploy record writes, and its
               artifact_sha256 equals the built digest; the after-reads file names the source-map commit, which touched only that file.
  IB168-1-AC2  the LIVE CodeSha256 of irpt-performance-adapter, read now, equals the built digest (so the apply landed and was not rolled back).
  IB168-1-AC3  the after-reads record: ledger CLOSED; the rollback S3 version named BEFORE the upload; BUILD_ONLY digest matched; plan 1 change 0 destroy; re-plan 0;
               not rolled back; 0 TypeError lines; (CTO half AMENDMENT 1, row S112) the kept selection refs read before and after: every readable ref's figure sha256
               equal and its claim equal to the PREDICTED claim, the two counts present, an unread ref counted with its reason and the SAME refusal code before and after (the import smoke), at least one readable; arm 1 live on a
               readable ref, arms 2-4 graded UNEXERCISED-LIVE with reasons; the persisted retained revisions COUNTED (0..2 x refs); no account id in the record.
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
        refs = a.get("refs") or {}
        reads = a.get("ref_reads") or []
        if not isinstance(refs.get("count"), int) or refs["count"] < 1 or len(reads) != refs["count"]:
            fail("refs.count must be an integer >= 1 and equal the number of ref_reads rows")
        readable = [x for x in reads if x.get("readable") is True]
        fallback = a.get("fallback") == "CTO-AMENDMENT-2-B"
        if not readable and not fallback:
            fail("no kept selection read before the upload and no fallback named: the apply should have stopped")
        for x in reads:
            if x.get("readable") is not True:
                if not x.get("unread_reason"):
                    fail("an unread ref needs its unread_reason (counted, not dropped)")
                rb, ra = x.get("refusal_code_before"), x.get("refusal_code_after")
                if not rb or rb != ra:
                    fail("ref %s: an unread ref is the import smoke, its refusal code must be the same before and after (got %r / %r)" % (x.get("n"), rb, ra))
                continue
            hb, ha = x.get("figure_sha256_before"), x.get("figure_sha256_after")
            if hb != ha or not re.fullmatch(r"[0-9a-f]{64}", str(ha or "")):
                fail("ref %s: the figure's sha256 must be equal before and after" % x.get("n"))
            if x.get("claim_predicted") is None or x.get("claim_after") != x.get("claim_predicted"):
                fail("ref %s: claim_after %r != predicted %r" % (x.get("n"), x.get("claim_after"), x.get("claim_predicted")))
            if x.get("counts_present_after") is not True:
                fail("ref %s: the two counts must appear after the apply" % x.get("n"))
        arms = a.get("direct_invoke_arms") or []
        by = {x.get("arm"): x for x in arms}
        if set(by) != {1, 2, 3, 4}:
            fail("direct_invoke_arms must hold arms 1, 2, 3 and 4, holds %s" % sorted(map(str, by)))
        a1 = by[1]
        if readable and (a1.get("exercised") is not True or a1.get("ref_n") not in [x.get("n") for x in readable]):
            fail("arm 1 must be exercised live on one of the readable refs (ref_n)")
        if not readable and (a1.get("exercised") is not False or a1.get("grade") != "UNEXERCISED-LIVE" or not a1.get("unexercised_reason")):
            fail("fallback: arm 1 must read exercised false, grade UNEXERCISED-LIVE, with its reason")
        for n in (2, 3, 4):
            if by[n].get("exercised") is not False or by[n].get("grade") != "UNEXERCISED-LIVE" or not by[n].get("unexercised_reason"):
                fail("arm %s must read exercised false, grade UNEXERCISED-LIVE, with its reason (the packet's offline replay)" % n)
        pr = a.get("persisted_retained_revisions")
        if not isinstance(pr, int) or isinstance(pr, bool) or pr < 0 or pr > 2 * refs["count"]:
            fail("persisted_retained_revisions must be an integer in 0..2 x refs.count (one invoke before, one after, per ref)")
        if not a.get("read_operation") or a.get("read_operation") != "performance-report":
            fail("read_operation must name performance-report, the function's one operation")
        raw = json.dumps(a)
        if re.search(r"(?<![0-9a-fA-F])\d{10,}(?![0-9a-fA-F])", raw):
            fail("the record carries a long digit run (an account id or a figure?)")
        print("OK: ledger CLOSED, rollback version named before upload, digest matched, plan 1/0, re-plan 0, %d of %d refs read with equal figures and predicted claims, %d retained revision(s) counted" % (len(readable), refs["count"], a["persisted_retained_revisions"]))
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
