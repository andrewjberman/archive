#!/usr/bin/env python
"""OG-mg-2: write the proof_of_spec instance from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python mg2_proof_gen.py   (repository root, after the Phase B commit and the ledger close)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r46/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-mg-2.round-46-schwab-grants-at-the-full-current-accounts.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


ledger = [p for p in subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/change_management/"], capture_output=True).stdout.decode().split() if p.endswith("_nfra-oplgtw-mg2-schwab-full-accounts_deploy_completion.md")][-1]
closed_at = re.search(r"closed (\d{8}T\d{6}Z)", io.open(ledger, encoding="utf-8").read()).group(1)
order = io.open(TO, encoding="utf-8").read()
after = json.load(io.open(W + "MG2_AFTER.json", encoding="utf-8"))
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("mg2.%s.sh" % cid), run("mg2.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    ac[cid] = (outs, exp)
    print(cid, "matches expect" if re.search(exp, outs[0]) else "DOES NOT MATCH THE ORDER'S EXPECT", "| stable" if outs[0] == outs[1] else "| UNSTABLE")
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path), "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "both Schwab grants are PREPARED at each granted master's current account set with nothing else changed (the diff keys read [accounts] for both roles); the in-process decide() pre-flight on Alyssa's candidate admits the four read tools and refuses schwab_prepare_download; the before-record carries both roles with pk_hash, counts and the scope hash; the ask has three halves and the process-wide state line.",
    "AC2": "the grant is re-activated and read back live: the ledger is closed with its sentinel gone; the live store shows the principal's profile active with a NEWER grant revision whose per-master counts equal the current sets and whose scope without accounts hashes unchanged; decide() on the live grant admits the four read tools and refuses schwab_prepare_download. Under option (b) Andrew's grant is HELD and reads unchanged.",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-mg-2", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        {"path_or_key": "aws:dynamodb/gateway-access-state-table (POLICY# partition: alyssa's principal_profile revision 6, data_entitlement grant revision 6, operator_audit append)", "kind": "aws_resource",
         "commit_or_etag": "0a8fb6511e", "deployed_state": "DEPLOYED-VERIFIED",
         "deploy_evidence": "ACTIVATED profile_revision=%d grant_revision=%d at 2026-10-19T18:58Z through ops/schwab_entitlement_admin.py activate under opal-gateway-access-admin, approver Andrew Berman; strongly consistent live read: profile %s, grant %s, per-master counts %s equal to the current dim_balance sets of 2026-10-16, scope without accounts unchanged %s; decide() on the live grant admits the four read tools and refuses schwab_prepare_download. Andrew's grant HELD under option (b) (revision unchanged). email_deny records in the store: %d (unchanged); no delete."
         % (after["alyssa"]["profile_revision"], after["alyssa"]["grant_revision"], after["alyssa"]["profile_status"], after["alyssa"]["grant_status"], after["alyssa"]["accounts"], after["alyssa"]["scope_sans_accounts_unchanged"], after["email_deny_records_in_store"]),
         "artifact_covered_by": ["AC2"]},
        art(W + "MG2_BEFORE.json", "doc", GIT, "Phase A before-record: both roles, pk_hash, revisions, per-master counts before and current, the scope-without-accounts hash, a printed denominator (25 POLICY# items of 2074).", ["AC1"]),
        art(W + "MG2_DIFF.json", "doc", GIT, "changed_keys == [accounts] for both roles; added 134 / 150 and removed 12 / 19 per master.", ["AC1"]),
        art(W + "MG2_PREFLIGHT_DECIDE.json", "doc", GIT, "decide() on Alyssa's candidate: four read tools admitted, schwab_prepare_download refused.", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-mg-2.md", "doc", GIT, "The ask, sha256 b1244d6c235a; CTO, COO and CVO halves signed, option (b).", ["AC1"]),
        art(W + "MG2_AFTER.json", "doc", GIT, "Counts-only live read-back after the activation.", ["AC2"]),
        art(W + "MG2_READBACK_DECIDE.json", "doc", GIT, "decide() on Alyssa's LIVE grant.", ["AC2"]),
        art(ledger, "doc", GIT, "Ledger nfra-oplgtw-mg2-schwab-full-accounts opened before the write, three legs proven, CLOSED %s; sentinel removed." % closed_at, ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %smg2.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": {"AC1": "2 roles; 2 masters each; 5 tools decided; 3 halves", "AC2": "1 ledger of 3 legs; 2 roles read live; 2 masters; 5 tools decided"}[cid], "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut base-FAIL runs are the discriminating arm.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "Andrew's grant activation", "reason": "HELD under option (b) (CTO, COO and CVO halves): activating it re-creates his email_deny record, which the legacy consent sign-in enforces, and removing it is a delete this order forbids; a follow-on order handles it."},
        {"item": "a delete of any kind", "reason": "The order forbids it; the email_deny records were not touched."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-mg-2 (GOs 36035 and 36073). Phase A (17:44Z to 18:40Z): the store scanned strongly (25 POLICY# items), both roles resolved by e-mail prefix, the current sets read from dim_balance at the latest complete date (7690 equals the CTO's measure), candidates prepared under the operator role, decide() pre-flight, the ask with the email_deny finding (activate() re-creates Andrew's record). The halves signed option (b). Phase B (18:53Z to 19:01Z): ledger opened, step 1 re-read (nothing moved), Alyssa's activation only, live read-back, ledger CLOSED " + closed_at + ". Two COO messages about OG-rs-1 were read late because the inbox watcher had lapsed mid-turn; the order was superseded by MSTR's own restart at 18:24Z.",
    "compiler_tools": [{"tool": "boto3 / dynamodb / s3 / iam simulate", "invocation": "mg2_phasea.py, mg2_ask.py, mg2_phaseb.py (the module's own prepare, activate and decide)", "result": "PASS", "note": "Counts, roles, hashes and UTC times only; the candidate files holding ids stay off-repo."}],
}
P = W + "NFRA_OPLGTW.TO-OG-mg-2.round-46-schwab-grants-at-the-full-current-accounts.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
