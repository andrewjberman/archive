# TO ADVI_49F.P14-VEHICLE — the backfill VEHICLE (SSM `--date`) + host mechanics for the ruled 531-partition pass (LAPTOP; P1.4)

<task_order id="ADVI_49F.P14-VEHICLE" project="ADVI_49F">
<issued_to>0.7.0_AE_CloudOps~L</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-27T15:2xZ</issued>
<status>pending -- GO received 2026-08-27T160935Z (COO msg 76134); vehicle legs V14-1/V14-2 UNGATED and in progress; execution legs held at V14-3</status>
<priority>P1 -- the ruled backfill (brief @e4f7ecbfdc P1.4) has NO vehicle today; vehicle work is ungated, execution is gated</priority>
<authority>The ruled 08-26 remediation design (@69b2b7678c); the assignee's own measurements @4da71d969b (--date vehicle gap) + @f62e93b9bb (no stage-scoping) + 74209 (dispatcher-halt trap, safe-default parameter); 74218 (the named ad-hoc/backfill boundary, ~U concurrence). Andrew-direct seat word 2026-08-27 ~15:0xZ @1d761ded1f.</authority>
</task_order>

## Context — this is YOUR plane, re-seated
This seat re-instantiates the 0.7.0_AE_CloudOps~L publisher/backfill context. Every hazard this TO
names was measured by this lane before the drawdown; the TO exists so the ruled loop has a vehicle
and the hazards cannot be re-discovered the hard way mid-loop.

## Scope
1. **THE VEHICLE (ungated, first act):** `advi-49f-chain-dispatch` today hardcodes
   `python3 chain_49f_entrypoint.py --production` and can express no historical date. Parameterize
   it (or mint a date-taking variant per the Build Ladder — minimum change that works): rendered
   command for a historical run is **`--date {{Date}} --upload`**. `--production` is PROHIBITED for
   historical runs — it derives T-1 and would run the SAME date 531 times, every iteration green.
2. **DRIVER MECHANICS:** the driver ensures the host running ONCE, sends `ssm send-command`
   DIRECTLY with `StartedByDispatcher` omitted (defaults `"false"`, the safe path), and halts the
   host ITSELF once at the end. **NEVER route through `advi-49f-gold-dispatch`** — the Lambda sets
   the parameter itself and would halt the host after date 1 of 531.
