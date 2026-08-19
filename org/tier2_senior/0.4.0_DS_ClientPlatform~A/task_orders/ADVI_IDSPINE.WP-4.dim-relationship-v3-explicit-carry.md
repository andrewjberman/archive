# TO ADVI_IDSPINE.WP-4 — a01 / `dim_relationship` v3: consume the carry EXPLICITLY (LAPTOP; UNGATED)

<task_order id="ADVI_IDSPINE.WP-4" project="ADVI_IDSPINE">
<issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:45Z</issued>
<dated>startable NOW -- depends on NOTHING (deliberately independent of WP-1..3)</dated>
<status>staged -- GO paired; UNGATED and independent</status>
<priority>P1 -- it is the leg that makes the fam carry HONEST rather than silent</priority>
<authority>SPEC_IDENTITY_SPINE_FAM_RESOLUTION_20260819.md §2 Layer 2 + §4 WP-4. Placement: LAPTOP, routed to ~A as the a01/runner-chain owner (DS base already carries WP-1/WP-3 plus the heaviest open load in the estate -- deliberate distribution, not default).</authority>
</task_order>

## Objective
`dim_relationship` (a01) v3 keeps its job at the **PER-TAXPAYER HOUSEHOLD GRAIN** and covers the
**1,925-account custodial tail**, sourced from fam **carried-as-of 2026-08-07** — with the carry
**LABELLED**, and **auto-heal preserved** for Schwab resumption.

## THE POINT: A CARRY THAT DOES NOT SAY IT IS A CARRY IS INDISTINGUISHABLE FROM FRESH DATA
The carry is **ruled and legitimate**. What makes it safe is the label. `identity_source` =
`fam-carried` + `source_as_of` on every row it answers, so a consumer can see which layer answered
and how old it is. **Without the label, a stale household attribution renders exactly like a current
one** — and nothing downstream can tell.

**Grain, per Rule 24:** fam `col_6` nests INSIDE BD relationships at 96.8% — a **consistent
hierarchy at a finer grain**, not a competitor. `dim_relationship` keeps the household grain;
`dim_account_identity_bd` (WP-3) keeps account grain; **both are kept because they are different
grains that nest.** Do not collapse one into the other.

**PII law:** fam `col_6` is TIN-shaped — **grouping-only, hashed anchor emitted.** a01's existing
law, unchanged.

## Acceptance criteria
- **WP4-1 BUILD SUCCEEDS ON THE CARRIED PARTITION WITHOUT A FRESH FAM.** This is the whole point —
  demonstrate it, because today the build's dependence on a live fam is exactly what R was blocking.
- **WP4-2 THE CARRY LABEL IS PRESENT** on every row it answers (`identity_source=fam-carried` +
  `source_as_of`), and is visibly distinguishable from a live-fam row.
- **WP4-3 AUTO-HEAL EXERCISED ON A SYNTHETIC FRESH PARTITION** — feed it a fresh partition and show
  it heals and re-labels. **An auto-heal path that has never been made to fire is not a feature, it
  is a hope**; R-WATCH already reads the frontier, so the trigger side is covered — this criterion
  is about the build's own behavior.
- **WP4-4 TAIL SCOPE DECLARED** — the 1,925-account custodial tail stated as a declared scope with
  its count, not implied.
- **WP4-5 proof instance VALID rc=0 positional: ids WP4-1..WP4-5.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>WP4-1,WP4-2,WP4-3,WP4-4,WP4-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~A/deliverables/ADVI_IDSPINE.WP-4_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- **Do not retire, delete, or stop consuming fam.** Dormancy is never a deletion warrant; the carry
  is ruled; Layer 3 (whether BD householding replaces the tail) is WP-6's conditional and terminates
  at Andrew's word.
- Do not widen any served universe. The 868 BD-only + held-away accounts stay OUT of Schwab-derived
  AUA and IN the printed subclasses (Andrew's denominator ruling).

## Reporting
COO at built, cc CRO~A. Session log w/ Compiler Tools section.
