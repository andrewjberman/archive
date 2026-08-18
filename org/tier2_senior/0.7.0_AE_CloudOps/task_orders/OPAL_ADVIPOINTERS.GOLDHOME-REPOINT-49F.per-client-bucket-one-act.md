# TO OPAL_ADVIPOINTERS.GOLDHOME-REPOINT-49F — the ADVI gold home moves to the per-client bucket, ONE ACT (Andrew-direct ~1730Z)

<task_order id="OPAL_ADVIPOINTERS.GOLDHOME-REPOINT-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.7.0_AE_CloudOps (primary — TF mint + IAM swap, CTO-gated apply) + 0.4.0_DS_ClientPlatform~A (sync + code flips) + 3.0.0_SA_CVO (pin/baseline re-anchor)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T17:42Z</issued>
<dated>TONIGHT after the 23:01Z fixture verdict, or early 08-19 — Andrew's own sequencing word: "proceed with the re-point before the P2 apply." The P2 build stays 08-19 and applies AFTER this lands. The fixture posture stands: AE applies nothing before the fixture verdict; this act's TF mint slots immediately after it.</dated>
<status>pending -- GO 173944Z @1b2ee34db7; AE leg first: TF prepped pre-fixture, mint applies immediately post-fixture-verdict (CTO gate on the plan), then DS~A -> CVO -> spine</status>
<priority>P1 — Andrew-sequenced ahead of the P2 apply; every downstream root reference reads through this act</priority>
<authority>Andrew-direct 2026-08-18 ~1730Z RATIFIED (verbatim @HEAD: org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260818_CLIENT_GOLD_BUCKET_SUPERSESSION.md): the ADVI gold home = opal-data-49financial/gold/{product}/{table}/date={D}/ (+_code/ rides the root) — the clean template slate AND the client agentic-query location. SUPERSEDES the 08-11 gold-home ruling FOR ADVI ONLY (MDPF gold + global scopes STAY at the assets root). Bucket-name template opal-data-{firm_id}, full canonical firm name, never a truncation. CTO decomposition shape 173703Z; CTO gates the TF apply.</authority>
</task_order>

## Objective
Move the 49F ADVI gold root from `opal-data-assets/portal/gold/advi/49financial/` to
`opal-data-49financial/gold/advi/` as ONE ACT: mint the bucket, sync the content, flip the code and
deploy rows, re-anchor the instruments, live-verify, then delete the old prefix
(migrate-before-kill). The frozen P4E-1 key list is UNCHANGED (key names, not roots). The five
affected TOs are amended BY REFERENCE in the same commit as this TO — their root references read
through this act.

## Sequencing spine (the one-act order; each leg MCPs the next)
AE mint+IAM -> DS~A sync+flips -> CVO re-anchor -> SPINE live-verify -> SPINE old-prefix delete.

## Acceptance criteria
Group AE (0.7.0):
- RP-AE-1 BUCKET MINTED (TF, safe-apply, CTO per-apply gate on the plan): `opal-data-49financial`
  with versioning ON, block-public-access ON, and the CROSS-FIRM IAM Deny minted AT CREATION per the
  NEVER#2 pattern — **cot-*/inf-* principal patterns (mdpf-* at CTO's word), and NOT bd-*: the 49F
  chain executes under the bd principal family (bd-exporter-profile per the ratified P2D-4 contract),
  so a bd-* Deny severs the product's own executor. CORRECTED 2026-08-18 ~17:52Z on AE's 175048Z
  catch — this line originally read "bd/cot/inf principals denied", pattern-matching the
  firm-separation triple without noticing the executing principal's own family; AE built it
  correctly and flagged rather than following the literal.** Plan expected-rows in writing
  pre-apply; 0-diff + tag after.
- RP-AE-2 IAM RE-POINTED per the record's three seams: the P3-leg runner grants on
  `portal/gold/advi/*` and the P4-PUBIAM publisher READ-side target re-point to the new bucket
  (the platinum Put half of P4-PUBIAM is UNCHANGED — serving stays at opal-data-portal-v2).
  Live-primitive proof per changed grant (one --resource-arns per call, separate positive control).
- RP-AE-3 P2-FLOOR TF draft target updated to the new root in the same window (the draft's open
  parameter resolves; still no P2 apply until this act lands + CTO gate).
Group DSA (0.4.0_DS_ClientPlatform~A):
- RP-DSA-1 SYNC two-sided: `portal/gold/advi/49financial/` -> `opal-data-49financial/gold/advi/` —
  object count AND bytes verified both sides (the P3-copy precedent bar; ~4,222 objects/~327MB
  expected, actual printed), sync manifest kept as the rollback instrument.
- RP-DSA-2 CODE FLIPS in one commit: `runner_common.py` BUCKET + OUT_ROOT; the safe_deploy_core advi
  row; the `_code/` home re-points to the new root — anything already landed at
  `portal/gold/advi/_code/` MOVES (no twin — the two-homes class); comp-pipescript/commit-gate clean.
Group CVO (3.0.0_SA_CVO):
- RP-CVO-1 RE-ANCHOR: pin files / baselines / sweep artifacts re-cite the new root (frame is
  key-names so members are untouched; roots re-cite; one-line statement per artifact touched).
Spine (AE executes, all three cite):
- RP-SPINE-1 LIVE-VERIFY: listing on the new root (count matches sync) + ONE runner read exercised
  against the new root (not a config read — an actual emitter/stage input resolution).
- RP-SPINE-2 OLD PREFIX DELETE, only after RP-SPINE-1: `portal/gold/advi/` prefix removed
  (migrate-before-kill; consumer basis per the record: platinum/advi is empty, portal reads nothing
  from gold — re-checked live at execution, denominator printed); absence read WITH an adjacent
  positive control; rollback = the sync manifest + versioned new bucket.
- RP-VAL proof instance per group, rc=0 positional, grammar below.

<proof_of_spec>
  <expected_criteria>RP-AE-1,RP-AE-2,RP-AE-3,RP-DSA-1,RP-DSA-2,RP-CVO-1,RP-SPINE-1,RP-SPINE-2,RP-VAL</expected_criteria>
  <instance_path_grammar>{assignee_folder}/deliverables/PROOF_OF_SPEC_GOLDHOME_REPOINT_49F_{group}_{YYYYMMDD}.json</instance_path_grammar>
</proof_of_spec>

## Cross-domain coordination
- The five affected TOs (P2-DISPATCH, P2-FLOOR, P3-CLOSE, P4-EMIT, P4-PUBIAM) are amended BY
  REFERENCE in this TO's issuing commit — assignees read their root references through this act; the
  frozen key list @5f1076e9c1 is untouched. DS~B: your emitters' READ root moves with RP-DSA-2;
  first emission still gates on AE's grant-live MCP (now against the new-bucket read grants).
- MDPF gold + global scopes DO NOT MOVE (the supersession is ADVI-only) — nothing under
  opal-data-assets outside portal/gold/advi is touched.

## Do not
- No P2 apply before this act lands (Andrew's sequencing word). No twin at either _code home. No
  bucket-name truncation (opal-data-49financial, never 49f). No touch of the bd platinum chain or
  anything the 23:01Z fixture reads.

## Reporting
COO (cc CTO, MSTR, DS~B) per leg at landed; CTO gates the TF apply and reads the spine. Surprise
channel: one banked line to COO. Session log with Compiler Tools section = deliverable per seat.
