"""apply5_checks.py -- the mechanical checks of IRPT_ANLREQ release 5 (irpt-status, build Iw3FADFr).

Usage:  python apply5_checks.py <check> [--root <repo root>]

  live      the live function's CodeSha256 is the release build (one get-function-configuration)   -> APPLY5-LIVE-OK
  record    the dell2 applier's record: R0, R1, R8 and the plan read, ledger closed, map moved      -> APPLY5-RECORD-OK
  reads     the laptop applier's after-reads R2..R7, each true or (R4 only) ABSENT with its census  -> APPLY5-READS-OK

Every check prints its token on the last line, or the same token with -FAIL after one FAIL line per problem.
The checks read files and one live resource; they write nothing.
"""
import json
import sys
from pathlib import Path

BUILT = "Iw3FADFrSt5G97zRTSkvZ7txSlXnaNQNpgPZi+G5tw0="
ROLLBACK = "6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc="
SLUG = "irpt-anlreq-r5-irpt-status-20261011"
RECORD = "org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r5/R5_apply_record.json"
READS = "org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y5_after_reads_result.json"
TOKENS = {"live": "APPLY5-LIVE", "record": "APPLY5-RECORD", "reads": "APPLY5-READS"}


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def live_sha(root):
    try:
        import boto3
        return 0, [boto3.client("lambda").get_function_configuration(FunctionName="irpt-status")["CodeSha256"]]
    except Exception as exc:  # noqa: BLE001 -- any failure of the one read is reported as a failed read, never as a digest
        return 1, ["READ-FAILED %s" % type(exc).__name__]


def load(root, rel, problems):
    path = root / rel
    if not path.is_file():
        problems.append("no %s" % rel)
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS:
        print(__doc__)
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1]) if "--root" in argv else Path(__file__).resolve().parents[8]
    problems = []
    if check == "live":
        rc, last = live_sha(root)
        print("live irpt-status CodeSha256: %s (rc=%d)" % (last[0], rc))
        if rc != 0 or last[0] != BUILT:
            problems.append("live is not the release build %s" % BUILT[:8])
        return finish(check, problems)
    if check == "record":
        doc = load(root, RECORD, problems)
        if doc is None:
            return finish(check, problems)
        if doc.get("R0", {}).get("code_sha256") != ROLLBACK or not doc.get("R0", {}).get("replaced_s3_object_version"):
            problems.append("R0 does not record the rollback digest and the S3 object version it replaced")
        if doc.get("R1", {}).get("code_sha256") != BUILT:
            problems.append("R1 does not record the release build as live")
        plan = doc.get("plan", {})
        if plan.get("resources_to_change") != 1 or plan.get("to_add") != 0 or plan.get("to_destroy") != 0:
            problems.append("the plan did not read exactly one resource to change, 0 to add, 0 to destroy")
        if doc.get("replan_after", {}).get("changes") != 0:
            problems.append("the re-plan after the apply does not read 0 changes")
        r8 = doc.get("R8") or []
        if not r8 or any(row.get("same_status_and_keys") is not True for row in r8):
            problems.append("R8 is absent or a tenant's status read differs from before the apply")
        print("R8 tenants read: %d" % len(r8))
        if (root / "org/critical_paths/.open_deploys" / (SLUG + ".json")).exists():
            problems.append("the ledger sentinel %s is still open" % SLUG)
        entry = json.loads((root / "infra/aws/lambda/ci/lambda-source-map.json").read_text(encoding="utf-8"))["functions"]["irpt-status"]
        if entry.get("artifact_sha256") != BUILT or entry.get("deployed_code_sha256") != BUILT:
            problems.append("the source map's artifact_sha256 and deployed_code_sha256 do not both read the release build (row D2-S33)")
        return finish(check, problems)
    doc = load(root, READS, problems)
    if doc is None:
        return finish(check, problems)
    if doc.get("release_under_test", {}).get("code_sha256") != BUILT or doc.get("release_under_test", {}).get("claim") != "measured":
        problems.append("the reads do not state, as measured, that they ran on the release build")
    reads = doc.get("reads") or {}
    for key in ("R2", "R3", "R5", "R6", "R7"):
        if reads.get(key, {}).get("result") is not True:
            problems.append("%s is not true: %r" % (key, reads.get(key, {}).get("result")))
    r4 = reads.get("R4", {})
    if r4.get("result") is not True and not (r4.get("result") == "ABSENT" and isinstance(r4.get("census"), dict)
                                             and isinstance(r4["census"].get("denominator"), int)):
        problems.append("R4 is neither true nor ABSENT with a census that prints its denominator")
    print("reads %s" % {key: reads.get(key, {}).get("result") for key in ("R2", "R3", "R4", "R5", "R6", "R7")})
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
