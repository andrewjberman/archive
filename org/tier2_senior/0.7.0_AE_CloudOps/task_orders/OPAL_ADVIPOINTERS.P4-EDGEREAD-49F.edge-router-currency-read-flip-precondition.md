# TO OPAL_ADVIPOINTERS.P4-EDGEREAD-49F — Lambda@Edge router currency read: the P4 flip PRECONDITION (CTO R-4)

<task_order id="OPAL_ADVIPOINTERS.P4-EDGEREAD-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T17:10Z</issued>
<dated>2026-08-20 — CTO R-4: the currency read is a P4 FLIP PRECONDITION; if a refresh is needed it lands + verifies BEFORE 08-22 or row 4c RE-DATES in writing.</dated>
<status>complete 2026-08-29T15:3xZ by 0.7.0_AE_CloudOps -- ER-1..ER-4 PASS, proof instance VALID rc=0 violations=0. ER-1: BOTH routers CURRENT, deployed published-version bytes BYTE-IDENTICAL to a faithful rebuild through the declared build input (public-data-router v7 873 B sha256 315adcb98080..., shared-advisor-router v25 5999 B sha256 fca5c275cd76...); pinning axis 5 of 5 live CloudFront associations == $LATEST, no stale pin. ER-2: no diff exists, so no divergent behaviour to name. ER-3 DISCHARGED VIA PATH (a) -- both CURRENT, flip proceeds; no re-date made. The 08-22 bound is CONDITIONAL ("IF a refresh is needed") and no refresh was needed, so the conditional never triggered. BOUND: current as of 2026-08-29, NOT as of 08-22 (v25 published 08-28); harmless only because the flip has not occurred, and this read EXPIRES if the flip defers past a further edge change. Nothing deployed, nothing uploaded, no TF act; build-nodejs-lambda.sh NOT run (build-and-upload, no dry-run flag).</status>
<priority>P1-adjacent — the 08-22 flip traverses shared-advisor-router; flipping through a stale edge is the two-homes class at the serving edge</priority>
<authority>CTO ruling set @CTO_GATE_AND_RULING_SET_20260818_1700Z.md R-4, on 0.8.0's DEPLOYCENSUS finding (public-data-router + shared-advisor-router running 05-14 builds with source moved since). Rule 22a CODE layer: deployed bytes vs built-from source resolved through the BUILD INPUT, never by filename.</authority>
</task_order>

## Objective
Rule-22a CODE read on the two deployed Lambda@Edge functions (`public-data-router`,
`shared-advisor-router`): download the DEPLOYED (published-version) packages, hash members, diff
against built-from source resolved through the build input. CLASSIFY (CURRENT / STALE-affecting-flip /
STALE-not-affecting-flip / DELIBERATELY-HELD). If any staleness AFFECTS the 49financial ADVI route
resolution (FIRM_BUCKET_MAP, key rewrite, auth legs): the refresh routes through the CTO per-apply
gate and lands + verifies before 08-22 — else row 4c re-dates in writing, never flips through it.

## Compiler tools (three-phase)
Phase 1: `comp-routes behaviors` + `comp-routes edge-versions` (the pinning axis) — note comp-routes
is DESIRED-plane; the deployed read is the point. Phase 2: commit before any TF change. Phase 3: if a
refresh ships — published-version hash re-read + one exercised route read per router (positive +
negative path).

## Cross-domain coordination
- shared_resource: shared-advisor-router — DE's P4R-1 read-surface enumeration cites it; MCP DE your
  classification (their per-key flip commits should cite the router vintage they flip through).
- shared_resource: CloudFront distribution — any refresh is a TF act under safe-apply + CTO gate.

## Acceptance criteria
- ER-1 DEPLOYED READ: both routers' published-version package member hashes vs build-input-resolved
  source, per-member diff printed with denominators; classification per router with the evidence.
- ER-2 FLIP-RELEVANCE: for any diff, the SPECIFIC divergent behavior named (which route/key/branch
  differs) — never a bare "stale"; a diff that cannot affect the 49financial resolution is stated as
  such with the reason.
- ER-3 THE PRECONDITION DISCHARGED, one of exactly three ways, in writing: (a) both CURRENT-or-
  irrelevant -> flip proceeds; (b) refresh landed + verified (hash + exercised route, CTO gate cited)
  before 08-22; (c) row 4c RE-DATED in writing. No fourth path; no silent flip through a stale edge.
- ER-4 proof instance VALID rc=0 positional: ids ER-1,ER-2,ER-3,ER-4.

<proof_of_spec>
  <expected_criteria>ER-1,ER-2,ER-3,ER-4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_ADVIPOINTERS.P4-EDGEREAD-49F_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No refresh without the CTO per-apply gate. No `aws lambda update-function-code` (Terraform only;
  edge functions deploy per their own TF pattern). Nothing before your fixture/TO-4/P2 rows tonight.

## Reporting
COO (cc CTO, DE, MSTR) at classification and at the precondition-discharged line. Surprise channel:
one banked line to COO. Session log with Compiler Tools section = deliverable.
