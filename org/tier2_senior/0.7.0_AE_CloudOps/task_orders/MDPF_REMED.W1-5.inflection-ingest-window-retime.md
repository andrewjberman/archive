<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-07-inflection-ingest-window-retime</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-08-07</date>
    <status>pending</status>
    <project_code>MDPF_CANPLAT</project_code>
  </metadata>

  <objective>
    ANDREW-DIRECT: re-time **every Orion and Eclipse inflection ingestion** so it lands inside the
    **12:00–13:30 UTC** window, then move `mdpf-scheduled-floor` to **13:30 UTC** — with at least
    **10 minutes** of margin between the last ingest landing and the floor.
    ⛔ **STEP 1 IS IDENTIFYING THE REAL PRODUCER. THE DECLARED SCHEDULE AND THE MEASURED LANDING DO
    NOT AGREE, AND RE-TIMING THE WRONG JOB CHANGES NOTHING.**
  </objective>

  <context>
    ANDREW-DIRECT 2026-08-07, COO terminal, two messages, VERBATIM:
      *"i am ok with moving mdpf_scheduled floor to 13:30, as long as whatever it needs from inf is
       at least 10 min before that."*
      *"ok yeah all that shit that we need from inflection should be somwhere between 12:00 and 13:30
       so any orion/eclipse ingestions, need to be in there"*

    >> **THE GROUNDING THAT MAKES THIS A DISCOVERY JOB, NOT A CRON EDIT.** Measured at the COO seat,
    true UTC from `list-objects-v2` LastModified (NOT `aws s3 ls`, which renders local EDT and will
    mislead you by 4 hours):

      eclipse/inflection/silver/fact_model_composition/  and  orion/inflection/silver/fact_positions/
        data 2026-08-01 -> written 2026-08-02T03:30:30Z     T+1 03:30
        data 2026-08-02 -> written 2026-08-03T03:30:30Z     T+1 03:30
        data 2026-08-03 -> written 2026-08-04T03:30:30Z     T+1 03:30
        data 2026-08-04 -> written 2026-08-05T03:30:30Z     T+1 03:30
        data 2026-08-05 -> written 2026-08-06T14:16:05Z     OFF-PATTERN
        data 2026-08-06 -> ** MISSING FROM BOTH FEEDS **
        data 2026-08-07 -> written 2026-08-07T22:31:10Z     OFF-PATTERN, same-day

    **The DECLARED producers are `opal-assets-silver-eclipse-sweep-daily` and
    `opal-assets-silver-orion-sweep-daily`, both `cron(0 16 * * ? *)` = 16:00 UTC, both ENABLED.
    The MEASURED landing is 03:30 UTC the following day. THOSE DO NOT RECONCILE**, and I could find
    nothing in EventBridge Rules or Scheduler firing at 03:30 UTC that would write this path.
    ⇒ **DO NOT assume the 16:00 sweeps are the producer. FIND OUT.** Candidates worth eliminating:
    the INF EC2 chain, `inf-silver-chain-bronze-complete` (Rule, ScheduleExpression None, ENABLED,
    event-driven off `inf-bronze-complete-emitter-daily` at 14:43 UTC), a Step Function, or a
    producer outside AWS entirely.

    ⚠ **A SCHEDULE CAN LIVE OUTSIDE AWS.** Before concluding a trigger is MISSING, ask whether the
    producer can even run in AWS — that exact error produced a false finding on 2026-08-06 with every
    control firing correctly.

    WHY ANDREW WANTS IT: `mdpf-scheduled-floor` currently fires 13:00 UTC and `mdpf-gold-lambda`
    returns non-green at 6/12, with inflection refusing on a CROSS-AXIS COHERENCE GATE and global
    skipped behind it (global requires ALL THREE firm legs —
    `mdpf_gold_consolidator.py:792-802`, source-confirmed).
    ⛔ **BUT BE HONEST ABOUT WHAT THIS FIXES: ON THE T+1 03:30 PATTERN THE DATA IS ALREADY ~9.5 HOURS
    OLD AT THE 13:00 FIRE, SO TIMING IS NOT CURRENTLY STARVING INFLECTION.** This TO makes the
    dependency EXPLICIT AND ORDERED, which is worth doing on its own merits — it does not, by itself,
    explain the cross-axis refusal, and it must not be reported as having fixed it.
  </context>

  <compiler_tools_mandate>
    Phase 1 — the discovery half:
      <run>comp-which "what writes eclipse inflection silver"</run>
      <run>comp-estate --resource eclipse</run> / <run>comp-estate --resource orion</run>
      <expect>The producer chain end to end. ⛔ PRINT THE DENOMINATOR of any sweep. An `aws events
      list-rules --query` is PER-PAGE — materialise the list and filter client-side.</expect>
      <if_mismatch>If you cannot identify the producer, say UNIDENTIFIED and STOP before changing any
      schedule. An unattributed re-time is a guess with a cron expression on it.</if_mismatch>
    Phase 2: <run>comp-iam service &lt;each function you touch&gt;</run> before any deploy.
    Phase 3: DESIRED **and** APPLIED per Rule 22a — a comp-tool cannot tell landed from planned.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - ⛔ **CROSS-PROGRAM: these are INF-owned feeds, not MDPF's.** Re-timing INF ingestion to suit an
      MDPF consumer is a change to another program's schedule. **Surface to CTO BEFORE applying**, and
      name the INF-side blast radius (the silver chain, the NNA leg, `inf-etf-ownership-daily` at
      15:00 UTC, anything downstream of the 16:00 sweeps).
    - ⚠ `mdpf-scheduled-floor` at 09:00 ET was the schedule that REPLACED the INF-marker dependency —
      the NEVER-rule instance about a pipeline whose only trigger is another pipeline's success.
      **Re-timing it around INF re-couples MDPF to INF implicitly.** That is Andrew's call and he has
      made it; record it as a deliberate coupling rather than letting it read as a coincidence.
  </cross_domain_coordination>

  <acceptance_criteria>

    >> 1. **THE PRODUCER IS IDENTIFIED BY MEASUREMENT, NOT BY SCHEDULE NAME.** Name the job that
       actually writes `eclipse/inflection/silver/**` and `orion/inflection/silver/**`, with evidence
       (invocation logs, a matching write timestamp, or an exercised run). ⛔ If the 16:00 sweeps turn
       out NOT to be it, say so loudly — that is a finding in its own right, because two ENABLED rules
       are named for work something else is doing.

    2. ALL ORION + ECLIPSE INFLECTION INGESTION LANDS IN **12:00–13:30 UTC**, and the LAST landing is
       at least **10 MINUTES** before the floor. State the measured last-landing time, not the cron.

    3. `mdpf-scheduled-floor` MOVES TO **13:30 UTC**. ⚠ Its current expression is
       `cron(0 9 * * ? *)` with `ScheduleExpressionTimezone: America/New_York` — **decide and state
       explicitly whether you are keeping the ET timezone (13:30 ET = 17:30 UTC) or switching to UTC.
       Andrew's window is stated in UTC; a timezone slip here reproduces the exact bug being fixed**,
       and DST would move it again in November.

    4. VERIFIED BY AN EXERCISED CYCLE, NOT BY THE CONSOLE. After the change, confirm on a real fire
       that the floor ran AFTER the ingests and that `mdpf-gold-lambda` saw fresh inflection silver.
       ⛔ Rule 22a: a schedule read is a config read; it is not a behavioural claim.

    5. >> **DO NOT REPORT THIS AS HAVING FIXED THE 6/12.** The cross-axis refusal is unexplained and
       the data was already ~9.5h old at the old fire time. If 6/12 becomes 12/12 that is a RESULT to
       report with surprise, not a confirmation of the premise. **If it stays 6/12, that is expected.**

    6. Session log with a Compiler Tools section and an archetype tag.

  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">the EventBridge Scheduler entry `mdpf-scheduled-floor` (via Terraform)</file>
      <file action="modify">the identified inflection ingest producer's schedule (via Terraform)</file>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/INFLECTION_INGEST_WINDOW_RETIME_20260807.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Identify the real producer before changing anything.</requirement>
    <requirement id="2">Land all orion/eclipse inflection ingestion in 12:00-13:30 UTC.</requirement>
    <requirement id="3">Move the floor to 13:30 with >=10 min margin; state the timezone explicitly.</requirement>
    <requirement id="4">Terraform only — never a console edit, never bare `terraform apply` (`safe-apply`).</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">The schedule changes, Terraform-applied, 0-diff verified.</deliverable>
    <deliverable type="document">Producer identification + before/after timing table in true UTC +
    the exercised-cycle evidence.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section.</deliverable>
  </deliverables>

  <do_not>
    <rule>⛔ DO NOT change a schedule before the producer is identified by measurement.</rule>
    <rule>⛔ DO NOT use `aws s3 ls` timestamps — they render LOCAL EDT. Use `list-objects-v2`
    LastModified for true UTC. A 4-hour error here would silently defeat the whole TO.</rule>
    <rule>DO NOT apply an INF-side schedule change without surfacing the cross-program blast radius
    to CTO first.</rule>
    <rule>DO NOT report the 6/12 as fixed by this change. See criterion 5.</rule>
    <rule>DO NOT chase the missing 2026-08-06 partition or the off-pattern writes under this TO —
    ONE BANKED LINE to COO. They are the better lead on the cross-axis refusal and they get their own
    work item.</rule>
    <rule>DO NOT break T-1 semantics. Every AUM/holdings pipeline is T-1 unless it explicitly
    qualifies otherwise; a re-time must not silently turn a T-1 read into a same-day one.</rule>
    <rule>DO NOT build any alert, alarm, checker or monitor around the new window.</rule>
  </do_not>
</task_order>
