#!/usr/bin/env python
"""OG-ap-44: write the proof_of_spec instance for the order from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ap44_proof_gen.py   (from the repo root of the worktree on box/sitez, after the Phase B commits and the ledger close; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r43/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-44.round-43-tenth-batched-release-access-log-repair.md"
LEDGER = "org/critical_paths/change_management/20261018T1919Z_nfra-oplgtw-gateway-release-batch11_deploy_completion.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
CHAN = "org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md"
RELEASE = "eff517546eeea48811cf13f3de38926c5944c6df"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
C11 = json.load(io.open(W + "CODE11_SERVED.json", encoding="utf-8"))["body"]
AL, RBK, CLK = C11["access_log"], C11["readback"], C11["host_clock"]
LEDGER_TEXT = io.open(LEDGER, encoding="utf-8").read()
CLOSED_AT = re.search(r"closed (\d{8}T\d{6}Z)", LEDGER_TEXT).group(1)
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("ap44.%s.sh" % cid), run("ap44.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else RELEASE, "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "the release is exactly the two files, byte-equal to trunk's, nothing barred; the base is the live ref read on the host and dell1's four harvest files are carried unchanged; in a fresh process on the host the four uvicorn loggers read the same before and after the listener's server is built, an access record still reaches the service's handler, the restore ran on a raising Config; no arming; the ask has the three halves.",
    "AC2": "the release landed and closed, after the clock and failed units were read; the 27-tool served read passes 27 of 27 under the guard; the listener was read UNARMED ONLY (403 probe_not_armed), armings 0; and THE ACCESS LOG IS BACK: the journal's POST /mcp lines over the 30-minute read-back are above zero and at least a quarter of the audit-lake records over the same window, and the listener's own /probe/ lines equal the requests made.",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-44", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:ec2/i-07dccb1615503ac99/opt/opal-gateway (opal-gateway service, round-43 tenth batched release: the repair of the access-log regression)", "aws_resource", "DEPLOYED-VERIFIED",
            "ONE deploy of release %s at 2026-10-18T19:21Z to 19:24Z through safe-ec2-deploy.sh, DEPLOY_BASE_REF=a0c83303ee, guard equal at both checkpoints, HALT_ACK after reading the messages (the first call stopped at the halt gate), no HALT_OVERRIDE. "
            "Host md5 141 of 141 equal to the release blobs, the host md5 of dell1's four harvest files, graph.py and probe_listener.py equal to the release's, 65 env keys, no MUSE_CLIENT_ID, tools/list 103 before and after, health 200, the marker equal to the release sha, unit limits unchanged. "
            "27 of 27 under the hard guard. UNARMED ONLY: the lease parameter absent before, after and at the close, no SSM write by this seat, %d calls to the listener answered 403 probe_not_armed, the service PID unchanged and NRestarts 0. "
            "THE ACCESS LOG: over the 30-minute read-back the journal holds %d POST /mcp lines against %d audit-lake records (ratio %s; the window before the OG-ap-40 deploy held %d); the listener's %d /probe/ lines equal the %d requests made. "
            "Read-back: %d probes, one PID, %d triggers. Rollback: the live ref's tarball opal-gateway-a0c83303ee.tar.gz, 914681 bytes, sha256 772364295276; not used."
            % (RELEASE, AL["listener_requests_made"], AL["post_mcp_lines_readback"], AL["audit_records_readback"], AL["ratio_lines_to_records"], AL["post_mcp_lines_before_ap40_30min"], AL["listener_access_lines"], AL["listener_requests_made"],
               RBK["probes"], RBK["triggers_fired"]), ["AC2"]),
        art(W + "CODE11_SERVED.json", "doc", GIT, "Counts, bytes, seconds, words and booleans only; the unarmed probe block, the access-log block (journal and lake over the same window), the unit limits, the clock and failed units read before the close, NRestarts 0.", ["AC2"]),
        art(W + "PHASE_A_OG-ap-44.json", "doc", GIT, "Phase A: in a fresh guarded process on the host the live ref's make_server empties the uvicorn.access handlers (the regression reproduced) and the candidate's leaves the four loggers unchanged, with the restore shown on a raising Config; tests; the full suite's failing set equal to the live ref's.", ["AC1"]),
        art(W + "ap44_release.json", "doc", GIT, "base a0c83303ee (= live_ref_host), release eff517546e, trunk b527ac88db (full shas).", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-44.md", "doc", GIT, "The ask, sha256 29959e4b1fee, signed by CTO a6538b26ad, COO 56da302547, CVO f66d721c05.", ["AC1"]),
        art(LEDGER, "doc", GIT, "Ledger nfra-oplgtw-gateway-release-batch11 opened before the act, three legs proven, CLOSED %s after the clock and failed units were read (%s) and the lease parameter was read absent; sentinel removed." % (CLOSED_AT, CLK["read_at"]), ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit eff517546e, previous a0c83303ee; file_checksums cross-checked against the host (10 of 10); none moves (probe_listener.py is not among the ten).", ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %sap44.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": ("2 files in the diff; 0 outside the take list; 4 of 4 harvest files carried; 3 halves" if cid == "AC1" else "27 tools; 141 host files; %d listener requests; %d read-back probes; %d journal lines against %d lake records; 1 ledger of 3 legs" % (AL["listener_requests_made"], RBK["probes"], AL["post_mcp_lines_readback"], AL["audit_records_readback"])),
         "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls (a zero-lines record, a 40-of-290 record, a listener-lines record) are the discriminating arms.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "the listener's access lines read as 0", "reason": "The order's first rule (listener lines 0) could not hold (row Z-S397: uvicorn logs per connection by hasHandlers()); the issuer amended AC2 to require the listener's lines to EQUAL the requests this seat made, which they do."},
        {"item": "an arming of the listener", "reason": "None in this order (NO ARMING, NO SSM write); OG-ev-7 is re-based on this release's live sha and needs its own three halves."}],
    "surprises": ["NFRA_OPLGTW-Z-S395", "NFRA_OPLGTW-Z-S397"],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ap-44 (GOs 35774 and 35784, amendment A1). Phase A: the host's live ref and uvicorn version read, the re-cut as eff517546e, the loggers measured on the host in a guarded fresh process (the live make_server reproduces the regression, the candidate's leaves the loggers unchanged), tests and the ask (sha256 29959e4b1fee); row Z-S397 (the listener's own lines) filed and AC2 amended by the issuer; the three halves signed. Phase B: preconditions re-read (the host marker, the md5 walk, the lease parameter absent, the open ledgers), ledger opened and merged, one deploy (the first call stopped at the halt gate, the second ran with HALT_ACK), host md5, marker, unit limits and the six named files' md5 read, the served read UNARMED ONLY, the 27-tool read, the 31-minute read-back with the journal and lake counts, clock and failed units, manifest and runbook clauses, ledger closed %s, CLOSED time and final sha sent to the CTO and MSTR." % CLOSED_AT,
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ap38_step1.py, ap44_loggers.py, ap42_unarmed_run.py, ap40_probe_host.py, ap36_guarded.py, ap40_monitor.py, ap44_accesslog.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, percentages, dates, hashes and UTC times only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-44.round-43-tenth-batched-release-access-log-repair.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
