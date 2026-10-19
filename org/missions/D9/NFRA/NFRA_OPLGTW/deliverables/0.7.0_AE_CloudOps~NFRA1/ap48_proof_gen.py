#!/usr/bin/env python
"""OG-ap-48: write the proof_of_spec instance for the order from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ap48_proof_gen.py   (from the repo root of the worktree on box/sitez, after the Phase B commits and the ledger close; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r45/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-48.round-45-twelfth-batched-release-the-audit-lake-leg.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
RELEASE = "6b1a9bd292855841826e194d0bddf9ac79bc8337"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


ledger = subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/change_management/"], capture_output=True).stdout.decode().split()
LEDGER = [p for p in ledger if p.endswith("_nfra-oplgtw-gateway-release-batch13_deploy_completion.md")][-1]
order = io.open(TO, encoding="utf-8").read()
C13 = json.load(io.open(W + "CODE13_SERVED.json", encoding="utf-8"))["body"]
AL, RBK, CLK, AFC = C13["access_log"], C13["readback"], C13["host_clock"], C13["audit_failure_counter"]
LEDGER_TEXT = io.open(LEDGER, encoding="utf-8").read()
CLOSED_AT = re.search(r"closed (\d{8}T\d{6}Z)", LEDGER_TEXT).group(1)
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("ap48.%s.sh" % cid), run("ap48.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else RELEASE, "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "the release is exactly the two files (audit.py, test_og_pr6.py), byte-equal to trunk's, nothing barred; the base is the live ref read on the host and dell1's four harvest files are carried unchanged; in a fresh guarded process on the host the audit S3 client has bounded timeouts and a retry cap, a put to a black-hole endpoint raises within a bound, the failure counter reads 1, one stderr line is written and the floor line is still written; process-wide state is named; no arming; the ask has the three halves and the process-wide state line.",
    "AC2": "the release landed and closed, after the clock and failed units were read; the 27-tool served read passes 27 of 27 under the guard; the listener was read UNARMED ONLY (403 probe_not_armed), armings 0; the dual count: the journal's POST /mcp lines over the 30-minute read-back are above zero and at least a quarter of the audit-lake records over the same window, and the listener's own /probe/ lines equal the requests made; and the audit failure counter reads 0 (no audit-lake WARN line in the read-back).",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-48", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:ec2/i-07dccb1615503ac99/opt/opal-gateway (opal-gateway service, round-45 twelfth batched release: the audit lake leg bounded and audible)", "aws_resource", "DEPLOYED-VERIFIED",
            "ONE deploy of release %s at 2026-10-19T07:02Z to 07:05Z through safe-ec2-deploy.sh, DEPLOY_BASE_REF=e09c30c3f0, guard equal at both checkpoints, HALT_ACK after reading the messages (the first call stopped at the halt gate, none a hold), no HALT_OVERRIDE. "
            "Host md5 143 of 143 equal to the release blobs; the host md5 of dell1's four harvest files, graph.py, probe_listener.py and audit.py equal to the release's (7 of 7); 65 env keys, no MUSE_CLIENT_ID, tools/list 103 before and after, health 200, the marker equal to the release sha, unit limits unchanged. "
            "27 of 27 under the hard guard. UNARMED ONLY: the lease parameter absent before, after and at the close, no SSM write by this seat, %d calls to the listener answered 403 probe_not_armed, the service PID unchanged and NRestarts 0. "
            "THE DUAL COUNT: over the 30-minute read-back the journal holds %d POST /mcp lines against %d audit-lake records (ratio %s; the window before the OG-ap-40 deploy held %d); the listener's %d /probe/ lines equal the %d requests made. "
            "THE NEW COUNTER: %d audit-lake WARN lines in the journal over the read-back, counter value %d. The client makes two sends (max_attempts 1 is one retry in botocore). "
            "Read-back: %d probes, one PID, %d triggers. Rollback: the live ref's tarball opal-gateway-e09c30c3f0.tar.gz, 921536 bytes, sha256 ebc920a03536; not used."
            % (RELEASE, AL["listener_requests_made"], AL["post_mcp_lines_readback"], AL["audit_records_readback"], AL["ratio_lines_to_records"], AL["post_mcp_lines_before_ap40_30min"], AL["listener_access_lines"], AL["listener_requests_made"],
               AFC["journal_lines_readback"], AFC["counter_value"], RBK["probes"], RBK["triggers_fired"]), ["AC2"]),
        art(W + "CODE13_SERVED.json", "doc", GIT, "Counts, bytes, seconds, words and booleans only; the unarmed probe block, the access-log block (journal and lake over the same window), the audit failure counter, the unit limits, the clock and failed units read before the close, NRestarts 0.", ["AC2"]),
        art(W + "PHASE_A_OG-ap-48.json", "doc", GIT, "Phase A: in a fresh guarded process on the host the audit client has connect 2 s, read 3 s and a retry cap; a put to a black-hole endpoint raised in 4.33 s after 2 sends; counter 1, one stderr line, floor line written; tests; the full suite's failing set equals the live ref's.", ["AC1"]),
        art(W + "ap48_release.json", "doc", GIT, "base e09c30c3f0 (= live_ref_host), release 6b1a9bd292, trunk 05a334c809 (full shas).", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ap-48.md", "doc", GIT, "The ask, sha256 942e7f6a3f0d, signed by CTO 2f57a5ef26, COO f89b95e3c6, CVO c57a121b47, with amendment A1.", ["AC1"]),
        art(LEDGER, "doc", GIT, "Ledger nfra-oplgtw-gateway-release-batch13 opened before the act, three legs proven, CLOSED %s after the clock and failed units were read (%s) and the lease parameter was read absent; sentinel removed." % (CLOSED_AT, CLK["read_at"]), ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit 6b1a9bd292, previous e09c30c3f0; file_checksums cross-checked against the host (10 of 10); none moves.", ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %sap48.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": ("2 files in the diff; 0 outside the take list; 4 of 4 harvest files carried; 3 halves" if cid == "AC1" else "27 tools; 143 host files; %d listener requests; %d read-back probes; %d journal lines against %d lake records; %d audit-lake WARN lines; 1 ledger of 3 legs" % (
             AL["listener_requests_made"], RBK["probes"], AL["post_mcp_lines_readback"], AL["audit_records_readback"], AFC["journal_lines_readback"])),
         "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls are the discriminating arms.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "an arming of the listener", "reason": "None in this order (NO ARMING, NO SSM write)."},
        {"item": "a write to the real audit lake in Phase A", "reason": "Phase A put to a non-routable endpoint in a scratch process; the lake was never written by the measurement."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ap-48 (GOs 35905 and 35912, amendment A1). Phase A: the live ref e09c30c3f0 read on the host, the release cut in a clean sparse tree as 6b1a9bd292 from trunk 05a334c809 (two files whole), the audit leg measured on the host under the cgroup guard against a black-hole endpoint (4.33 s, two sends, counter 1, one stderr line), tests in both orders, the full suite compared with the live ref's (identical failing sets), the ask written with the code-comment discrepancy recorded. Phase B: ledger batch13 opened first, the wrapper stopped once at the halt gate (no hold among the messages listed), HALT_ACK then deploy 07:02:30Z to 07:05:17Z; the manifest auto-commit refused as in earlier releases and was recorded on box/sitez by ap48_manifest.py after a host md5 control; the served read UNARMED ONLY, the dual count and the audit failure counter over the 30-minute read-back; host clock and failed units read before the close.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ap38_step1.py, ap48_audit.py, ap42_unarmed_run.py, ap40_probe_host.py, ap36_guarded.py, ap40_monitor.py, ap44_accesslog.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, percentages, dates, hashes and UTC times only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-48.round-45-twelfth-batched-release-the-audit-lake-leg.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
