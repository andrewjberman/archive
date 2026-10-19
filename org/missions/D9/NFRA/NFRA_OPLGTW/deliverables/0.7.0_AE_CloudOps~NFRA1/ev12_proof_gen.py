#!/usr/bin/env python
"""OG-ev-12: write the proof_of_spec instance for the order from a real run of AC1 (run twice for the determinism control).
usage: python ev12_proof_gen.py   (from the repo root of the worktree that holds ORGANIC_429.json, after it is committed; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r45/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-12.round-45-who-answered-the-organic-429.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run():
    r = subprocess.run(["bash", CK + "ev12.AC1.sh"], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
B = json.load(io.open(W + "ORGANIC_429.json", encoding="utf-8"))["body"]
exp = re.search(r'<criterion id="AC1"[^>]*>.*?<expect>(.*?)</expect>', order, re.S).group(1)
outs = [run(), run()]
for o in outs:
    assert re.search(exp, o), o
stable = outs[0] == outs[1]
J, L = B["journal"], B["lake"]
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ev-12", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        {"path_or_key": W + "ORGANIC_429.json", "kind": "doc", "commit_or_etag": pin(W + "ORGANIC_429.json"), "deployed_state": GIT,
         "deploy_evidence": "Read-only record: journal %s to %s (%d POST /mcp lines, %d answered 429, %d other-route 429s); lake 2026-10-18T19:00Z to 20:00Z %d gw_ratelimit rows over %d objects (%d read errors); the ALB access logs show no 429 on 2026-10-18 or 2026-10-19 so far "
                            "and exactly one 429 span on 2026-10-17 (17:21:43Z to 17:21:44Z, answered by this service) against one lake row; throttle rule read at %s: refusal window %s s; verdict %s by the rule fixed before the run." % (
                                J["first_access_line_ts"], J["window_end"], J["post_mcp_lines"], J["post_mcp_429_lines"], J["other_429_lines"], L["gw_ratelimit_rows"], L["denominator"], L["read_errors"], B["code_sha"][:10], B["throttle_rule"]["refusal_window_s"], B["verdict"]),
         "artifact_covered_by": ["AC1"]},
        {"path_or_key": W + "ev12_collect.py", "kind": "doc", "commit_or_etag": pin(W + "ev12_collect.py"), "deployed_state": GIT, "deploy_evidence": "The read-only collector (journalctl over SSM, the lake and the ALB access logs listed and read, the throttle rule via git show at the pinned sha). Writes nothing but its local record.",
         "artifact_covered_by": ["AC1"]},
    ],
    "acceptance": [
        {"criterion_id": "AC1", "criterion_verbatim": "the journal and lake counts are present and read without error, the throttle rule is read at the pinned sha and equals the record, the verdict equals what the rule returns from those counts, and the record holds no email, no principal and no long digit run.",
         "method": "command", "invocation": 'bash %sev12.AC1.sh; echo "exit=$?"' % CK, "expect": exp, "output_evidence": outs[0],
         "denominator": "%d lake objects read (0 errors); %d journal POST /mcp lines; %d ALB lines in the window" % (L["denominator"], J["post_mcp_lines"], B["alb_access_logs"]["lines"]), "status": "PASS"}],
    "controls": {
        "determinism": {"method": "AC1 was run twice against the same record, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the check recomputes the verdict from the numbers, which is the discriminating arm.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [{"item": "the 429 response body shape", "reason": "No log read here keeps a response body; guard_middleware_body_seen is null and the evidence says what was read instead."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ev-12 (GO 35903; read-only). ev12_collect.py read the journal over SSM, the lake, the ALB access logs the account keeps (S3, read-only) and the throttle rule at the live sha. The journal's access log returned at 2026-10-18T19:23:53Z, after the 19:20Z start of the span, so by the rule fixed before the run the verdict is UNDETERMINED; the ALB logs add that no 429 passed the ALB on 2026-10-18 or 2026-10-19 so far, and that the one 429 span they hold (2026-10-17 17:21Z) has its first-refusal row in the lake.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ev12_collect.py", "result": "PASS", "note": "Counts, UTC times and status words only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ev-12.round-45-who-answered-the-organic-429.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
