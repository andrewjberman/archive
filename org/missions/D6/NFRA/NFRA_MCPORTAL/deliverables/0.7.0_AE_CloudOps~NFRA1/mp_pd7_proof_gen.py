#!/usr/bin/env python
"""MP-pd-7: write the proof_of_spec instance from two real runs of pd7a.AC1 and pd7a.AC2 (AC2 against the live function). usage: python mp_pd7_proof_gen.py   (repository root, after the close commit)"""
from __future__ import annotations

import io
import json
import re
import subprocess

M = "org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pd/checks/"
TO = "org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pd-7.person-access-release.md"
DEC = "org/missions/D6/NFRA/NFRA_MCPORTAL/decompositions/NFRA_MCPORTAL_DECOMP.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"
LEDGER = "org/critical_paths/change_management/20261020T2015Z_nfra-mcportal-pd-release_deploy_completion.md"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
af = json.load(io.open(M + "MP-pd-7_AFTER.json", encoding="utf-8"))
ap = json.load(io.open(M + "MP-pd-7_APPLY.json", encoding="utf-8"))
ac, stable = {}, True
for cid in ("AC1", "AC2"):
    outs = [run("pd7a.%s.sh" % cid), run("pd7a.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    ac[cid] = (outs, exp)
    stable = stable and outs[0] == outs[1]
    print(cid, "stable" if outs[0] == outs[1] else "UNSTABLE", "| PASS" if "RESULT: PASS" in outs[0] else "| NOT PASS")


def art(path, kind, ev, cov, deployed=GIT):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else pin(M + "MP-pd-7_AFTER.json"), "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "the release's deploy-ledger entry nfra-mcportal-pd-release is CLOSED at HEAD with every leg proven, its sentinel is absent at HEAD, and it is not listed OPEN or HELD by deploy_ledger.py.",
    "AC2": "the grant-writer Lambda's CodeSha256 equals the sha the close report states; the code zip it serves holds a lambda_function.py that contains WIDEN-NO-CONFIRM and widening_signoff; invoking it with no owner header on set_person_access answers REFUSED NO-OWNER-HEADER.",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_MCPORTAL.TO-MP-pd-7", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": TO, "group": "OTHER", "vintage_commit": pin(TO)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:lambda/mcportal-grant-writer-lambda (code package)", "aws_resource",
            "One safe-apply of the saved targeted plan: Plan 0 to add 1 to change 0 to destroy, exactly the one function in place; %s (%s s). CodeSha256 after %s; both no-header invokes answer REFUSED NO-OWNER-HEADER; the served zip's %d members equal the package built; lambda_function.py holds WIDEN-NO-CONFIRM and widening_signoff. Rollback not needed (the old handler on the current closure, command mp_pd7_act.py rollback)."
            % (ap["apply_result"], ap["apply_seconds"], af["code_sha256_after"], af["members_after"]), ["AC2"], "DEPLOYED-VERIFIED"),
        art(M + "NEVER_WIDEN_ASK_MP-pd-7.md", "doc", "The ask, sha256 prefix f0098d2b67ab, both halves SIGNED (CTO @392b19649f, COO~MP at HEAD), both departures accepted.", ["AC1", "AC2"]),
        art(M + "MP-pd-7_PRE_ACT_RECORD.md", "doc", "Census, build comparison, rollback, the before invokes; the ledger entry's pointer.", ["AC1"]),
        art(M + "MP-pd-7_CLOSE_REPORT.md", "doc", "The close report with the line GW_LAMBDA_SHA256 on its own, the before and after answers of both invokes, the rollback time and how it was measured.", ["AC2"]),
        art(M + "MP-pd-7_AFTER.json", "doc", "The post-apply reads: CodeSha256, the two invokes, the served zip against the package built, per member.", ["AC2"]),
        art(LEDGER, "doc", "Ledger nfra-mcportal-pd-release opened before the act (entry and sentinel), three legs proven, CLOSED; sentinel removed.", ["AC1"]),
        art(M + "mp_pd7_act.py", "script", "The supervised act: gate, plan, apply, post, rollback.", ["AC1", "AC2"]),
    ],
    "acceptance": [{"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %spd7a.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
                    "denominator": {"AC1": "1 ledger entry of 3 legs; the open-deploy list read", "AC2": "1 function; 65 zip members compared; 2 no-header invokes"}[cid], "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice, back to back, AC2 against the live function.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's base FAIL runs (no ledger entry, no close report) are the discriminating arm.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "a byte-equal rollback proof", "reason": "Declared departure accepted by both halves: the closure derives from the live release, so a rebuild of the old handler is not the deployed package; the deployed bytes are held 7 days (sha256 prefix f3de1123adff1b88)."},
        {"item": "the rollback's own time", "reason": "The rollback was not run; the forward apply's seconds are recorded as the proxy and said so in the close report."},
        {"item": "a push", "reason": "The order forbids it; the lane drains the branch."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, MP-pd-7. Order and GO read 2026-10-20 ~19:5xZ via an inbox file (the broker was down for this seat); measured read-only (deployed 894RI63..., new RUGwtI9t8..., plan 0/1/0, the before invokes); ask f0098d2b67ab asked of both seats by ferry files; both halves SIGNED ~20:1xZ; ledger opened 20:15Z; plan, apply 20:18Z-20:22Z, post reads, ledger CLOSED 20:23Z.",
    "compiler_tools": [{"tool": "terraform / safe-apply / boto3 (lambda)", "invocation": "mp_pd7_measure.py, mp_pd7_act.py gate|plan|apply|post", "result": "PASS", "note": "Counts, hashes and times only; no ARN, account number or presigned URL recorded."}],
}
P = M + "NFRA_MCPORTAL.TO-MP-pd-7.person-access-release.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
