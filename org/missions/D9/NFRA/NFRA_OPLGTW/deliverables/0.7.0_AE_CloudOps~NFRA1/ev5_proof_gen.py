#!/usr/bin/env python
"""OG-ev-5: write W/NFRA_OPLGTW.TO-OG-ev-5.trace-the-near-empty-fees-stretch.proof_of_spec.json from a real run of AC1 (run twice for the determinism control).
usage: python ev5_proof_gen.py   (from the repo root of the worktree, after the record commit; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-5.trace-the-near-empty-fees-stretch.md"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(path):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--", path], capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
outs = [run("ev5.AC1.sh"), run("ev5.AC1.sh")]
exp = re.search(r'<criterion id="AC1"[^>]*>.*?<expect>(.*?)</expect>', order, re.S).group(1)
assert re.search(exp, outs[0]), outs[0]
stable = outs[0] == outs[1]
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def art(path, kind, ev):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path), "deployed_state": GIT, "deploy_evidence": ev, "artifact_covered_by": ["AC1"]}


inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ev-5", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md", "group": "OTHER", "vintage_commit": "5bee627be9"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md", "vintage_commit": "5bee627be9", "to_ref": TO},
    "artifacts_produced": [
        art(W + "FEES_TRACE.json", "doc", "Counts, dates and fixed words only: the stretch 2026-08-17 to 2026-09-15 (30 days, the CVO's, 109 source rows, agreed), verdict source (ratio 0.173), the account not assessable (median 0)."),
        art(W + "FEES_TRACE_COUNTS.json", "doc", "Per dated partition: ALL source rows, rows kept by the 49F fence, the account's rows, the account's non-zero fee amounts; 394 of 394 partitions of the window, read in a new process on the host through the installed adapter's read path."),
        art(W + "ev5_trace.py", "script", "The read-only host program (Rule 12, S3 to SSM): bd._read_partitions 30 partitions a page, host memory checked between pages (stop at 75 percent; the peak stayed below it), audit sink stubbed, nothing written."),
        art(W + "ev5_build.py", "script", "Assembles FEES_TRACE.json from the counts and lib/trading_calendar.py; checks the CVO's 109."),
    ],
    "acceptance": [
        {"criterion_id": "AC1", "criterion_verbatim": re.search(r"`AC1`: (.*?)(?=\n\n)", order, re.S).group(1).replace("\n", " ")[:500], "method": "command",
         "invocation": 'bash %sev5.AC1.sh; echo "exit=$?"' % CK, "expect": exp, "output_evidence": outs[0],
         "denominator": "394 of 394 fees partitions of the 13-month window; 30 stretch dates, 21 trading days, all 21 present", "status": "PASS"}],
    "controls": {
        "determinism": {"method": "AC1 was run twice against the same record, back to back.", "observed": "outputs identical" if stable else "outputs differ",
                        "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls (a verdict contradicting the counts three ways; a 20-day stretch; a missing partition; an e-mail in the record) are the discriminating arms.",
                   "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "partitions on non-trading dates in the stretch", "reason": "The order defines the partitions expected as the stretch's trading days; the table is daily (9 weekend-dated partitions, 63 rows, in the stretch), so the equality in AC1 is read on the 21 trading-day partitions and the rest is stated in the record's extra fields and in the observation row filed at the close."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1 (GO msg 35460). One run of ev5_trace.py on the host (new process, read only), the per-date counts, the stretch taken from the CVO's row and checked, the 25 percent rule applied by ev5_build.py. An OBSERVATION row (thin July to September; daily partitions) is filed in the surprise channel at the close.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ev5_trace.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts and dates only; 394 partitions, memory below the stop."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ev-5.trace-the-near-empty-fees-stretch.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
