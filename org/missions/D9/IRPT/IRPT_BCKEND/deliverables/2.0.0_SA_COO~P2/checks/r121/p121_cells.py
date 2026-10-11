"""IRPT_BCKEND round 121 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one apply order:
  IB121-1  IB-pr-423  the vendor performance release applied on 0.7.0_AE_CloudOps~IB2 under the pair (COO half @468df7baa4,
                      CTO half @7a01aa805a): source map re-pinned, two session-read policies, then IB-pr-421's adapter zip.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB121-1-AC1  the adapter's source-map entry equals the IB-pr-421 candidate apart from artifact_sha256 (which the apply
               rewrites; it must equal the built digest), and the after-reads name the landing commit. Base: FAIL.
  IB121-1-AC2  the live role holds both session policies, each ONE statement granting only secretsmanager:GetSecretValue on
               its ONE expected secret ARN, and 9 inline policies in all. Base: FAIL (7 policies, neither present).
  IB121-1-AC3  live adapter CodeSha256 == OF+8j4uc...; after-reads: digest matched, not rolled back, live call typed with 0
               TypeError and 0 AccessDenied lines, ledger CLOSED, the close statement says APPLIED, UNEXERCISED, and a
               vendor reach (if any) carries its use record key. Base: FAIL (live == 9kYLdR64...).
"""
import json
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
A1 = D + "0.7.0_AE_CloudOps~IB2/IB121-1_vendor_path_release_after_reads.json"
CAND = D + "0.9.0_WK_IRPT_BCKEND~282/candidate_source_map.json"
REAL = "infra/aws/lambda/ci/lambda-source-map.json"
FN = "irpt-performance-adapter"
ROLE = "irpt-performance-adapter-role"
BUILT = "OF+8j4ucXsxwJ195NKEQZnma22T8bYVUriw9YP859RU="
GRANTS = {"irpt-performance-approved-session-policy": "arn:aws:secretsmanager:us-east-1:313476888478:secret:blackdiamond/cot/session-jnzOyC",
          "irpt-performance-approved-orion-session-policy": "arn:aws:secretsmanager:us-east-1:313476888478:secret:orion/jwt/current-ewrBtp"}


def aws(root, *args):
    p = subprocess.run(["bash", str(root / ".tools" / "aws")] + list(args), capture_output=True, timeout=50)
    return p.returncode, p.stdout.decode("utf-8", "replace").strip()


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB121"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    def aslist(v):
        return v if isinstance(v, list) else [v]

    if cid == "IB121-1-AC1":
        cand = (load(CAND).get("functions") or {}).get(FN)
        real = (load(REAL).get("functions") or {}).get(FN)
        if not cand or not real:
            fail("no %s entry in the candidate or the real map" % FN)

        def strip(e):
            return {k: v for k, v in e.items() if k != "artifact_sha256"}
        if strip(real) != strip(cand):
            fail("source-map entry differs from the candidate beyond artifact_sha256")
        if real.get("artifact_sha256") != BUILT:
            fail("source-map artifact_sha256 %r is not the built digest" % real.get("artifact_sha256"))
        if not load(A1).get("source_map_commit"):
            fail("after-reads names no source_map_commit")
        print("OK: adapter source-map entry equals the candidate; artifact_sha256 is the built digest; landing commit named")
    elif cid == "IB121-1-AC2":
        rc, out = aws(root, "iam", "list-role-policies", "--role-name", ROLE, "--query", "PolicyNames", "--output", "json")
        if rc != 0:
            fail("list-role-policies rc %d" % rc)
        names = json.loads(out or "[]")
        if len(names) != 9:
            fail("role holds %d inline policies, expected 9" % len(names))
        for name, arn in GRANTS.items():
            if name not in names:
                fail("role lacks %s" % name)
            rc, out = aws(root, "iam", "get-role-policy", "--role-name", ROLE, "--policy-name", name, "--query",
                          "PolicyDocument", "--output", "json")
            if rc != 0:
                fail("get-role-policy %s rc %d" % (name, rc))
            st = aslist(json.loads(out).get("Statement") or [])
            if len(st) != 1 or st[0].get("Effect") != "Allow" or aslist(st[0].get("Action")) != ["secretsmanager:GetSecretValue"] \
                    or aslist(st[0].get("Resource")) != [arn]:
                fail("%s statement is not the one signed grant" % name)
        print("OK: role holds 9 inline policies; both session policies are the single signed grants")
    elif cid == "IB121-1-AC3":
        rc, got = aws(root, "lambda", "get-function-configuration", "--function-name", FN, "--query", "CodeSha256", "--output", "text")
        if rc != 0 or got != BUILT:
            fail("adapter live %r != built" % got)
        a = load(A1)
        r = a.get("function") or {}
        if r.get("built_sha256") != BUILT or r.get("build_only_digest_matched") is not True or r.get("rolled_back") is not False:
            fail("function row %r" % {k: r.get(k) for k in ("built_sha256", "build_only_digest_matched", "rolled_back")})
        lc = r.get("live_call") or {}
        if not isinstance(lc.get("status"), int) or lc.get("status") >= 500 or lc.get("typeerror_lines") != 0 \
                or lc.get("accessdenied_lines") != 0:
            fail("live_call %r" % lc)
        if not isinstance(lc.get("vendor_reached"), bool) or (lc["vendor_reached"] and not lc.get("use_record_key")):
            fail("vendor_reached %r / use_record_key %r" % (lc.get("vendor_reached"), lc.get("use_record_key")))
        if (a.get("ledger") or {}).get("state") != "CLOSED":
            fail("ledger %r" % a.get("ledger"))
        if "APPLIED, UNEXERCISED" not in str(a.get("close_statement") or ""):
            fail("close_statement lacks 'APPLIED, UNEXERCISED'")
        print("OK: adapter live == built; live call typed, 0 TypeError, 0 AccessDenied; ledger CLOSED; close says APPLIED, UNEXERCISED")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
