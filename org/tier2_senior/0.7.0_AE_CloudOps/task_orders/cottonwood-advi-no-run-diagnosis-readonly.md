<task_order>
<id>COT_ADVI_DIAG (ad-hoc)</id>
<title>Cottonwood ADVI has not run in ~a week — READ-ONLY grounded-mechanism diagnosis (NOT a fix)</title>
<project>ad-hoc (Andrew-direct via CTO)</title>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T22:22Z</issued_at>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "cottonwood-advi-no-run-diagnosis-readonl" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
<priority>ANDREW-DIRECT, idle-capacity reallocation (COO standing authority 07-19; dispatch cleared by CTO 222113Z)</priority>

<authorization>
Andrew-direct at the CTO terminal ~22:2xZ, VERBATIM (recorded by CTO, custody his):
> "Also, Cottonwood ADVI has not run in a week, probably worth checking that out too if the main fabric
> is not doing anything right now."
Down the single LD-0333 path: Andrew -> CTO -> COO -> you. CTO 222113Z: "Dispatch the investigation now."
</authorization>

<scope priority="READ-ONLY — the deliverable is a MECHANISM REPORT, not a fix">
Andrew observed that "Cottonwood ADVI has not run in a week." **That is his OBSERVATION to be confirmed
or refuted in TRADING DAYS, not inherited as a finding.** The deliverable is a grounded mechanism report
to CTO + Andrew answering *what is actually true and WHY* — modeled on the 3F-B7 pattern that worked
tonight: mechanism source-confirmed, then a repull/repair recommendation as a SEPARATE CTO-gated question.

**FIVE STEPS, in order:**

1. **GROUND WHAT "COTTONWOOD ADVI" CONCRETELY IS** — the advisor-intelligence pipeline/runs scoped to
   `cot`. `comp-which "<plain-English question>"` / `pipescript` FIRST (Rule 21). ⛔ **DO NOT ASSUME the
   49F/0833 ADVI surface is the same thing** — `0833` is the **49F ADVI master**, and **firm separation
   binds** (cot is a COMPLETELY separate firm pipeline from bd; never mirror/sync, gate+IAM enforced).
   Name the actual resources: producer(s), scheduler/trigger, S3 output prefixes, served surface.

2. **FIRE HISTORY** on its scheduler/trigger — **EventBridge Rules AND the Scheduler namespace, BOTH**
   (tonight's census lesson: a producer can be a Scheduler schedule or a Lambda destination that
   `list-rules` structurally cannot see; the eclipse puller was a gold-chain segment, not a target at
   all). **Print the DENOMINATOR of every census** ("N matched of M total"). **Explicit-Z timestamps
   ONLY** — never bare `aws s3 ls` / `git log --since` (both parse/print LOCAL time here, UTC-4; a
   time-windowed zero is byte-identical between "nothing fired" and "I looked in the wrong window").

