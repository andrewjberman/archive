#!/usr/bin/env python
"""OG-ap-40: write the proof_of_spec instance for the order from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ap40_proof_gen.py   (from the repo root of the worktree on box/sitez, after the Phase B commits and the ledger close; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r42/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-40.round-42-eighth-batched-release-probe-listener.md"
LEDGER = "org/critical_paths/change_management/20261018T0945Z_nfra-oplgtw-gateway-release-batch9_deploy_completion.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
CHAN = "org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md"
RELEASE = "3b94a83e0572f9a14851c2f229ca4aba64c7e670"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("ap40.%s.sh" % cid), run("ap40.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else RELEASE, "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "the release is exactly the three files, byte-equal to trunk's, nothing barred; the SSRF audit reads CLEAN 0; harvest_research.py is carried at the live ref's blob; the host measurements of the listener under the guard pass; the ask has the three halves.",
    "AC2": "the release landed and closed, after the clock and failed units were read; the 27-tool served read passes 27 of 27 under the guard; the service was driven THROUGH THE LISTENER on one arming (etfs_compare_peers with the heap printed, the window chain with the heap flat, the refusals, the expiry, the delete and ParameterNotFound).",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-40", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:ec2/i-07dccb1615503ac99/opt/opal-gateway (opal-gateway service, round-42 eighth batched release: the loopback probe listener)", "aws_resource", "DEPLOYED-VERIFIED",
            "ONE deploy of release %s at 2026-10-18T09:50Z to 09:52Z through safe-ec2-deploy.sh, DEPLOY_BASE_REF=aa2efa2cf3, guard equal at both checkpoints, HALT_ACK after reading the messages (the first call stopped at the halt gate), no HALT_OVERRIDE. "
            "Host md5 140 of 140 equal to the release blobs, harvest_research.py md5 596c299597067fe5a8afb8e3493a0ed9 equal to the blob (CT1), 65 env keys, no MUSE_CLIENT_ID, tools/list 103 before and after, health 200, the marker equal to the release sha, unit limits unchanged. "
            "27 of 27 under the hard guard. ONE arming of 25 minutes: etfs_compare_peers 57 rows with the service heap 134 to 260 MB, the 12-page window chain with median growth 1.65 MB and highest VmRSS 392 MB, the refusals, the lapse, the delete (ParameterNotFound), NRestarts 0. "
            "31-minute read-back: 32 probes, one PID, 0 triggers. Rollback: the live ref's tarball opal-gateway-aa2efa2cf3.tar.gz, 903604 bytes, sha256 1c9ead556da8; not used." % RELEASE, ["AC2"]),
        art(W + "CODE9_SERVED.json", "doc", GIT, "Counts, bytes, seconds, words and booleans only; the probe block (one arming), the unit limits, the clock and failed units read before the close, NRestarts 0.", ["AC2"]),
        art(W + "PHASE_A_OG-ap-40.json", "doc", GIT, "Phase A: the listener measured in a guarded scratch process with a fake lease source; step zero (the gateway role may read the lease parameter); the ALB target group; tests; the full suite's failing set equal to the live ref's.", ["AC1"]),
        art(W + "ap40_release.json", "doc", GIT, "base aa2efa2cf3, release 3b94a83e05, trunk 9caafbe4ef (full shas).", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-40.md", "doc", GIT, "The ask, sha256 723cf849a41a, signed by CTO 6be7d4ffe9, COO 542bfd58fb, CVO b0c17d02f0.", ["AC1"]),
        art(LEDGER, "doc", GIT, "Ledger nfra-oplgtw-gateway-release-batch9 opened before the act, three legs proven, CLOSED 2026-10-18T10:31:55Z after the clock and failed units were read (10:26:20Z) and the lease parameter was read absent; sentinel removed.", ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit 3b94a83e05, previous aa2efa2cf3; file_checksums cross-checked against the host (10 of 10); one moves (app/server.py).", ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %sap40.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": ("3 files in the diff; 0 outside the take list; 3 halves" if cid == "AC1" else "27 tools; 140 host files; 12 chain pages; 1 arming; 32 read-back probes; 1 ledger of 3 legs"),
         "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls are the discriminating arms.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "a SECOND arming of the listener", "reason": "The CTO's ruling (msg 35661) allows exactly one: the lease does not pin the firm, so a second arming waits for a round-43 cell that pins it."},
        {"item": "the disarm of Z-S375 and Z-S338", "reason": "Done by the CVO's clock on the issuer's word after the issuer's own run of ap40.AC2 (condition C14); the applier disarms nothing."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ap-40 (GOs 35648 and 35666, amendments A1 to A5). Phase A: step zero, the SSRF gate, the re-cut as 3b94a83e05, the listener measured on the host in a guarded fresh process with a fake lease source, tests and the ask (sha256 723cf849a41a); the three halves signed. Phase B: preconditions re-read (the manifest, the host md5, no lease parameter, the sentinel union), ledger opened and merged, one deploy (the first call stopped at the halt gate, the second ran with HALT_ACK), host md5, marker, unit limits and harvest md5 read, the one arming with the probes through the running service, the 27-tool read, the lapse and the delete, the 31-minute read-back, clock and failed units, manifest and runbook clauses, ledger closed 10:31:55Z, CLOSED time and final sha sent to the CTO and MSTR.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ap38_step1.py, ap40_probe_run.py, ap40_probe_host.py, ap36_guarded.py, ap40_monitor.py, ap38_wincalls.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, percentages, dates, hashes and UTC times only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-40.round-42-eighth-batched-release-probe-listener.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
