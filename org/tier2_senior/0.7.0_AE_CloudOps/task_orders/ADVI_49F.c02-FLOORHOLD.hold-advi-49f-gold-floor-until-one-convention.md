# TO ADVI_49F.c02-FLOORHOLD — HOLD the `advi-49f-gold-floor` schedule (TF, targeted safe-apply) until `twr_daily` carries ONE gross-leg convention; lift-by TUE 2026-09-01 12:40Z

<task_order id="ADVI_49F.c02-FLOORHOLD" project="ADVI_49F">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T01:4xZ</issued>
<decomp_ref>org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md -- <owned_cells>C02-g-4</owned_cells> (C02-g-2 / C02-g-3 are the DS and AE~L halves whose landing LIFTS this hold; NOT in this TO)</decomp_ref>
<proof_of_spec>
  <expected_criteria>H-1,H-2,H-3,H-4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ADVI_49F.c02-FLOORHOLD.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json H-1,H-2,H-3,H-4 -->
</proof_of_spec>
<status>complete -- CLOSED BY THE ISSUER 2.0.0_SA_COO 2026-08-30 03:5xZ: H-1..H-4 COMPLETE. Hold applied 01:53:22Z on the measured scheduler advi-49f-gold-floor; LIFTED 03:43:53Z on the CONDITION (CVO 85167: C02-g-3 ACCEPTED, R-5 535 of 535 zero at "1.0"; issuer word 85176), the DISABLED attribute removed to restore the recorded baseline, Expression/Target/Input/FlexWindow read back IDENTICAL to the baseline captured live at the hold with State the only mover (AE base 85206); ledger 20260830T0153Z closed "Remaining open: NONE"; the TUE 12:40Z lift-by never fired. || PRIOR: ACTIVE -- prep started on 84137 (RAVC ACK 84144: TF diff DESIRED-only + ledger draft + the deployed-bytes read); APPLY on the completed never-widen sign-off (COO 84135 + CTO 84164), before 12:40Z 2026-08-30</status>
<priority>P0 -- TIME-SHAPED to 12:45Z TODAY (SUN 2026-08-30): the floor fires daily incl. weekends and today's fire overwrites served date=2026-08-28 in place with a mixed-vintage r_gross. The hold costs ZERO new data through MON (both fires re-derive D=2026-08-28); the lift-by is the first NEW date, TUE 09-01.</priority>
<authority>CVO 84079's fallback ("the HOLD goes on the c02 DISPATCH specifically, never on bd-49f-fees-session-daily as a whole"); DS~N 84104 measured executor + schedule + overwrite; never-widen sign-off COO 84135 + CTO 84164; Andrew's LD-0477 A2 word ruled the ROLLBACK, not the range, and this hold costs no new data through Monday so it does not contradict it. Cell C02-g-4.</authority>
</task_order>

## READ THIS FIRST — the decomp cell is the specification

**`org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md`, cell `C02-g-4`** — the measured time-shape, the domain (ONE schedule's State, nothing else), the four criteria, and the lift condition. **This face does not restate it.** Where the two differ, the cell governs; tell the issuer.

## Acceptance criteria — H-1 through H-4, verbatim from cell `C02-g-4`

<criterion id="H-1" cell_refs="C02-g-4"/> **READ BEFORE HOLD.** Deployed bytes of `advi-49f-gold-dispatch` + the SSM document's APPLIED state (a broken dispatcher moots the hold); and no surviving campaign leg on `i-01003b035d2988dfb` able to run the chain off-schedule. Both stated either way, first, read-only.
<criterion id="H-2" cell_refs="C02-g-4"/> **THE HOLD, TF-DECLARED, -TARGETED.** `advi_49f_floor.tf:279-291` State -> DISABLED; plan on the 1.9.8 shim; `safe-apply -target aws_scheduler_schedule.advi_49f_gold_floor` (the untargeted plan carries the held 08-11 emitter repoint + IAM adds AND the P2F-3b accelerator rows; precedent 76182/76186 is to target). Applied BEFORE 12:40Z today. Read back `scheduler get-schedule` State == DISABLED, not tf output.
<criterion id="H-3" cell_refs="C02-g-4"/> **LEDGERED.** `org/critical_paths/change_management/` entry opened at the apply carrying the lift condition, the lift-by, and the NAMED COUPLING: the P2F-3b accelerator (target `advi-49f-gold-dispatch`) is sequenced AFTER this hold lifts (CTO 84164 (2)). Closed at the lift with the State read-back.
<criterion id="H-4" cell_refs="C02-g-4"/> **THE LIFT CONDITION.** Lift = `C02-g-3` R-5 READ (vintage on 534 of 534, zero at "1.0") OR the hard lift-by TUE 2026-09-01 ~12:40Z, whichever first; **if the re-emission has not landed by then the hold LIFTS ANYWAY** (a missed production date is the larger cost). Same act in reverse (State ENABLED, targeted safe-apply, read-back), same seat, on the issuer's word or the clock.

## Do NOT

- ⛔ **Do not use a bare `aws scheduler update-schedule`** — it drifts from TF; the declared state must match the applied state.
- ⛔ **Do not hold, edit, or touch any `bd-49f-*-session-daily` rule** — they do not reach c02 and CVO excluded them.
- ⛔ **Do not apply untargeted** — the plan carries foreign rows (emitter repoint, accelerator) on an unrelated authorisation.
- ⛔ **Do not edit the entrypoint** for a c02-only skip — wider than the hold, under an 11h clock.
- ⛔ **Do not let the hold outlive its lift-by** — the lift is the issuer's word OR the clock, whichever first; a hold with no lift is the permanent-hold class.
- ⛔ **Do not route anything on this subject to `4.0.0_SA_CRO`.**

## Lane and mechanics

- **Rule 13 infra:** `bare terraform apply` is NEVER; `safe-apply` only. `terraform fmt -check` (never `-diff`, it WRITES). Binary trap: `.tools/terraform.exe` 1.9.8 vs PATH 1.14.5 — safe-apply refuses a cross-version plan file.
- **NEVER-2:** the deploy-ledger entry is opened at the apply and closed at the lift, in-session or escalated loud; an entry left OPEN across a session end is measured, never re-executed (world-done -> SUPERSEDED).
- Report the apply with `scheduler get-schedule` State read back; report the lift the same way.

## What is owed back, and when

H-1 first (read-only; can moot the rest). Then the apply read-back to `2.0.0_SA_COO` + `1.0.0_SA_CTO` before 12:40Z — **that message is what consumes drive-pair ledger row 17.** Then, on `C02-g-3` R-5 or the lift-by clock, the lift read-back to the same two seats and `3.0.0_SA_CVO`.
