# TO OPAL_ADVIPOINTERS.P1-CLOSE-49F — D-fleet inventory (EMITTED-with-instance / DECLARED-GATED) + the backfill DETERMINATION + priced card (push plan §3 row 1)

<task_order id="OPAL_ADVIPOINTERS.P1-CLOSE-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.4.0_DS_ClientPlatform~A (runner lane; POD4 enumerated)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>2026-08-19 — the P1-close date for Advisor Intelligence / 49 Financial / Schwab 08335338. Start NOW (GO paired with this commit). A slip is re-dated in writing, never silent.</dated>
<status>staged -- GO sent same window; flip to pending on receipt</status>
<priority>P1 — phase-close gate for the whole push: P2 opens on P1 close (framework law)</priority>
<authority>Andrew-direct 2026-08-18 ~1500Z (49F end-to-end push, whole fabric, NOW) + CTO push plan @a2f27c8d0a §3 row 1. Close criterion is CTO-attested — your deliverable is the evidence table, CTO attests.</authority>
</task_order>

## Objective
Close P1 for 49F: produce the attestation table over the D fleet (every family EMITTED-with-instance
or DECLARED-GATED with a NAMED blocker), determine what backfill actually REMAINS (your 154051Z
grounded read is folded — see P1C-2), and hand CVO the table for the parity sweep the same day.

## Context
You hold the reinstantiation pack (plan §4). Census = `data/assets/scripts/gold/runners_49f/d00_census_out.json`
(census_version ...-r8d, families=104, legs=3). Spine backfill ledger CLOSED @61d9600bf2 (fill-2
2,103/2,103 zero failures; twr_daily 525 REAL partitions) — VERIFIED by COO this session against git.
The 49F `dim_relationship` two-writers defect is FILED-not-fixed @c127712198 — carry it in the table
as the named blocker where it gates a family; do not fix it under this TO. CVO holds 9/17 BAR-CLEARED,
8/17 SCOPE-VALIDATED (their 154146Z input; residuals P3/P4-phase by declaration).

## Compiler tools (three-phase)
Phase 1 (before write): `comp-pipescript io d00_served_shape_census --pipeline bd` — expect: consumers
listed, no COLUMN GAPS on census inputs; if mismatch flag COO. Phase 2 (before commit): commit-gate
automatic. Phase 3 (after): `comp-validate` on any emitted artifact (NO_CONFIG = say so in the log,
never signal SAFE on it).

## Cross-domain coordination
- shared_resource: `opal-data-assets/portal/gold/advi/49financial/**` (read) — also in
  OPAL_ADVIPOINTERS.P2-FLOOR-49F (AE writes via schedule), P2-DISPATCH-49F, P4-EMIT-49F (DS~B reads).
  MCP DS~B + AE before any write into that root.
- shared_resource: the D-family inventory table — consumed by CVO P1-SWEEP-49F same day. CVO is the
  reader; commit first, then MCP CVO the commit hash (commit-first handoff form).

## Acceptance criteria
- P1C-1 INVENTORY: attestation table committed under your deliverables/ — one row per D family from
  the run-8d census (print the family denominator you enumerated over), each row EXACTLY ONE of:
  EMITTED-with-instance (instance path cited, schema-valid) / DECLARED-GATED (blocker NAMED — e.g.
  A_07-gated, billing-pending, backfill-gated-with-scope, two-writers @c127712198). A family you
  cannot classify gets its own UNKNOWN row stated as such — never silently dropped (missing-third-state
  test). Forbidden shortcut, named: re-labelling an unknown family DECLARED-GATED with a vague blocker
  ("pending data") re-commits the rot — a blocker is NAMED only if it cites the artifact/ruling that
  clears it.
- P1C-2 BACKFILL DETERMINATION: against the CLOSED spine-fill ledger @61d9600bf2, ENUMERATE (list, not
  digit) what backfill remains for the D families (candidates you named: the ~10 window/series
  families' fan-out over the now-filled spine; the V16/17/18 legs @3d8a6892d6). Each remaining item
  carries its scope (tables x dates). If the remainder is EMPTY: deliver a discharge report citing
  @61d9600bf2 + the framework CURRENT-STATE line it supersedes, routed to CTO for the plan-line
  correction — do NOT re-price the closed spine fill (forbidden shortcut, named).
- P1C-3 PRICED CARD (conditional on P1C-2 nonempty): run the timing sample ON THE REMAINING SCOPE
  (>=20 representative dates, ad-hoc QA runs per the ad-hoc-runs rule — run-and-read, nothing
  standing; rc AND wall-clock per stage printed), derive the priced fill-word card (scope x per-date
  cost = hours), deliver to COO for MSTR->Andrew. The card prices the REMAINDER, never the closed fill.
- P1C-4 CVO HANDOFF: inventory committed BEFORE the MCP; CVO receives the commit hash + the frame
  statement (see P4-EMIT-49F P4E-1 — the frozen served-key list is DS~B+CVO's; your table is at
  FAMILY grain and must SAY SO, so the two grains are never conflated).
- P1C-5 proof-of-spec instance VALID: `python .tools/proof-of-spec-check.py <instance> P1C-1,P1C-2,P1C-3,P1C-4,P1C-5`
  rc=0 taken WITHOUT a pipe (positional ids — no flags). P1C-3 row may read N/A-DISCHARGED with the
  P1C-2 evidence pointer if the remainder was empty.

<proof_of_spec>
  <expected_criteria>P1C-1,P1C-2,P1C-3,P1C-4,P1C-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/OPAL_ADVIPOINTERS.P1-CLOSE-49F_PROOF_OF_SPEC~A.json</instance_path>
</proof_of_spec>

## Do not
- Do not fix defects found during inventory (two-writers class) — FILE + name as blocker.
- Do not touch `opal-data-bd` legacy serving paths (P5 is not open; NEVER#3 on served keys).
- No shadow channels, no comparators (Andrew 08-04 veto). Ad-hoc QA runs are run-and-read.

## Reporting
COO (cc CTO, MSTR, CVO) at inventory-committed and at card-delivered-or-discharged. Surprise channel:
one banked line to COO, no chase. Session log with Compiler Tools section = explicit deliverable.
