#!/usr/bin/env python
"""OG-ap-50: write the proof_of_spec instance for the order from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ap50_proof_gen.py   (from the repo root of the worktree on box/sitez, after the Phase B commits and the ledger close; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r46/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-50.round-46-thirteenth-batched-release-the-family-depth-route.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
RELEASE = "6d1b5dcb64b945deb98664c6ae078d8f1e8a6c5c"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


ledger = subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/change_management/"], capture_output=True).stdout.decode().split()
LEDGER = [p for p in ledger if p.endswith("_nfra-oplgtw-gateway-release-batch14_deploy_completion.md")][-1]
order = io.open(TO, encoding="utf-8").read()
C13 = json.load(io.open(W + "CODE14_SERVED.json", encoding="utf-8"))["body"]
AL, RBK, CLK, AFC = C13["access_log"], C13["readback"], C13["host_clock"], C13["audit_failure_counter"]
LEDGER_TEXT = io.open(LEDGER, encoding="utf-8").read()
CLOSED_AT = re.search(r"closed (\d{8}T\d{6}Z)", LEDGER_TEXT).group(1)
ac = {}
for cid in ("AC1", "AC2", "AC3"):
    outs = [run("ap50.%s.sh" % cid), run("ap50.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else RELEASE, "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "the release is exactly the two files (admin_api.py with two added lines, test_og_cd2.py), byte-equal to trunk's, nothing barred; the base is the live ref read on the host and dell1's four harvest files are carried unchanged; in a fresh guarded process on the host the admin app has one more route, /gateway/families answers 401 with no identity, 403 to a verified non-owner and never calls read(), the whoami control answers 401 and a missing route 404; the real family_depth.read() runs once on the host as the gateway instance role (families equal to the denominator, measured values above zero, claim-less zero); process-wide state is named; no arming; the ask has the three halves and the process-wide state line.",
    "AC2": "the release landed and closed, after the clock and failed units were read; the 27-tool served read passes 27 of 27 under the guard; the listener was read UNARMED ONLY (403 probe_not_armed), armings 0; the dual count: the journal's POST /mcp lines over the 30-minute read-back are above zero and at least a quarter of the audit-lake records over the same window, and the listener's own /probe/ lines equal the requests made; the audit failure counter reads 0; and the new route is mounted behind the owner gate on the running service (404 before the deploy, 401 after with no identity header, the whoami control 401, a missing route 404).",
    "AC3": "the FWD-20 proof: the DEPLOYED family_depth module read once on the host in a fresh guarded process as the gateway instance role after the release is live; every value carries a claim and every absent value its reason; one family's cadence equals its live schedule and one family's depth (frontier and earliest served date) equals the independent reads of its status object and first silver partition; no write attempted; no e-mail-shaped string and no run of 9 or more digits in the record.",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-50", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:ec2/i-07dccb1615503ac99/opt/opal-gateway (opal-gateway service, round-46 thirteenth batched release: the family_depth route GET /api/admin/gateway/families, owner-gated)", "aws_resource", "DEPLOYED-VERIFIED",
            "ONE deploy of release %s at 2026-10-19T16:35:59Z through safe-ec2-deploy.sh from rel-nfra-oplgtw-batch14, DEPLOY_BASE_REF=6b1a9bd292 (the live ref read on the host), guard equal at both checkpoints, HALT_ACK after the messages were read (none a hold), no HALT_OVERRIDE. "
            "Host md5 143 of 143 equal to the release blobs; the host md5 of dell1's four harvest files, graph.py, probe_listener.py, audit.py, admin_api.py and family_depth.py equal to the release's (9 of 9); 65 env keys, no MUSE_CLIENT_ID, tools/list 103 before and after, health 200, the marker equal to the release sha, unit limits unchanged. "
            "27 of 27 under the hard guard. THE ROUTE on the running service (local request, no identity header): 404 before the deploy, 401 after, the whoami control 401, a missing route 404. "
            "UNARMED ONLY: the lease parameter absent before, after and at the close, no SSM write by this seat, %d calls to the listener answered 403 probe_not_armed, the service PID unchanged and NRestarts 0. "
            "THE DUAL COUNT: over the 30-minute read-back the journal holds %d POST /mcp lines against %d audit-lake records (ratio %s); the listener's %d /probe/ lines equal the %d requests made. "
            "THE COUNTER: %d audit-lake WARN lines in the journal over the read-back, counter value %d. Read-back: %d probes, one PID, %d triggers. "
            "Rollback: the live ref's tarball opal-gateway-6b1a9bd292.tar.gz, 922261 bytes, sha256 6fa88e6f58d5; not used."
            % (RELEASE, AL["listener_requests_made"], AL["post_mcp_lines_readback"], AL["audit_records_readback"], AL["ratio_lines_to_records"], AL["listener_access_lines"], AL["listener_requests_made"],
               AFC["journal_lines_readback"], AFC["counter_value"], RBK["probes"], RBK["triggers_fired"]), ["AC2"]),
        art(W + "CODE14_SERVED.json", "doc", GIT, "Counts, bytes, seconds, words and booleans only; the route block (404, 401, 401, 404), the unarmed probe block, the access-log block (journal and lake over the same window), the audit failure counter, the unit limits, the clock and failed units read before the close, NRestarts 0.", ["AC2"]),
        art(W + "FWD20_DRIVEN_READ.json", "doc", GIT, "The ONE driven read of the deployed module (FWD-20): 13 of 13 rows, 59 values (17 measured, 11 inferred, 31 absent each with a reason, 0 claim-less), 0 writes; the eclipse family's schedule, frontier and earliest served date equal my own AWS CLI reads; the deploy script staged in a scratch tree only (row Z-S406 ruling), disclosed.", ["AC3"]),
        art(W + "PHASE_A_OG-ap-50.json", "doc", GIT, "Phase A: in fresh guarded processes on the host the admin app has 16 routes against 15, /gateway/families answers 401 / 403 and never calls read() on a refusal; the real read() as the instance role returned 13 of 13 rows; tests; the full suite's failing set equals the live ref's (74 each).", ["AC1"]),
        art(W + "ap50_release.json", "doc", GIT, "base 6b1a9bd292 (= live_ref_host), release 6d1b5dcb64, trunk 49de05db93 (full shas).", ["AC1", "AC3"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-50.md", "doc", GIT, "The ask, sha256 50ed64086cb3, signed by CTO 10285a7d35, COO e7b6fb5676 (G1-G8) and CVO b6d2c59637 (C1).", ["AC1"]),
        art(LEDGER, "doc", GIT, "Ledger nfra-oplgtw-gateway-release-batch14 opened before the act, three legs proven, CLOSED %s after the clock and failed units were read (%s) and the lease parameter was read absent; sentinel removed." % (CLOSED_AT, CLK["read_at"]), ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit 6d1b5dcb64, previous 6b1a9bd292; file_checksums cross-checked against the host (10 of 10); none moves.", ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %sap50.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": {"AC1": "2 files in the diff; 0 outside the take list; 4 of 4 harvest files carried; 3 halves; 16 routes against 15; 13 rows of 13",
                         "AC2": "27 tools; 143 host files; %d listener requests; %d read-back probes; %d journal lines against %d lake records; %d audit-lake WARN lines; 3 route reads; 1 ledger of 3 legs" % (
                             AL["listener_requests_made"], RBK["probes"], AL["post_mcp_lines_readback"], AL["audit_records_readback"], AFC["journal_lines_readback"]),
                         "AC3": "13 rows; 59 values; 1 family compared on cadence and depth; 0 writes"}[cid],
         "status": "PASS"} for cid in ("AC1", "AC2", "AC3")],
    "controls": {
        "determinism": {"method": "AC1, AC2 and AC3 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut arms and the 401 / 403 / 404 controls are the discriminating arms.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "an arming of the listener", "reason": "None in this order (NO ARMING, NO SSM write)."},
        {"item": "the owner's 200 branch of the route on the running service", "reason": "The owner's identity header comes only from the load balancer, so no agent can supply it; the owner's own read of the panel is Andrew's, later, and not this order's. The 401 branch read after the deploy is the served proof of the gate."},
        {"item": "a push", "reason": "The order forbids it; the issuer drains the branch."}],
    "surprises": [
        "NFRA_OPLGTW-Z-S406: a fresh process needs deploy-to-ec2.sh, which is absent on the host; the driven read staged the release's byte-equal copy in a scratch tree only (COO ruling, row Z-S408).",
        "NFRA_OPLGTW-Z-S407: the route's response can carry the role ARN and account number in AWS error text (8 of 59 values); released as ruled, the mask is cut for round 47; no record of this order carries either."],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ap-50 (GOs 35983 and 36000). Phase A: the live ref 6b1a9bd292 read on the host, the release cut in a clean sparse tree as 6d1b5dcb64 from trunk 49de05db93 (two files whole), the route leg and the real family_depth read measured on the host under the cgroup guard, tests in both orders, the full suite compared with the live ref's (identical failing sets), the ask written with the response-content widening disclosed. Phase B: step 1 re-read, ledger batch14 opened first, the route read 404, the wrapper deployed 16:33Z to 16:36Z, the route read 401, the served read UNARMED ONLY, the 27-tool read, the 30-minute read-back and dual count, the driven read and my own independent CLI reads, host clock and failed units read before the close at 17:23:23Z; the manifest auto-commit refused as in earlier releases and recorded on box/sitez by ap50_manifest.py after a host md5 control.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ap38_step1.py, ap50_host.py, ap50_route.py, ap42_unarmed_run.py, ap36_guarded.py, ap38_monitor.py, ap44_accesslog.py, ap50_auditwarn.py, ap50_driven.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, percentages, dates, hashes and UTC times only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-50.round-46-thirteenth-batched-release-the-family-depth-route.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
