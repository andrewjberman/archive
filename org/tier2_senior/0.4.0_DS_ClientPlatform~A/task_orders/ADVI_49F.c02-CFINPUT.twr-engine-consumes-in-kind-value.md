# TO ADVI_49F.c02-CFINPUT — the TWR engine's cash-flow INPUT SELECTION (LAPTOP; MON, drive-to-EXACT first act)

<task_order id="ADVI_49F.c02-CFINPUT" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T21:47Z</issued>
<dated>MON 2026-08-24 -- the drive-to-EXACT loop's FIRST ACT</dated>
<status>staged -- GO paired; gated on ADVI_49F.c00-FIX landing (its honest output is this TO's input)</status>
<priority>P1 -- it is the SECOND HALF of a defect Andrew already ruled fixed "MON at latest", not optional scope growth</priority>
<authority>CTO ruling 2026-08-19 ~21:37Z + ~21:38Z, resolving DS~A's source-confirmed scope conflict on ADVI_49F.c00-FIX. Placement: LAPTOP (49F runner/engine chain).</authority>
</task_order>

## Why this TO exists — and it is NOT scope growth
`ADVI_49F.c00-FIX` was written to accept on a harness re-read that **structurally could not move**:
DS~A source-confirmed that **`c02_twr_engine.py` never consumes `in_kind_value`** (zero occurrences;
`:19` states the design, `:128` is the only cf source, and `signed_amount` is 0.0 on IC rows BY
DESIGN per `c01:45`). So a perfect c00 fix leaves TWR **bit-identical**.

**My original TO asked for an outcome and fenced its only mechanism.** CTO ruled the split: the c00
fence HOLDS, and the mechanism opens **here**, as its own reviewed act.

**THE DISTINCTION THAT MAKES THIS RULABLE RATHER THAN FENCED:** the **LINKING METHOD IS NOT
IMPEACHED** and is not touched. What is missing is **WHICH ROWS c02 SELECTS AS CASH FLOWS.** Those
are different acts; the blanket "do not widen into the valuation chain" collapsed them — correctly
conservative when written, before the mechanism was known, and correctly split now that it is.

## Objective
`c02` cash-flow assembly **consumes `in_kind_value` on EXTERNAL IC legs.**

## Scale — read before you scope the testing
C00-2's full census (527 partitions exact, pagination-proven, 0 failed reads):
- **1,728 TWR-material accounts** carry a zero-buried EXTERNAL in-kind leg (5,427 with any IC leg).
- **515 of 527 partitions** affected.
- **NO SERVING WINDOW of any length or start date avoids an affected day** — 434 affected dates in
  serve scope, zero gaps over 7 days across 648 days.

**This is not a narrow fix.** It changes cash flows on 1,728 accounts across effectively the whole
served history, so its verification carries the weight the c00 fix did not.

## Acceptance criteria
- **CF-1 `c02` CONSUMES `in_kind_value` ON EXTERNAL IC LEGS** — row selection only. **Cite the
  linking method as UNTOUCHED**, with the diff showing it.
- **CF-2 THE HARNESS RE-READ IS THIS TO's ACCEPTANCE** (moved here from c00-FIX's C00-4, never
  deleted — it is CRO~A's matched-window harness): **the +341% specimen day re-reads ~0%, and SI
  ties BD in-band.** This is the movement c00 could not produce and this TO must.
- **CF-3 MAGNITUDE IS NOW MEASURED, NOT ASSUMED.** The census COUNTS affected accounts; it does not
  measure per-account TWR error. **This TO produces the magnitude distribution across the affected
  class** — the +341% specimen proves the error CAN be severe, not that it is severe everywhere, and
  the declaration currently says exactly that. Close that gap with numbers.
- **CF-4 NO SILENT RE-STATEMENT.** Served TWR values will CHANGE for affected accounts. That is the
  point — but it is a served-semantics change on 1,728 accounts, so it routes **P4-class through
  CTO** with per-key never-widen where served keys move. **A correction shipped silently is
  indistinguishable from a regression.**
- **CF-5 proof instance VALID rc=0 positional: ids CF-1..CF-5.** MEASURED/RULED-class run rows only.
  Cite the expected-id set the checker ran against — a bare rc=0 does not establish positional
  coverage.

<proof_of_spec>
  <expected_criteria>CF-1,CF-2,CF-3,CF-4,CF-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~A/deliverables/ADVI_49F.c02-CFINPUT_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- **Do not touch the LINKING METHOD.** It is not impeached and it is not in scope. Row selection only.
- **Do not start before c00-FIX lands** — this consumes c00's honest output; running it against
  zero-buried input measures the old defect.
- **Do not re-value HISTORY here.** The historical re-valuation (526 partitions, the a03 + b01
  backfill legs) is a **BACKFILL-PROGRAM decision**, scoped at the MON census with cost/benefit
  framed, and **Andrew's word if it carries real cost.** Separate item.

## Reporting
COO at implemented and at harness-verified; **cc CTO (the P4 gate) and CRO~A (harness owner).**
Session log w/ Compiler Tools section = deliverable.
