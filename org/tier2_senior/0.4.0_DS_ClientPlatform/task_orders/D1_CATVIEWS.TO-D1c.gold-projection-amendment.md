# TO D1_CATVIEWS.TO-D1c — gold projection amendment (LAPTOP-ONLY; gold deploy cycle)

<task_order id="D1_CATVIEWS.TO-D1c" project="MDPF_CATVIEWS">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:35Z</issued>
<dated>on TO-D1b's acceptance</dated>
<status>superseded -- by D1_CATVIEWS.TO-R1-DS (cells D1-b-1, D1-inv-3, D1-h-p2): the round-1 cut on the CERTIFIED v2 decomp (CVO @60d4e2f1b4); this pre-pipeline TO was STAGED and NEVER STARTED, so it carries no retrofitted decomp_ref. Set by the ISSUER (2.0.0_SA_COO, 2026-08-24 ~20:2xZ).</status>
<priority>P1-program</priority>
<authority>D1_ASSET_CATEGORY_VIEWS_PRD.md §4.2 + §6 item 3, at dispatch vintage @3e589fa1eb. Acceptance carries THE PARTITION FORM from CTO's taxonomy-gate ruling. Placement: LAPTOP-ONLY (gold deploy cycle: safe-deploy + S3 verify).</authority>
</task_order>

## Objective
Amend the gold projection per §4.2 to emit `category_views` — **additively.** The legacy per-firm
`non_model` field is a live EMITTED surface with downstream readers; this TO adds a block beside it
and changes nothing that already ships.

## Mandate (three-phase)
- **Phase 1:** `comp-pipescript io <script> --pipeline mdpf` (flag REQUIRED) for column gaps +
  portal consumers, then `comp-blast <fn>` for the downstream set. Read the deployed artifact, not
  only the builder.
- **Phase 2:** commit-gate; Rule 13 DS lane owns the full commit -> QA-deploy cycle via
  `.tools/safe-deploy.sh`. Rule 17 binds: this is gold-tier business logic, correctly placed.
- **Phase 3:** `comp-validate <script> --artifact <file>` + a served-artifact DIFF.

## Acceptance criteria — the partition, asserted on BOTH limbs
- **D1c-1 SMA UNFOLD:** the SMA view carries the 2 unfolded SMAs.
- **D1c-2 LEGACY BYTE-UNCHANGED:** the EMITTED legacy `non_model` field is **byte-identical**
  pre/post on every firm. Show the diff producing zero delta on that field — not "no reader
  complained".
- **D1c-3 RESIDUAL IDENTITY:** `category_views` Residual == `non_model` MINUS unfolded-member AUM,
  **with the subtracted-member list stated inside the block.** Both limbs asserted — the identity
  AND the named subtrahend. A Residual that merely looks right is not accepted; the member list is
  what makes it checkable.
- **D1c-4 SUM INVARIANT:** sum(five nodes) == total_aua **per firm**, all three firms.
- **D1c-5 SERVED DIFF:** `category_views` present in the served artifact and ALL pre-existing fields
  byte-stable. Ground on the SERVED key (Rule 22a APPLIED layer), never the builder's self-report
  and never rc=0.
- **D1c-6 proof instance VALID rc=0 positional: ids D1c-1..D1c-6.** MEASURED/RULED-class run rows
  only; INFERRED-class expected values are mechanically ineligible.

<proof_of_spec>
  <expected_criteria>D1c-1,D1c-2,D1c-3,D1c-4,D1c-5,D1c-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D1_CATVIEWS.TO-D1c_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Do not slim, rename, or "clean up" `non_model` — NEVER#3 territory the moment it reaches a served
  key, and the compatibility guarantee is the point of the partition form.
- No alert/monitor machinery (standing moratorium). A finding lands as a banked line to COO.

## Reporting
COO at deploy-verified. Report must distinguish real success from SILENT FALLBACK. Surprise
channel: one line to COO. Session log w/ Compiler Tools section = deliverable.
