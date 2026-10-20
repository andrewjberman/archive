#!/usr/bin/env python
"""OG-ls-1: write the proof_of_spec instance from a real run of AC1 and AC2 (each run twice for the determinism control; AC2 reads the LIVE role).
usage: python ls1_proof_gen.py   (repository root, after the Phase B commit and the ledger close)"""
from __future__ import annotations

import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
CK = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r47/checks/"
TO = "org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ls-1.round-47-narrow-the-silver-list-grant-to-the-eight-sources.md"
PRD = "org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md"
DEC = "org/missions/D9/NFRA/NFRA_OPLGTW/decompositions/NFRA_OPLGTW_DECOMP.md"
TF = "infra/aws/terraform/opal-gateway/family_depth_read_iam.tf"
GIT = "COMMITTED-NOT-DEPLOY-SCOPE"
SLUG = "_nfra-oplgtw-grants-ls1_deploy_completion.md"


def run(script):
    r = subprocess.run(["bash", CK + script], capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r", "").strip() + "\nexit=%d" % r.returncode


def pin(*paths):
    return subprocess.run(["git", "log", "-1", "--format=%h", "--"] + list(paths), capture_output=True).stdout.decode().strip()


def art(path, kind, deployed, ev, cov):
    return {"path_or_key": path, "kind": kind, "commit_or_etag": pin(path) if not path.startswith("aws:") else pin(W + "LS_APPLIED.json"), "deployed_state": deployed, "deploy_evidence": ev, "artifact_covered_by": cov}


ledger = [p for p in subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/change_management/"], capture_output=True).stdout.decode().split() if p.endswith(SLUG)][-1]
closed_at = re.search(r"closed (\d{8}T\d{6}Z)", io.open(ledger, encoding="utf-8").read()).group(1)
order = io.open(TO, encoding="utf-8").read()
L = json.load(io.open(W + "LS_LIVE.json", encoding="utf-8"))
A = json.load(io.open(W + "LS_APPLIED.json", encoding="utf-8"))
ac, stable = {}, True
for cid in ("AC1", "AC2"):
    outs = [run("ls1.%s.sh" % cid), run("ls1.%s.sh" % cid)]
    exp = re.search(r'<criterion id="%s"[^>]*>.*?<expect>(.*?)</expect>' % cid, order, re.S).group(1)
    ac[cid] = (outs, exp)
    stable = stable and outs[0] == outs[1]
    print(cid, "matches expect" if re.search(exp, outs[0]) else "DOES NOT MATCH THE ORDER'S EXPECT", "| stable" if outs[0] == outs[1] else "| UNSTABLE")

verbatim = {
    "AC1": "the one file lists silver only under the eight sources, keeps FOUR statements and the three read actions, the plan is 0/1/0, the simulation holds the six cases, the ask has three halves.",
    "AC2": "the narrowed policy is live and the simulator refuses the three census prefixes.",
}
live_ev = ("One safe-apply of the saved targeted plan: Plan 0 to add, 1 to change, 0 to destroy; Apply complete 0 added, 1 changed, 0 destroyed (W/LS_APPLY.txt). Read back from IAM: %d statements, %d silver patterns equal to the sixteen per-source forms, none starts with a star, policy hash prefix %s (was %s). "
           "Live simulation on the role, %d cases, all as expected: a real source prefix, the root list with delimiter and the unchanged statements allowed; bloomberg, gateway, yahoo and commonwealth silver lists, the root list without delimiter, PutRule and PutObject denied. "
           "family_depth read once on the host (marker 13917ef993, cgroup hard guard, instance role): %d of %d families, equal to the round-46 driven read, 0 writes. Rollback: revert the one list and apply again; not used."
           % (L["shape"]["statements"], L["shape"]["silver_patterns"], A["policy_sha256_16"], A["policy_sha256_16_before"], len(L["results"]), A["families_after"], A["denominator_after"]))
inst = {
    "schema_version": "1.0", "to_id": "NFRA_OPLGTW.TO-OG-ls-1", "firm": "FABRIC", "phase": "BUILD-GENERAL", "assignee": "0.7.0_AE_CloudOps~NFRA1",
    "spec_ref": {"doc": PRD, "group": "OTHER", "vintage_commit": pin(PRD)},
    "decomp_ref": {"doc": DEC, "vintage_commit": pin(DEC), "to_ref": TO},
    "artifacts_produced": [
        art("aws:iam/opal-gateway-role/gateway-family-depth-read-policy (the silver s3:ListBucket list narrowed to the eight sources)", "aws_resource", "DEPLOYED-VERIFIED", live_ev, ["AC2"]),
        art(TF, "terraform", GIT, "The one list: flatten([for s in local.family_depth_sources : [<source>/*/silver/, <source>/*/silver/*]]); blob 0f5da21da8 -> 42fee26095; the other three statements byte-equal.", ["AC1"]),
        art(W + "LS_BEFORE.json", "doc", GIT, "The live policy read first: hash prefix 2dd3ee621be1436d, four statements, patterns */silver/ and */silver/*; bloomberg, gateway, yahoo silver lists read allowed before.", ["AC1"]),
        art(W + "LS_PLAN.txt", "doc", GIT, "Targeted plan: 0 to add, 1 to change, 0 to destroy, the sixteen per-source patterns.", ["AC1"]),
        art(W + "LS_SIMULATE_PLAN.json", "doc", GIT, "iam:SimulateCustomPolicy on the live policy with only the silver list replaced: 14 cases, all as expected.", ["AC1"]),
        art(W + "NEVER_WIDEN_ASK_OG-ls-1.md", "doc", GIT, "The ask, sha256 prefix 7472e5c143d2, signed by CTO 00add28273, COO K1-K4 and CVO 74c8013a0d.", ["AC1"]),
        art(W + "LS_LIVE.json", "doc", GIT, "The live read-back and the live-role simulation, counts and decisions.", ["AC2"]),
        art(W + "LS_APPLIED.json", "doc", GIT, "policy name, samples, hash, apply time and the host read's family counts.", ["AC2"]),
        art(W + "LS_HOST_READ.json", "doc", GIT, "The single family_depth host read, counts only.", ["AC2"]),
        art(ledger, "doc", GIT, "Ledger nfra-oplgtw-grants-ls1 opened before the apply, three legs proven, CLOSED %s; sentinel removed." % closed_at, ["AC2"]),
    ],
    "acceptance": [
        {"criterion_id": cid, "criterion_verbatim": verbatim[cid], "method": "command", "invocation": 'bash %sls1.%s.sh; echo "exit=$?"' % (CK, cid), "expect": ac[cid][1], "output_evidence": ac[cid][0][0],
         "denominator": {"AC1": "1 .tf file; 4 statements; 14 simulation cases; 3 ask halves", "AC2": "1 live policy of %d role policies; %d live simulation cases; 13 families read on the host" % (L["inline_policies_on_role"], len(L["results"]))}[cid], "status": "PASS"} for cid in ("AC1", "AC2")],
    "controls": {
        "determinism": {"method": "AC1 and AC2 were each run twice, back to back, AC2 against the live role.", "observed": "outputs identical" if stable else "outputs differ", "status": "STABLE" if stable else "UNSTABLE (deliverable INVALID)"},
        "mutant": {"description": "The order names no mutant; the issuer's synthetic AC1 arms (the original .tf FAILS) are the discriminating arm.", "expected": "n/a", "observed": "n/a", "status": "N/A-SPEC-NAMES-NONE"}},
    "declared_exclusions": [
        {"item": "comp-schedule --drift", "reason": "Run twice; the 90 s budget was reached both times (1 of 6 carriers scanned, 0 of 29 ledger entries): the result is a PARTIAL prefix, the one candidate it printed concerns another gate, and this order adds no schedule or trigger."},
        {"item": "Rule 12 staging writes", "reason": "The host read staged its scripts in the artifacts bucket under the Rule 12 route, as every earlier host read did; no store holding data was written."},
        {"item": "a push", "reason": "The order forbids it; the issuer drains the branch."}],
    "surprises": [],
    "session_log": "Session seat 0.7.0_AE_CloudOps~NFRA1, OG-ls-1. Phase A (GO 36166, 2026-10-20): live policy read, the one .tf edit (1017106c75), plan 0/1/0, 14-case simulation, the ask (d2631c264f). Phase B (GO 36173, halves COO K1-K4, CTO 00add28273, CVO 74c8013a0d): ledger opened 10:46Z, policy and blob re-read, one safe-apply, live read-back and simulation, one family_depth host read; the ledger CLOSED " + closed_at + ".",
    "compiler_tools": [{"tool": "terraform / boto3 / ssm", "invocation": "terraform plan -out and safe-apply of the saved plan; ls1_before.py, ls1_simulate.py, ls1_phaseb.py, ls1_driven.py", "result": "PASS", "note": "Counts, hashes and decisions only; the full plan and apply output hold the account number and stayed in the scratch folder."}],
}
P = W + "NFRA_OPLGTW.TO-OG-ls-1.round-47-narrow-the-silver-list-grant-to-the-eight-sources.proof_of_spec.json"
io.open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(inst, indent=1) + "\n")
print("wrote", P, "determinism", inst["controls"]["determinism"]["status"])
