"""apply6_checks.py -- the mechanical checks of IRPT_ANLREQ release 6 (the READY gate on the commentary composition read).

Usage:  python apply6_checks.py <check> [--root <repo root>]

  live      the live function's CodeSha256 is the release build (one get-function-configuration)  -> APPLY6-LIVE-OK
  record    the applier's record: the grant read as applied BEFORE the code, the build, the three
            after-reads, the ledger closed, the map corrected                                      -> APPLY6-RECORD-OK

Each check prints its token last, or the token with -FAIL after one FAIL line per problem. They read files and one live
resource and write nothing. The default root is this file's own repository root (ten parents up).
"""
import json
import sys
from pathlib import Path

FUNCTION = "irpt-commentary-composition-read-lambda"
BUILT = "DbvBUxTGlCsdG4htVOhbI4NBxBMNbmjD6BLpMGu2Yo4="
ROLLBACK = "ZZmWOFSA/GjO0d/cKHSm9G5+xDc5sNfEHOpbmfIabQ0="
SLUG = "irpt-anlreq-r6-composition-read-ready-gate-20261011"
RECORD = "org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r6/R6_apply_record.json"
TOKENS = {"live": "APPLY6-LIVE", "record": "APPLY6-RECORD"}


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS:
        print(__doc__)
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1]) if "--root" in argv else Path(__file__).resolve().parents[9]
    if not (root / ".tools").is_dir():
        print("FAIL: root %s is not the repository root (no .tools there)" % root)
        print("%s-FAIL" % TOKENS[check])
        return 1
    problems = []
    if check == "live":
        try:
            import boto3
            sha = boto3.client("lambda").get_function_configuration(FunctionName=FUNCTION)["CodeSha256"]
        except Exception as exc:  # noqa: BLE001 -- a failed read is reported as a failed read, never as a digest
            sha = "READ-FAILED %s" % type(exc).__name__
        print("live %s CodeSha256: %s" % (FUNCTION, sha))
        if sha != BUILT:
            problems.append("live is not the release build %s" % BUILT[:8])
        return finish(check, problems)
    path = root / RECORD
    if not path.is_file():
        return finish(check, ["no %s" % RECORD])
    doc = json.loads(path.read_text(encoding="utf-8"))
    step0 = doc.get("step0") or {}
    if step0.get("code_sha256") != ROLLBACK or not step0.get("replaced_s3_object_version"):
        problems.append("step0 does not record the rollback digest and the S3 object version it replaced")
    if step0.get("may_invoke") is not True:
        problems.append("step0 does not record that the box may invoke the function (a STOP if it may not)")
    grant = doc.get("grant") or {}
    if grant.get("plan") != {"resources_to_change": 1, "to_add": 0, "to_destroy": 0}:
        problems.append("the grant's plan did not read exactly one resource to change")
    if grant.get("G1_both_tables_in_S1") is not True or grant.get("G1_both_tables_in_S2") is not True:
        problems.append("G1 does not show both tables in S1 and S2 of the live role policy")
    g2, a1, a2, a3 = (doc.get(k) or {} for k in ("G2", "A1", "A2", "A3"))
    if g2.get("status") != "OK" or not g2.get("sha256") or g2.get("code_sha256_at_read") != ROLLBACK:
        problems.append("G2 is not an OK composition read with its sha256, made on the OLD code after the grant")
    code = doc.get("code") or {}
    if code.get("built_sha256") != BUILT or code.get("live_after") != BUILT or code.get("replan_changes") != 0:
        problems.append("the code step does not record the build, the live digest after, and a zero re-plan")
    if code.get("plan") != {"resources_to_change": 1, "to_add": 0, "to_destroy": 0}:
        problems.append("the code's plan did not read exactly one resource to change")
    if a1.get("status") != "OK" or a1.get("sha256") != g2.get("sha256") or a1.get("keys") != g2.get("keys"):
        problems.append("A1 does not equal G2 (status, sha256 and key names)")
    if a2.get("refusal") != "UNAVAILABLE" or a3.get("refusal") != "UNAVAILABLE":
        problems.append("A2 or A3 is not the refusal UNAVAILABLE")
    if any("body" in (doc.get(k) or {}) or "composition" in (doc.get(k) or {}) for k in ("G2", "A1")):
        problems.append("G2 or A1 carries composition content: the record holds a sha256, a status and key names only")
    if doc.get("rolled_back") is not False or doc.get("parity_skip_used") is not True:
        problems.append("rolled_back must read false and parity_skip_used true (the close says the skip in words)")
    if (root / "org/critical_paths/.open_deploys" / (SLUG + ".json")).exists():
        problems.append("the ledger sentinel %s is still open" % SLUG)
    entry = json.loads((root / "infra/aws/lambda/ci/lambda-source-map.json").read_text(encoding="utf-8"))["functions"][FUNCTION]
    if entry.get("artifact_sha256") != BUILT or not entry.get("last_deployed_commit") or not entry.get("last_deployed_at"):
        problems.append("the source map entry does not state the release (digest, last_deployed_commit, last_deployed_at)")
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