3. **THE EXECUTION (gated on `ADVI_49F.c01-SIGNFIELD` + `ADVI_49F.c02-CFINPUT` landing):** ONE
   full-chain entrypoint-driven pass per affected date over the ruled set
   {c00 -> c01 -> c02 -> c04 dependents} + `nna_canonical` — full chain per date because **no
   stage-scoping exists** (@f62e93b9bb); do not build stage-scoping to avoid it (Build Ladder /
   YAGNI — the full chain is the ruled form).
   <!-- BANKED 2026-08-27 by 0.7.0_AE_CloudOps~L on 0.4.0_DS_ClientPlatform~U 76340, relayed by
        2.0.0_SA_COO 76342 ("bank it beside the D-1-pull rationale"). A SECOND, INDEPENDENT reason
        the full-chain form is load-bearing, measured on a DIFFERENT instrument than the first:
          reason 1 (D-1 pull): _pull_prev_valuation_into_mirror lives in main(), not _stage_list, so a
            stage-scoped driver would write 531 all-refused partitions GREEN.
          reason 2 (input availability, ~U's partition census): the A/B-plane inputs DO NOT EXIST over
            history -- fact_trn 538, canonical_valuation 533, flow_ledger 533, twr_daily 532, but
            ref_txn_classification 7, canonical_positions 7, dim_boundary 8, dim_calendar 8. A
            stage-scoped backfill would FAIL OUTRIGHT on historical dates, not merely emit refusals.
            The full chain re-mints those planes via a00-a07 and b00-b03 before c00 runs.
        CONSEQUENCE FOR ANY FUTURE READER: the 531 denominator is unaffected and WHICH scripts the pass
        runs is unchanged -- but the a0x/b0x re-mint is LOAD-BEARING, not incidental. Trimming stages
        off this loop trims the thing that makes the loop possible. Two independent instruments now
        agree, so this is corroboration rather than repetition. -->
4. **STANDING OF THE WRITES (74218, state it in every report):** the backfill's OWN writes take the
   named ad-hoc/backfill boundary — they repair history the scheduled path produced wrongly and
   BECOME production history. The step-(4) verification fire stays a QA instrument and is NEVER
   production evidence. Two `--date` invocations, different standing; conflating them is the
   named failure.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam service advi-49f-chain-dispatch</run>
      <expect>Action-level grants for the SSM path enumerated. NECESSARY, NOT SUFFICIENT (action-grain only): for any NEW resource ARN touched, verify on the live primitive with aws iam simulate-principal-policy, ONE --resource-arns per call, positive control as a SEPARATE invocation.</expect>
      <if_mismatch>STOP. A missing grant surfaces to COO before any document edit.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript postdeps chain_49f_entrypoint --firm bd</run>
      <expect>Downstream consumer set of the chain's writes enumerated (flagless silently defaults bd -- the flag is stated deliberately). No consumer outside the ruled backfill set's read plane.</expect>
      <if_mismatch>STOP. An unlisted consumer inherits re-emitted history -- surface to COO.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-iam gaps</run>
      <expect>Run ONLY if iam.tf changed: no new permission gaps. If iam.tf unchanged, record that fact -- the run is then N/A by its own trigger rule.</expect>
      <if_mismatch>STOP. Do not commit an IAM change with open gaps.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>aws ssm get-document --name advi-49f-chain-dispatch (or the variant) # rail-checked: live-document APPLIED-state read, no comp-tool reads live SSM document content</run>
      <expect>The LIVE document carries the date parameter with its allowedPattern and the rendered --date {{Date}} --upload form. DESIRED (tf/source) is not APPLIED -- this read is the acceptance substrate, not the tf diff.</expect>
      <if_mismatch>STOP. The vehicle does not exist until the live document says so.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

## Acceptance criteria
- **V14-1 VEHICLE LIVE:** the LIVE SSM document (get-document read, APPLIED state) accepts a date
  parameter and renders `--date {{Date}} --upload`; `--production` absent from the historical path.
- **V14-2 HALT TRAP RULED OUT BY EXERCISE:** >=2 consecutive direct sends on a control date with the
  parameter omitted; host stays up across both (read from instance state, not send rc).
- **V14-3 GATE HONORED:** zero backfill execution before c01-SIGNFIELD + c02-CFINPUT land — the
  dependency block below is the record.
- **V14-4 EXECUTION COVERAGE:** every affected date driven; DENOMINATOR PRINTED (n of 531 at the
  ruled count — re-derive the affected set at execution time, never copy 531 as a constant);
  per-date completion read from produced artifacts, never rc; failures enumerated by date.
- **V14-5 ACCEPTANCE RE-READS GREEN (joint with 0.4.0_DS_ClientPlatform~U):** the all-ten table
  @4a1fd3e09b + the NNA delta table @e8ccd8eb77 re-read against the backfilled history.
  0.4.0_DS_ClientPlatform~U validates; this seat produces.
- **V14-6 proof instance VALID rc=0 positional: ids V14-1..V14-6**, validated BY RC (never an
  output string), the validator invocation + its TRUE rc recorded as evidence IN the instance
  (D2 lock-in, CVO 76086 point 1).
- Session log with Compiler Tools section reproducing every `<run>` + observed result + pass/fail
  vs `<expect>`. Missing rows = REWORK.

<proof_of_spec>
  <expected_criteria>V14-1,V14-2,V14-3,V14-4,V14-5,V14-6</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~L/deliverables/ADVI_49F.P14-VEHICLE_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<dependencies>
  <!-- COO clarification 2026-08-27 ~16:1xZ on 0.7.0_AE_CloudOps~L 76141 (issuer edit; the finding
       was correct to surface): `status` here is the REQUIRED terminal state of the named task for
       the execution legs to unlock -- the org/XXX.md dependency-rule form -- NOT a claim about
       current state. Current state at GO: BOTH tasks open at 0.4.0_DS_ClientPlatform~U (c01
       staged/pending, c02 gated on c01). The execution legs unlock ONLY when both FACES read
       complete, read at the faces themselves at unlock time; V14-3 is the record of honoring it.
       An attribute that can be read two ways with a permissive arm is a defect on a face guarding
       a 531-partition production-history write, hence this note at the source. -->
  <dependency agent="0.4.0_DS_ClientPlatform~U" task="ADVI_49F.c01-SIGNFIELD" status="complete" scope="execution leg only -- vehicle work (V14-1, V14-2) is ungated"/>
  <dependency agent="0.4.0_DS_ClientPlatform~U" task="ADVI_49F.c02-CFINPUT" status="complete" scope="execution leg only"/>
</dependencies>

<cross_domain_coordination>
Shares the runners_49f chain + chain_49f_entrypoint with ADVI_49F.c01-SIGNFIELD and
ADVI_49F.c02-CFINPUT (0.4.0_DS_ClientPlatform~U): the backfill SET derives from their field
placement -- MCP that seat before executing if the ruled set changes. The SSM document is shared
infra: any OTHER consumer of advi-49f-chain-dispatch found at Phase 1 is MCP'd before the edit.
~X cohort (D11): reads, never edits -- no filings.
</cross_domain_coordination>

## Reporting
COO at vehicle-live (V14-1/2), at gate-clear, and at execution-complete with the denominator.
cc CTO. Surprise channel: one line to 3.0.0_SA_CVO (cc COO), keep working.
