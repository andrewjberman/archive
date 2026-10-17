#!/usr/bin/env python
"""OG-ap-36: write W/NFRA_OPLGTW.TO-OG-ap-36.round-41-fifth-batched-release.proof_of_spec.json from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ap36_proof_gen.py   (from the repo root of the worktree on box/sitez, after the Phase B commit; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-36.round-41-fifth-batched-release.md"
LEDGER = "org/critical_paths/change_management/20261017T1657Z_nfra-oplgtw-gateway-release-batch6_deploy_completion.md"
RELEASE = "efcc8ae19f7eebb04e2f45f45c0def28af037c24"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(path):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--", path], capture_output=True).stdout.decode().strip()


def vintage(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("ap36.%s.sh" % cid), run("ap36.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else RELEASE,
            "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-36", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": vintage(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": vintage(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:ec2/i-07dccb1615503ac99/opt/opal-gateway (opal-gateway service, round-41 fifth batched release)", "aws_resource", "DEPLOYED-VERIFIED",
            "ONE deploy of release %s at 2026-10-17T17:06Z through safe-ec2-deploy.sh, DEPLOY_BASE_REF=1753c741d9, guard equal at both checkpoints, HALT_ACK after reading 23 messages, no HALT_OVERRIDE. "
            "Host md5 139 of 139 equal to the release blobs, 65 env keys, no MUSE_CLIENT_ID, tools/list 103 before and after, health 200, marker equal to the release sha, "
            "harvest_research.py md5 equal to its 1753c741d9 blob. Served read 26 of 27 by ruling (exception etfs_compare_peers, row Z-S375). Read-back 2: 30 minutes, 0 triggers, ZERO window calls served. "
            "Rollback: the live ref's tarball opal-gateway-1753c741d9.tar.gz sha256 7cf249065b6b, not used." % RELEASE, ["AC2"]),
        art(W + "CODE6_SERVED.json", "doc", GIT, "Counts, seconds, percentages, dates and booleans only; memory_basis and e12_basis fresh_process; per_tool_exception etfs_compare_peers; host_clock Normal; systemd_failed_units 0.", ["AC2"]),
        art(W + "MEM_GATE_OG-ap-36.json", "doc", GIT, "The Phase A memory gate on 948e8b47cc: median growth +1.7 MB per page, first page 1.93 s.", ["AC1"]),
        art(W + "CT1_CONCURRENT_OG-ap-36.json", "doc", GIT, "CT1 on the re-cut: the second windowed call waits and equals solo under the real wait, answers window_read_busy under 0.5 s.", ["AC1"]),
        art(W + "ap36_release.json", "doc", GIT, "base 1753c741d9, release efcc8ae19f, trunk 409399f8716a (full shas).", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-36.md", "doc", GIT, "The ask, sha256 20815be2b2c6, signed by COO 23e5a7b07e, CTO f02ad0309a, CVO 1df8f8a2df.", ["AC1"]),
        art(LEDGER, "doc", GIT, "Ledger nfra-oplgtw-gateway-release-batch6 opened before the act, three legs proven, CLOSED 2026-10-17T18:11:52Z; sentinel removed.", ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit efcc8ae19f, previous 1753c741d9; file_checksums cross-checked against the host (10 of 10).", ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": re.search(r"`%s`: (.*?)(?=; `AC\d`|\n\n)" % cid, order, re.S).group(1).replace("\n", " ")[:500], "method": "command",
         "invocation": 'bash %sap36.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": ("9 files in the diff; 6 compared pages; 3 halves" if cid == "AC1" else "26 of 27 tools by ruling; 139 host files; 9 arms; 31 read-back probes; 1 ledger of 3 legs"),
         "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ",
                        "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls (the memory record of another release, a take-list file not byte-equal to trunk, a barred file in the diff) are the discriminating arms.",
                   "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "a page chain run in the SERVICE process", "reason": "/mcp takes only a bearer signed by the gateway key; the arms ran in a fresh process through the installed code. The service served zero window calls in read-back 2; Z-S338 stays open until an organic call."},
        {"item": "the 27th tool of the served read (etfs_compare_peers)", "reason": "Graded 26 of 27 by ruling (CTO 35540, 35541; COO 35543, amendment A7): the module is byte-equal on both refs and not this release's widening; row NFRA_OPLGTW-Z-S375 is open and ARMED. It is a trigger set aside by ruling, not one that stayed clear."}],
    "surprises": ["NFRA_OPLGTW-Z-S375"],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, Phase B (GO msgs 35534, 35535; rulings 35540, 35543, 35545, 35547). C2 re-reads equal at the GO; ledger opened and merged; one deploy (the first call stopped at the halt gate and deployed nothing); host md5, tools/list, arms (run twice: the first run's fees chain stopped on an empty page the harness read as a refusal), the 27-tool harness (run unguarded once: the host ran out of memory at 17:21Z and the kernel killed the gateway once and eight system daemons, since restored; then twice under a hard guard); read-back 1 spans that restart, read-back 2 is a clean 30 minutes; the ledger was closed at 18:11:52Z BEFORE the seat read the CVO's clock condition (A8), which then read Normal / synchronised / 0 failed units at 18:16:58Z after one stale init.scope flag was cleared.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ap36_arms.py, ap36_guarded.py, ap36_monitor.py, ap34_wincalls.py, ap36_host_md5.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, percentages, dates and UTC times only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-36.round-41-fifth-batched-release.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
