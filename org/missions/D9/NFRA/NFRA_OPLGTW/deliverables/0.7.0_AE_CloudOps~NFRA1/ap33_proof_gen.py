#!/usr/bin/env python
"""OG-ap-33: write W/NFRA_OPLGTW.TO-OG-ap-33.land-harvst-release-on-trunk.proof_of_spec.json from a real run of AC1, AC2 and AC3 (each run twice for the determinism control).
usage: python ap33_proof_gen.py   (from the repo root of the landing worktree, after the record commit; bash on PATH)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r38/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-33.land-harvst-release-on-trunk.md"
G = "infra/aws/ec2/opal-gateway/"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(path):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--", path], capture_output=True).stdout.decode().strip()


order = io.open(TO, encoding="utf-8").read()
ac = {}
for cid in ("AC1", "AC2", "AC3"):
    script = "ap33.%s.sh" % cid
    outs = [run(script), run(script)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    assert re.search(exp, outs[0]), outs[0]
    ac[cid] = (outs, exp)
stable = all(o[0] == o[1] for o, _ in ac.values())
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def art(path, kind, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path), "deployed_state": GIT, "deploy_evidence": ev, "artifact_covered_by": cov}


inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ap-33", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md", "group": "OTHER", "vintage_commit": "53cac446ff"},
    "decomp_ref": {"doc": "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md", "vintage_commit": "53cac446ff", "to_ref": TO},
    "artifacts_produced": [
        art(W + "ap33_landing.json", "doc", "trunk_base bf207c6bbd, hvst 319c9413a2, release 9d5b712557, merge 60412142ac on branch land-hvst-cc7b-nfra1; not pushed.", ["AC1", "AC2", "AC3"]),
        art(G + "app/client_adapter_bd49f.py", "script", "Merged to the blob at release_sha 9d5b712557 (equal to the live bytes); no live byte moved.", ["AC2"]),
        art(G + "app/refs/DATA_CATALOG.yaml", "config_data", "Merged to the blob at release_sha 9d5b712557 (equal to the live bytes).", ["AC2"]),
        art(G + "deploy-to-ec2.sh", "script", "Takes the LIVE blob whole (A2); OG-db-1's preflight is re-landed by the cell OG-db-2.", ["AC2"]),
        art(G + "app/tools.py", "script", "Takes trunk's blob (A2): the live blob holds no line trunk lacks; harvest_get_published_analysis imported, registered and allowlisted exactly once.", ["AC2"]),
        art("infra/aws/ec2/EC2_MANIFEST.json", "config_data", "services.opal-gateway block equals trunk's; the 26 other services equal trunk's and hvst's.", ["AC2"]),
        art("infra/aws/terraform/opal-gateway/advi_billing_gateway_iam.tf", "terraform", "Merged as text, NOT applied: trunk's side carries the whole hvst side plus the market_update block.", ["AC3"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": re.search(r"`%s`: (.*?)(?= `AC\d`: |\n)" % cid, order).group(1)[:500],
         "method": "command", "invocation": 'bash %s%s; echo "exit=$?"' % (CK, "ap33.%s.sh" % cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": "20 conflicted paths (merge-tree of trunk_base and hvst)", "status": "PASS"} for cid in ("AC1", "AC2", "AC3")],
    "controls": {
        "determinism": {"method": "AC1, AC2 and AC3 were each run twice against the same merge, back to back.", "observed": "outputs identical" if stable else "outputs differ",
                        "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's pre-cut controls (conflict markers left; the adapter at the HVST bytes; the mcportal entries trunk-side only; a one-parent commit; a three-way path set to the live blob; the allowlist entry twice) are the discriminating arms.",
                   "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [{"item": "a push of the merge", "reason": "The order forbids it: 0.0.0_AB_MSTR~Z carries the merge to origin on the issuer's word."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1 (GOs msg 35397, then 35439 under Amendment A2). First attempt stopped before any merge (row Z-S356). Second: worktree C:/tmp/og-land-hvst from trunk head bf207c6bbd, safe-merge of 319c9413a2 (rc 4), 20 paths resolved per A2, gateway tests 68 passed in both orders, py_compile ok, the first --continue refused downstream (org/devices missing from the sparse cone), redone with it in the cone; merge 60412142ac.",
    "compiler_tools": [{"tool": "python py_compile and pytest", "invocation": "py_compile app/tools.py app/destructive_ops.py app/client_adapter_bd49f.py; pytest the six conflicted gateway test files and test_og_en18 in both orders", "result": "PASS", "note": "68 passed forward, 68 reverse, 68 at trunk_base."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ap-33.land-harvst-release-on-trunk.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
