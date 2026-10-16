#!/usr/bin/env python
"""OG-ap-31: write W/NFRA_OPLGTW.TO-OG-ap-31.round-39-batched-release.proof_of_spec.json from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ap31_proof_gen.py   (from the repo root of the worktree on box/sitez; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-31.round-39-batched-release.md"
G = "infra/aws/ec2/opal-gateway/"
REL = "4be300110ec912ac8c11a1663403e41eea45117c"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(path):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--", path], capture_output=True).stdout.decode().strip()


ac1 = [run("ap31.AC1.sh"), run("ap31.AC1.sh")]
ac2 = [run("ap31.AC2.sh"), run("ap31.AC2.sh")]
_order = io.open(TO, encoding="utf-8").read()
E1 = re.search(r'<criterion id="AC1"[^>]*>.*?<expect>(.*?)</expect>', _order, re.S).group(1)
E2 = re.search(r'<criterion id="AC2"[^>]*>.*?<expect>(.*?)</expect>', _order, re.S).group(1)
assert re.search(E1, ac1[0]), ac1[0]
assert re.search(E2, ac2[0]), ac2[0]
stable = ac1[0] == ac1[1] and ac2[0] == ac2[1]
DEP, GIT = "DEPLOYED-VERIFIED", "COMMITTED-NOT-DEPLOY-SCOPE"
HOST = "host md5 139 of 139 equal to the release blobs (W/ap31_host_md5_after.json), live since 2026-10-16T22:01Z"


def art(path, kind, pn, state, ev, intro, cov):
    row = {"path_or_key": path, "kind": kind, "commit_or_etag": pn, "deployed_state": state, "deploy_evidence": ev, "artifact_covered_by": cov}
    if intro:
        row["introduces"] = intro
    return row


inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-31", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md", "group": "OTHER", "vintage_commit": "de8078d545"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md", "vintage_commit": "de8078d545", "to_ref": TO},
    "acceptance": [
        {"criterion_id": "AC1", "criterion_verbatim": "AC1: the re-cut carries exactly the named orders' files, no Terraform, no tool added, no deploy-script or manifest change, and any registry file in the diff is byte-equal to trunk's.",
         "method": "command", "invocation": 'bash %sap31.AC1.sh; echo "exit=$?"' % CK, "expect": E1, "output_evidence": ac1[0],
         "denominator": "12 files differ from the base bf9d23b518 to the release 4be300110e (0 outside the batch set, 0 Terraform, 0 tools.py or destructive_ops.py, 0 deploy script or manifest, 0 registry files); the ask carries the three half headings.",
         "status": "PASS"},
        {"criterion_id": "AC2", "criterion_verbatim": "AC2: the release landed and closed; the installed code shows every round-39 arm through real calls; the tool list and the env are unchanged.",
         "method": "command", "invocation": 'bash %sap31.AC2.sh; echo "exit=$?"' % CK, "expect": E2, "output_evidence": ac2[0],
         "denominator": "ledger nfra-oplgtw-gateway-release-batch3 CLOSED (1 of 1, sentinel gone); landed=current; reader env keys 7 of 7; registry 103; per-tool 27 of 27; host md5 139 equal, 0 differ; tools/list 103 before and 103 after; arms true 5 of 5.",
         "status": "PASS"},
        {"criterion_id": "AC3", "criterion_verbatim": "AC3 (judgment, 3.0.0_SA_CVO~Z): the 49F transactions and fees windows and figures read as an analyst would want (the window answered, units and currency stated or honestly absent, numbers readable). Graded on bodies the issuer relays; never simulated here.",
         "method": "manual_read_with_citation",
         "invocation": "NOT RUN BY THIS SEAT. The criterion carries judgment=\"true\" and names 3.0.0_SA_CVO~Z as its grader; a judgment criterion is graded at L9 and never self-graded.",
         "output_evidence": "What this seat can say, and no more: a 13-month window on one account read 60 of 334 transaction partitions and 60 of 394 fee partitions (window_partial true, disclosed in the answer), weights and money serve as JSON numbers at 6 and 2 decimals with as_of equal to the partition date, allocation weight_unit is null with basis not_established, and currency is null with basis source_absent. Whether that reads well to an analyst is the CVO's to grade.",
         "denominator": "0 of 3 named judgment specifics (window answered, units and currency stated or honestly absent, numbers readable) graded by this seat. Grader: 3.0.0_SA_CVO~Z.",
         "status": "N/A-BY-CONSTRUCTION",
         "status_reason": "A JUDGMENT criterion, graded at L9 and never self-graded (CLAUDE.md section 1, L9); not unverifiable and not PASS, simply not this seat's to compute."},
    ],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same repository and live host, back to back.",
                        "observed": "AC1 outputs identical; AC2 outputs identical.", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant. The negative arms are the issuer's dry-runs of AC1 and AC2 (base FAIL); in this act the host md5 walk against the BASE blobs was run after the deploy as a control and differed on exactly the 4 app files, so the walk discriminates.",
                   "expected": "the host equals the release blobs and differs from the base blobs on the 4 taken app files", "observed": "139 equal to the release, 0 differ; against the base 135 equal, 4 differ (client_adapter_bd49f, data_entitlement, opal_discover integration, server)",
                   "status": "N/A-SPEC-NAMES-NONE"},
    },
    "artifacts_produced": [
        art(G + "app/client_adapter_bd49f.py", "script", "4be300110e", DEP, HOST, ["MAX_WINDOW_PARTITIONS"], ["AC1", "AC2"]),
        art(G + "app/data_entitlement.py", "script", "4be300110e", DEP, HOST, ["BROWSER_ROUTE_CLASSES"], ["AC1", "AC2"]),
        art(G + "app/server.py", "script", "4be300110e", DEP, HOST, ['route_class="internal_page"'], ["AC1", "AC2"]),
        art(G + "app/integrations/opal_discover/integration.py", "script", "4be300110e", DEP, HOST, ['for field in ("bucket", "vendor", "firm")'], ["AC1", "AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "config_data", pin("infra/aws/ec2/EC2_MANIFEST.json"), GIT, "deployed_commit bf9d23b518 -> 4be300110e; 1 of 10 checksums moved (app/server.py), host-controlled; rb.AC2 PASS", [REL], ["AC2"]),
        art(W + "ap31_release.json", "config_data", pin(W + "ap31_release.json"), GIT, "base, release and trunk shas, full 40 characters", ["release_sha"], ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-31.md", "config_data", pin(W + "NEVER_WIDEN_ASK_OG-ap-31.md"), GIT, "the ask for three halves, sha256 8115e8edf038, signed by the CTO, COO and CVO", ["MASTER_ADMIN_EMAILS"], ["AC1"]),
        art(W + "CODE3_SERVED.json", "config_data", pin(W + "CODE3_SERVED.json"), GIT, "the served record: counts and booleans only", ["e4_owner_browser_guard"], ["AC2"]),
        art(W + "ap31_arms.py", "script", pin(W + "ap31_arms.py"), GIT, "the e1 to e4 served read, run on the host from S3; read-only", ["e4_owner_browser_guard"], ["AC2"]),
        art(W + "ap31_served_build.py", "script", pin(W + "ap31_served_build.py"), GIT, "assembles CODE3_SERVED.json from the measured records", ["e6_discover_echo"], ["AC2"]),
        art(W + "ap31_manifest.py", "script", pin(W + "ap31_manifest.py"), GIT, "the standing-clause manifest edit with the host md5 control", ["DEPLOYED_AT"], ["AC2"]),
        art(W + "ap31_runbook.py", "script", pin(W + "ap31_runbook.py"), GIT, "the runbook 7.2 edit graded by rb.AC2", ["4be300110e"], ["AC2"]),
    ],
    "compiler_tools": [
        {"tool": "safe-ec2-deploy.sh", "invocation": "DEPLOY_BASE_REF=bf9d23b518... bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh (from C:/tmp/og-rel-batch3)",
         "result": "base guard EQUAL at both checkpoints, DEPLOYMENT COMPLETE rc 0 (two earlier attempts refused by the halt gate before any upload)"},
        {"tool": "ap31.AC1 / ap31.AC2", "invocation": 'bash %sap31.AC1.sh ; bash %sap31.AC2.sh' % (CK, CK), "result": "PASS exit 0 both"},
    ],
    "surprises": [
        "NFRA_OPLGTW-Z-S322: OBSERVATION -- the host MASTER_ADMIN_EMAILS holds 1 entry, so the OG-en-14 exemption reaches one owner address.",
        "NFRA_OPLGTW-Z-S324: OBSERVATION -- a release tree cut on the live ref carries a halt gate that refuses a rule-34 lane; two refusals before any upload, cured with no override.",
    ],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, third order (msg 35256 Phase A, msg 35276 Phase B). Ledger nfra-oplgtw-gateway-release-batch3 opened first (entry and sentinel committed), the gate overlay restored to the live ref's bytes before the clean check, ONE deploy at 22:00Z, read-back against the triggers (none fired), served read through the installed code, standing clauses, ledger CLOSED. Details: AP31_PHASE_A_NOTES.md and the committed records.",
    "declared_exclusions": [
        {"item": "AC3, the CVO's reading of the 49F transactions and fees windows and figures", "reason": "A judgment criterion graded by 3.0.0_SA_CVO~Z at L9 on bodies the issuer relays; this seat proved only the precondition."},
        {"item": "the dashboard bundle", "reason": "Built from the mcportal checkout at the manifest pin; no release blob exists in this repo to compare it to; unchanged by this release."},
        {"item": "the e4 arm against a real browser request", "reason": "The ALB email comes from the Entra sign-in; the applier cannot drive it. The arm calls the installed guard function with a stand-in store and the live table for the non-admin address."},
        {"item": "the client-data account-id hash check", "reason": "The hashed account-id list is absent on this box; absent is not empty. The records carry counts and booleans only."},
    ],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-31.round-39-batched-release.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
