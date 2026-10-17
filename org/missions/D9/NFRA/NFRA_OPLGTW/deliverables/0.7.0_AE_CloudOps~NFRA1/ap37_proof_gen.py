#!/usr/bin/env python
"""OG-ap-37: write W/NFRA_OPLGTW.TO-OG-ap-37.land-dell1-harvest-release-on-trunk.proof_of_spec.json from a real run of AC1 and AC2 (each run twice for the determinism control).
usage: python ap37_proof_gen.py   (from the repo root of the worktree on land-hvst-cd2-nfra1, after the record and row commits; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-37.land-dell1-harvest-release-on-trunk.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
CHAN = "org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
ac = {}
for cid in ("AC1", "AC2"):
    outs = [run("ap37.%s.sh" % cid), run("ap37.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())


def art(path, ev, cov):
    return {"path_or_key": path, "kind": "doc", "commit_or_etag": pin(path), "deployed_state": GIT, "deploy_evidence": ev, "artifact_covered_by": cov}


verbatim = {
    "AC1": "a true merge of dell1's release commit on the trunk head, no conflict marker left, no gateway, Terraform or other byte changed.",
    "AC2": "the manifest block still names the live release (efcc8ae19f, previous 1753c741d9) and nothing else in it moved.",
}
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-37", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art(W + "ap37_landing.json", "trunk_base 6013328e18, dell1 1753c741d9, merge 82244ac7a3 (parents exactly the two, tree equal to trunk_base's), manifest source dell1's commit 25699bc8e5.", ["AC1", "AC2"]),
        art(CHAN, "Row Z-S378: safe-merge cannot land a lineage-only merge; the landing was made by commit-tree on the scratch branch land-hvst-cd2-nfra1.", ["AC1"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command",
         "invocation": 'bash %sap37.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": ("2 conflicted paths (merge-tree); 0 gateway paths differing from trunk_base" if cid == "AC1" else "1 manifest block; 1 source commit"),
         "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ",
                        "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls (one parent, a differing harvest blob, an extra gateway file, a Terraform file, the manifest on the old ref, another service changed) are the discriminating arms.",
                   "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "step 1's literal tool (.tools/safe-merge.sh) for the merge commit",
         "reason": "safe-merge refuses a merge that stages no files (its lines 775 to 781) and aborts it; with both conflicts resolved to trunk's blobs (order A2) the landing changes no byte, so the commit was made by commit-tree on the scratch branch, the shape the script's own fast lane lands by. Row Z-S378. Nothing touched a shared branch."}],
    "surprises": ["NFRA_OPLGTW-Z-S378"],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1 (GO msg 35552, trunk_base_sha 6013328e18 = box/sitez head at the GO, A1 and A2 read). merge-tree: 2 conflicted gateway paths (the denominator), matching A2. safe-merge started the merge and handed back the conflict; both paths resolved to trunk's blob (hash-object equal, 0 markers); --continue refused (no staged file) and aborted. Merge commit 82244ac7a3 by commit-tree; record, row and AC runs on the branch land-hvst-cd2-nfra1. No push, no deploy, no gateway byte.",
    "compiler_tools": [{"tool": "git merge-tree / commit-tree", "invocation": "git merge-tree --write-tree --name-only; git commit-tree", "result": "PASS", "note": "Shas and counts only."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-37.land-dell1-harvest-release-on-trunk.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