3. **ARTIFACT FRESHNESS** on its outputs, with the **TRADING-DAY basis resolved BEFORE any staleness
   claim (NEVER#1).** Resolve weekends + market holidays first; count in trading days. "A week" wall-clock
   spans a weekend — confirm whether the true trading-day lag matches Andrew's read or is smaller.

4. **CHECK THE STANDING-RECORD POINTER EXPLICITLY.** The cot `bd-cot-silver-stale-*` alarm was recorded
   as the **FIRST TRUE reading of an 18-day-old cot silver failure** (memory:
   `project_cot_snapshot_zero_row_freeze_20260709` — *"close nothing on it"*). **IF cot ADVI consumes cot
   silver, a week of no-runs may be DOWNSTREAM of that known break, not a new defect.** Establish which,
   with citations at vintage. A pipeline correctly declining to run on frozen/zero-row upstream is
   *healthy behavior*, not a dead producer.

5. **CHECK WHETHER THE LD-0333 RESTART/HOLD INTERACTED WITH ITS SCHEDULE.** A held fabric can look like a
   dead pipeline — that is tonight's own founding lesson, from the sovereign's vantage. If a
   hold/disable/teardown touched its trigger, that is the mechanism, not a defect.
</scope>

<constraints priority="BINDING">
- ⛔ **NO ad-hoc gold runs to "test" anything** (NEVER#4). Validate on scheduled artifacts + live state.
- ⛔ **NO repairs, NO re-enables, NO alarm-building.** This is diagnosis only. Any fix is a SEPARATE,
   CTO-gated second step. Alarm-building specifically is against Andrew's standing word.
- ✅ **Working-state verification EXERCISED where cheap AND read-only** — exercise the path that would
   fail if your claim is false, not a config read (Rule 22a; Andrew's "make sure everything is working").
- **Firm separation binds throughout.** Read cot resources only; never reference a bd resource from the
   cot investigation. cot-BD vendor egress is lifted (standing) but this is read-only estate diagnosis.
- **Every causal claim carries its grounding** (`file:line @ commit-ish` or comp-tool + output). An
   ungrounded "why" is INFERRED and non-actionable (Rule 22). "root cause / source-confirmed" are
   reserved words.
</constraints>

<compiler_tools_mandate>
  <phase id="1" when="grounding">
    <step>
      <run>comp-which "what is the cottonwood advisor-intelligence pipeline and what runs it"</run>
      <expect>Routes to the canonical tool or runs an on-rails comp-grep/comp-glob; the cot ADVI producer + scheduler + output prefixes named. Record output even if NO CURATED RULE MATCHED.</expect>
      <if_mismatch>If nothing routes, that is itself a finding (an unnamed pipeline). Proceed to pipescript + rail-checked primitives; record the coverage gap.</if_mismatch>
    </step>
    <step>
      <run>pipescript &lt;cot advi thread name&gt;   (pipescript --list for names first)</run>
      <expect>Full named-thread traversal: resources + producers->served->frontend + owning tool + debt/reachability flags. NO silent Unknown.</expect>
      <if_mismatch>If cot ADVI is not a named pipescript thread, ground it via comp-grep on the cot tree + the scheduler census below.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="fire history + freshness">
    <step>
      <run># rail-checked: applied-truth schedule census, BOTH namespaces, denominators printed
aws events list-rules (paginated; "N matched of M total") + aws scheduler list-schedules + Lambda destinations on candidates</run>
      <expect>The trigger NAMED with state + cron cited verbatim, OR a measured absence stating what was searched and how many objects examined.</expect>
      <if_mismatch>An empty rules result is NOT "not fired" — two namespaces + destinations are structurally distinct surfaces. Print denominators; an absence without one is not a finding.</if_mismatch>
    </step>
    <step>
      <run>comp-freshness on the cot ADVI outputs + aws s3api list-objects-v2 (explicit-Z) on the output prefixes</run>
      <expect>freshness_basis: trading-day-frontier; the true trading-day lag stated with the calendar resolved FIRST.</expect>
      <if_mismatch>A flat-hours entry WILL misread the weekend. Resolve lib/trading_calendar.py before any staleness claim; a wall-clock "week" is not a finding (NEVER#1).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="lineage + hold">
    <step>
      <run>Trace cot ADVI's UPSTREAM inputs; check whether it consumes cot silver (the bd-cot-silver-stale-* / project_cot_snapshot_zero_row_freeze_20260709 surface)</run>
      <expect>A definite verdict: no-runs are (a) downstream of the known 18-day cot silver freeze, (b) an LD-0333 hold/disable interaction, (c) a genuinely new defect, or (d) healthy T-1 misread as stale — with citations at vintage.</expect>
      <if_mismatch>If upstream is the frozen cot silver, a non-running ADVI may be CORRECT (declining to run on zero-row input). Do not call a healthy guard a dead producer.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. "Cottonwood ADVI" GROUNDED to named resources (producer, trigger, output prefixes, served surface),
   explicitly distinct from the 49F/0833 ADVI surface, firm-separation stated.
2. Fire-history census across BOTH EventBridge namespaces + destinations, denominators printed,
   explicit-Z timestamps, trigger state cited verbatim.
3. A TRADING-DAY freshness verdict (calendar resolved first) — Andrew's "a week" confirmed or refuted in
   trading days.
4. An explicit verdict on the standing-record pointer (downstream-of-cot-silver-freeze) AND on the
   LD-0333 hold interaction, each with citations at vintage.
5. A grounded MECHANISM report to CTO + Andrew, with the repull/repair recommendation as a SEPARATE
   CTO-gated question (the B7 pattern). NO fix executed.
6. Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail.
</acceptance_criteria>

<escalation>
Report to 2.0.0_SA_COO; the mechanism report goes to CTO + Andrew. Escalate immediately if the diagnosis
finds a NEW live defect (not downstream-of-known-break, not hold-interaction) — that changes it from a
scheduled-visibility item to an active one.
</escalation>
</task_order>
