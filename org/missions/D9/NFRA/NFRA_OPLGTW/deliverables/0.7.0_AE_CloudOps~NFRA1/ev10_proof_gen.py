#!/usr/bin/env python
"""OG-ev-10: write the proof_of_spec instance for the order from a real run of AC1 (run twice for the determinism control).
usage: python ev10_proof_gen.py   (from the repo root of the worktree that holds AUDIT_REFUSAL_WRITE.json, after it is committed; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r44/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-10.round-44-is-the-audit-refusal-write-failing.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run():
    r = subprocess.run(["bash", CK + "ev10.AC1.sh"], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
B = json.load(io.open(W + "AUDIT_REFUSAL_WRITE.json", encoding="utf-8"))["body"]
exp = re.search(r'<criterion id="AC1"[^>]*>.*?<expect>(.*?)</expect>', order, re.S).group(1)
outs = [run(), run()]
for o in outs:
    assert re.search(exp, o), o
stable = outs[0] == outs[1]
J, L = B["journal"], B["lake"]
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ev-10", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        {"path_or_key": W + "AUDIT_REFUSAL_WRITE.json", "kind": "doc", "commit_or_etag": pin(W + "AUDIT_REFUSAL_WRITE.json"), "deployed_state": GIT,
         "deploy_evidence": "STEP 1 record (read-only): journal from %s to %s: %d POST /mcp lines in all, %d answered 429, %d writer WARN lines; lake: %d gw_ratelimit rows over %d objects, %d read errors; counter exposed by no route; controlled refusal none; verdict %s. "
                            "The 10 records of the OG-ev-7 window not labelled probe: 9 etfs_compare_peers source reads inside the 3 served calls and 1 hx_teams (GET /hx/teams/chats), all matched to journal lines." % (
                                J["first_access_line_ts"], J["last_line_ts"], J["post_mcp_lines"], J["post_mcp_429_lines"], J["ratelimit_audit_warn_lines"], L["gw_ratelimit_rows"], L["denominator"], L["read_errors"], B["verdict"]),
         "artifact_covered_by": ["AC1"]},
        {"path_or_key": W + "ev10_step1.py", "kind": "doc", "commit_or_etag": pin(W + "ev10_step1.py"), "deployed_state": GIT, "deploy_evidence": "The read-only collector (journalctl over SSM, the lake listed and read). Writes nothing but its local record.", "artifact_covered_by": ["AC1"]},
    ],
    "acceptance": [
        {"criterion_id": "AC1", "criterion_verbatim": "the journal and lake counts are present and read without error, the verdict equals what the rule returns from those counts, the 10 records of OG-ev-7's window not labelled probe are accounted for by (label, tool) pairs that sum to 10, and the record holds no email, no principal and no long digit run.",
         "method": "command", "invocation": 'bash %sev10.AC1.sh; echo "exit=$?"' % CK, "expect": exp, "output_evidence": outs[0],
         "denominator": "%d lake objects read (0 errors); %d journal POST /mcp lines; 10 records of the OG-ev-7 window" % (L["denominator"], J["post_mcp_lines"]), "status": "PASS"}],
    "controls": {
        "determinism": {"method": "AC1 was run twice against the same record, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the check recomputes the verdict from the numbers, which is the discriminating arm.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [{"item": "STEP 2 (the controlled refusal)", "reason": "The order stops at NOT_EXPOSED and waits for the issuer's reply; STEP 2 needs an ask, three signed halves and a GO."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ev-10 STEP 1 (GO 35852; read-only). The journal and the lake were read by ev10_step1.py (SSM send-command for the journal, boto3 list and get for the lake); the OG-ev-7 limb was cross-checked against the journal of 21:08:00Z to 21:09:05Z by class (5 probe lines, 1 hx line, 4 health lines, 0 POST /mcp, 1 outbound Graph client line). No ask, no halves, nothing written to AWS.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ev10_step1.py", "result": "PASS", "note": "Counts, UTC times and (label, tool) names only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ev-10.round-44-is-the-audit-refusal-write-failing.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
