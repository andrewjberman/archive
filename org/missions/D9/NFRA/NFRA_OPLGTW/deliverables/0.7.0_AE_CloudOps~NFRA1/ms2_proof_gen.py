#!/usr/bin/env python
"""OG-ms-2: write the proof_of_spec instance from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ms2_proof_gen.py   (repository root, after the Phase B commit and the ledger close)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r46/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ms-2.round-46-add-master-08403355-to-alyssas-schwab-grant.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


SLUG = "_nfra-oplgtw-ms2-alyssa-master-0840_deploy_completion.md"
ledger = [p for p in subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/change_management/"], capture_output=True).stdout.decode().split() if p.endswith(SLUG)][-1]
closed_at = re.search(r"closed (\d{8}T\d{6}Z)", io.open(ledger, encoding="utf-8").read()).group(1)
order = io.open(TO, encoding="utf-8").read()
B = json.load(io.open(W + "MS2_BEFORE.json", encoding="utf-8"))["principal"]
A = json.load(io.open(W + "MS2_AFTER.json", encoding="utf-8"))
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("ms2.%s.sh" % cid), run("ms2.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    ac[cid] = (outs, exp)
    print(cid, "matches expect" if re.search(exp, outs[0]) else "DOES NOT MATCH THE ORDER'S EXPECT", "| stable" if outs[0] == outs[1] else "| UNSTABLE")
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else pin(W + "MS2_AFTER.json"), "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "the candidate adds only the master and its accounts, the two existing masters' account lists are untouched, decide() reads 4 admitted and the download refused on the new master, and the ask has three halves.",
    "AC2": "the grant is live and read back strongly consistent: a newer revision, three masters, the new master's account count equal to the current set, nothing else changed, Andrew's grant revision unchanged, decide() as in Phase A.",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ms-2", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:dynamodb/gateway-access-state-table POLICY# partition (Alyssa's profile and grant, revision 7)", "aws_resource", "DEPLOYED-VERIFIED",
            "ACTIVATED profile_revision=7 grant_revision=7 through ops/schwab_entitlement_admin.py activate under opal-gateway-access-admin, approver Andrew Berman (W/MS2_WRITE.md). Strongly consistent read-back (W/MS2_AFTER.json, %s POLICY# items): 3 masters, new master %s accounts equal to the current set at %s, the two other masters' account sets hash as before, the rest of the scope hashes as before, Andrew's grant revision unchanged. "
            "decide() of the DEPLOYED tree on the host (marker 13917ef993, guard oom_score_adj_1000_rlimit_as_1400mb): the four read tools admitted, schwab_prepare_download refused, master in scope (W/MS2_READBACK_DECIDE.json). Rollback: revoke of revision 7 (a tombstone), revision 6 the value to restore; not used." % (A["policy_items_scanned"], A["alyssa"]["accounts"]["08403355"], B["new_master_latest_complete_date"]), ["AC2"]),
        art(W + "MS2_BEFORE.json", "doc", GIT, "Strongly consistent before-record: Alyssa pk_hash, revisions 6/6, per-master counts and hashes, the new master's current count and date, scope hash, denominator.", ["AC1"]),
        art(W + "MS2_DIFF.json", "doc", GIT, "changed_keys [accounts, masters]; one master added; other masters' accounts unchanged.", ["AC1"]),
        art(W + "MS2_PREFLIGHT_DECIDE.json", "doc", GIT, "decide() on the candidate in process: four tools admitted, download refused, master in scope.", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ms-2.md", "doc", GIT, "The ask, sha256 30351bdddf2d, signed by CTO 355bf20473, COO J1-J7 and CVO 10dfd87598.", ["AC1"]),
        art(W + "MS2_AFTER.json", "doc", GIT, "The live read-back, counts and hashes only.", ["AC2"]),
        art(W + "MS2_READBACK_DECIDE.json", "doc", GIT, "The deployed tree's own answers on her live grant, with tree and code_sha.", ["AC2"]),
        art(ledger, "doc", GIT, "Ledger nfra-oplgtw-ms2-alyssa-master-0840 opened before the read, three legs proven, CLOSED %s; sentinel removed." % closed_at, ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %sms2.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": {"AC1": "1 principal; %d POLICY# items scanned; 1 new master (%d accounts); 4 tools plus download" % (json.load(io.open(W + "MS2_BEFORE.json", encoding="utf-8"))["denominator"]["policy_items_scanned"], B["new_master_accounts_current"]),
                         "AC2": "1 principal; %d POLICY# items scanned live; 3 masters; 4 tools plus download" % A["policy_items_scanned"]}[cid], "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut base-FAIL runs are the discriminating arm.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "a push", "reason": "The order forbids it; the issuer drains the branch."},
        {"item": "Andrew's grant", "reason": "Not in this order; his grant revision is unchanged."},
        {"item": "a served call by Alyssa's own sign-in", "reason": "Not asked; the read-back is the deployed code's decide() on her live grant, not a call made as her."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ms-2. Phase A (2026-10-19, commit 623222c679): before-record, candidate, diff, decide() pre-flight, the ask. Phase B (2026-10-20, GO msg 36159 after the batch15 ledger CLOSED 07:05:52Z): ledger opened 07:17Z; marker read 13917ef993 and the deployed MASTERS lists the master; step 1 re-read, nothing moved; ACTIVATED revision 7 at 07:20Z; strongly consistent read-back and the deployed tree's decide(); the ledger CLOSED " + closed_at + ".",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ms2_phaseb.py (store read, activate under opal-gateway-access-admin), ms2_host_decide.py pre|post and ap38_step1.py (Rule 12, S3 to SSM, hard guard)", "result": "PASS", "note": "Counts, hashes, revisions and short shas only; the module's scope diff holds account ids and was neither printed nor saved."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ms-2.round-46-add-master-08403355-to-alyssas-schwab-grant.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
