<task_order>
<id>NFRA_SYSPARITY.WS-6.incorporation-debt-sla</id>
<project>NFRA_SYSPARITY</project>
<issued_to>0.8.0_AE_CloudComp~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_SYSPARITY, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
<priority>P2 -- STAGED, sequenced AFTER ~A's WS-3 (both are ~A's drift-gate/NESTEDABSTRACT domain; don't parallel-collide the abstraction_loop). GO on WS-3 land. Context-reallocation continuation of ~A (NESTEDABSTRACT owner).</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_SYSPARITY_PRD.md @8f0b596f4 (WS-6 = S3 sixth bullet)</ref>
  <ref type="charter">org/tier0/ledger/LD-0318.md</ref>
</references>

<objective>
Set an INCORPORATION-DEBT SLA on the NESTEDABSTRACT abstraction-ledger. Today 4/5 NA rows are `pending` (NA-0001/0002/0004/0005),
and the drift-gate's "age alone is NOT drift" means nothing pressures their closure -- so debt can accumulate silently. Set a
PENDING-AGE SLA: a `pending` NA row past N days ESCALATES (surfaces as a tracked SLA breach). NESTEDABSTRACT BURNS IT DOWN (its
forward loop incorporates the pending abstractions when their enhancement flip-triggers fire); SYSPARITY SETS the SLA + verifies a
past-SLA row surfaces. Do NOT duplicate the forward incorporation loop -- WS-6 is the SLA/pressure mechanism, not the incorporation.
</objective>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>read infra/system/sdk/abstraction_loop/ABSTRACTION_LEDGER.jsonl (the NA rows + their logged_utc + status)</run>
      <expect>The 4 pending NA rows + their ages. The SLA keys on pending-AGE (logged_utc vs now) -- an aged-pending row is the debt signal, distinct from the drift-gate's trigger-surface signal.</expect>
      <if_mismatch>N/A -- grounding.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>exercise the SLA: seed/point at a past-SLA pending row, run the SLA check</run>
      <expect>A pending row past the SLA age SURFACES (a tracked breach signal) -- EXERCISED, not asserted. A within-SLA pending row does NOT surface (age-conditioned, not noise). Alert-suspension-clean (on-demand/reporting, no new scheduled CI/alert).</expect>
      <if_mismatch>STOP -- an SLA that doesn't surface a real past-SLA row (or fires on within-SLA) is not the control. Fix.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. A pending-age SLA exists on the abstraction-ledger (a `pending` NA row past N days surfaces as a tracked breach), EXERCISED (seed a past-SLA row -> it surfaces; within-SLA -> silent).
1a. **DISPOSITIONED, NOT DATED (CVO+MSTR refined bar @224903Z):** the SLA must force each pending NA row to a DISPOSITION -- INCORPORATED or EXPLICITLY-DEFERRED -- not merely log an SLA date. An SLA that logs a date is a CALENDAR; an SLA that forces each row to a disposition is a CONTROL. Exercised: each of the (currently 6) pending rows resolves to incorporated-or-deferred, not "date stamped".
1b. **BURN-DOWN > GENERATION (CVO+MSTR refined bar):** the SLA must account for its OWN FEED -- parity/enhancement work GENERATES incorporation debt (this session: NA-0006 WS-2 gate + NA-0007 firm-aliases were the session's own fixes, loop-detected). So closing "the current 6" is insufficient: if burn-down rate <= generation rate, the debt is PERMANENT-BY-CONSTRUCTION. The design must EITHER set a burn-down cadence that exceeds the generation rate, OR explicitly BOUND what feeds the queue (e.g. only NFRA-core enhancements generate incorporation obligations). State which, and why it converges.
2. Alert-suspension-clean (on-demand / reporting surface, no new scheduled CI/alert cadence -- consolidation suspension).
3. Does NOT duplicate the NESTEDABSTRACT forward incorporation loop (WS-6 = the SLA/pressure; ~A's loop burns it down). The SLA-breach surface feeds COO's cadence-sweep reporting (COO cadence-owner surfaces the breach + the override-rate at milestones).
4. LD-0318 CVO-VERIFIED GATE (TWO conditions, both EXERCISED, per CVO @224903Z): (i) the 6 pending each DISPOSITIONED (incorporated-or-explicitly-deferred, exercised -- not dated); AND (ii) the SLA mechanism actually CLOSES-FASTER-THAN-IT-FEEDS (or bounds the feed). A dated-not-dispositioned SLA, or one whose burn-down <= generation, FAILS the bar. Ping CVO on land.
5. Session log with Compiler Tools section reproducing each <run> vs <expect>.
</acceptance_criteria>

<cross_domain_coordination>
- Sequenced AFTER WS-3 (same abstraction_loop dir; don't parallel-collide ~A's own two WS on the drift-gate). GO on WS-3 land.
- The SLA-breach + the drift-gate sweep + the comp-system-gate override-rate all feed COO's cadence-owner milestone reporting -- coordinate the surface so COO reports them together (one cadence-owner report, three signals).
- N (the SLA age) is a policy value -- propose it (e.g. tied to the enhancement cadence); COO/CTO confirm.
</cross_domain_coordination>

<notes>
Context-reallocation continuation of ~A per Andrew-direct (2026-07-19): ~A owns NESTEDABSTRACT (the abstraction-ledger + the forward loop);
WS-6 SLAs the incorporation debt on that ledger -- its exact domain, sequenced after WS-3 so its two drift-gate/abstraction_loop WS don't
collide. The SLA-breach signal joins the COO cadence-owner reporting set (drift-gate sweep + comp-system override-rate + this SLA).
</notes>
</task_order>
