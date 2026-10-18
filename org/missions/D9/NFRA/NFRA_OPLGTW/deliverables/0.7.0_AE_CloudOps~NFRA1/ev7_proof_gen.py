#!/usr/bin/env python
"""OG-ev-7: write the proof_of_spec instance for the order from a real run of AC1 (run twice for the determinism control).
usage: python ev7_proof_gen.py   (from the repo root of the worktree that holds PEERS_MEASURE.json, after it is committed; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r43/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-7.round-43-peers-call-in-the-service-under-one-firm-pinned-lease.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run():
    r = subprocess.run(["bash", CK + "ev7.AC1.sh"], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
B = json.load(io.open(W + "PEERS_MEASURE.json", encoding="utf-8"))["body"]
exp = re.search(r'<criterion id="AC1"[^>]*>.*?<expect>(.*?)</expect>', order, re.S).group(1)
outs = [run(), run()]
for o in outs:
    assert re.search(exp, o), o
stable = outs[0] == outs[1]
w = [c["wall_s"] for c in B["calls"]]
C = B["counts"]


def art(path, ev, cov):
    return {"path_or_key": path, "kind": "doc", "commit_or_etag": pin(path), "deployed_state": GIT, "deploy_evidence": ev, "artifact_covered_by": cov}


inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ev-7", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art(W + "PEERS_MEASURE.json", "The measurement record: ONE 15-minute arming (placeholder account reference, firm 49financial read on the host), three etfs_compare_peers calls through the listener (walls %s s, heap signal on/on/off), one fresh guarded process (%s s), verdict %s by the rule fixed before the run, lease deleted %s, ParameterNotFound read, the listener refused a call after the wait. Counts: journal POST /probe/ %d, lake probe:OG-ev-7 %d, probe:unarmed %d."
            % (w, B["fresh_process_wall_s"], B["verdict"], B["deleted_at"], C["journal_post_probe"], C["lake"]["probe_og_ev_7_labelled"], C["lake"]["probe_unarmed_labelled"]), ["AC1"]),
        art(W + "ev7_run_raw.json", "The runner's raw record: the state before and after (marker eff517546e, 65 env keys, one process, NRestarts 0), the unarmed calls, the firm read, the three calls with the heap lines, the fresh call. Counts, MB, seconds and status words only.", ["AC1"]),
        art(W + "ev7_run.py", "The runner, committed before the arming (blob %s); it refuses to start unless the uploaded bytes equal the committed blobs." % B["committed_blobs"]["ev7_probe_host.py"][:12] + " ev7_probe_host.py is the host side.", ["AC1"]),
    ],
    "acceptance": [
        {"criterion_id": "AC1", "criterion_verbatim": "the peers call measured in the running service, to explain Z-S389: the verdict is computed from the numbers by the rule fixed before the run (COLD, SLOW_IN_SERVICE, SIGNAL_COST or INCONCLUSIVE), under the safety bounds.",
         "method": "command", "invocation": 'bash %sev7.AC1.sh; echo "exit=$?"' % CK, "expect": exp, "output_evidence": outs[0],
         "denominator": "3 service calls (57 rows each), 1 fresh-process call, 1 arming, 5 listener requests (journal 5, lake 3 + 2)", "status": "PASS"}],
    "controls": {
        "determinism": {"method": "AC1 was run twice against the same record, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the check recomputes the verdict from the numbers, which is the discriminating arm.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "an explanation of the 17.9 s of OG-ap-40", "reason": "The cell grades a verdict, not the 17.9 s. This arming read 3.59 / 1.07 / 1.09 s in service against 4.2 s fresh: the 17.9 s did not recur, and one arming is one occasion."},
        {"item": "journal POST /mcp lines in the window", "reason": "The window (56 s) held %d service /mcp lines; the three counts compared are the listener's (journal 5, lake 5 of the 5 requests)." % C["journal_post_mcp"]}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ev-7 Step 2 (GO 35802, all three halves on ask sha256 34333184f199; CT2 placeholder account ****0000/probe adopted). Scripts ev7_probe_host.py and ev7_run.py committed (7531e7b4bb) before the arming; blobs verified equal to the uploaded bytes. Live ref eff517546e, 65 env keys, one process PID unchanged, NRestarts 0, no other gateway ledger open. Unarmed call 403, firm read on the host 49financial (equal to the ask's), lease written 21:08:14Z for 15 minutes, 7 s wait, three calls, fresh call, lease deleted 21:08:37Z, ParameterNotFound, 7 s wait, refused 403. VmRSS 248 MB throughout, host memory 31 to 33 percent. Verdict COLD by the rule.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ev7_run.py with ev7_probe_host.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, seconds, status words and UTC times only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ev-7.round-43-peers-call-in-the-service-under-one-firm-pinned-lease.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
