#!/usr/bin/env python
"""OG-mg-1: write W/NFRA_OPLGTW.TO-OG-mg-1.r30-grant-writes.proof_of_spec.json from a real run of AC1 and AC2 (each run twice for the
determinism control). usage: python mg1_proof_gen.py   (from the repo root; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r37/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-mg-1.r30-grant-writes.md"
PIN = "8e44440e66"


def run(script: str) -> str:
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return (r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode)


ac1 = [run("mg1.AC1.sh"), run("mg1.AC1.sh")]
ac2 = [run("mg1.AC2.sh"), run("mg1.AC2.sh")]
E1 = r"(?s)before-record: roles andrew\+bbg with pk_hash and state: yes; denominator printed: yes.*ask items: 6 of 6; email addresses in the ask: 0 \(want 0\).*RESULT: PASS.*exit=0"
E2 = r"(?s)status CLOSED=yes; sentinel at HEAD=no.*andrew active\+13mo: yes; bbg active: yes; bbg scope == andrew scope: yes; alyssa unchanged: yes.*RESULT: PASS.*exit=0"
assert re.search(E1, ac1[0]) and re.search(E2, ac2[0]), (ac1[0], ac2[0])
stable = ac1[0] == ac1[1] and re.sub(r"policy items \d+", "", ac2[0]) == re.sub(r"policy items \d+", "", ac2[1])


def art(path, kind, pin, state, ev, intro, cov):
    row = {"path_or_key": path, "kind": kind, "commit_or_etag": pin, "deployed_state": state, "deploy_evidence": ev, "artifact_covered_by": cov}
    if intro:
        row["introduces"] = intro
    return row


GIT = "COMMITTED-NOT-DEPLOY-SCOPE"
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-mg-1", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~Z",
    "session_log": "org/tier2_senior/0.7.0_AE_CloudOps~Z/logs/2026-10-16/mg1_phase_b.md",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md", "group": "OTHER", "vintage_commit": "f2b066d9ad"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md", "vintage_commit": "3b056fd12e", "to_ref": TO},
    "acceptance": [
        {"criterion_id": "AC1", "criterion_verbatim": "AC1: both records are prepared and asked, with their current state and rollback.",
         "method": "command", "invocation": 'bash %smg1.AC1.sh; echo "exit=$?"' % CK, "expect": E1, "output_evidence": ac1[0],
         "denominator": "before-record for 2 of 2 roles (andrew, bbg) with pk_hash and state, the 17-item POLICY# denominator printed in W/MG1_BEFORE.json; 6 of 6 ask items; 0 email addresses in the ask (sha256 757f5146afee); run twice, identical.",
         "status": "PASS"},
        {"criterion_id": "AC2", "criterion_verbatim": "AC2: both are written, read back live, and mirrored; the one existing profile is untouched.",
         "method": "command", "invocation": 'bash %smg1.AC2.sh; echo "exit=$?"' % CK, "expect": E2, "output_evidence": ac2[0],
         "denominator": "25 POLICY# items in a strongly consistent, fully paginated live scan (17 before: +2 profiles, +2 grants, +2 operator_audit, +2 email_deny); 2 of 2 written principals active; 1 of 1 pre-existing active profile (Alyssa, revision 4) unchanged. Run on the check as fixed by 2.0.0_SA_COO~O at f30d9fdce8 (row Z-S174: the first run, on the original check, graded FAIL on its own shape while a direct deserialized read-back was correct). Independent direct read-back: W/MG1_READBACK.json (mirror equal, Alyssa's 9 items hash b93cd3cbf990 before and after).",
         "status": "PASS"},
        {"criterion_id": "AC3", "criterion_verbatim": "AC3 (judgment, 3.0.0_SA_CVO~Z; CTO ruling msg 33850): after r30 AND these writes, 0.0.3_BG_BBGTerminal re-runs its own capability exercise on the 8 gateway data tools it measured denied (opal_discover, mdpf_get_aum_metrics, mdpf_get_aggregate_aua, mdpf_get_account_distribution, mdpf_get_model_benchmarks, etfs_get_positioning, gateway_query_catalog, ycharts_freshness), the same way it read them, and reads 8 of 8 ALLOWED. Denied after both is a BLOCKING row, not a pass.",
         "method": "manual_read_with_citation",
         "invocation": "NOT RUN BY THIS SEAT. The act is owed by 0.0.3_BG_BBGTerminal (relayed by 2.0.0_SA_COO~O); the criterion carries judgment=\"true\" and is graded by 3.0.0_SA_CVO~Z at L9, never self-graded.",
         "output_evidence": "What this seat can say, and no more: r30 is live (release 3d5c9c8bf1, ledger nfra-oplgtw-gateway-release-r30 CLOSED) and both grant records are in the store, active restricted at revision 1 with the same scope, so the precondition of the re-exercise holds. The 8-tool exercise was not run here.",
         "denominator": "0 of 8 tools exercised by this seat; precondition (r30 live, R1 and R2 written and read back) met. Grader: 3.0.0_SA_CVO~Z; actor: 0.0.3_BG_BBGTerminal.",
         "status": "UNVERIFIABLE-BY-INSTRUMENT",
         "status_reason": "A JUDGMENT criterion whose act belongs to 0.0.3_BG_BBGTerminal and whose grade belongs to 3.0.0_SA_CVO~Z (spine L9); no instrument this seat holds can read the Bloomberg seat's own exercise."},
    ],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same repository and live store, back to back; the fixed AC2 reads the live store, so the policy-item count is masked in the comparison.",
                        "observed": "AC1 outputs identical; AC2 outputs identical after masking the count (25 both times).", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant. The negative arm is the pre-write state: at the cut mg1.AC2 graded FAIL as expected (ledger absent, andrew no, bbg no), and the first run after the writes graded FAIL on the original check's own shape (row Z-S174), which the issuer fixed at f30d9fdce8; the direct deserialized read-back (W/MG1_READBACK.json) was the independent arm that showed the world was right and the instrument wrong.",
                   "expected": "AC2 FAILs before the writes; PASSes after them on a correct instrument",
                   "observed": "FAIL at the cut (issuer's pre-cut note); FAIL after the writes on the unfixed check; PASS after the fix", "status": "N/A-SPEC-NAMES-NONE"},
    },
    "artifacts_produced": [
        art("org/critical_paths/change_management/20261016T1120Z_nfra-oplgtw-r30-grant-writes_deploy_completion.md", "script", PIN, GIT,
            "the deploy ledger, opened and committed first (entry AND sentinel), 3 legs closed with proof, then CLOSED; the sentinel is removed at HEAD", None, ["AC2"]),
        art(W + "MG1_WRITE.md", "script", PIN, GIT, "the C2 re-read table, the two ACTIVATED lines and the read-back, with no identifier", ["ACTIVATED profile_revision=1 grant_revision=1"], ["AC2"]),
        art(W + "MG1_READBACK.json", "script", PIN, GIT, "the deserialized strongly consistent read-back: roles, pk hashes, revisions, scope keys, counts and short hashes only", ["mirror_r2_equals_r1"], ["AC2"]),
        art(W + "mg1_activate.py", "script", PIN, GIT, "the one-activate-per-record runner under opal-gateway-access-admin; full prepare diff held off-repo", ["mg1-phaseb-%s"], ["AC2"]),
        art(W + "mg1_phaseb_reread.py", "script", PIN, GIT, "the C2 re-read of store and host at the GO; exits 2 on any STOP condition", ["WANT_R1_SHA10"], ["AC2"]),
        art(W + "mg1_readback.py", "script", PIN, GIT, "the C5 read-back instrument", ["ALYSSA_BEFORE_HASH"], ["AC2"]),
        art("gateway-access-state-table POLICY# partitions: two principal_profile, two data_entitlement revision 1, two operator_audit, two email_deny items", "ddb_rows",
            "strong read 2026-10-16T11:23:57Z", "DEPLOYED-VERIFIED", "read back from the store by W/MG1_READBACK.json and again by mg1.AC2 (25 POLICY# items)", None, ["AC2"]),
    ],
    "compiler_tools": [
        {"tool": "the schwab_entitlement_admin activate CLI", "invocation": "python W/mg1_activate.py r1 ; python W/mg1_activate.py r2 (one activate each, under opal-gateway-access-admin)",
         "result": "ACTIVATED profile_revision=1 grant_revision=1 twice; no REFUSED, no stale base, no retry"},
        {"tool": "mg1.AC1 / mg1.AC2", "invocation": 'bash %smg1.AC1.sh ; bash %smg1.AC2.sh' % (CK, CK), "result": "PASS exit 0 both (AC2 on the fixed check f30d9fdce8)"},
    ],
    "surprises": ["NFRA_OPLGTW-Z-S174: mg1.AC2.sh read calendar_months at the scope's top level of a typed map and could not pass on the live store; fixed by the issuer at f30d9fdce8."],
    "declared_exclusions": [
        {"item": "AC3, the Bloomberg seat's 8-tool re-exercise", "reason": "Owed by 0.0.3_BG_BBGTerminal and graded by 3.0.0_SA_CVO~Z; this seat proved only the precondition."},
        {"item": "the client-data account-id hash check", "reason": "The hashed account-id list is absent on this box, so the commit hook could not check these records for client account ids; absent is not empty. The records carry no account id by construction (hashes, roles, keys and counts only)."},
        {"item": "rollback not exercised", "reason": "Both records read correct, so no revoke was run; the path (revoke under the same role, a tombstone, never a delete) stands as signed in the ask section 2."},
    ],
}
P = W + "NFRA_OPLGTW.TO-OG-mg-1.r30-grant-writes.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
