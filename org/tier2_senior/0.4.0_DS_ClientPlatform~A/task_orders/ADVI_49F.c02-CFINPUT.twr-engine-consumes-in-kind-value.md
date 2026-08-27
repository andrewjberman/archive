# TO ADVI_49F.c02-CFINPUT — the TWR engine's cash-flow INPUT SELECTION (LAPTOP; MON, drive-to-EXACT first act)

<task_order id="ADVI_49F.c02-CFINPUT" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T21:47Z</issued>
<dated>MON 2026-08-24 -- the drive-to-EXACT loop's FIRST ACT</dated>
<status>complete -- COO FLIP 2026-08-27 ~19:5xZ on the full three-instrument chain: seat evidence (implemented @cab1f8bff9, deployed-verified @21170203c5, 5-of-6 honest scoring 76467) + issuer RAVC-4 (76474) + CVO completion read PASS @7464585f22 (validator independent, rows=6, TRUE rc bare). **CF-2 CLAUSE 2 IS OPEN-AND-CARRIED, not satisfied**: the "SI ties BD in-band" read on the original 2026-03-24 specimen needs the backfilled history and is consumed by the P1.5 re-grade per the V14-3 ruling @c65ceb968a; 2026-03-24 stands UNMEASURED-PRE-BACKFILL, owed by the P14 pass. "Complete" here means: every criterion is either evidenced or transferred with a named carrier and verifier -- the record teaches exactly that. PRIOR LINE PRESERVED BELOW (issuer refresh 2026-08-27 ~19:0xZ on AE~L 76425 / CTO 76429; both prior halves were stale-restrictive): c00-FIX gate SATISFIED (complete @6e13cba4ee). Implemented @cab1f8bff9; harness-verified to the reachable bound, proof instance VALID rc=0 @6523480924 over the 6-id set. CF-4 gate PASSED-TO-DEPLOY (CTO 76421, four conditions), deploy in progress at 0.4.0_DS_ClientPlatform~U. AT DEPLOYED-VERIFIED the executing seat APPENDS to this line: "DEPLOYED-THROUGH-CF-4 @<deploy-evidence-hash>" -- the exact token the P14-VEHICLE unlock read acts on (a bare "complete" would not tell that reader the CF-4 clause was satisfied). CF-2 clause 2 OPEN post-backfill; CF-5 finalizes at deploy. DEPLOYED-THROUGH-CF-4 @21170203c5 -- appended 2026-08-27 by 0.4.0_DS_ClientPlatform~U at deployed-verified, issuer-authorized COO 76439/76442. All four CF-4 conditions met: scope one file; basis re-verified at deploy time on three planes each with its own positive control; post-deploy identity by LF-normalised content against the committed build input (S3 3ff237d8364296d7 == commit cab1f8bff9, parent 1c270beda617b07c DIFFERING) after the CRLF trap fired on the raw compare; no serve, no flip, no backfill.</status>
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
- **CF-3b THE PAIR-SCAN (issuer amendment 2026-08-27 ~18:1xZ, on CTO ruling 76330 — NON-GATING,
  runs beside or after CF-3 full scope, never blocks it):** the cross-account pair-scan over
  code-rule INTERNAL in-kind legs — same day, same CUSIP, opposite-direction quantity in ANOTHER
  account's ledger. Rows where the scan ESTABLISHES a counterparty graduate into the admitted set
  through the EXISTING pair-match provenance (zero new principle; the one-line
  INTER_ACCOUNT_PROVENANCE mechanism untouched). Unestablished rows stay EXCLUDED,
  refused-BY-REASON in the census, **and the P1.5 re-grade report CARRIES the residual's per-day
  dollar size with its denominator** so the arm-(a) serve read is made with the number in view —
  materiality at the serve gate is Andrew's judgment, never a silent drop.
- **CF-5 proof instance VALID rc=0 positional: ids CF-1,CF-2,CF-3,CF-3b,CF-4,CF-5** (widened from
  CF-1..CF-5 by this amendment; disclosed to `3.0.0_SA_CVO` for delta-cert, the RPS 5->7 form).
  MEASURED/RULED-class run rows only. Cite the expected-id set the checker ran against — a bare
  rc=0 does not establish positional coverage.

<proof_of_spec>
  <expected_criteria>CF-1,CF-2,CF-3,CF-3b,CF-4,CF-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~U/deliverables/ADVI_49F.c02-CFINPUT_PROOF_OF_SPEC.json</instance_path>
  <!-- instance_path re-pointed ~A -> ~U by issuer 2026-08-27 ~18:3xZ (76355 question): the executing
       seat is ~U per the SEATING-EXECUTED block; the ~A path was a fossil of the historical face.
       Beside the seat's c01 instance, one deliverables home per seat. -->

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

---
## ⚖ COO RECONCILIATION 2026-08-27 (P0.2 record pass, D2 brief @e4f7ecbfdc) — **ABSORBED into the ruled 08-26 remediation design; face re-based BEFORE any GO**

Verdict: **ABSORB.** The need stands (this TO IS brief phase P1.2), but two clauses above predate
the 08-26 rulings and would point a fresh seat at a design CTO ruled OUT (74187) — the exact
superseded-plan-in-a-live-artifact class DS~U corrected in their own record @69b2b7678c.

**MECHANISM RE-BASED (supersedes the Objective + CF-1 wording above where they differ):**
- `in_kind_value` **KEEPS its unsigned contract** — do NOT re-sign in place, do NOT have c02 consume
  it raw. The ruled design: a **NEW SIGNED FIELD** lands in `flow_ledger` (c00/c01 plane, with c01's
  deliberate defect-3 sign-branch fix @07bcdafb2b carrying its own acceptance), and **c02 consumes
  the new signed field via the grain-parameterized filter**. Root cause record @ea7c227a24; ruled
  design end-to-end in DS~U's corrected artifact @69b2b7678c.
- CF-2 (harness re-read = acceptance), CF-3 (magnitude distribution), CF-4 (no silent re-statement,
  P4-class through CTO) **stand unchanged**.
- The "Do not re-value HISTORY here" exclusion is **RESOLVED, not deleted**: the backfill is now
  RULED as **ONE full-chain entrypoint-driven pass over the 531 partitions covering
  {c00 -> c01 -> c02 -> dependent c04} + nna_canonical** (brief P1.4), a separate TO carrying its
  two pre-measured hazards: no stage-scoping exists (@f62e93b9bb) + the SSM `--date` vehicle gap
  (@4da71d969b, `--date D --upload`, direct send, never via the dispatcher Lambda — halt trap).
- Pre-registered acceptances for the chain: the all-ten table @4a1fd3e09b + the NNA delta table
  @e8ccd8eb77. The backfill's own writes take the named ad-hoc/backfill boundary (74218); the
  verification fire does NOT.

**SEATING — EXECUTED 2026-08-27 ~15:2xZ:** re-pointed to **`0.4.0_DS_ClientPlatform~U`** per
Andrew's serialed seat word @1d761ded1f (the original `<issued_to>` above is superseded by this
block; the file stays in the ~A folder as the historical face — `issued_to` here is the truth, file
location never is). Gated on `ADVI_49F.c01-SIGNFIELD` (the new signed field is this TO's input;
the c00-FIX gate above is SATISFIED — complete @89204884d7). Status `staged`; GO pairs AFTER
3.0.0_SA_CVO cert step-zero + spawn confirmation (D2 lock-in, CVO 76086).

**D2 LOCK-IN RIDER (CVO 76086 point 1) on CF-5:** the proof instance is validated BY RC (never an
output string), and the validator invocation + its TRUE rc are recorded as evidence IN the
instance.
