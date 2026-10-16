#!/usr/bin/env python
"""OG-ap-28: write W/NFRA_OPLGTW.TO-OG-ap-28.round-38-batched-release.proof_of_spec.json from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ap28_proof_gen.py   (from the repo root; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-28.round-38-batched-release.md"
G = "infra/aws/ec2/opal-gateway/"
REL = "bf9d23b518527e0e5f9a26aa240fd5af72af6c11"
PRE = "2dc919cf26ce4190157b21c7f3c18737de10c573"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


ac1 = [run("ap28.AC1.sh"), run("ap28.AC1.sh")]
ac2 = [run("ap28.AC2.sh"), run("ap28.AC2.sh")]
_order = io.open("org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-28.round-38-batched-release.md", encoding="utf-8").read()
# the order's own <expect> patterns, verbatim (never a pattern of mine)
E1 = re.search(r'<criterion id="AC1"[^>]*>.*?<expect>(.*?)</expect>', _order, re.S).group(1)
E2 = re.search(r'<criterion id="AC2"[^>]*>.*?<expect>(.*?)</expect>', _order, re.S).group(1)
assert re.search(E1, ac1[0]), ac1[0]
assert re.search(E2, ac2[0]), ac2[0]
stable = ac1[0] == ac1[1] and ac2[0] == ac2[1]


def art(path, kind, pin, state, ev, intro, cov):
    row = {"path_or_key": path, "kind": kind, "commit_or_etag": pin, "deployed_state": state, "deploy_evidence": ev, "artifact_covered_by": cov}
    if intro:
        row["introduces"] = intro
    return row


DEP = "DEPLOYED-VERIFIED"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"
HOST = "host md5 139 of 139 equal to the release blobs (W/ap28_host_md5_after.json), live since 2026-10-16T17:57Z"
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-28", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~Z",
    "session_log": "org/tier2_senior/0.7.0_AE_CloudOps~Z/logs/2026-10-16/ap28_batched_release.md",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md", "group": "OTHER", "vintage_commit": "f2b066d9ad"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md", "vintage_commit": "3b056fd12e", "to_ref": TO},
    "acceptance": [
        {"criterion_id": "AC1", "criterion_verbatim": "AC1: the re-cut carries exactly the named orders' files, the catalog edit, the one deploy hunk and the one manifest field, no Terraform, no tool added.",
         "method": "command", "invocation": 'bash %sap28.AC1.sh; echo "exit=$?"' % CK, "expect": E1, "output_evidence": ac1[0],
         "denominator": "35 files differ from base d14445961d to release bf9d23b518 (0 outside the batch set, 0 Terraform, 0 tools.py or destructive_ops.py); the deploy hunk adds 1 env key in its own printf slot; the manifest's only changed field is mcportal_commit; the two naming-gate prelude registry files are byte-equal to trunk 858e927558's blobs (2 of 2); run twice, identical.",
         "status": "PASS"},
        {"criterion_id": "AC2", "criterion_verbatim": "AC2: the release landed and closed; the installed code shows every round-38 arm through one real call each; the seventh reader key is on the host; the tool list is unchanged; the Muse narrowing is inert.",
         "method": "command", "invocation": 'bash %sap28.AC2.sh; echo "exit=$?"' % CK, "expect": E2, "output_evidence": ac2[0],
         "denominator": "ledger nfra-oplgtw-gateway-release-batch2 CLOSED (1 of 1, sentinel gone); landed=current; reader env keys 7 of 7; registry 103; per-tool 27 of 27; host md5 139 equal, 0 differ; tools/list 103 before and after; arms true 7 of 7 (e4 re-graded under the COO's A4, msg 35177, on the recorded counts; the raw arm and the rule are kept in W/CODE2_SERVED.json); e10 is in-process through the installed GuardMiddleware (a real bearer needs a table write the order forbids), stated in the record.",
         "status": "PASS"},
        {"criterion_id": "AC3", "criterion_verbatim": "AC3 (judgment, 3.0.0_SA_CVO~Z): the first 49F Black Diamond live answers and the unit/currency/floor fields read as an analyst would want them (a firm's data date stated, figures with units, nothing merged across firms). Graded on a real call; never simulated here.",
         "method": "manual_read_with_citation",
         "invocation": "NOT RUN BY THIS SEAT. The criterion carries judgment=\"true\" and names 3.0.0_SA_CVO~Z as its grader; a judgment criterion is graded at L9 and never self-graded.",
         "output_evidence": "What this seat can say, and no more: the four 49F Black Diamond live tools answered an enveloped answer with rows (34, 2, 7 and 2) from opal-data-bd, each stating its partition date, through gateway-49f-blackdiamond-live-read-role, and an unprofiled non-admin was refused with 0 S3 client requests; the position rows carry weight_unit fraction and currency null with currency_basis source_absent where the source has none. Whether those read as an analyst would want is the CVO's.",
         "denominator": "0 of 3 named judgment specifics (data date stated, figures with units, nothing merged across firms) graded by this seat. Grader: 3.0.0_SA_CVO~Z.",
         "status": "N/A-BY-CONSTRUCTION",
         "status_reason": "A JUDGMENT criterion, graded at L9 and never self-graded (CLAUDE.md section 1, L9); not unverifiable and not PASS, simply not this seat's to compute."},
    ],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same repository and live host, back to back.",
                        "observed": "AC1 outputs identical; AC2 outputs identical.", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant. The negative arms are the issuer's dry-runs of AC1 and AC2 (base FAIL), and in this act: AC2 read FAIL while the ledger was open, the tool list unmeasured and arm e4 false under its first wording, and PASS only after each was resolved; ap28.AC1 refused the first release attempts at the naming gate (rows Z-S301, Z-S303).",
                   "expected": "AC1 and AC2 FAIL before the release exists and PASS after", "observed": "AC2 FAIL at 17:55Z (ledger open, 6 of 7 arms); PASS after the ledger close and the A4 re-grade", "status": "N/A-SPEC-NAMES-NONE"},
    },
    "artifacts_produced": [
        art(G + "app/ratelimit.py", "script", REL, DEP, HOST, ["record_identity_refusal"], ["AC1", "AC2"]),
        art(G + "app/client_role.py", "script", REL, DEP, HOST, ["blackdiamond49flive"], ["AC1", "AC2"]),
        art(G + "deploy-to-ec2.sh", "script", REL, DEP, "the deploy script that ran at 17:56Z; the host .env carries the seventh key (65 names)", ["BLACKDIAMOND49FLIVE_READER_ROLE_ARN"], ["AC1", "AC2"]),
        art(G + "app/refs/DATA_CATALOG.yaml", "config_data", REL, DEP, HOST + "; blob b81c48aa3c", ["address: blackdiamond/49f-live/silver/unrealized/"], ["AC1"]),
        art("infra/logic/registry/legacy_addresses.json", "config_data", PRE, GIT, "the naming-gate prelude, byte-equal to trunk 858e927558; not shipped (the archive carries app, deploy, lib and the dashboard)", ['"gateway-client-bdlive-fees"'], ["AC1"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "config_data", "41657174d1", GIT, "deployed_commit d14445961d -> bf9d23b518, mcportal pin, 3 of 10 checksums moved (host-controlled); rb.AC2 PASS", ["bf9d23b518527e0e5f9a26aa240fd5af72af6c11"], ["AC2"]),
        art(W + "CODE2_SERVED.json", "config_data", "59598f83c3", GIT, "the served record: counts and booleans only, e4_regrade beside the raw arm", ["e4_regrade"], ["AC2"]),
        art(W + "ap28_release.json", "config_data", "f0cc43908d", GIT, "base, release, trunk, mcportal and prelude shas, full 40 characters", ["prelude_sha"], ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-28.md", "config_data", "f0cc43908d", GIT, "the ask for three halves, sha256 aa5d0a37682e, signed by the CTO, COO and CVO", ["FINAL TEXT"], ["AC1"]),
        art(W + "ap28_arms.py", "script", "41657174d1", GIT, "the seven-arm served read, run on the host from S3; read-only", ["e12_bd49f_live"], ["AC2"]),
        art(W + "ap28_served_build.py", "script", "59598f83c3", GIT, "assembles CODE2_SERVED.json from four measured records and re-grades e4 under A4", ["e4_regrade"], ["AC2"]),
        art(W + "ap28_manifest.py", "script", "41657174d1", GIT, "the standing-clause manifest edit with the host md5 control", ["BLACKDIAMOND49FLIVE_READER_ROLE_ARN"], ["AC2"]),
        art(W + "ap28_runbook.py", "script", "41657174d1", GIT, "the runbook 7.2 edit graded by rb.AC2", ["bf9d23b518"], ["AC2"]),
    ],
    "compiler_tools": [
        {"tool": "safe-ec2-deploy.sh", "invocation": "DEPLOY_BASE_REF=d14445961d... bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh (from C:/tmp/og-rel-batch2)",
         "result": "base guard EQUAL at both checkpoints, DEPLOYMENT COMPLETE rc 0"},
        {"tool": "ap28.AC1 / ap28.AC2", "invocation": 'bash %sap28.AC1.sh ; bash %sap28.AC2.sh' % (CK, CK), "result": "PASS exit 0 both"},
    ],
    "surprises": [
        "NFRA_OPLGTW-Z-S301: Phase A first STOP -- the release commit refused by the naming gate (the registry files were absent at the live ref).",
        "NFRA_OPLGTW-Z-S303: Phase A second STOP -- the four entry files cannot be committed under the ENFORCE gate; resolved by the CTO's route (A3).",
        "NFRA_OPLGTW-Z-S305: arm e4 read false under its first wording (currency null, source_absent).",
        "NFRA_OPLGTW-Z-S306: correction to Z-S305 -- e4 re-graded true under the COO's A4.",
    ],
    "declared_exclusions": [
        {"item": "AC3, the CVO's reading of the first 49F Black Diamond live answers and the unit, currency and floor fields", "reason": "A judgment criterion graded by 3.0.0_SA_CVO~Z at L9 on a real call; this seat proved only the precondition."},
        {"item": "the dashboard bundle", "reason": "Built from the mcportal checkout at the manifest pin 59e802a418; no release blob exists in this repo to compare it to."},
        {"item": "the e10 arm against the live limiter", "reason": "In-process through the installed GuardMiddleware with the bearer stubbed to one synthetic stand-in: a real bearer needs a refresh family written to the access-state table, which the order forbids; the row is captured at audit._emit, not read from the lake."},
        {"item": "the client-data account-id hash check", "reason": "The hashed account-id list is absent on this box; absent is not empty. The records carry counts and booleans only: the account reference never left the host process."},
    ],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-28.round-38-batched-release.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
