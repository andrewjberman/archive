#!/usr/bin/env python3
"""Build the ADVI_BDPARITY.P2-1-AE proof of spec.

commit_or_etag is DERIVED per row (the CCX identity rule): dirty -> PENDING-THIS-COMMIT,
clean -> full 40-hex, clean-with-no-commit -> refuse. criterion_verbatim is EXTRACTED from
the face's bytes.

Run: python org/tier2_senior/0.8.0_AE_CloudComp/deliverables/build_p21ae_proof.py
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FACE = ROOT / ("org/tier2_senior/0.8.0_AE_CloudComp/task_orders/"
               "ADVI_BDPARITY.P2-1-AE.feed-selector-apply-on-the-deployed-puller.md")
OUT = ROOT / ("org/tier2_senior/0.8.0_AE_CloudComp/deliverables/"
              "ADVI_BDPARITY.P2-1-AE.proof_of_spec.json")
PEND = "PENDING-THIS-COMMIT"


def row_identity(rel: str) -> str:
    """DERIVE, never assert. A committed-and-unchanged file does not ride this commit."""
    dirty = subprocess.run(["git", "status", "--porcelain", "--", rel],
                           cwd=str(ROOT), capture_output=True, text=True).stdout.strip()
    if dirty:
        return PEND
    h = subprocess.run(["git", "log", "-1", "--format=%H", "--", rel],
                       cwd=str(ROOT), capture_output=True, text=True).stdout.strip()
    if not h:
        raise SystemExit(f"FAIL: {rel} clean but has no commit -- cannot identify it")
    return h


def face_criteria() -> dict[str, str]:
    t = FACE.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<criterion id="([^"]+)"/>\s*(.*?)(?=<criterion |\Z)', t, re.S):
        cid, body = m.groups()
        out[cid] = " ".join(body.split())[:1400]
    return out


DEN = {
    "PA-1": "1 patch, sha256 verified against 2 candidate pins x 3 byte-forms before applying; 11 of 11 test arms rc=0; +40/-3 lines; 0 added and 0 removed DRY_RUN lines",
    "PA-2": "1 acting resource of 4 resource_changes; 3 changed keys, all code; ENV 0 / TRIGGER 0 / IAM 0; Plan 0 add / 1 change / 0 destroy",
    "PA-3": "1 address; apply triple exactly 0 added / 1 changed / 0 destroyed; 5 HALT-GATE messages reviewed, 0 STOP-class",
    "PA-4": "6 of 6 ledger legs closed with proof; 5 env keys set-identical; 1 deployed package downloaded from the running function; re-plan detailed-exitcode 0",
}

EVIDENCE = {
    "PA-1": (
        "⛔ THE PATCH THE FACE NAMED WAS REFUSED. The face @30c8b1c9c6 and dispatch 86676 declared "
        "sha256 a312067025073ea173f73b5d53ccc7cd39ffa573ee3f515ac17ffd3bdba43873; the bytes on disk "
        "hashed to ab417c452533af2d2b25b345760db12640ca09f432fcb54b144d712b99084261. I stopped rather "
        "than apply an artifact whose identity failed, and traced the cause MYSELF before any seat "
        "told me: d9ac9dc597 (5,002 B, a3120670...) is SUPERSEDED by d981d2366a (5,145 B, ab417c45..., "
        "'fix: correct a MISATTRIBUTION I made', +8 min). Tested raw / CR-stripped / CRLF-ified at "
        "BOTH pins and the worktree before concluding, because a sha mismatch and a line-ending "
        "artifact are indistinguishable from one hash; only d9ac9dc597 raw matched the declared value. "
        "86709 (issuer) / 86720 (DS~C) / 86721 (gate) then confirmed ab417c45 as final and the face's "
        "digest was corrected at 41de7149ae. APPLIED THE FINAL ONE: git apply --check rc=0 -> git "
        "apply rc=0, +40/-3, target 66f324ae7c90... -> c1278acb257e05b9f18b4ba194c6cae754976dbb55b149"
        "b4eaa79985ad483fb6, CR count 0 before and 0 after. THE 11 ARMS RE-RUN AT THIS SEAT, 11 of 11 "
        "rc=0 -- not inherited from DS~C's run. commit-gate clean 1 of 1. Committed 49a851ea2e citing "
        "d981d2366a + the digest. THE TWO 'DO NOT' CLAUSES, EACH MEASURED: DRY_RUN untouched -- 0 "
        "ADDED and 0 REMOVED diff lines mention it (the two hits are context), and the expression is "
        "byte-identical, DRY_RUN = os.environ.get('DRY_RUN', '1') == '1'; default unchanged -- "
        "resolve_feeds(feeds=None) still returns all three, preserving OPAL_TAXSMA_PT2's silver build "
        "which reads reporting_costbasis + reporting_allocation."
    ),
    "PA-2": (
        "THE PLAN ASSERTED FROM THE PLAN JSON, NOT THE TEXT RENDERING -- '(4 unchanged blocks hidden)' "
        "is a rendering, not a measurement. terraform show -json over the saved plan: resource_changes "
        "4, ACTING (non no-op) 1 = module.bd49f_reporting_pull.aws_lambda_function.this [update]; "
        "CHANGED keys exactly {last_modified, s3_object_version, source_code_hash}; known-after-apply "
        "{last_modified}; ENV rows changed 0; TRIGGER rows changed 0; IAM rows changed 0; "
        "'environment before == after: True'. Plan: 0 to add, 1 to change, 0 to destroy. ⭐ THE ENV "
        "IDENTITY IS THE PROPERTY THAT MATTERS AND THE GATE SAID SO: this function's TF env carries "
        "DRY_RUN='0' (egress ENABLED, Andrew-direct 2026-07-17) and INSURANCE_EGRESS='1'; a code-only "
        "plan is the proof neither switch moves. THE ZIP, DOWNLOADED FROM S3 AND READ BY CONTENT: "
        "lambda_function.py 28,533 bytes, RAW CR count 0, LF sha256 c1278acb257e05b9... == the "
        "committed INDEX blob (never the worktree). ⚠ NOT TRIPLE CORROBORATION: the build script's "
        "printed SHA256, the plan's source_code_hash target and the source-map field all read "
        "yO0R5JDSL86L1cp+..., but the plan reads it from the S3 object's content-sha256 metadata and "
        "the source map was written by the same build computation -- ONE method, three carriers. The "
        "content comparison above is the independent rung. Built via the canonical "
        "build-and-upload.sh; its own gate (source committed) checked and satisfied for this function: "
        "0 dirty entries in the function directory, all 3 vendored modules index==worktree; the 6 "
        "dirty entries under infra/aws/lambda/ are deleted .pyc in an unrelated layer. Source-map "
        "update committed separately at da9afee96d: 2 changed lines, one entry, no other function "
        "touched."
    ),
    "PA-3": (
        "APPLY ON THE GATE'S WORD (1.0.0_SA_CTO 86922), issuer half at 86887. safe-apply on the 1.9.8 "
        "shim, applied THE SAVED PLAN FILE rather than a re-plan, so exactly the reviewed plan landed "
        "and no drift could enter between review and apply. HALT-GATE FIRED FIRST and blocked: 5 "
        "pending messages, each read; NONE carries a [STOP] or [HALT] subject prefix, so all five are "
        "routine-class and HALT_ACK=1 is the sanctioned path. THREE OF THE FIVE BEAR ON THIS DEPLOY "
        "and are recorded rather than waved past: (a) CVO's ARMED-candidate that "
        "record-terraform-deploy.sh's commit-derivation limb silently no-ops under bun while the tool "
        "STILL COMMITS, (b) the gate naming 0.8.0_AE_CloudComp -- this lane's base -- as its disarm "
        "owner with an INTERIM executor check for every deploy-record on this device, and (c) CVO's "
        "census naming THIS function's source-map last_deployed_commit as stale-but-content-plausible. "
        "CONSEQUENCE, ACTED ON: I did NOT run record-terraform-deploy.sh. The face does not require it "
        "(PA-3 requires safe-apply + the NEVER#6 ledger via deploy_ledger.py, which was opened at the "
        "apply and closed on proof), and running a tool with a live ARMED-candidate half-write defect "
        "to record an irreversible act would be the wrong call. The source map's last_deployed_commit "
        "for this function REMAINS f559cbc5160798b78c284a53a470748bf76caace and is therefore still "
        "stale after this deploy -- stated rather than silently left, and owned by the (k) carrier "
        "item, not by this face. tombstone-gate CLEAN (2 planned creates checked against 7 "
        "tombstones). RESULT: 'Apply complete! Resources: 0 added, 1 changed, 0 destroyed' -- exactly "
        "the required triple, on the ONE address, with the output captured unfiltered. Terraform's own "
        "-target warning is present in that output and is expected for a targeted apply."
    ),
    "PA-4": (
        "READ ON THE RUNNING ARTIFACT, on the LIVE plane, never from the apply report. CodeSha256: "
        "GMfBZrn/elvrVJCY2L0BIDzt9lUoDX3eaCczb9rG174= -> yO0R5JDSL86L1cp+V3qla1NsYWjvAL4lYi1drQvesIk= "
        "== the uploaded zip EXACTLY, and changed from before. LastModified 2026-08-30T02:54:33Z -> "
        "09:14:51Z, post-dating the apply. CodeSize 33,102 -> 33,902. ENV SET-IDENTICAL before and "
        "after by dict equality over all 5 keys (BD_BASE, BD_SESSION_SECRET_ID, DRY_RUN, "
        "INSURANCE_EGRESS, MONOLITH_BUCKET); DRY_RUN '0' -> '0'; INSURANCE_EGRESS '1' -> '1'. ⭐ THE "
        "STRONGEST RUNG: the DEPLOYED PACKAGE was downloaded from the RUNNING function via the "
        "get-function presigned URL -- not from S3 and not from the worktree -- 33,902 bytes, 6 "
        "entries; its lambda_function.py is 28,533 bytes with RAW CR count 0 and LF sha256 "
        "c1278acb257e05b9f18b4ba194c6cae754976dbb55b149b4eaa79985ad483fb6 == the committed index blob; "
        "and the selector is demonstrably IN the running bytes ('def resolve_feeds', 'feeds_requested' "
        "and 'event.get(\"feeds\")' all present). 0-DIFF RE-PLAN: 'No changes. Your infrastructure "
        "matches the configuration.' AND -detailed-exitcode rc=0 -- read machine-readably, not from "
        "the prose alone (0 = no changes, 2 = changes present). NEVER#6 LEDGER opened via "
        ".tools/deploy_ledger.py at the apply and CLOSED with all 6 legs carrying proof; sentinel "
        "removed. NO VENDOR CALL AT ANY STEP: the selector was exercised only by DS~C's "
        "boundary-patched test; a live pull is P2-2 and waits on Andrew's word."
    ),
}


def main() -> None:
    crit = face_criteria()
    missing = set(EVIDENCE) - set(crit)
    if missing:
        raise SystemExit(f"FAIL: evidence for criteria absent from the face: {sorted(missing)}")

    acceptance = [
        {
            "criterion_id": cid,
            "criterion_verbatim": crit[cid],
            "method": "live_read" if cid in ("PA-3", "PA-4") else "command",
            "invocation": {
                "PA-1": "git apply --check / git apply; python <DS~C 11-arm test>; .tools/commit-gate.sh",
                "PA-2": ".tools/terraform.exe plan -target=module.bd49f_reporting_pull -out=<plan>; terraform show -json; aws s3 cp + zipfile read",
                "PA-3": "HALT_ACK=1 bash .tools/safe-apply.sh apply -no-color <saved plan>; python .tools/deploy_ledger.py open/close",
                "PA-4": "aws lambda get-function-configuration; aws lambda get-function (presigned Code.Location) + zipfile; terraform plan -detailed-exitcode",
            }[cid],
            "output_evidence": EVIDENCE[cid],
            "denominator": DEN[cid],
            "status": "PASS",
        }
        for cid in sorted(EVIDENCE)
    ]

    arts = []
    for rel, kind, note in (
        ("infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py",
         "script", "The patched puller. Applied from ab417c45 @d981d2366a; the RUNNING artifact's copy re-verified against this index blob."),
        ("infra/aws/lambda/ci/lambda-source-map.json",
         "config_data", "artifact_sha256 updated by the canonical build-and-upload; 2 changed lines, one entry."),
        ("org/critical_paths/change_management/20260830T0910Z_advi-bdparity-p2-1-ae-selector_deploy_completion.md",
         "doc", "NEVER#6 ledger, opened at the apply via the tool and CLOSED with all 6 legs proven."),
        ("org/tier2_senior/0.8.0_AE_CloudComp/deliverables/build_p21ae_proof.py",
         "script", "This builder; identities derived per row, criterion_verbatim extracted from the face."),
    ):
        arts.append({
            "path_or_key": rel,
            "kind": kind,
            "commit_or_etag": row_identity(rel),
            "deployed_state": "DEPLOYED-VERIFIED" if rel.endswith("lambda_function.py") else "COMMITTED-NOT-DEPLOY-SCOPE",
            "deploy_evidence": note,
            "artifact_covered_by": ["PA-1", "PA-2", "PA-3", "PA-4"],
        })
    arts.append({
        "path_or_key": "arn:aws:lambda:us-east-1:313476888478:function:opal-assets-bd49f-reporting-pull",
        "kind": "s3_object",
        "commit_or_etag": "sha256:yO0R5JDSL86L1cp+V3qla1NsYWjvAL4lYi1drQvesIk=",
        "deployed_state": "DEPLOYED-VERIFIED",
        "deploy_evidence": ("The live function. CodeSha256 read from get-function-configuration AFTER the "
                            "apply equals the uploaded zip; the package downloaded from the running "
                            "function carries lambda_function.py at LF sha c1278acb..., raw CR 0."),
        "artifact_covered_by": ["PA-3", "PA-4"],
    })

    proof = {
        "schema_version": "1.0",
        "to_id": "ADVI_BDPARITY.P2-1-AE",
        "firm": "49F",
        "phase": "P3-REPOINTS",
        "assignee": "0.8.0_AE_CloudComp~Y",
        "decomp_ref": {
            "doc": ("org/tier2_senior/0.4.0_DS_ClientPlatform~C/task_orders/"
                    "ADVI_BDPARITY.P2-CENSUS.full-population-parity-census.md"),
            "vintage_commit": "30c8b1c9c6",
            "to_ref": ("org/tier2_senior/0.8.0_AE_CloudComp/task_orders/"
                       "ADVI_BDPARITY.P2-1-AE.feed-selector-apply-on-the-deployed-puller.md"),
        },
        "spec_ref": {
            "doc": "org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_BDPARITY.P2-1_feed_selector.patch",
            "group": "OTHER",
            "vintage_commit": "d981d2366a",
        },
        "artifacts_produced": arts,
        "acceptance": acceptance,
        "controls": {
            "mutant": {
                "description": ("DS~C's 11-arm boundary-patched battery, RE-RUN at the applying seat rather "
                                "than inherited. Its refusal arms are the mutants: an unlisted feed name "
                                "(three spellings incl. a case variant), an empty list, and DRY_RUN as a "
                                "second independent refusal. The positive controls are the unmutated "
                                "paths: unspecified still spends all three (6 calls for 2 accounts) and "
                                "narrowed spends one per account (2 for 2)."),
                "expected": "11 of 11 rc=0, with the refusal arms refusing and the spend arms proving the pre-existing behaviour intact.",
                "observed": ("11 of 11 rc=0 at THIS seat after the patch applied. The 'UNSPECIFIED still "
                             "spends all three' arm is the one that matters for safety -- it proves the "
                             "scheduled OPAL_TAXSMA_PT2 fire, which carries no feeds key, is untouched."),
                "status": "FIRED-AS-EXPECTED",
            },
            "determinism": {
                "status": "STABLE",
                "method": ("The deployed identity checked on three independent planes: the S3 artifact's "
                           "content, the live CodeSha256, and the package downloaded from the running "
                           "function. Plus a 0-diff re-plan read by -detailed-exitcode."),
                "observed": ("All three agree on the same bytes; re-plan 'No changes' with "
                             "-detailed-exitcode rc=0. The zip's and the running package's "
                             "lambda_function.py both hash to c1278acb... == the committed index blob."),
            },
        },
        "declared_exclusions": [
            {"item": "Any vendor call to the 49F reporting API.",
             "reason": "The face forbids it at every step; the selector was exercised only by the boundary-patched test. A live pull is P2-2 and waits on Andrew's per-use word."},
            {"item": "Changing the feeds=None default.",
             "reason": "The face's DO-NOT. A performance-only default would silently starve OPAL_TAXSMA_PT2's silver build; the default stays all-three and the caller narrows."},
            {"item": "record-terraform-deploy.sh.",
             "reason": ("Not required by this face, and it carries a live ARMED-candidate defect on this "
                        "device (CVO 78829: the commit-derivation limb silently no-ops under bun while the "
                        "tool still commits), with this lane's own base named as disarm owner. The NEVER#6 "
                        "obligation was met via deploy_ledger.py instead. Consequence stated: the source "
                        "map's last_deployed_commit for this function remains f559cbc516... and is still "
                        "stale after this deploy.")},
            {"item": "Any wider terraform target.",
             "reason": "The gate's word was 'this plan and nothing wider'. The saved plan file was applied, so no re-plan drift could widen it."},
            {"item": "Fixing the BUILD_MANIFEST vs shipped-zip discrepancy.",
             "reason": "Routed to DS~C as the manifest's owner by the issuer, due after P2-1 closes. Accepted OBSERVATION/INERT by the gate."},
        ],
        "surprises": [
            ("OBSERVATION / INERT (3.0.0_SA_CVO, cc 2.0.0_SA_COO): THE SHIPPED ZIP CARRIES SIX .py WHILE "
             "BUILD_MANIFEST DECLARES THREE. The manifest states taxsma_resolver.py and taxsma_seed.py "
             "are 'NOT packaged (never imported by the handler)'; the package downloaded from the RUNNING "
             "function contains both, plus taxsma_newacc.py. Pre-existing -- the build script globs the "
             "function directory -- and the import-closure check passes, so nothing breaks today; the "
             "manifest's stated reason for excluding resolver (a pandas dependency the runtime lacks) is "
             "a live risk only if something ever imports it at runtime. Accepted by the gate as the "
             "manifest class in the OVER-inclusion direction and routed to DS~C."),
            ("OBSERVATION / INERT (3.0.0_SA_CVO, cc 2.0.0_SA_COO): THE FACE DECLARED A SUPERSEDED PATCH "
             "DIGEST, AND THE REFUSAL IS WHAT CAUGHT IT. The identity check on an artifact about to reach "
             "a production Lambda is the one place a stale pin is cheap to catch and expensive to miss. "
             "The issuer confirmed the stale digest was its own carrier error and corrected it at "
             "41de7149ae. Recorded because the general form is worth more than the instance: a declared "
             "digest that fails is not automatically a corrupted artifact -- it is equally often a "
             "correct artifact against a stale declaration, and only tracing the pins tells you which."),
            ("OBSERVATION / INERT (3.0.0_SA_CVO, cc 2.0.0_SA_COO): THE HALT-GATE EARNED ITS PLACE. It "
             "blocked this apply and surfaced five pending messages, three of which bear directly on it "
             "-- including a live ARMED-candidate defect in record-terraform-deploy.sh owned by this "
             "lane's own base serial, and a census naming THIS function's source-map "
             "last_deployed_commit as stale. None was STOP-class so HALT_ACK=1 was correct, but the "
             "review changed what I did: I used deploy_ledger.py for the NEVER#6 obligation and did not "
             "touch the defective recorder. A gate that only blocks is worth less than one that is read."),
        ],
        "session_log": "org/tier2_senior/0.8.0_AE_CloudComp/logs/2026-08-30/ (at session close, with a Compiler Tools section)",
        "compiler_tools": [
            {"tool": "comp-to", "invocation": "comp-to ADVI_BDPARITY.P2-1-AE",
             "result": "PASS -- bound and read back before the first tool run of this face."},
            {"tool": "comp-find", "invocation": "--name and content, scoped pathspecs, for the TF address, the module's code sourcing and the build tooling",
             "result": "PASS with denominators printed. The comp-rail HUD gate correctly refused one raw directory grep of mine and routed it here."},
            {"tool": ".tools/safe-apply.sh", "invocation": "HALT_ACK=1 safe-apply apply <saved plan>",
             "result": "PASS rc=0. The HALT-GATE blocked first with 5 pending messages -- see the surprise row; tombstone-gate CLEAN; triple 0/1/0."},
            {"tool": ".tools/deploy_ledger.py", "invocation": "open --slug advi-bdparity-p2-1-ae-selector (6 legs); close-leg x6; close",
             "result": "PASS -- opened at the apply, all 6 legs closed with proof, sentinel removed. Used INSTEAD of record-terraform-deploy.sh, which carries a live defect on this device."},
            {"tool": ".tools/commit-gate.sh", "invocation": "on the patched lambda_function.py",
             "result": "PASS clean 1 of 1 (py_compile + ds-precommit + ruff py39)."},
        ],
    }

    OUT.write_text(json.dumps(proof, indent=1) + "\n", encoding="utf-8")
    print(f"OK: wrote {OUT.relative_to(ROOT)}")
    for a in acceptance:
        print(f"   {a['criterion_id']}  status={a['status']}")
    for a in arts:
        print(f"   artifact {a['path_or_key'].split('/')[-1][:44]:46} {a['commit_or_etag'][:44]}")


if __name__ == "__main__":
    main()
