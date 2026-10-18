#!/usr/bin/env python
"""OG-ap-38: write W/NFRA_OPLGTW.TO-OG-ap-38.round-41-sixth-batched-release-hazard-repair.proof_of_spec.json from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ap38_proof_gen.py   (from the repo root of the worktree on box/sitez, after the Phase B commits; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-38.round-41-sixth-batched-release-hazard-repair.md"
LEDGER = "org/critical_paths/change_management/20261017T2315Z_nfra-oplgtw-gateway-release-batch7_deploy_completion.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
CHAN = "org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md"
RELEASE = "d077cef04333500595a7a531ebddc2f43e5f8789"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("ap38.%s.sh" % cid), run("ap38.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else RELEASE, "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "the re-cut carries exactly the five files, byte-equal to trunk's, nothing barred, and the host measurements under the hard guard passed (the call that ran away is bounded; a valid pair answers; the 49F chain unchanged; the unit acceptable to systemd).",
    "AC2": "the release landed and closed, after the clock and failed units were read; the unit's limits are live; the 27-tool served read passes 27 of 27 under the guard (the hazard Z-S375 is repaired).",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-38", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:ec2/i-07dccb1615503ac99/opt/opal-gateway (opal-gateway service and unit, round-41 sixth batched release)", "aws_resource", "DEPLOYED-VERIFIED",
            "ONE deploy of release %s at 2026-10-17T23:19Z to 23:21Z through safe-ec2-deploy.sh, DEPLOY_BASE_REF=efcc8ae19f, guard equal at both checkpoints, HALT_ACK after reading 37 messages, no HALT_OVERRIDE. Host md5 139 of 139 equal to the release blobs, "
            "65 env keys, no MUSE_CLIENT_ID, tools/list 103 before and after, health 200, the marker equal to the release sha, MemoryMax 1468006400, MemoryHigh 1258291200, OOMScoreAdjust 300, cgroup memory.max 1468006400. 27 of 27 under the hard guard. "
            "30-minute read-back: 31 probes, one PID, NRestarts 0, service 126.8 to 130.9 MB, 0 triggers, ZERO window calls served. Rollback: the live ref's tarball opal-gateway-efcc8ae19f.tar.gz, 900200 bytes, sha256 b07656f114f9; not used." % RELEASE, ["AC2"]),
        art(W + "CODE7_SERVED.json", "doc", GIT, "Counts, bytes, seconds, words and booleans only; the four arms, the unit limits, the clock and failed units read before the close, NRestarts 0, peers_through_service basis fresh_process (disarm WITHHELD).", ["AC2"]),
        art(W + "PHASE_A_OG-ap-38.json", "doc", GIT, "Phase A: the runaway call bounded (empty section, 475.5 MB), a valid pair (57 rows), the 49F chain by amendment A2's rule (median of five run medians 11.4 MB; the first run's 21.5 named), the unit, tool27 (26 of 27 equal).", ["AC1"]),
        art(W + "ap38_release.json", "doc", GIT, "base efcc8ae19f, release d077cef043, trunk bae898b6a7 (full shas).", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-38.md", "doc", GIT, "The ask, sha256 33686c0a63cb, signed by CTO f6807b0bba, CVO f1ac7e004e, COO 371e908238.", ["AC1"]),
        art(LEDGER, "doc", GIT, "Ledger nfra-oplgtw-gateway-release-batch7 opened before the act, three legs proven, CLOSED 2026-10-18T00:02:10Z after the clock and failed units were read (23:54:02Z); sentinel removed.", ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit d077cef043, previous efcc8ae19f; file_checksums cross-checked against the host (10 of 10).", ["AC2"]),
        art(CHAN, "doc", GIT, "Rows Z-S380 (Phase A first stop) and Z-S382 (the chain limb's first run).", ["AC1"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %sap38.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": ("5 files in the diff; 5 chain runs of 4 pages; 27 tools compared; 3 halves" if cid == "AC1" else "27 tools; 139 host files; 4 arms; 31 read-back probes; 1 ledger of 3 legs"),
         "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls (a file missing; tools.py in the diff; a candidate peak of 900 MB; the live code answering under the guard; no guard named; a wrong MemoryMax; the clock read after the close) are the discriminating arms.",
                   "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "peers_through_service basis service (the Z-S375 disarm evidence)", "reason": "/mcp takes only a bearer signed by the gateway key and no seat mints one (C6, C16); no organic etfs_compare_peers call arrived in the 30 minutes (audit records 0). The basis is fresh_process and ap38.AC2 grades the disarm WITHHELD, as the COO's condition C16 anticipated."},
        {"item": "a page chain or window call in the SERVICE process", "reason": "The service served zero window calls in the read-back; Z-S338 is re-read, not closed."}],
    "surprises": ["NFRA_OPLGTW-Z-S380", "NFRA_OPLGTW-Z-S382"],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ap-38 (GOs 35554, 35557, 35571, 35574; rulings 35556, 35559, 35563). Phase A stopped twice (Z-S380, Z-S382), the repairs OG-en-26 and the A2 rule followed, then tool27. Phase B: C2 re-read equal; baseline chain pages captured; ledger opened and merged; one deploy (the first call stopped at the halt gate); host md5, unit limits, marker, arms, the 27-tool read under the guard, a 30-minute read-back, clock and failed units read before the close, standing clauses, ledger closed. No gateway code ran on the host without the hard guard.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ap38_step1.py, ap38_installed.py, ap38_pagehash.py, ap36_guarded.py, ap38_monitor.py, ap38_wincalls.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, percentages, dates, hashes and UTC times only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-38.round-41-sixth-batched-release-hazard-repair.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
