# TO MDPF_REMED.RP-W5b — EMITTER REPAIR: drop the deleted-table write, REPOINT the guard (never drop it), remove the TF re-create — one change

<task_order id="MDPF_REMED.RP-W5b" project="MDPF_REMED">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-11T00:3xZ</issued>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "MDPF_REMED" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: pending</status>
<priority>P0 — LIVE PRODUCER OUTAGE (opal-assets-daily-emitter down since 08-08; mdpf/feeds/* frozen;
zeros in the aggregate; serve protected only by the 08-05 carry-forward). CTO ruled (a) at 003242Z;
(b) re-create REFUSED (reverses Andrew's 08-07 deletion — needs HIS word and is not being sought);
(c) successor store REFUSED (Build Ladder rung 1). Your lane (emitter.tf + emitter code).</priority>

<references>
  <ref type="ruling">CTO 20260811T003242Z — inbox record</ref>
  <ref type="evidence">Your own 003022Z read: 08-09/08-10 BatchWriteItem ResourceNotFoundException on opal-assets-daily-aua; 08-08 VintageContradiction (separate leg, DS checks it under RP-W1)</ref>
</references>

## SCOPE — one coherent change, three parts
1. **DROP the BatchWriteItem write** to `opal-assets-daily-aua` from the emitter.
2. **REPOINT the value-repeat-guard reads. ⛔ CTO VERBATIM, in this TO by order: "DROP THE
   DEPENDENCY" MUST NOT BECOME "DROP THE GUARD."** The guard's FUNCTION is preserved and re-pointed
   (e.g. to the S3 record the emitter itself writes, or the feed artifacts), not deleted because its
   store vanished. Same shape as the mirror ruling: narrow/re-point the assertion, never disable the
   control. **If the guard genuinely cannot be re-pointed without a store, STOP and say so — that is
   a different fork and CTO takes it.** Do not ship a version with one fewer control than it started
   with.
3. **REMOVE the `opal-assets-daily-aua` resource declaration from the opal-assets TF root in the
   SAME change** — otherwise the plan wants to resurrect the table forever and the hazard survives
   its own cause. (The plan-time-deny gate CANDIDATE stays on CTO's carried queue regardless;
   targeted-apply discipline stays until the declaration is gone.)

NOT in scope: the 08-08 VintageContradiction (DS checks whether W1 dissolves it, per RP-W1 3a);
item-4's gate deploy (COO sequences it AFTER this lands, so the total-feeder-failure RED fires
against a fixed emitter).

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-blast opal-assets-daily-emitter ; comp-iam service opal-assets-daily-emitter</run>
      <expect>Consumer set of the DDB write enumerated (expect: none live — the table is gone); guard read path candidates identified. comp-iam necessary-not-sufficient as always.</expect>
      <if_mismatch>A live consumer of the DDB write = STOP, surface — something else also never heard about the deletion.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before apply">
    <step>
      <run>safe-commit then .tools/safe-apply.sh -target'ed (CTO-binding: opal-assets root applies are targeted + plan READ; the plan must show the daily-aua declaration REMOVED, not re-created)</run>
      <expect>Plan: emitter change + declaration removal ONLY; NO re-create row; 0-diff post-apply; tag + push --follow-tags per integrator discipline.</expect>
      <if_mismatch>STOP on any unexpected row.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after apply">
    <step>
      <run>EXERCISE: invoke the emitter (ad-hoc QA legal) — completes without ResourceNotFoundException, mdpf/feeds/* advance; guard EXERCISED both ways (a repeat-value case RAISES via the re-pointed read; a fresh-value case passes)</run>
      <expect>Emitter completes; feeds advance past 08-08/08-06 frontiers; guard demonstrably ABLE TO FAIL post-repoint.</expect>
      <if_mismatch>Roll back in-window; a guard that cannot fail post-repoint is item-2 of this ruling violated.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Item-4's gate (code @2ba6417fbb, deploy held at COO) deploys AFTER this lands — do not bundle.
RP-W4 selector proceeds in parallel in your lane; keep commits separate and attributable. The
scheduled emitter run after this lands is the first true test — its output feeds the same aggregate
the item-4 gate will then police.
</cross_domain_coordination>

<acceptance_criteria>
1. Emitter completes on an exercised run WITHOUT ResourceNotFoundException. *(RE-CUT 011911Z on
   AE's measured correction: the emitter does NOT write mdpf/feeds/* — the feed writers are the WS
   lambdas (chain-fed; wsb-49f last clean 08-08 03:31Z, no EventBridge rule matches 'wsb'). "Feeds
   ADVANCE" is NOT dischargeable by this fix alone; the feed-freeze mechanism is a SEPARATE read,
   surfaced not claimed — likely the same chain question as mdpf-daily-refresh-trigger.)*
2. Guard function preserved: positive control (repeat value RAISES) + negative control (fresh value
   passes) via the re-pointed read.
3. TF declaration gone: plan output shows removal, and a subsequent un-targeted plan no longer
   carries a daily-aua re-create row (read and quoted).
4. No new stores, tables, alarms, or schedules.
5. Session log Compiler Tools section reproduces every &lt;run&gt; + output + pass/fail.
</acceptance_criteria>
</task_order>
