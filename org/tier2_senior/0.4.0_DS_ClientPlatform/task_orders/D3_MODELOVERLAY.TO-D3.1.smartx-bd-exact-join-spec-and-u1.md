# TO D3_MODELOVERLAY.TO-D3.1 — SMARTX_BD_EXACT_JOIN spec + the U1 model-identity edge (LAPTOP; STARTABLE NOW)

<task_order id="D3_MODELOVERLAY.TO-D3.1" project="D3_ACCOUNT_MODEL_OVERLAY">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:50Z</issued>
<dated>startable NOW -- gates on nothing (CVO's dispatch-order note names it in the startable set)</dated>
<status>complete -- CLOSED BY THE ISSUER 2.0.0_SA_COO 2026-08-30 05:2xZ (the terminal status this face left to COO), on the D3.2 gate pre-read by 0.4.0_DS_ClientPlatform~E (85970, measured on origin): DELIVERED @1914fa3fd6, proof VALID, contract RATIFIED @b513a7fdbd, U1 ANSWERED; D3.1-6 ("register the axis in SYSTEM_DEFINITIONS") SUPERSEDED by Andrew's 2026-08-20 naming-law act at the CRO terminal (v3.9 changelog: the join disposition RELOCATED OUT under the bar; the axis's ratification stands at data/_contracts/smartx_bd_join_disposition.yaml v1.0 @f097698bf6) and its carry-over VOIDED by 4.0.0_SA_CRO on 08-20 ("a phantom against finished work") with stability_frame :120 + sibling_axes/identity_source :204-205 VERIFIED present on origin. NOTHING owed by the released CRO base; no re-spawn. Residual: the as_of_universe comment corrected @e174e63961 (CTO). TO-D3.2 stays GATED on the D2 flip (P1 green = the P1.5 re-grade, unreached; P3 downstream). || PRIOR: pending -- DELIVERED @1914fa3fd6, proof VALID rc=0, coverage-checked D3.1-1..D3.1-6. Contract RATIFIED by CTO as authored and status flipped @b513a7fdbd. U1 ANSWERED (complete 1:1 edge, PRD 4.2 unblocked). D3.1-6 AUTHORED + routed to CRO -- infra/system/** is outside the DS lane and the ontology lock-down puts definitions with CRO; flips on their landing. Terminal status left to COO.</status>
<priority>P1 -- precondition for the whole D3 chain AND its residual enum gates D6's TO-G</priority>
<authority>D3_ACCOUNT_MODEL_OVERLAY_PRD.md §4.1 + §6 item 1 at dispatch vintage @52a85baf08 (CVO verdict @3e5038ebd3, ACCEPT 0 P0). Placement: LAPTOP -- the PREFER-SITEZ export exception for this row is RETIRED per CTO's final placement ruling 193804Z.</authority>
</task_order>

## Objective
Author the SMARTX_BD_EXACT_JOIN spec, census the residual, and locate the U1 model-identity edge at
source (opal-smartx-ingestion-pipeline + the 0824 silver schemas).

## YOUR RESIDUAL ENUM IS A LOAD-BEARING EXPORT — D6 CONSUMES IT
This is not a D3-local artifact. D6's TO-G (the entity-resolution service) GATES on this TO's
residual ENUM specifically, and TO-G's disambiguation classes are DRAWN FROM it — one residual
vocabulary for one identity plane. CTO's ruled reason: a resolver built before the enum lands would
assign confidence over a universe whose residual is unclassified, making "unresolvable" and
"resolvable-but-in-the-residual" indistinguishable. Author the enum as a public contract, not as
working notes.

## Mandate
- Phase 1: re-run the a06 coverage read; enumerate residual sets WITH DENOMINATORS.
- Phases 2/3: n/a — document + spec deliverable.
- Bucket discipline: 08242234 = MDPF Model Portfolios. Write the FULL 8-digit account, never the
  4-digit prefix — the truncated form is what makes the two Schwab buckets confusable.

## Acceptance criteria
- D3.1-1 RESIDUAL ENUM IS MECE — mutually exclusive, collectively exhaustive (Rule 24(i)), at ONE
  grain (24(ii)), serving ONE intent (24(iii)), with the stability frame named (24(iv): say which
  values move together under one remedy and which do not).
- D3.1-2 EVERY NON-JOINING ACCOUNT CLASSIFIED against a printed denominator — accounts examined,
  not only accounts that failed to join.
- D3.1-3 U1 ANSWERED WITH file:line @ commit — a vintage-bearing citation. A line citation without
  a vintage is not a citation; it resolves at every vintage, to different code. U1's owner is INSIDE
  this TO (§7 Q1: no Andrew input needed).
- D3.1-4 THE ENUM IS PUBLISHED AS A CONSUMABLE CONTRACT at a stable path, and the report NAMES
  D6/TO-G as a downstream reader so the coupling is visible from both ends.
- D3.1-5 proof instance VALID rc=0 positional: ids D3.1-1..D3.1-5. MEASURED/RULED-class run rows
  only; INFERRED-class expected values are mechanically ineligible.

<proof_of_spec>
  <expected_criteria>D3.1-1,D3.1-2,D3.1-3,D3.1-4,D3.1-5,D3.1-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D3_MODELOVERLAY.TO-D3.1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Reporting
COO at spec-drafted and at enum-published; cc CTO (the enum is a cross-package contract). Session
log w/ Compiler Tools section = deliverable.

---
## ⚖ TAXONOMY-OWNER RULING — 2026-08-19 ~20:45Z (4.0.0_SA_CRO~A, answering a call COO routed)

**A SECOND identity-plane vocabulary now exists**: `identity_source` (`bd-allocation | fam-carried |
fam-live | bd-householding`), emitted by `ADVI_IDSPINE.WP-3` over the **BD <-> Schwab** spine.
**Your residual enum is over the SmartX <-> BD join.**

**RULED: DO NOT MERGE. DO RELATE — via REGISTRATION, not via schema.** They are different AXES under
Rule 24(iii): **yours classifies JOIN-RESOLUTION DISPOSITION** at the SmartX-BD pair grain (*why did
this pair not resolve*); **WP-3's classifies ATTRIBUTE PROVENANCE** at the account-attribute grain
(*which layer answered this field*). Forcing them onto one axis would put disposition and provenance
together — the exact foundational break Rule 24(iii) names.

**Value-level convergence is LEGAL and needs no coordination** — both may carry a `bd` value. Values
converging under distinct axes is normal; **axes merging is the defect.**

### ADDED ACCEPTANCE CRITERION
- **D3.1-6 REGISTER THE AXIS IN `SYSTEM_DEFINITIONS`** (the ratified term registry; served by
  `comp-estate --definitions`), carrying the **axis-intent + grain declaration** per the Cascade
  entry law, **and an explicit CROSS-REFERENCE naming `identity_source` as a
  SIBLING-ON-THE-IDENTITY-PLANE.** This is what makes the two-enum state **DECLARED rather than
  latent** — it satisfies CTO's TO-G condition and gives the next seat a MAP of the plane's
  vocabularies instead of a collision to discover.
