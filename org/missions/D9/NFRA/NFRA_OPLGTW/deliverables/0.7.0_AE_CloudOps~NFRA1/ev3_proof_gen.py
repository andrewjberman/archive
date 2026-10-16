#!/usr/bin/env python
"""OG-ev-3: write W/NFRA_OPLGTW.TO-OG-ev-3.measure-full-13-month-read-on-the-host.proof_of_spec.json from a real run of AC1 (run twice for the determinism control).
usage: python ev3_proof_gen.py   (from the repo root of the worktree on box/sitez; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-3.measure-full-13-month-read-on-the-host.md"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(path):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--", path], capture_output=True).stdout.decode().strip()


ac1 = [run("ev3.AC1.sh"), run("ev3.AC1.sh")]
E1 = re.search(r'<criterion id="AC1"[^>]*>.*?<expect>(.*?)</expect>', io.open(TO, encoding="utf-8").read(), re.S).group(1)
assert re.search(E1, ac1[0]), ac1[0]
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def art(path, kind, ev, intro, cov):
    row = {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path), "deployed_state": GIT, "deploy_evidence": ev, "artifact_covered_by": cov}
    if intro:
        row["introduces"] = intro
    return row


inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ev-3", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md", "group": "OTHER", "vintage_commit": "f4372fcac9"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md", "vintage_commit": "f4372fcac9", "to_ref": TO},
    "artifacts_produced": [
        art(W + "WINDOW_MEASURE.json", "doc", "Seconds, counts and bytes only, assembled by ev3_build.py from the two host records. Transactions: 334 of 334 files, one complete run 239.888 s; fees: 396 of 396, five runs, p95 147.157 s; verdict outside.", ["inside_threshold_seconds"], ["AC1"]),
        art(W + "ev3_measure.py", "script", "The host measurement: ThreadPoolExecutor(16) through the installed adapter's ctx.read_rows with the adapter's own column lists, a memory monitor aborting above 80 percent, a 16-file pilot first.", ["PILOT_STOP_PCT"], ["AC1"]),
        art(W + "ev3_transactions.json", "doc", "The transactions host record: 1 complete run, run 2 stopped by the memory guard at 190 of 334 files.", ["STOPPED-IN-RUN-2"], ["AC1"]),
        art(W + "ev3_fees.json", "doc", "The fees host record: 5 complete runs of 396 files.", ["COMPLETE"], ["AC1"]),
    ],
    "acceptance": [
        {"criterion_id": "AC1", "criterion_verbatim": "AC1: the record is complete and self-consistent: the whole window of each table was read at concurrency 16, p50 at or below p95, the verdict follows the stated rule from the recorded p95s, and nothing but numbers and fixed words is in it (A1: fewer than 5 runs only when the verdict is outside and the fastest run is above 30 s).",
         "method": "command", "invocation": 'bash %sev3.AC1.sh; echo "exit=$?"' % (CK), "expect": E1, "output_evidence": ac1[0],
         "denominator": "transactions 334 of 334 window partitions read (1 complete run); fees 396 of 396 (5 complete runs); worst p95 239.888 s against the 30 s threshold.",
         "status": "PASS", "status_reason": "Passes the check as amended by the issuer (A1, msg 35292); it did not pass the original, which demanded 5 runs of every table and rejected the nine-digit bytes integer (row Z-S327)."}],
    "controls": {
        "determinism": {"method": "AC1 was run twice against the same record, back to back.", "observed": "AC1 outputs identical.", "status": "STABLE" if ac1[0] == ac1[1] else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant. The issuer's pre-cut controls and the original check's two refusals (runs, digit run) are the discriminating arms; AC1 read FAIL on this very record before A1 and PASS after it.",
                   "expected": "AC1 FAIL on the record under the original check, PASS under the amended check", "observed": "FAIL (runs 1, digit runs 1) at 23:2xZ; PASS after A1",
                   "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "four more complete transactions runs", "reason": "Run 2 hit the 80 percent memory guard (81.6 percent) on a host with no swap; the verdict is outside by a factor of 8 on the one complete run, and A1 admits fewer than 5 runs in that case."}],
    "surprises": [
        "NFRA_OPLGTW-Z-S327: BLOCKING -- ev3.AC1 could not pass as written (5 runs, nine-digit bytes); corrected by the issuer's A1.",
        "NFRA_OPLGTW-Z-S328: OBSERVATION -- every ctx.read_rows call lists the whole prefix first (0.4 of 0.55 s on fees)."],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, fourth order (msg 35288; A1 msg 35292). Pilot first, then 5 runs per table under a memory monitor; transactions stopped by the guard in run 2; fees complete; a single-threaded timing diagnostic of one read_rows call. Read-only; the host recovered to baseline and /health stayed 200.",
    "compiler_tools": [{"tool": "pyarrow/boto3 via the installed adapter", "invocation": "ev3_measure.py --host <table> (S3 -> SSM, Rule 12)", "result": "PASS", "note": "Seconds, counts and bytes only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ev-3.measure-full-13-month-read-on-the-host.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
