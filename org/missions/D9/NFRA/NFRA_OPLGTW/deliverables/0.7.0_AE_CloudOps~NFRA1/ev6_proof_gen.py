#!/usr/bin/env python
"""OG-ev-6: write W/NFRA_OPLGTW.TO-OG-ev-6.round-42-window-page-size-sweep-on-the-host.proof_of_spec.json from a real run of ev6.AC1 (run twice for the determinism control).
usage: python ev6_proof_gen.py   (from the repo root of the worktree on box/sitez, after the record commit; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r42/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-6.round-42-window-page-size-sweep-on-the-host.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
outs = [run("ev6.AC1.sh"), run("ev6.AC1.sh")]
exp = re.search(r'<criterion id="AC1"[^>]*>.*?<expect>(.*?)</expect>', order, re.S).group(1)
assert re.search(exp, outs[0]), outs[0]
stable = outs[0] == outs[1]
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ev-6", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        {"path_or_key": W + "PAGE_SWEEP.json", "kind": "doc", "commit_or_etag": pin(W + "PAGE_SWEEP.json"), "deployed_state": GIT,
         "deploy_evidence": "Nine fresh cgroup-guarded runs (three per size at 30, 60, 120 partitions per page) of the 49F test account's transactions window on the host, trunk 2550dab3df over live 4257a2aa42; hashes, seconds, MB, percentages and counts only. chosen_partitions 30.",
         "artifact_covered_by": ["AC1"]},
        {"path_or_key": W + "ev6_sweep.py", "kind": "doc", "commit_or_etag": pin(W + "ev6_sweep.py"), "deployed_state": GIT,
         "deploy_evidence": "The runner, the host driver and the guarded child that assigns PAGE_PARTITIONS in the process before the first call.", "artifact_covered_by": ["AC1"]},
    ],
    "acceptance": [{"criterion_id": "AC1", "criterion_verbatim": "the record has three fresh runs for each of the three sizes with every field, the guard is named, one row hash covers all runs, and chosen_partitions equals the size the rule gives when recomputed from the runs. It PASSES whatever size the rule chooses (30 is an answer).",
                    "method": "command", "invocation": 'bash %sev6.AC1.sh; echo "exit=$?"' % CK, "expect": exp, "output_evidence": outs[0],
                    "denominator": "3 sizes x 3 fresh runs = 9 runs; 120 partitions covered by every run", "status": "PASS"}],
    "controls": {
        "determinism": {"method": "AC1 was run twice against the same record, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the check recomputes the rule from the runs, so a record whose chosen_partitions disagrees with them is the discriminating arm.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "a re-run of a size that failed", "reason": "The order says a failed measurement is NOT re-run until it passes and no limit is relaxed: the three runs of 60 (growth) and of 120 (growth and a different row set) are the record."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1. GO msg 35592 (trunk_sha 2550dab3df), held by msg 35601 until dell1's HVST-cg-3 deploy closed; msg 35604 gave the new live ref 4257a2aa42. cg-3's ledger read CLOSED (02:13:41Z) before the first run; host md5 139 of 139 against the live ref; the nine runs 02:4xZ; every gateway-code run in a fresh process under oom_score_adj_1000_cgroup_memmax_1400mb. No deploy, no ledger, nothing written to any bucket or table; the scratch folder removed.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ev6_sweep.py, ap36_host_md5.py, ap38_step1.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Seconds, MB, percentages, counts and sha256 of canonical rows only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ev-6.round-42-window-page-size-sweep-on-the-host.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
