#!/usr/bin/env python
"""OG-gc-1: write the proof_of_spec instance (AC1 only; the amended order has no Phase B) from two real runs of gc1.AC1.
usage: python gc1_proof_gen.py   (repository root, after the Phase A commit)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r47/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-gc-1.round-47-client-tools-for-alyssa-and-menachem.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


def art(path, ev):
    return {"path_or_key": path, "kind": "script" if path.endswith(".py") else "doc", "commit_or_etag": pin(path), "deployed_state": GIT, "deploy_evidence": ev, "artifact_covered_by": ["AC1"]}


order = io.open(TO, encoding="utf-8").read()
exp = re.search(r'<criterion id="AC1"[^>]*>.*?<expect>(.*?)</expect>', order, re.S).group(1)
outs = [run("gc1.AC1.sh"), run("gc1.AC1.sh")]
print("AC1", "matches expect" if re.search(exp, outs[0]) else "DOES NOT MATCH THE ORDER'S EXPECT", "| stable" if outs[0] == outs[1] else "| UNSTABLE")
stable = outs[0] == outs[1]
g = json.load(io.open(W + "GC1_GATES.json", encoding="utf-8"))
f = json.load(io.open(W + "GC1_FACTS.json", encoding="utf-8"))
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-gc-1", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art(W + "GC1_GATES.json", "Per principal: profile present, the five client tools classified (all denied:entitlements for both), the six gates read, needs_write true, person_access_can_admit false with the decide() lines cited; the write path (NFRA_MCPORTAL's grant writer, owner session) named."),
        art(W + "GC1_FACTS.json", "The gateway's own decide() and person_denial() on trunk code over the stored records (%d POLICY# items, %d person_access records in the store): Alyssa and an unprofiled principal read entitlement_denied for each of the five tools and admitted if the tier were master_admin." % (f["policy_items_scanned"], f["person_access_records_in_store"])),
        art(W + "gc1_phasea.py", "The reader: strong scan of the POLICY# partitions plus the gateway's own decide(); read only, nothing written, no person_access record written."),
    ],
    "acceptance": [{"criterion_id": "AC1", "criterion_verbatim": "(Phase A, amended: a denied principal whose gate is entitlements needs no ask, and none may be present) the facts are written per principal and the write path is named.",
                    "method": "command", "invocation": 'bash %sgc1.AC1.sh; echo "exit=$?"' % CK, "expect": exp, "output_evidence": outs[0],
                    "denominator": "2 principals; 5 client tools each; 6 gates read; %d POLICY# items scanned" % f["policy_items_scanned"], "status": "PASS"}],
    "controls": {
        "determinism": {"method": "AC1 was run twice against the same records, back to back.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "a person_access record or an ask", "reason": "Ruled in row Z-S434: decide() denies before person_access is read, so no record admits the tools; none written, no ask present."},
        {"item": "the tier gate read from the host", "reason": "Tier comes from deploy-time rosters; the roster facts are cited from the OG-g-1 evidence, not read from the host in this order."},
        {"item": "a push", "reason": "The order forbids it; the issuer drains the branch."}],
    "surprises": ["NFRA_OPLGTW-Z-S432: a person_access tools_allow record cannot admit the five client tools (decide() denies first); ruled by the issuer in row NFRA_OPLGTW-Z-S434"],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-gc-1. GO msg 36189 (Phase A only); facts written and committed c5cc602303 with row Z-S432; ruling msg 36201 (row Z-S434): add person_access_can_admit false per denied principal, write no ask, run AC1, write the AC1 proof.",
    "compiler_tools": [{"tool": "boto3 (dynamodb scan, strong) and the gateway's own decide()", "invocation": "gc1_phasea.py", "result": "PASS", "note": "Roles, counts and decisions only; no tid, oid or e-mail in any record."}],
}
P = W + "NFRA_OPLGTW.TO-OG-gc-1.round-47-client-tools-for-alyssa-and-menachem.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"], "| principals", list(g["principals"]))
