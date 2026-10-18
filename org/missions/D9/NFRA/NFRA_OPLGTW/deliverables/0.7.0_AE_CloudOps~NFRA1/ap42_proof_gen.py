#!/usr/bin/env python
"""OG-ap-42: write the proof_of_spec instance for the order from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ap42_proof_gen.py   (from the repo root of the worktree on box/sitez, after the Phase B commits and the ledger close; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r43/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-42.round-43-ninth-batched-release-firm-pin-and-graph-pin.md"
LEDGER = "org/critical_paths/change_management/20261018T1542Z_nfra-oplgtw-gateway-release-batch10_deploy_completion.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
CHAN = "org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md"
RELEASE = "a0c83303ee48c95c16a61c0d5e8bd186b1083b66"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("ap42.%s.sh" % cid), run("ap42.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else RELEASE, "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "the release is exactly the four files, byte-equal to trunk's, nothing barred; the SSRF audit reads CLEAN 0; the base is the live ref read on the host and dell1's four harvest files are carried unchanged; the pins are exercised on the host under the guard with a fake lease source and NO arming; the ask has the three halves.",
    "AC2": "the release landed and closed, after the clock and failed units were read; the 27-tool served read passes 27 of 27 under the guard; the listener was read UNARMED ONLY (403 probe_not_armed), armings 0, and the lease parameter was absent before and after.",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-42", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:ec2/i-07dccb1615503ac99/opt/opal-gateway (opal-gateway service, round-43 ninth batched release: the probe-lease firm pin and the Graph host pin)", "aws_resource", "DEPLOYED-VERIFIED",
            "ONE deploy of release %s at 2026-10-18T15:46Z to 15:49Z through safe-ec2-deploy.sh, DEPLOY_BASE_REF=922ee425fe, guard equal at both checkpoints, HALT_ACK after reading the messages (the first call stopped at the halt gate), no HALT_OVERRIDE. "
            "Host md5 141 of 141 equal to the release blobs, the host md5 of dell1's four harvest files and the two taken app files equal to the release's, 65 env keys, no MUSE_CLIENT_ID, tools/list 103 before and after, health 200, the marker equal to the release sha, unit limits unchanged. "
            "27 of 27 under the hard guard. UNARMED ONLY: the lease parameter absent before, after and at the close, no SSM write by this seat, three calls to the listener answered 403 probe_not_armed, the service PID unchanged and NRestarts 0. "
            "31-minute read-back: 32 probes, one PID, 0 triggers, 272 Graph-backed tool calls (hx_teams 103, hx_msgs 30, poll_addressed_teams_messages 69, read_channel_messages 69, whoami 1; all ok), 0 GraphHostRefused (the first count of 1 was wrong and is superseded). Rollback: the live ref's tarball opal-gateway-922ee425fe.tar.gz, 913956 bytes, sha256 d025c8a103f3; not used." % RELEASE, ["AC2"]),
        art(W + "CODE10_SERVED.json", "doc", GIT, "Counts, bytes, seconds, words and booleans only; the unarmed probe block, the unit limits, the clock and failed units read before the close, NRestarts 0, the Graph counts of the CTO's CT4.", ["AC2"]),
        art(W + "PHASE_A_OG-ap-42.json", "doc", GIT, "Phase A: the firm pin (4 mismatches refused with 0 tool runs, 3 firm-less leases malformed) and the Graph pin (7 of 7 forged URLs refused, 0 clients built) measured on the host under the guard with a fake lease source; tests; the full suite's failing set equal to the live ref's.", ["AC1"]),
        art(W + "ap42_release.json", "doc", GIT, "base 922ee425fe (= live_ref_host), release a0c83303ee, trunk ada46a0f40 (full shas) and dell1's four harvest blobs.", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-42.md", "doc", GIT, "The ask, sha256 cd24609722a8, signed by CTO 79867ca983, COO 990b4e2cf1, CVO b838692826.", ["AC1"]),
        art(LEDGER, "doc", GIT, "Ledger nfra-oplgtw-gateway-release-batch10 opened before the act, three legs proven, CLOSED 2026-10-18T16:32:05Z after the clock and failed units were read (16:23:01Z) and the lease parameter was read absent (16:25:35Z); sentinel removed.", ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit a0c83303ee, previous 922ee425fe; file_checksums cross-checked against the host (10 of 10); one moves (app/graph.py).", ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %sap42.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": ("4 files in the diff; 0 outside the take list; 4 of 4 harvest files carried; 3 halves" if cid == "AC1" else "27 tools; 141 host files; 3 unarmed calls; 32 read-back probes; 1 ledger of 3 legs"),
         "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls are the discriminating arms.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "the firm pin exercised in the SERVICE", "reason": "No lease was written (NO ARMING, NO SSM write: the order and the CTO's CT3); the pin was exercised in a guarded scratch process in Phase A and is exercised in the service by the later arming order OG-ev-7."},
        {"item": "a live Graph call through the allowed branch", "reason": "The allowed branch is proven by a stub and the 21-site audit; the read-back window held 272 organic Graph-backed tool calls (all ok) and 0 GraphHostRefused lines; the journal's access log was silent in the window (row Z-S395), so the counts come from the audit lake."}],
    "surprises": ["NFRA_OPLGTW-Z-S395"],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ap-42 (GOs 35721 and 35741, amendment A1). Phase A: the host's live ref read (922ee425fe), the SSRF gate, the re-cut as a0c83303ee, the pins measured on the host in a guarded fresh process with a fake lease source on a test port, tests and the ask (sha256 cd24609722a8); the three halves signed. Phase B: preconditions re-read (the host marker, the md5 walk, the lease parameter absent, the open ledgers), ledger opened and merged, one deploy (the first call stopped at the halt gate, the second ran with HALT_ACK), host md5, marker, unit limits and the six named files' md5 read, the served read UNARMED ONLY, the 27-tool read, the 31-minute read-back with the Graph counts, clock and failed units, manifest and runbook clauses, ledger closed 16:32:05Z, CLOSED time and final sha sent to the CTO and MSTR.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ap38_step1.py, ap42_pins.py, ap42_unarmed_run.py, ap40_probe_host.py, ap36_guarded.py, ap40_monitor.py, ap42_graphcounts.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, percentages, dates, hashes and UTC times only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-42.round-43-ninth-batched-release-firm-pin-and-graph-pin.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
