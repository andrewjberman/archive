# TO ADVI_IDSPINE.WP-5 — consumer re-point: ADVI book figures partition on PRIMARY GROUP (P4-class, CTO gate)

<task_order id="ADVI_IDSPINE.WP-5" project="ADVI_IDSPINE">
<issued_to>0.4.0_DS_ClientPlatform~B + 0.4.0_DE_ClientPlatform; 1.0.0_SA_CTO gates (P4-class)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:45Z</issued>
<dated>on WP-2 (= T2-DIMS) + WP-3 + CTO ratification</dated>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "ADVI_IDSPINE" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged -- GATED ON WP-2/WP-3 + CTO RATIFY. P4-class: served semantics move here.</status>
<priority>P1 -- this is where the group-based book ruling actually reaches a served figure</priority>
<authority>SPEC_IDENTITY_SPINE_FAM_RESOLUTION_20260819.md §4 WP-5 + the Andrew ruling 2026-08-19 ~20:12Z (book = GROUP-BASED). Placement: LAPTOP; routed to ~B as the dims owner (they hold T2-DIMS and T1-ORACLE, so the producer and its re-point sit together).</authority>
</task_order>

## Objective
Re-point ADVI book figures to partition on **PRIMARY GROUP** (`bridge_group_account.is_primary`),
with roles retained as an **attribute view**.

## SEQUENCE WITH THE ORACLE YOU ALREADY HOLD — DO NOT DUPLICATE IT
**`ADVI_BDPARITY.T1-ORACLE` is the book tie-out oracle** (qt6 group-grain) and it is at your seat.
**T1-ORACLE MEASURES; WP-5 RE-POINTS.** Run the oracle first and use it as WP-5's verification
instrument — do not build a second tie-out inside this TO. One oracle, one re-point.

## NEVER SUM ACROSS GROUPS — AND IT MUST BE STRUCTURAL, NOT DISCIPLINED
90.6% of accounts are multi-member **by design**, and a naive membership sum measured a **$10.2B
phantom on a ~$1.77B book.** Aggregations join through **`is_primary=true`** unless a view
EXPLICITLY wants membership scope. **The bridge table is what makes this structural** — a
cross-group sum should be inexpressible, not merely avoided.

## SERVED-SEMANTICS DISCIPLINE (this is why it is P4-class)
- **CTO ratifies before anything served moves.** The book ruling authorizes the BASIS; it does not
  bypass the gate.
- **Per-key never-widen sign-off where served keys move** (NEVER#3). A verified DELTA=0 deploy needs
  no hold — but the verification is the price of skipping it.
- **The basis is STAMPED** into every served artifact, so a future basis change is visible rather
  than silent.

## Acceptance criteria
- **WP5-1 SERVED LEADERBOARD REPRODUCES THE VENDOR-NATIVE BOOK NUMBER for the Travis specimen,
  within the PRE-REGISTERED BANDS.** Cite the pre-registration; do not invent a band after seeing
  the number.
- **WP5-2 SUBCLASS DENOMINATORS PRINTED ON EVERY SERVED FIGURE** — BD-covered / fam-only /
  held-away / non-8-digit (Andrew's denominator ruling; the Travis enumeration is the template).
- **WP5-3 CROSS-GROUP SUM TEST FAILS LOUD** — exercised, showing the phantom is inexpressible.
- **WP5-4 CTO RATIFICATION CITED** before any served key moves; never-widen sign-off where applicable.
- **WP5-5 BASIS STAMPED** in every served artifact touched.
- **WP5-6 proof instance VALID rc=0 positional: ids WP5-1..WP5-6.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>WP5-1,WP5-2,WP5-3,WP5-4,WP5-5,WP5-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~B/deliverables/ADVI_IDSPINE.WP-5_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Do not widen the served universe: the 868 BD-only + held-away accounts stay OUT of Schwab-derived
  AUA and IN the printed subclasses.
- Do not move a served key without the gate. Do not build a second tie-out oracle.

## Reporting
COO at ratified and at re-pointed, cc CTO (gate) and CRO~A. Session log w/ Compiler Tools section.
