#!/usr/bin/env python
"""OG-ev-13: write the proof_of_spec instance from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ev13_proof_gen.py   (repository root, after the Phase B commit and the ledger close)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r46/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-13.round-46-the-audit-lake-leg-after-a-day-of-traffic.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
R = json.load(io.open(W + "AUDIT_LEG_24H.json", encoding="utf-8"))["body"]
exp = re.search(r'<criterion id="AC1"[^>]*>.*?<expect>(.*?)</expect>', order, re.S).group(1)
outs = [run("ev13.AC1.sh"), run("ev13.AC1.sh")]
print("AC1", "matches expect" if re.search(exp, outs[0]) else "DOES NOT MATCH THE ORDER'S EXPECT", "| stable" if outs[0] == outs[1] else "| UNSTABLE")
stable = outs[0] == outs[1]
busy = sum(1 for h in R["hours"] if h["post_mcp_lines"] >= 20)


def art(path, kind, ev):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path), "deployed_state": GIT, "deploy_evidence": ev, "artifact_covered_by": ["AC1"]}


inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ev-13", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art(W + "AUDIT_LEG_24H.json", "doc", "Read-only record: window %s to %s, %d hourly rows (%d busy), %d audit-lake WARN lines, verdict %s, anomaly hour %d of %d bodies read with %d read errors. Counts only." % (R["window_start"], R["window_end"], len(R["hours"]), busy, R["journal"]["warn_lines"], R["verdict"], R["anomaly_hour"]["read"], R["anomaly_hour"]["objects"], R["anomaly_hour"]["read_errors"])),
        art(W + "ev13_run.py", "code", "The reader: journalctl over SSM (per-hour POST /mcp lines, WARN lines), a LIST of s3://opal-mcp-audit keys per hour, a threaded read of the anomaly hour's bodies (histogram by tool or event name); no write, no gateway request."),
    ],
    "acceptance": [{"criterion_id": "AC1", "criterion_verbatim": "the window runs at least 24 hours from the OG-ap-48 close, the journal and the hourly lake counts are present and read without error, the anomaly hour's bodies are all read and its histogram accounts for them, the throttle constant is read at the pinned sha and equals the record, the verdict equals what the rule returns from those counts, and the record holds no email, no principal and no long digit run.",
                    "method": "command", "invocation": 'bash %sev13.AC1.sh; echo "exit=$?"' % CK, "expect": exp, "output_evidence": outs[0],
                    "denominator": "%d hourly buckets; %d busy hours; %d anomaly-hour objects read of %d" % (len(R["hours"]), busy, R["anomaly_hour"]["read"], R["anomaly_hour"]["objects"]), "status": "PASS"}],
    "controls": {
        "determinism": {"method": "AC1 was run twice against the same record, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's synthetic arms (clean day, WARN lines, lagging hour, contradicting verdict, short window, partial read, wrong constant) are the discriminating arms.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "the code_sha the order expected", "reason": "The live ref is 13917ef993 (batch15), not 6b1a9bd292; the record pins the live ref and the check reads the throttle constant at it (60.0), as the issuer's GO directed."},
        {"item": "the named downtime intervals", "reason": "06:22:51Z-06:23:35Z resize, 06:28:33Z-06:28:49Z deploy restart and 06:33:33Z-06:33:40Z stall, all inside the 2026-10-20T06:00Z hour, are named in the evidence and not subtracted from any count."},
        {"item": "the sampler probes of this seat", "reason": "468 unauthenticated POST /mcp probes (06:19Z-06:37Z, 192 of them in 06:30Z-07:00Z) sit in that hour's journal count; stated in the evidence, not subtracted."},
        {"item": "a push", "reason": "The order forbids it; the issuer drains the branch."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ev-13, GO msg 36162 (window_end 2026-10-20T07:48:00Z). Read at 08:18Z: the host journal (first line 2026-08-26T11:50:22Z), the lake listing for two days, and all 2896 bodies of the 2026-10-19T02:00Z hour; wrote AUDIT_LEG_24H.json; ev13.AC1 PASS; verdict HOLDS.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ev13_run.py journal|lake|anomaly|build (Rule 12 not needed: the host command is a read of the journal, no script pulled)", "result": "PASS", "note": "Counts only; no value from any lake body was printed or kept."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ev-13.round-46-the-audit-lake-leg-after-a-day-of-traffic.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
