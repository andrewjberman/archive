<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-07-mdpf-adhoc-chain-exercise</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-08-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "MDPF_REMED" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: pending</status>
    <project_code>MDPF_CANPLAT</project_code>
  </metadata>

  <objective>
    ANDREW-DIRECT: fire the MDPF chain AD HOC, **ONE LAMBDA AT A TIME, IN ORDER, READING THE OUTPUT
    BETWEEN EACH**, and report whether it works. This is a QA exercise of the flow before tomorrow's
    09:00 ET unattended fire — the first one Andrew watches as its oracle.
  </objective>

  <context>
    ANDREW-DIRECT 2026-08-07 ~2215Z at the COO terminal, VERBATIM:
      *"have somebody institute an ad hoc run, just trigger each lambda step by step and see if it
       works."*
    Earlier the same evening, on the remediation transition: *"...and run an ad hoc run to test the
    flow."*

    **AD-HOC RUNS ARE SANCTIONED FOR QA** — CLAUDE.md: *"an ad-hoc run is a legitimate QA instrument —
    fire one to test, exercise, or reproduce."* ⛔ **AND ITS ARTIFACTS ARE NEVER PRODUCTION EVIDENCE.**
    Production numbers come from the scheduled run. Say so in the report.

    THE CHAIN, measured at the COO seat tonight (EventBridge **Scheduler**, America/New_York):
      1. `mdpf-scheduled-floor`                    cron(0 9 * * ? *)  -> **mdpf-gold-lambda**
      2. `mdpf-accrual-bridge-daily`               cron(40 9 * * ? *) -> **mdpf-accrual-trigger**
      3. `opal-assets-mdpf-portal-publisher-daily` cron(50 9 * * ? *) -> **opal-assets-mdpf-portal-publisher**
    Separately, `mdpf-daily-refresh-trigger` is an EventBridge **RULE** with
    `ScheduleExpression: None`, ENABLED, firing only on the INF completion marker — an ACCELERATOR,
    not the schedule. **Its marker is 8 days stale (`run_date 2026-07-31`), which is expected and is
    NOT what you are testing.**

    DATA ROUTE the chain moves things along:
      opal-data-assets `schwab/08242234/silver/fact_rps_s2` (+ cot/eclipse/orion silver)
        -> gold scripts -> `gold/mdpf_revamp/` (STAGING, underscore spellings)
        -> consolidator -> `portal/gold/mdpf/{scope}/{artifact}/YYYY-MM-DD.json` (A4, 4x3=12)
        -> publisher -> `opal-data-portal-v2/platinum/mdpf/{scope}/{artifact}.json` (14 incl. 2 extra)
  </context>

  <compiler_tools_mandate>
    Phase 1 — BEFORE the first invoke:
      <run>aws lambda get-function-configuration --function-name &lt;each of the 3&gt; --query '{LastModified:LastModified,CodeSha256:CodeSha256}'</run>
      <expect>Record all three. **PIN THE CODE VINTAGE AT START** — `0.4.0_DS_ClientPlatform` is
      landing an atomic 4-file custody commit in this same chain tonight, and a deploy that lands
      mid-run makes the result uninterpretable.</expect>
      <if_mismatch>If a sha changes between your start pin and your end pin, SAY SO and treat the run
      as mixed-vintage rather than reporting it as a clean pass.</if_mismatch>
    Phase 3 — after: <run>comp-freshness</run> on the served prefix, and record every denominator.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - ⚠ **MCP `0.4.0_DS_ClientPlatform` BEFORE STEP 1.** They are mid-commit on
      `dim_mdpf_aggregate_aua_timeseries.py` + `route_bindings.yaml` in this exact chain. Ask whether
      their deploy has landed; run AFTER it if it is imminent, so the exercise tests one coherent state.
    - ⚠ **STEP 3 WRITES TO THE LIVE CLIENT-FACING SERVING LAYER.** See criterion 3.
    - `0.3.0_DT` may run a SECOND portal promote tonight — unrelated tree, no collision expected, but
      do not be surprised by portal activity.
  </cross_domain_coordination>

  <acceptance_criteria>

    >> 1. **ONE AT A TIME, IN ORDER, AND STOP ON FAILURE.** Invoke `mdpf-gold-lambda`, READ ITS OUTPUT,
       verify its artifacts, and only THEN proceed to `mdpf-accrual-trigger`, then the publisher.
       ⛔ **A NON-ZERO EXIT IS NOT THE ONLY FAILURE, AND rc=0 IS NOT THE PASS.** Read what each step
       actually EMITTED — keys written, counts, dates. CLAUDE.md: never trust a producer's self-report
       or rc=0; verify against the SERVED/written artifact.
       ⛔ **IF A STEP FAILS, STOP THERE.** Do not run the next one to "see if it also works" — the
       whole point of step-by-step is that the first failure localises the defect. Report and hold.

    2. EACH STEP'S VERIFICATION IS AGAINST WHAT IT WROTE, WITH DENOMINATORS:
         gold-lambda   -> which `gold/mdpf_revamp/` + `portal/gold/mdpf/` keys appeared, and their dates
         accrual       -> what the bridge produced/updated
         publisher     -> **how many of the 14 expected pairs landed** (12 RULED + the 2
                          `R12_EXTRA_PAIRS`), and the manifest it wrote
       ⚠ The consolidator's own completeness log reads `emitted/a4_expected` where **both sides derive
       from one closed tuple** (`mdpf_gold_consolidator.py:968`/`:999`). **DO NOT QUOTE ITS 12/12 AS
       YOUR EVIDENCE** — list the actual keys. That check cannot see a type outside its tuple.

    >> 3. ⛔ **CAPTURE THE SERVED PRE-STATE BEFORE STEP 3, BECAUSE STEP 3 OVERWRITES LIVE CLIENT
       ARTIFACTS.** The publisher writes to `opal-data-portal-v2/platinum/mdpf/**` — what the portal
       serves right now, the thing Andrew confirmed on his own screen after last night's cutover.
       Before invoking: `head-object` every object you expect it to touch and record **key + ETag +
       VersionId + Size + LastModified**. That makes a bad publish ONE STEP to reverse instead of an
       archaeology problem.
       *Banked precedent: on 2026-08-01 a "rollback onto itself" that everyone read as a no-op
       OVERWROTE A DELIBERATELY-SET SERVED VINTAGE. Verify live state before treating any mutation as
       safe.*

    4. THE RUN IS LABELLED AD-HOC IN THE REPORT AND ITS OUTPUT IS NOT OFFERED AS PRODUCTION EVIDENCE.
       If the numbers look right, that is the CHAIN working — the production numbers still come from
       the scheduled fire.

    5. CODE VINTAGE PINNED AT START **AND** AT END (all three functions). A mid-run deploy makes the
       result mixed-vintage; say so rather than reporting a clean pass.

    6. Session log with a Compiler Tools section and an archetype tag (`VALIDATE`).

  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_ADHOC_CHAIN_EXERCISE_20260807.md</file>
      <file action="reference">infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py</file>
      <file action="reference">data/mdpf/scripts/gold/mdpf_gold_consolidator.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Invoke the three in order, verifying between each; stop at the first failure.</requirement>
    <requirement id="2">Capture the served pre-state before the publisher step.</requirement>
    <requirement id="3">Pin code vintage at start and end.</requirement>
    <requirement id="4">Report per-step: what it wrote, how many, what dates, what you could not verify.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">The step-by-step exercise record with per-step evidence + the served
    pre-state capture + a plain verdict: does the chain work, yes or no, and where it broke if not.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section.</deliverable>
  </deliverables>

  <do_not>
    <rule>⛔ DO NOT fire all three at once. Andrew said step by step and the sequencing IS the test.</rule>
    <rule>⛔ DO NOT invoke the publisher without the served pre-state captured first.</rule>
    <rule>DO NOT report rc=0 as a pass. Read what was written.</rule>
    <rule>DO NOT quote the consolidator's `emitted/a4_expected` as completeness evidence.</rule>
    <rule>DO NOT offer ad-hoc output as production evidence.</rule>
    <rule>DO NOT "fix" anything you find mid-run. ⛔ **THE FLOW IS: MAKE A PLAN, COMPLETE THE PLAN,
    THEN REVIEW** (Andrew-direct today). A defect found mid-exercise is ONE BANKED LINE to COO and the
    exercise continues or stops per criterion 1 — it does not become a repair.</rule>
    <rule>DO NOT re-trigger, re-run or "try again" a failed step to see if it passes the second time.
    Report the first failure as the result.</rule>
    <rule>DO NOT build any alert, alarm, checker or monitor.</rule>
  </do_not>
</task_order>
