#!/usr/bin/env python
"""OG-ap-39: write the proof_of_spec instance for the order from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ap39_proof_gen.py   (from the repo root of the worktree on box/sitez, after the Phase B commits and the ledger close; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r42/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-39.round-42-seventh-batched-release-page-size.md"
LEDGER = "org/critical_paths/change_management/20261018T0617Z_nfra-oplgtw-gateway-release-batch8_deploy_completion.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
CHAN = "org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md"
RELEASE = "aa2efa2cf3dee82030c00f85425f686132adcf4a"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("ap39.%s.sh" % cid), run("ap39.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else RELEASE, "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "the re-cut carries exactly the two files, byte-equal to trunk's, nothing barred; harvest_research.py is carried unchanged at the live ref's blob; the 27-tool read live against candidate passes; the ask has the three halves.",
    "AC2": "the release landed and closed, after the clock and failed units were read; the unit's limits are still live; the served tool descriptions carry the absent_reason notes and the fee note is source-scoped; the 27-tool served read passes 27 of 27 under the hard guard.",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-39", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:ec2/i-07dccb1615503ac99/opt/opal-gateway (opal-gateway service, round-42 seventh batched release)", "aws_resource", "DEPLOYED-VERIFIED",
            "ONE deploy of release %s at 2026-10-18T06:20Z to 06:22Z through safe-ec2-deploy.sh, DEPLOY_BASE_REF=4257a2aa42, guard equal at both checkpoints, HALT_ACK after reading the messages (the first call stopped at the halt gate), no HALT_OVERRIDE. "
            "Host md5 139 of 139 equal to the release blobs, harvest_research.py md5 596c299597067fe5a8afb8e3493a0ed9 equal to the live ref's blob (CT1), 65 env keys, no MUSE_CLIENT_ID, tools/list 103 before and after, health 200, the marker equal to the release sha, "
            "MemoryMax 1468006400, MemoryHigh 1258291200, OOMScoreAdjust 300, cgroup memory.max 1468006400. 27 of 27 under the hard guard; the installed registry serves the notes on 5 of 5 client tools, the fee note source-scoped. "
            "30-minute read-back: 31 probes, one PID, NRestarts 0, service 124.3 to 133.4 MB, 0 triggers, 157 /mcp requests, ZERO window calls served. Rollback: the live ref's tarball opal-gateway-4257a2aa42.tar.gz, 902884 bytes, sha256 f59e4b4009cf; not used." % RELEASE, ["AC2"]),
        art(W + "CODE8_SERVED.json", "doc", GIT, "Counts, bytes, seconds, words and booleans only; the four arms, served_notes read from the installed registry, the unit limits, the clock and failed units read before the close, NRestarts 0.", ["AC2"]),
        art(W + "PHASE_A_OG-ap-39.json", "doc", GIT, "Phase A re-cut: the 27-tool read 27 of 27 equal, 103 tool names equal, 5 descriptions differ (the docstring notes).", ["AC1"]),
        art(W + "ap39_release.json", "doc", GIT, "base 4257a2aa42, release aa2efa2cf3, trunk 23efa6e1f4 (full shas).", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-39.md", "doc", GIT, "The ask, sha256 034d2c346e5d, signed by CTO 43b1f58f19, COO 2ce52fead7, CVO 50c8f718bf.", ["AC1"]),
        art(LEDGER, "doc", GIT, "Ledger nfra-oplgtw-gateway-release-batch8 opened before the act, three legs proven, CLOSED 2026-10-18T07:01:17Z after the clock and failed units were read (06:55:17Z); sentinel removed.", ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit aa2efa2cf3, previous 4257a2aa42; file_checksums cross-checked against the host (10 of 10); one moves (app/tools.py).", ["AC2"]),
        art(CHAN, "doc", GIT, "Row Z-S385 (the CVO's, the fee note) is the reason for the A4 re-cut; no new row was filed in Phase B.", ["AC1"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %sap39.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": ("2 files in the diff; 27 tools compared; 3 halves" if cid == "AC1" else "27 tools; 139 host files; 4 arms; 31 read-back probes; 1 ledger of 3 legs"),
         "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls are the discriminating arms.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "a page chain or window call in the SERVICE process", "reason": "The service served zero window calls in the read-back; Z-S338 is re-read, not closed."},
        {"item": "the Z-S375 disarm (a service etfs_compare_peers call)", "reason": "No organic call arrived and no seat mints a bearer; this order does not grade it. Disarm stays WITHHELD."}],
    "surprises": ["NFRA_OPLGTW-Z-S385"],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ap-39 (GOs 35608, 35625, 35636). Phase A cut on 43a6659615 was superseded by the CVO's row Z-S385 and re-cut as aa2efa2cf3 after OG-en-30. Phase B: C2 re-read of the open gateway ledgers; baseline page hashes and host md5 captured; ledger opened and merged; one deploy (the first call stopped at the halt gate, the second ran with HALT_ACK); host md5, marker, unit limits, harvest md5, page hashes and the installed registry's notes read; 27-tool served read; 30-minute read-back; clock and failed units read; manifest and runbook standing clauses; ledger closed 07:01:17Z; CLOSED time and final sha sent to the CTO and COO.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ap38_step1.py, ap39_notes.py, ap38_pagehash.py, ap36_guarded.py, ap38_monitor.py, ap38_wincalls.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, percentages, dates, hashes and UTC times only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-39.round-42-seventh-batched-release-page-size.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
