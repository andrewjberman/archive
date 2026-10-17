#!/usr/bin/env python
"""OG-ap-34: write W/NFRA_OPLGTW.TO-OG-ap-34.round-40-fourth-batched-release.proof_of_spec.json from a real run of AC1 and AC2 (each run twice for the determinism control).
AC3 is a judgment criterion (3.0.0_SA_CVO~Z) and is never graded here.
usage: python ap34_proof_gen.py   (from the repo root of the worktree on box/sitez, after the Phase B commit; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-34.round-40-fourth-batched-release.md"
LEDGER = "org/critical_paths/change_management/20261017T0516Z_nfra-oplgtw-gateway-release-batch5_deploy_completion.md"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(path):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--", path], capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
ac = {}
for cid, script in (("AC1", "ap34.AC1.sh"), ("AC2", "ap34.AC2.sh")):
    outs = [run(script), run(script)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("ec2:") else "9d5b7125571520b977401634a01935924f4c9787",
            "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-34", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md", "group": "OTHER", "vintage_commit": "53cac446ff"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md", "vintage_commit": "53cac446ff", "to_ref": TO},
    "artifacts_produced": [
        art("ec2:i-07dccb1615503ac99:/opt/opal-gateway (opal-gateway service, round-40 fourth batched release)", "ec2_deploy", "DEPLOYED-VERIFIED",
            "ONE deploy of release 9d5b7125571520b977401634a01935924f4c9787 at 2026-10-17T05:19:28Z through safe-ec2-deploy.sh, DEPLOY_BASE_REF=d3ae88be46, guard equal, no HALT_OVERRIDE. "
            "Host md5 139 of 139 equal to the release blobs, 65 env keys, no MUSE_CLIENT_ID, tools/list 103 before and after, 27 of 27 tools, health 200. 30-minute service read-back: "
            "31 probes, service RSS 113.5 to 132.2 MB, host max 52.1 percent, 0 triggers; the service served ZERO window calls in it. Rollback: the pre-deploy content held by "
            "d3ae88be46, S3 tarball sha256 764f565cffef.", ["AC2"]),
        art(W + "CODE5_SERVED.json", "doc", GIT, "Counts, seconds, percentages, dates and booleans only; memory_basis fresh_process; the limits state that the service heap over a full chain is not measured.", ["AC2"]),
        art(W + "MEM_GATE.json", "doc", GIT, "The Phase A memory gate: median growth -10.4 MB per page over pages 2 to 4, first page 30.4 s.", ["AC1"]),
        art(W + "CHAIN_PRE.json", "doc", GIT, "CTO CT1 Amendment 2: two full 12-page chains in one fresh process, the second chain's net growth +24.9 MB (limit 50), host peak 55.1 percent.", ["AC2"]),
        art(W + "ap34_release.json", "doc", GIT, "base d3ae88be46, release 9d5b712557, trunk d9364e3e9c (full shas).", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-34.md", "doc", GIT, "The ask, sha256 bdccc464670e, signed by CTO 9bbfd119eb, COO 1c5a9ba7ee, CVO b94a795131.", ["AC1"]),
        art(LEDGER, "doc", GIT, "Ledger nfra-oplgtw-gateway-release-batch5 opened before the act, three legs proven, CLOSED; sentinel removed.", ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit 9d5b712557, previous d3ae88be46; file_checksums cross-checked against the host (10 of 10).", ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": re.search(r"`%s`: (.*?)(?=\n- `AC\d`|\n\n)" % cid, order, re.S).group(1).replace("\n", " ")[:500], "method": "command",
         "invocation": 'bash %s%s; echo "exit=$?"' % (CK, "ap34.%s.sh" % cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": ("9 files in the diff; 4 memory-gate pages; 3 halves" if cid == "AC1" else "27 tools; 139 host files; 5 arms; 31 read-back probes; 1 ledger of 3 legs"),
         "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ",
                        "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls (memory gate median 40 MB per page; first page 50 s; the memory record of another release; tools.py touched; the old catalog blob) are the discriminating arms.",
                   "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "AC3 (judgment, 3.0.0_SA_CVO~Z): the 13-month transactions and fees read as an analyst would want", "reason": "A judgment criterion is graded by the CVO on the bodies the issuer relays; it is never self-graded here."},
        {"item": "a page chain run in the SERVICE process", "reason": "/mcp takes only a bearer signed by the gateway key; minting one as a roster principal is impersonation (CTO Amendment 1 ruled a fresh-process chain). The service served zero window calls in the 30-minute read-back."}],
    "surprises": ["NFRA_OPLGTW-Z-S350: OBSERVATION (CVO) -- window_read_busy cannot occur in the service (sync tools run on the event loop); not graded as a served outcome."],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1 (GOs msgs 35362, 35371, 35383; CTO Amendments 1 and 2). C2 re-reads equal; stand-in cannot reach the service (stopped and reported); the plateau test; ledger opened and merged; one deploy; host md5, tools/list, 27-tool harness, arms, 30-minute read-back, window-call count; manifest and runbook on box/sitez; ledger closed; AC1 and AC2 run.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ap34_fullchain.py, ap34_arms.py, ap34_monitor.py, ap34_wincalls.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, percentages, dates and UTC times only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-34.round-40-fourth-batched-release.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
