# TO OPAL_ADVIPOINTERS.P3-CLOSE-49F — the copy root IS the live root; dim_security/dim_boundary move into the scheduled chain (push plan §3 row 3)

<task_order id="OPAL_ADVIPOINTERS.P3-CLOSE-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.4.0_DS_ClientPlatform~A (runner lane)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>2026-08-20 — after the first unattended P2 cycle (the 08-20 morning write is the evidence source). Sequenced behind P2-FLOOR + P2-DISPATCH; if P2 slips this slips WITH it in writing, never silently.</dated>
<status>pending -- GO received 160631Z; prep may start now, close evidence from the 08-20 scheduled run</status>
<priority>P1 — closes production-bar criterion (i) for the last two session-act producers</priority>
<authority>Push plan @a2f27c8d0a §3 row 3; PRD §5.D.11 (dim_security/dim_boundary: location correct, producer still a session act). CTO attests the close.</authority>
</task_order>

## Objective
Attest P3-closed for 49F: every table's newest partition at the canonical root written by the
SCHEDULED stage (not a session act), including `dim_security`/`dim_boundary` whose producers you fold
into the scheduled chain.

## Compiler tools (three-phase)
Phase 1: `comp-pipescript io a02_dim_boundary --pipeline bd` + same for a03_dim_security — expect
consumers enumerated; if a portal consumer appears flag COO (unexpected blast). Phase 2: commit-gate.
Phase 3: `comp-pipescript deployed` MATCH for both moved producers.

## Cross-domain coordination
- shared_resource: `opal-data-assets/portal/gold/advi/49financial/{canonical,dimensions}/**` — also in
  P2-DISPATCH (the chain writes it), P4-EMIT (DS~B reads it). Your change adds the two dims to the
  SAME scheduled chain — MCP AE if the entrypoint stage list changes after P2D-4's contract was
  delivered (AE's schedule references it).

## Acceptance criteria
- P3C-1 DIMS SCHEDULED: dim_security + dim_boundary producers execute inside the scheduled chain
  (entrypoint stage list cited at commit; the S3 default path is the only path — any `--*-local`
  override never used in the scheduled invocation, stated).
- P3C-2 LIVE LISTING: for EVERY table in the chain (denominator printed), the newest `date={D}`
  partition at `portal/gold/advi/49financial/` == T-1 per the trading calendar
  (`lib/trading_calendar.py` frontier — NEVER wall-clock), and its manifest identifies the scheduled
  run (run id / trigger source in the manifest), not a session act.
  **SCOPE PINNED (COO amendment 17:00Z, from DS~B's 165804Z readiness facts): "every table in the
  chain" INCLUDES the D-fleet exact-read inputs that today have NO S3 home at the product root —
  `canonical_positions` (b01's output, absent from canonical/) and the A_07 pair
  (`dim_asset_classification` + `alias_key_expansion`, today session-local only). A P3 close on
  which the publisher's own inputs are still session acts fails criterion (i) in the exact shape
  this TO exists to end — the two named tables persist at the root from the scheduled stage before
  the close is attested. d05/d06 read them (DS~B's measured list); if landing them forces a
  pattern-spec grammar question, that goes to CTO, not decided here.**
- P3C-3 ZERO FIRM-BUCKET SILVER READS: measured over the chain's source set — grep/AST count of reads
  against non-canonical silver homes = 0, with the file+line denominator printed beside it.
- P3C-4 proof instance VALID rc=0 positional: ids P3C-1,P3C-2,P3C-3,P3C-4.

<proof_of_spec>
  <expected_criteria>P3C-1,P3C-2,P3C-3,P3C-4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/OPAL_ADVIPOINTERS.P3-CLOSE-49F_PROOF_OF_SPEC~A.json</instance_path>
</proof_of_spec>

## Do not
- Do not tear down the old root (P3 copies and repoints; P5 tears down — NEVER#3 on served keys).
- Do not "fix" a stale partition by an ad-hoc production write — the scheduled run is the production
  path; an ad-hoc artifact is never production evidence.

## Reporting
COO (cc CTO, MSTR) with the live listing at close. Surprise channel: one banked line to COO.
Session log with Compiler Tools section = explicit deliverable.
