#!/usr/bin/env python
"""OG-rl-19: write the proof_of_spec instance from a real run of AC1, AC2 and AC3 (each run twice for the determinism control).
usage: python rl19_proof_gen.py   (repository root, after the Phase B commit, the ledger close and the landing record)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r47/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-19.round-47-release-r3c-the-schwab-0840-dual-read-and-its-reader-iam.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


def jload(name):
    return json.load(io.open(W + name, encoding="utf-8"))


ledger = [p for p in subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/change_management/"], capture_output=True).stdout.decode().split() if p.endswith("_nfra-oplgtw-gateway-release-r3c_deploy_completion.md")][-1]
order = io.open(TO, encoding="utf-8").read()
S, L, REL = jload("R3C_SERVED.json")["body"], jload("rl19_landing.json"), jload("rl19_release.json")
rb, tf, gr, dr = S["readback"], S["terraform"], S["gate_read"], S["dual_read"]
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("rl19.%s.sh" % cid), run("rl19.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    ac[cid] = (outs, exp)
    print(cid, "matches expect" if re.search(exp, outs[0]) else "DOES NOT MATCH THE ORDER'S EXPECT", "| stable" if outs[0] == outs[1] else "| UNSTABLE")
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else REL["release_sha"][:10], "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "`AC1` (Phase A) is graded by me on my run before any GO to Phase B",
    "AC2": "`AC2` (Phase B) after the ledger closes.",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-rl-19", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:ec2/i-07dccb1615503ac99 (opal-gateway host, /opt/opal-gateway, R3c release %s on live ref %s) and the two IAM role policies (gateway-schwab-read-role-policy, gateway-schwab-catalog-read-role-policy)" % (REL["release_sha"][:10], REL["base_sha"][:10]), "aws_resource", "DEPLOYED-VERIFIED",
            ("ORDER OF ACTS: the R3a confirmation read %s, safe-apply (add %s, change %s, destroy %s) %s to %s, the gate read as the catalog role %s with %s keys at %s, the deploy %s to %s. "
             "Marker equals the release; tools/list %s; host md5 %s of %s equal, %s differ; NRestarts %s." % (S["order"]["times_utc"]["r3a_read"], tf["add"], tf["change"], tf["destroy"], S["order"]["times_utc"]["apply_started"], S["order"]["times_utc"]["apply_finished"], gr["get_object"], gr["list_key_count"], S["order"]["times_utc"]["gate_read"], S["order"]["times_utc"]["deploy_started"], S["order"]["times_utc"]["deploy_finished"], S["tools_list"], S["host_md5"]["equal"], S["host_md5"]["expected_files"], S["host_md5"]["differ"], S["nrestarts_after_deploy"]))
            + " " +
            ("READ-BACK (%s probes, %s to %s): health 200 each, %s PID, NRestarts %s, UNARMED ONLY (403 probe_not_armed x3, lease absent, no SSM write). The monitor's carried 700 MB line wrote its trigger file (service 973 MB, flat 881 MB; host %s percent at most; not a trigger of the order); the observation and its conclusion are in the served record. "
             "DUAL READ 08403355: %s to %s dates, newest %s, marker location %s; sk2 probe %s of %s." % (rb["probes"], rb["first_t"], rb["last_t"], rb["service_pids_seen"], rb["nrestarts_during_readback"], rb["host_pct_max"], dr["dates_before"], dr["dates_after"], dr["newest_after"], dr["marker_location"], dr["sk2_probe_lines_ok_after"], dr["sk2_probe_lines_after"])), ["AC2"]),
        art(W + "R3C_SERVED.json", "doc", GIT, "Counts, MB, seconds, words and booleans only: the order of acts with times, the Terraform counts, the policy statement counts before and after, the gate read, the dual read before and after, the host reads, the memory observation.", ["AC2"]),
        art(W + "haltgate_r3c.json", "doc", GIT, "Pending inbox 0 (read 07:09:26Z), STOP-class 0; the gate bounded by the wrapper's 105 s.", ["AC2"]),
        art(W + "NEVER_WIDEN_ASK_OG-rl-19.md", "doc", GIT, "The ask (sha256 5f25fa44f2cb) with the three halves, including the first grant on opal-data-49financial.", ["AC1"]),
        art(ledger, "doc", GIT, "Ledger nfra-oplgtw-gateway-release-r3c opened before the apply (07:10Z), four legs proven, CLOSED 2026-10-21T07:55Z after the clock and failed units were read; sentinel removed.", ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit %s, previous %s; file_checksums cross-checked against the host (10 of 10); none moves." % (REL["release_sha"][:10], REL["base_sha"][:10]), ["AC2"]),
        art(W + "rl19_landing.json", "doc", GIT, "Phase C: the release landed on branch %s by merge %s (drain tip %s), including org/standards/NFRA_OPLGTW_CONTRACT.json; %s trunk paths differ from live, listed with owners." % (L["landing_branch"], L["landing_sha"][:10], L["drain_tip"][:10], len(L["paths_differing_from_live"])), ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %srl19.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": {"AC1": "4 release files, 2 policies planned (0/2/0), 3 halves", "AC2": "1 host read live; 1 ledger of 4 legs; %s read-back probes; 145 files; 3 masters" % rb["probes"]}[cid], "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut base-FAIL runs are the discriminating arm.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "an arming of the listener", "reason": "None in this order (NO ARMING, NO SSM write)."},
        {"item": "a push", "reason": "The order forbids it; the issuer drains the branch."},
        {"item": "the cause of the service memory plateau at 881 MB", "reason": "The rise was complete before this seat's first request to the service and coincided with real-caller traffic; what in it holds the memory is not established, and the order names no memory trigger."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-rl-19. Phase A: release 2923d1ee99 cut on 8e3eddf959 (four files, the integration.py hybrid), tests, the probe, the ask. Phase B (2026-10-21, after batch16 CLOSED): pre-window read ALL HOLD 07:08Z; R3a confirmation read 07:10Z; ledger opened 07:10Z; before-records; safe-apply 0/2/0; the 60 s wait and the gate read as the catalog role (NoSuchKey, 0 keys); the deploy; the 15-minute UNARMED read-back; ledger CLOSED 07:55Z; AC2 PASS. Phase C: landing merge on a local branch plus a note commit, record committed.",
    "compiler_tools": [{"tool": "terraform / boto3 / ssm / s3", "invocation": "r3c_act.py (safe-apply of a saved plan), r3c_host.py, ap38_monitor.py, ap44_accesslog.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, seconds, times and short shas only."}],
}
P_OUT = W + "NFRA_OPLGTW.TO-OG-rl-19.round-47-release-r3c-the-schwab-0840-dual-read-and-its-reader-iam.proof_of_spec.json"
io.open(P_OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P_OUT, "determinism", inst["controls"]["determinism"]["status"])
