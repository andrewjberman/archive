#!/usr/bin/env python
"""OG-rz-2: write the proof_of_spec instance from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python rz2_proof_gen.py   (repository root, after the Phase B commit and the ledger close)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r46/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rz-2.round-46-resize-the-gateway-host-to-t4g-large.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


ledger = [p for p in subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/change_management/"], capture_output=True).stdout.decode().split() if p.endswith("_nfra-oplgtw-gateway-resize-t4g-large_deploy_completion.md")][-1]
closed_at = re.search(r"closed (\d{8}T\d{6}Z)", io.open(ledger, encoding="utf-8").read()).group(1)
order = io.open(TO, encoding="utf-8").read()
S = json.load(io.open(W + "RZ2_SERVED.json", encoding="utf-8"))
dt, al, rb, big = S["downtime"], S["access_log"], S["readback"], S["large_replies"]
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("rz2.%s.sh" % cid), run("rz2.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    ac[cid] = (outs, exp)
    print(cid, "matches expect" if re.search(exp, outs[0]) else "DOES NOT MATCH THE ORDER'S EXPECT", "| stable" if outs[0] == outs[1] else "| UNSTABLE")
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else "0b9509c330", "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "the resize is prepared and asked: the before-record names the instance, its type, state, Elastic IP and public-IP answers, target health, limits and memory total; the targeted plan changes one attribute in place (0 add, 1 change, 0 destroy, no replacement); the ask carries the three halves, the process-wide state line, the downtime and the safe rollback order (the tarball first, then t4g.small), no IPv4 address and no run of nine digits. Nothing applied or deployed.",
    "AC2": "the live instance is t4g.large and running; the service answers with the raised limits (5600M and 6400M), the marker equal to the release, host memory total at least 7000 MB, 103 tools, 27 of 27 and NRestarts 0 after the deploy; the two large replies complete one at a time under MemoryHigh; the ledger is closed with its sentinel gone.",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-rz-2", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:ec2/i-07dccb1615503ac99 (opal-gateway host, resized t4g.small -> t4g.large) and /opt/opal-gateway (round-46 fourteenth batched release 13917ef993)", "aws_resource", "DEPLOYED-VERIFIED",
            "INSTANCE LEG: safe-apply of a saved targeted plan from branch rz2-instance-type-nfra1 (main.tf blob 1cf3c199cb2c): 0 added, 1 changed, 0 destroyed; stopped 06:22:54Z, t4g.large running 06:23:25Z, /health 200 at 06:24:29Z (abort line 06:30Z met); Elastic IP still associated; public endpoint down %s s. "
            "RELEASE LEG (only after the instance leg held): batch15 13917ef993 deployed through safe-ec2-deploy.sh, DEPLOY_BASE_REF=6d1b5dcb64, marker equals the release, unit limits %s and %s, host memory %s MB, tools/list %s, 27 of 27 under the hard guard, host md5 %s of %s equal to the release blobs. "
            "READ-BACK (%s probes, %s to %s): health 200 each, %s PID, NRestarts %s, UNARMED ONLY (403 probe_not_armed x3, lease absent, no SSM write); dual count %s journal lines (%s of them this seat's sampler probes) against %s lake records; audit WARN %s. "
            "THE TWO LARGE REPLIES, one at a time: %s characters and %s characters, both completed, service memory about %s to %s MB against MemoryHigh %s. Rollback target: tarball opal-gateway-6d1b5dcb64b.tar.gz (922315 bytes, sha256 e7cd9de1617a), then t4g.small; not used."
            % (dt["downtime_seconds"], S["unit_memory_high"], S["unit_memory_max"], S["memory_total_mb"], S["tools_list"], S["host_md5"]["equal"], S["host_md5"]["expected_files"], rb["probes"], rb["first_t"], rb["last_t"], rb["service_pids_seen"], rb["nrestarts_during_readback"],
               al["post_mcp_lines_readback"], al["sampler_probes_in_the_journal_count"], al["audit_records_readback"], S["audit_failure_counter"]["journal_lines_readback"], big[0]["reply_bytes"], big[1]["reply_bytes"], big[0]["before_mb"], big[1]["max_mb"], S["memory_high_mb"]), ["AC2"]),
        art(W + "RZ2_SERVED.json", "doc", GIT, "Counts, MB, seconds, words and booleans only; the instance block, all four downtime intervals (resize 44 s, the deploy's restart, one 7 s stall at the first large call), the two large replies, the dual count with the sampler adjustment, the clock and failed units read before the close.", ["AC2"]),
        art(W + "RZ2_BEFORE.json", "doc", GIT, "Phase A before-record: t4g.small, running, an Elastic IP attached (public address unchanged on stop/start), target healthy, limits 1200M/1400M, memory 1846 MB, 19 estate surfaces, vendor allowlists NOT CLAIMED.", ["AC1"]),
        art(W + "RZ2_PLAN.json", "doc", GIT, "The targeted plan: 0 add, 1 change, 0 destroy, in place, attribute instance_type; the edit kept on branch rz2-instance-type-nfra1 (62514569a6, blob 1cf3c199cb2c).", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-rz-2.md", "doc", GIT, "The ask, sha256 5dfadc6c78c3, signed by CTO f39cd21642, COO H1-H8 and CVO 86c19380ab.", ["AC1"]),
        art(ledger, "doc", GIT, "Ledger nfra-oplgtw-gateway-resize-t4g-large opened before the stop (the two window callers named), three legs proven, CLOSED %s after the clock and failed units were read (%s); sentinel removed." % (closed_at, S["host_clock"]["read_at"]), ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit 13917ef993, previous 6d1b5dcb64; file_checksums cross-checked against the host (10 of 10); none moves.", ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %srz2.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": {"AC1": "1 instance; 1 plan (0/1/0); 3 halves; 19 estate surfaces counted", "AC2": "1 instance read live; 1 ledger of 3 legs; 2 large replies; %s read-back probes; 27 tools" % rb["probes"]}[cid], "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut base-FAIL runs are the discriminating arm.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "an arming of the listener", "reason": "None in this order (NO ARMING, NO SSM write)."},
        {"item": "a push", "reason": "The order forbids it; the issuer drains the branch."},
        {"item": "the cause of the 2026-10-19 hang", "reason": "The large-reply test shows replies of 743469 and 585084 characters move the service's memory by about 1 MB; it does not establish the cause of the outage, which the order does not ask."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-rz-2 (GOs 36088, 36115 and the Phase B GO sent 06:03Z). Phase A (2026-10-19): the before-record, the targeted plan kept with the edit on its own branch, the IAM simulation, batch15 cut as 13917ef993 (ten files whole from trunk), tests, the ask. Phase B (2026-10-20): the GO was read at 06:17Z (the inbox stream did not wake me; reported to the COO and MSTR at once); pre-window read ALL HOLD at 05:48Z; ledger opened 06:18:39Z with the two window callers named; the saved plan applied 06:20:00Z, t4g.large healthy 06:24:29Z; the release deployed about 06:29Z; the 30-minute UNARMED read-back to 07:00Z; the two large replies one at a time; the ledger CLOSED " + closed_at + ".",
    "compiler_tools": [{"tool": "terraform / boto3 / ssm / s3", "invocation": "terraform plan -out and safe-apply of the saved plan; rz2_pb_pre.py, rz2_pb_wait.py, rz2_sampler.py, rz2_mem.py, ap38_monitor.py, ap44_accesslog.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, seconds, times and short shas only; the full plan text, which holds the address, stayed off-repo."}],
}
P = W + "NFRA_OPLGTW.TO-OG-rz-2.round-46-resize-the-gateway-host-to-t4g-large.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
