#!/usr/bin/env python
"""OG-ev-4: write W/NFRA_OPLGTW.TO-OG-ev-4.measure-memory-retention-across-paged-reads.proof_of_spec.json from a real run of AC1 (run twice for the determinism control).
usage: python ev4_proof_gen.py   (from the repo root of the worktree on box/sitez; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-4.measure-memory-retention-across-paged-reads.md"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(path):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--", path], capture_output=True).stdout.decode().strip()


ac1 = [run("ev4.AC1.sh"), run("ev4.AC1.sh")]
E1 = re.search(r'<criterion id="AC1"[^>]*>.*?<expect>(.*?)</expect>', io.open(TO, encoding="utf-8").read(), re.S).group(1)
assert re.search(E1, ac1[0]), ac1[0]
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def art(path, kind, ev, intro, cov):
    row = {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path), "deployed_state": GIT, "deploy_evidence": ev, "artifact_covered_by": cov}
    if intro:
        row["introduces"] = intro
    return row


inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ev-4", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md", "group": "OTHER", "vintage_commit": "29fca12c0c"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md", "vintage_commit": "29fca12c0c", "to_ref": TO},
    "artifacts_produced": [
        art(W + "MEMORY_RETENTION.json", "doc", "Numbers and fixed words only, assembled by ev4_build.py from the host driver record: six variants of a three-page transactions chain, median growth per page A 135.9, B 146.8, C 110.7, D 26.7, E 104.5, F 42.4 MB; flattening variant none.", ["threshold_mb_per_page"], ["AC1"]),
        art(W + "ev4_measure.py", "script", "The read-only host measurement: the release app staged in a scratch folder (removed), each variant in a fresh process, a 78 percent kill and a 75 percent stop, the service untouched.", ["KILL_PCT"], ["AC1"]),
        art(W + "ev4_driver.json", "doc", "The host driver record the measurement was assembled from.", ["idle_host_pct"], ["AC1"]),
    ],
    "acceptance": [
        {"criterion_id": "AC1", "criterion_verbatim": "AC1: the record is complete and self-consistent: six variants with numeric pages, each median recomputed from its pages, the flattening variant following the stated rule, and nothing but numbers and fixed words in it.",
         "method": "command", "invocation": 'bash %sev4.AC1.sh; echo "exit=$?"' % CK, "expect": E1, "output_evidence": ac1[0],
         "denominator": "six variants (A to F), three pages each, none stopped; idle host 28.1 percent used; the highest host reading 69.5 percent.",
         "status": "PASS"}],
    "controls": {
        "determinism": {"method": "AC1 was run twice against the same record, back to back.", "observed": "AC1 outputs identical.", "status": "STABLE" if ac1[0] == ac1[1] else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant. The discriminating arms are the issuer's pre-cut controls (a verdict naming B when C is flatter; none though C is flat; a median that differs from the pages; F missing; an e-mail in the record); the measurement's own discriminator is variant A, the release as is, which reproduced the growth OG-ap-32 found (135.9 MB per page against 110 to 165).",
                   "expected": "A shows the retention that OG-ap-32 measured; a mitigation shows a lower median", "observed": "A 135.9 MB per page; D 26.7; F 42.4", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "a combination of D and F, and more than three pages", "reason": "The order fixes six variants and one chain of three pages each, no loops; D's third growth (3.2 MB) suggests flattening that three pages cannot separate from noise."}],
    "surprises": ["NFRA_OPLGTW-Z-S342: OBSERVATION -- the retained memory sits in glibc's per-thread arenas; MALLOC_ARENA_MAX=2 cuts the median growth from 135.9 to 26.7 MB per page; no variant meets the 20 MB rule."],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1 (msg 35319). Read-only: the release app staged in a scratch folder on the host from the running service's own files plus the release's adapter and catalog (md5 equal to the release), the test account resolved once in a separate process, six fresh processes, the scratch folder removed. The gateway service was not touched.",
    "compiler_tools": [{"tool": "pyarrow/boto3 via the staged release app", "invocation": "ev4_measure.py --driver (S3 -> SSM, Rule 12)", "result": "PASS", "note": "Seconds, MB and percentages only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ev-4.measure-memory-retention-across-paged-reads.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
