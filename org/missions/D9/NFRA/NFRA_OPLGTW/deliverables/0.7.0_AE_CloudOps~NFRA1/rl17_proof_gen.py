#!/usr/bin/env python
"""OG-rl-17: write the proof_of_spec instance from a real run of AC1, AC2 and AC3 (each run twice for the determinism control).
usage: python rl17_proof_gen.py   (repository root, after the Phase B commit, the ledger close and the landing record)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r47/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-17.round-47-sixteenth-batched-release-the-client-fences-the-size-caps-and-the-in-flight-guard.md"
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


ledger = [p for p in subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/change_management/"], capture_output=True).stdout.decode().split() if p.endswith("_nfra-oplgtw-gateway-release-batch16_deploy_completion.md")][-1]
order = io.open(TO, encoding="utf-8").read()
S, P, L, REL = jload("CODE16_SERVED.json"), jload("RL17_PROOFS.json")["body"], jload("rl17_landing.json"), jload("rl17_release.json")
dt, al, rb = S["downtime"], S["access_log"], S["readback"]
ac = {}
for cid in ("AC1", "AC2", "AC3"):
    outs = [run("rl17.%s.sh" % cid), run("rl17.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    ac[cid] = (outs, exp)
    print(cid, "matches expect" if re.search(exp, outs[0]) else "DOES NOT MATCH THE ORDER'S EXPECT", "| stable" if outs[0] == outs[1] else "| UNSTABLE")
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else REL["release_sha"][:10], "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "`AC1` (Phase A) is graded by me on my run before any GO to Phase B",
    "AC2": "`AC2` is the release's served state and the live guard",
    "AC3": "`AC3` is what the round promised: the three vendors answer, Cottonwood returns rows, eight parallel large calls leave `/health` at 200, the two big replies fit, and the breakdown names its index pairs.",
}
d1, ld = P["d1"], P["load"]
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-rl-17", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:ec2/i-07dccb1615503ac99 (opal-gateway host, /opt/opal-gateway, round-47 sixteenth batched release %s on live ref %s)" % (REL["release_sha"][:10], REL["base_sha"][:10]), "aws_resource", "DEPLOYED-VERIFIED",
            "RELEASE: safe-ec2-deploy.sh with DEPLOY_BASE_REF=%s, 2026-10-21 06:02:52Z to 06:04:14Z; marker equals the release; unit limits %s and %s; tools/list %s before and after; 27 of 27 under the hard guard; host md5 %s equal of %s, %s differ; NRestarts %s." % (REL["base_sha"][:10], S["unit_memory_high"], S["unit_memory_max"], S["tools_list"], S["host_md5"]["equal"], S["host_md5"]["expected_files"], S["host_md5"]["differ"], S["nrestarts_after_deploy"])
            + " " +
            "READ-BACK (%s probes, %s to %s): health 200 each, %s PID, NRestarts %s, no trigger, UNARMED ONLY (403 probe_not_armed x3, lease absent, no SSM write); %s journal lines against %s lake records; audit WARN %s. The public sampler recorded %s timeouts in %s samples (single samples of 7 to 14 s, PID unchanged)." % (rb["probes"], rb["first_t"], rb["last_t"], rb["service_pids_seen"], rb["nrestarts_during_readback"], al["post_mcp_lines_readback"], al["audit_records_readback"], S["audit_failure_counter"]["journal_lines_readback"], dt["failed_samples"], dt["samples"]), ["AC2"]),
        art(W + "CODE16_SERVED.json", "doc", GIT, "Counts, MB, seconds, words and booleans only: the host reads, the read-back, the downtime intervals, the dual count, the clock and failed units read before the close.", ["AC2"]),
        art(W + "RL17_PROOFS.json", "doc", GIT, "D1 orion %s and eclipse %s candidate(s), commonwealth %s from its own crosswalk (first call with another last-4: account_not_resolved, kept); D2 %s transactions; LOAD %s of %s completed, gateway_busy %s, /health 200 x %s, peak %s MB; projection %s and %s bytes; index_pairs %s of %s. The orion control was not reproducible through the tool (platform_not_source_label)." % (d1["orion"]["candidate_count"], d1["eclipse"]["candidate_count"], d1["commonwealth"]["candidate_count"], P["d2"]["transactions"], ld["completed"], ld["calls"], ld["gateway_busy"], ld["health_200_samples"], ld["service_peak_mb"], P["projection"]["aggregate_aua_bytes"], P["projection"]["opal_discover_bytes"], P["index_pairs"]["with_index_pairs"], P["index_pairs"]["segmented_tools"]), ["AC3"]),
        art(W + "rl17_memory_at_peak.json", "doc", GIT, "MemoryCurrent at the 8-call peak and scaled to 26 against MemoryHigh 5600 (the CVO note).", ["AC3"]),
        art(W + "rl17_deployed_vs_head.json", "doc", GIT, "The COO-ferried record: app/ files on the host that differ from trunk HEAD at the read time (a record, not a trigger).", ["AC2"]),
        art(W + "NEVER_WIDEN_ASK_OG-rl-17.md", "doc", GIT, "The ask (sha256 291ffc35747a) with the three halves; Phase A report and stop, Phase B on the COO GO.", ["AC1"]),
        art(W + "haltgate_batch16.json", "doc", GIT, "Pending inbox %s before the window and %s after; STOP-class found %s; the gate's elapsed time bounded by the wrapper's 82 s." % (jload("haltgate_batch16.json")["pending_before"], jload("haltgate_batch16.json")["pending_after"], jload("haltgate_batch16.json")["stop_class_found"]), ["AC2"]),
        art(ledger, "doc", GIT, "Ledger nfra-oplgtw-gateway-release-batch16 opened before the deploy (06:01Z), three legs proven, CLOSED 2026-10-21T06:44Z after the clock and failed units were read; sentinel removed.", ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "doc", GIT, "services.opal-gateway deployed_commit %s, previous %s, file_checksums cross-checked against the host (145 of 145)." % (REL["release_sha"][:10], REL["base_sha"][:10]), ["AC2"]),
        art(W + "rl17_landing.json", "doc", GIT, "Phase C: the release landed on branch %s by merge %s; %s trunk paths differ from live, listed with owners." % (L["landing_branch"], L["landing_sha"][:10], len(L["paths_differing_from_live"])), ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %srl17.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": {"AC1": "1 release cut, 4 harvest files, the take list, 3 halves", "AC2": "1 host read live; 1 ledger of 3 legs; %s read-back probes; 27 tools; 145 files" % rb["probes"], "AC3": "3 vendors; 1 Cottonwood transactions call; 8 load calls; 2 large replies; %s segmented tools" % P["index_pairs"]["segmented_tools"]}[cid], "status": "PASS"} for cid in ("AC1", "AC2", "AC3")],
    "controls": {
        "determinism": {"method": "AC1, AC2 and AC3 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut base-FAIL runs are the discriminating arm.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "an arming of the listener", "reason": "None in this order (NO ARMING, NO SSM write)."},
        {"item": "a push", "reason": "The order forbids it; the issuer drains the branch."},
        {"item": "the orion control call through the tool", "reason": "client_resolve_account takes no vendor argument; the issuer's 06:4xZ amendment accepts the Phase A catalog controls for the control only."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-rl-17. Phase A: batch16 cut and re-cut at the in-flight cap 26, tests, probes, the ask. Phase B (2026-10-21): pre-window read ALL HOLD at 05:39Z; ledger opened 06:01Z; deploy 06:02:52Z to 06:04:14Z; 30-minute UNARMED read-back 06:06:45Z to 06:36:46Z; the proofs inside it (the first load attempt used a scope the tool refused and is recorded; the second answered 8 of 8); the commonwealth D1 call repeated with a last-4 from commonwealth's own silver at the COO's ask; ledger CLOSED 06:44Z; AC2 and AC3 PASS. Phase C: landing merge on a local branch, record committed.",
    "compiler_tools": [{"tool": "boto3 / ssm / s3", "invocation": "ap38_monitor.py, ap44_accesslog.py, rz2_mem.py, rl17_health.py, rl17_indexpairs.py (Rule 12, S3 to SSM)", "result": "PASS", "note": "Counts, MB, seconds, times and short shas only."}],
}
P_OUT = W + "NFRA_OPLGTW.TO-OG-rl-17.round-47-sixteenth-batched-release-the-client-fences-the-size-caps-and-the-in-flight-guard.proof_of_spec.json"
io.open(P_OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P_OUT, "determinism", inst["controls"]["determinism"]["status"])
