#!/usr/bin/env python
"""OG-ap-35: write W/NFRA_OPLGTW.TO-OG-ap-35.narrow-alyssa-no-download.proof_of_spec.json from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ag1_proof_gen.py   (from the repo root of the worktree on box/sitez, after the Phase B commit; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-35.narrow-alyssa-no-download.md"
LEDGER = "org/critical_paths/change_management/20261017T0338Z_nfra-oplgtw-alyssa-no-download_deploy_completion.md"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(path):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--", path], capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
ac = {}
for cid, script in (("AC1", "ag1.AC1.sh"), ("AC2", "ag1.AC2.sh")):
    outs = [run(script), run(script)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("ddb:") else "activate 2026-10-17", "deployed_state": deployed,
            "deploy_evidence": ev, "artifact_covered_by": cov}


inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-35", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md", "group": "OTHER", "vintage_commit": "53cac446ff"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md", "vintage_commit": "53cac446ff", "to_ref": TO},
    "artifacts_produced": [
        art("ddb:gateway-access-state-table/principal_profile+data_entitlement (one client principal, role alyssa, pk hash 2c61471b14)", "ddb_rows", "DEPLOYED-VERIFIED",
            "ONE activate under opal-gateway-access-admin: ACTIVATED profile_revision=5 grant_revision=5. Strongly consistent re-read: operations describe, list, query (download_filtered gone); scope-without-operations hash 5f95dcbca8 equal; the two other principals' grant hashes equal; email_deny hash 1c83c567ea equal before and after. Installed code on the host (SSM c22f52ff, in-process decide): schwab_prepare_download refused; schwab_list_files, schwab_describe_dataset, schwab_query answer. Rollback: activate the before scope as revision 6 (X/alyssa_restore_candidate.json, off-repo).", ["AC2"]),
        art(W + "AG1_AFTER.json", "doc", GIT, "Hashes, revisions, operation names and booleans only; carries email_deny_hash_before and _after (equal).", ["AC2"]),
        art(W + "AG1_BEFORE.json", "doc", GIT, "The Phase A before-record: usage 0 with a positive control, operations carrying download_filtered.", ["AC1", "AC2"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-35.md", "doc", GIT, "The ask, sha256 224a80d88a52, signed by CTO df73e21192, COO 4aea561614, CVO 03311f4476.", ["AC1"]),
        art(LEDGER, "doc", GIT, "Ledger nfra-oplgtw-alyssa-no-download opened before the act, both legs proven, CLOSED; sentinel removed.", ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": re.search(r"`%s`: (.*?)(?= `AC\d`: |\n)" % cid, order).group(1)[:400], "method": "command",
         "invocation": 'bash %s%s; echo "exit=$?"' % (CK, "ag1.%s.sh" % cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": ("one principal; usage census 96 objects read in 21 day partitions, 0 errors" if cid == "AC1"
                         else "one principal, three principals compared (two others unchanged), one ledger of two legs, one activate"),
         "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ",
                        "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls (no ledger, a second key removed, download_filtered still present, another scope key changed, another principal moved, the download not refused, the revision jumping by 2) are the discriminating arms.",
                   "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [{"item": "a call made as her principal through the live gateway", "reason": "The order forbids any call as her and any contact with her or her firm; the read-back ran the installed decision code in-process on the host."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1 (GO msg 35330). Ledger opened and merged, re-read (nothing moved), one activate, re-read after, host read-back by SSM, AG1_AFTER written, ledger closed, AC1 and AC2 run. Identifiers stayed in X outside the worktree.",
    "compiler_tools": [{"tool": "boto3 / ssm", "invocation": "ag1_hostread.py (host decision in-process with the installed code)", "result": "PASS", "note": "Booleans, revisions, operation names and counts only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-35.narrow-alyssa-no-download.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
