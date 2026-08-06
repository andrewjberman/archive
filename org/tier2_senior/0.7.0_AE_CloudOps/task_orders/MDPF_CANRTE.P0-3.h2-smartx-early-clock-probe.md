<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-h2-smartx-early-clock</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-06</date>
    <status>superseded -- ADOPTED INTO MDPF_CANPLAT.P0-2R.vendor-early-clock-probes (body incorporated by pinned reference @a6ae64326) (2.0.0_SA_COO~Z 2026-08-06 fresh decomposition off PRD @24d3eb2f8; single live dispatch authority = org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_CANPLAT_DECOMPOSITION_20260806.md. DO NOT ACT ON THIS TO.)</status>
    <project_code>MDPF_CANRTE</project_code>
  </metadata>

  <objective>
    Establish whether the SmartX same-day legs (model AUM + allocation roster) can land in canonical silver
    by 08:40 ET on the Clock v3 proposed schedule (JWT ~07:45 ET, pull ~08:00 ET), producing the same data
    contract as the incumbent 09:00/09:15 ET run — so the 09:00 ET gold floor sees them.
  </objective>

  <context>
    SmartX is the THIRD independent clock in this program and it moves on its own. Your own 30-day census
    established the incumbent shape and it is not in dispute:

      smartx_model_aum_daily          same_day  n=24  min 09:37 med 09:40 max 15:38  misses 08:40: 24/24
      smartx_model_allocation_roster  same_day  n=24  min 09:37 med 09:40 max 15:38  misses 08:40: 24/24

    UNANIMOUS MISS. Unlike Inflection, there is no wave structure to exploit and no exception to remove —
    the current JWT-at-09:00 / pull-at-09:15 clock simply cannot produce silver by 08:40. Clock v3 proposed
    approximately 07:45 / 08:00 / 08:15 ET.

    ### WHAT H2 ACTUALLY ASKS, AND THE PART THE PACK GOT WRONG

    `04` §6 H2 says the early probe's execution "was not found." CTO~Z's classification adds a requirement
    the pack omits: SEARCH THE RECORD FOR THE 08-05 RUN CLOCK V3 PRE-REGISTERED, AND PRINT THE DENOMINATOR.
    §6 states "not found" WITH NO DENOMINATOR — which is an unsupported absence claim of exactly the kind
    this program keeps catching. Either locate that run's evidence, or state what you searched and how much
    of it, so "not found" becomes a measured result rather than an assertion.

    ### CLASS A' — WHAT THIS PROBE MAY ASSERT

    CTO~Z classifies H2 as Class A': measurement of a VENDOR WE DO NOT CONTROL. The result is a SAMPLE, not
    a durable fact. A closure may assert "valid early ON THE DAYS PROBED" and nothing stronger. Note the
    incumbent max of 15:38 in your own census — the tail is real, so a single clean morning says little
    about the distribution.

    ### H12 — THE PROBE-FAIL BRANCH IS ALREADY RULED. DO NOT INVENT ONE.

    Clock v3 rules it: SHIFTS LAND ON PROBE PASS; vendor lateness surfaces as LABELED CARRY (2 TD window,
    every carried point labeled, transition visible) — NEVER as a held publish. A negative probe is a
    COMPLETED probe: the schedule does not shift, lateness carries with an honest label, and the 10:00 ET
    publish deadline still holds. Do not stall, do not escalate for a new design, do not invent a
    compensating path.

    ### VENDOR EGRESS — AND NOTE THIS ASK IS SEPARATE FROM P0-2's

    Probing the SmartX endpoints is an EXTERNAL VENDOR API CALL. CLAUDE.md Agent Autonomy: never call a
    non-Opal vendor API without Andrew's explicit per-use word. AVAILABILITY IN THE TOOLSET IS NOT
    AUTHORIZATION, and neither is a per-use word granted for a DIFFERENT vendor.

    ⚠ COO~Z's original escalation to Andrew named the ORION and ECLIPSE endpoints only. SMARTX WAS NOT IN
    IT. A correction has been surfaced via MSTR~Z. Until Andrew's word explicitly covers SmartX, THIS PROBE
    DOES NOT RUN — a grant for Inflection is not a grant for SmartX, and reading it as one is precisely the
    scope-widening the rule forbids.

    IF HIS WORD COVERS SMARTX: run inside the proposed window.
    IF IT DOES NOT: execute the S3-SIDE FALLBACK. It is PRE-APPROVED by MSTR~Z and needs NO second
    escalation. Do not cross the vendor line on schedule pressure.

    ### SMARTX MOVES — MEASURED, AND IT IS THE OPPOSITE OF ORION

    CTO~Z measured both JWT clocks on the live plane (`comp-trigger`, denominator 139 events-rules + 16
    schedules), corrected @5022e995d:

      smartx-jwt-refresher-daily   cron(0 9 * * ? *)    TZ America/New_York  -> ET-ANCHORED
      opal-inf-jwt-fetch           cron(5 12 * * ? *)   no tz field          -> UTC-FIXED (08:05 ET in EDT)

    SO THE CLOCK MOVE IS NOT UNIFORM ACROSS THE TWO VENDORS, and doc 03's blanket "shift the associated
    upstream chains earlier" is CORRECT FOR SMARTX AND WRONG FOR ORION:

      SMARTX — ET-anchored, so it MOVES as doc 03 specifies (JWT 07:45 / pull 08:00 ET) and is DST-SAFE BY
               CONSTRUCTION. No fixed-clock hazard equivalent to Orion's. This is your feed to move.
      ORION  — UTC-fixed by deliberate design (Clock v3 Amendment 1, off the 12:00/12:30 hazard marks
               year-round). MUST NOT MOVE. That constraint is P0-2's, not yours.

    Criterion 2 below still stands, but as CONFIRMATION AGAINST THE PLANE rather than an open investigation:
    verify the ET-anchored expression yourself and cite it. Do not inherit the number from this TO or from
    Clock v3 — the record says 12:15Z for Orion while the plane runs 12:05Z, so THE GOVERNING CLOCK DOCUMENT
    IS WRONG ABOUT THE ONE MEMBER IT EXISTS TO PIN. Cite the live cron expression, never the ruling doc.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-which "what schedules drive the smartx pull and jwt and what consumes their silver"</run>
      <expect>Routes to comp-trigger / comp-estate, or runs comp-grep on-rails.</expect>
      <if_mismatch>Repeat override for one intent = COVERAGE GAP -> report to COO~Z (Rule 21).</if_mismatch>

      <run>comp-trigger smartx</run>
      <expect>SmartX JWT + pull + converter schedules, DENOMINATOR PRINTED (rules + schedules scanned).</expect>
      <if_mismatch>comp-trigger renders scheduler rows as `schedule: -` — it structurally does not expose
      ScheduleExpression/timezone. Ground-truth on the live primitive per Rule 22a; never read `-` as
      "no schedule."</if_mismatch>

    Phase 2 — before committing:
      <run>comp-blast &lt;each schedule/handler you propose to move&gt;</run>
      <expect>Blast radius WITH DENOMINATOR; every consumer of a moved schedule named.</expect>
      <if_mismatch>A non-MDPF consumer in the radius = STOP, message COO~Z. SmartX silver may feed more than
      MDPF, and moving a shared upstream clock is not an MDPF-local act. A zero is a LOWER BOUND.</if_mismatch>

    Phase 3 — after committing: record the probe outcome and the branch taken in the session log Compiler
    Tools table.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>SmartX JWT + pull + on-success converter schedules (upstream modules)</shared_resource>
    <also_in_to>P0-2 (the other clock probe — independent; do NOT couple them) · P4-1 (applies the change) ·
    P5-1 (Phase 5 step 7 applies upstream clock modules FIRST)</also_in_to>
    <last_write_owner>0.7.0_AE_CloudOps~Z</last_write_owner>
    <required_action>THIS TO PROBES AND DECIDES; IT APPLIES NOTHING. Report the resolved design to COO~Z so
    P4-1 is written against a decision. Retain the same on-success converter path (doc 03 Phase 0 item 4) —
    a moved pull with an unmoved converter produces early bronze and unchanged silver, which would read as
    a probe failure caused by our own plumbing rather than by the vendor.</required_action>

    <shared_resource>Any non-MDPF consumer of SmartX silver</shared_resource>
    <also_in_to>surfaced by your Phase 2 comp-blast</also_in_to>
    <required_action>If SmartX silver feeds anything outside MDPF, moving its clock is a cross-domain act.
    Name every such consumer and MCP COO~Z before the design is finalized.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    ⛔ **THE GOVERNING CRITERION — ACCEPTANCE ASSERTS ON THE OUTCOME, NEVER ON THE INTERVENTION.**
       (CTO~Z ruled 2026-08-06 ~2112Z, STANDING across every clock TO in this program.)
         THE CRITERION IS: **"canonical SmartX silver OBJECT exists by 08:40 ET."**
         IT IS **NOT**: "the schedules were moved to 07:45/08:00."
       WHY THIS IS THE FIRST CRITERION AND NOT A STYLE NOTE: *"did the schedules move?"* IS PRECISELY THE
       CHECK THAT PASSES WHILE THE REMEDY FAILS. Criterion 0 below documents a live instance — doc 03's own
       prescribed remedy moves two schedules that do not produce the binding silver, and an
       intervention-shaped acceptance would have certified it as delivered. AN OUTCOME ASSERTION IS IMMUNE
       TO TARGETING THE WRONG RESOURCE, because a wrong target simply does not produce the outcome.
       Same shape as the `calendar_source()` ruling: ASSERT THE THING, NOT THE ACT SUPPOSED TO CAUSE IT.
       Every criterion below is subordinate to this one. If any of them can be satisfied while the silver
       object is absent at 08:40 ET, that criterion is wrong and you should tell COO~Z rather than satisfy it.
       SIZING INPUT, from the measured ~10-minute converter lag: a pull at 08:00 predicts silver ~08:10,
       comfortably inside 08:40.

    0. ⚠ THE PROBE TARGETS `smartx-assets-daily-pull-daily` (09:30 ET), NOT the 09:15 rest pull.
       ADDED 2026-08-06 ~2110Z — DOC 03's H2 REMEDY MOVES SCHEDULES THAT DO NOT PRODUCE THE BINDING SILVER.
       Measured on the primitive, fully paginated (7 SmartX Lambdas, 4 Scheduler entries, 3 classic rules —
       doc 03 describes TWO of those fourteen):
         `smartx-assets-daily-pull` -> event-invoke-config OnSuccess destination = `opal-assets-silver-smartx`
         `smartx-rest-pull`         -> event-invoke-configs: **ZERO. Nothing chains off it.**
       So the binding silver is produced by THE 09:30 ASSETS PULL VIA ITS OnSuccess CHAIN. Doc 03 Phase 0
       item 4 says "set JWT 07:45 ET and pull 08:00 ET; retain the same on-success converter path" — and
       THOSE ARE THE TWO SCHEDULES THAT DO NOT PRODUCE `fact_model_aum_daily`.
       ⛔ **EXECUTED LITERALLY, DOC 03's REMEDY MOVES THE JWT AND THE REST PULL, LEAVES
       `smartx-assets-daily-pull` AT 09:30 ET, AND THE SILVER LANDS AT ~09:40 ET EXACTLY AS BEFORE — WHILE
       THE CHANGE READS AS DELIVERED.** That is the failure this criterion exists to prevent, and it would
       have passed every downstream check that looked at whether the schedules moved.
       The 30-day census corroborates the MECHANISM, not merely the timing: pull 09:30 -> OnSuccess ->
       silver 09:37-09:41, median 09:40, 24 of 24 days — a ten-minute converter lag off a 09:30 trigger,
       not off an 09:15 one.
       CORRECTED REMEDY: move `smartx-assets-daily-pull-daily`. The JWT must still precede it (ET-anchored,
       DST-safe, moves cleanly). PROVE OR REFUTE THIS AT THE PROBE rather than asserting it — but the design
       must target the right schedule or the probe validates a move that changes nothing.

    0a. TWO COUPLING FACTS THAT FALL OUT OF THE SAME MEASUREMENT — record both, act on neither today.
       (i) **SMARTX IS THE ONLY FAMILY IN `opal-data-assets` WITH NO S3 BRONZE NOTIFICATION.** All 8
       notification configs are S3 ObjectCreated on a bronze prefix (blackdiamond/cottonwood,
       eclipse/inflection, orion/inflection, schwab/08242234, schwab/08335338, trueshares/DIVZ,
       trueshares/IDVZ, pathfinder/filepoint) — there is no `smartx/` prefix among them. Every other family
       converts on DATA LANDING; SMARTX ALONE CONVERTS ON PULL SUCCESS. Good news for the remedy (its
       converter moves with its pull) but it means **A PULL THAT SUCCEEDS WITHOUT WRITING STILL FIRES THE
       CONVERTER, AND A WRITE THAT LANDS BY ANY OTHER ROUTE NEVER DOES.** Know that before leaning on the
       coupling — a green converter is not evidence that data landed.
       (ii) **THE BACKSTOP IS UTC-FIXED AND LANDS PAST THE DEADLINE.**
       `opal-assets-silver-smartx-sweep-daily` is a classic rule at `cron(0 16 * * ? *)` with NO timezone
       field = 12:00 ET in EDT, 11:00 ET in EST. If the OnSuccess chain fails after the pull moves, the
       catch-up does not run until TWO HOURS AFTER the 10:00 ET platinum deadline. And because the sweep is
       UTC-fixed while the pulls are ET-anchored, THE PULL-TO-BACKSTOP GAP CHANGES BY AN HOUR SEASONALLY —
       the same ET-vs-UTC split CTO~Z identified BETWEEN SmartX and Orion exists INSIDE the SmartX chain,
       between its pull and its own backstop. CTO~Z's constraint 2 assigned SmartX wholesale to the ET side;
       that is right for the pulls and WRONG FOR THE SWEEP. Routed to CTO~Z; do not resolve it here.
       ⚠ **`smartx-account-distribution-daily` IS IN SCOPE — CTO~Z ruled it in, and the argument is short.**
       It is a classic rule at 11:30Z = 07:30 ET EDT / 06:30 ET EST, ALWAYS BEFORE the ET-anchored 09:00
       JWT. So it either carries its own auth or runs on a PRIOR-DAY TOKEN. Whichever it is, **IT IS A
       CONSUMER OF THE JWT WE ARE MOVING, AND ANY JWT MOVE MUST ACCOUNT FOR EVERY CONSUMER OF THAT JWT.**
       That alone puts it in Phase 0 regardless of what it produces. DETERMINE WHICH OF THE TWO IT IS BEFORE
       THE JWT SHIFTS — if it runs on a prior-day token, moving the mint CHANGES ITS TOKEN AGE, and that is
       a live behavioural change nobody has modelled. Doc 03 does not mention it at all.

    0c. **THE RESOURCE-TYPE RULE — CHECK THE TYPE, NOT THE NAME** (CTO~Z re-ruled at resource-TYPE level,
       6/6 correlation across everything this project has touched):
         EventBridge **SCHEDULER** entry -> carries `ScheduleExpressionTimezone` -> CAN be ET-anchored, DST-aware
         Classic EventBridge **RULE**    -> NO timezone field exists              -> **STRUCTURALLY UTC-ONLY, ALWAYS**
       Nobody memorizes which resource is which — THE TYPE TELLS YOU. And it predicts the general case:
       **every classic rule in the estate carrying an ET wall-clock contract has a one-hour seasonal drift
       BY CONSTRUCTION, not by oversight.**
       ⚠ CONSEQUENCE THAT MUST BE STATED IN THESE WORDS: `opal-assets-silver-smartx-sweep-daily` fires at
       12:00 ET in EDT, **TWO HOURS AFTER the 10:00 ET deadline — SO IT IS NOT A BACKSTOP FOR THE PUBLISH
       AT ALL. IT IS A NEXT-DAY REPAIR WEARING A BACKSTOP'S NAME.** Anyone reasoning "the sweep covers us if
       the OnSuccess chain fails" is wrong for the deadline that matters.

    0b. NO `--no-paginate` LIST IS ACCEPTED AS EVIDENCE FOR AN ABSENCE OR A DENOMINATOR.
       ⛔ MEASURED 2026-08-06: `aws <svc> list-* --no-paginate` DOES NOT MEAN "return everything without
       paging" — IT MEANS "RETURN ONLY THE FIRST PAGE." Same calls, paginated vs page-1:
         `lambda list_functions`   196 across 4 pages — page 1 returns **50. A 74% SHORTFALL.**
         `events list_rules`       139 across 2 pages — page 1 returns 100.
         `scheduler list_schedules` 16 across 1 page  — 16. No shortfall, BY LUCK.
       WHAT IT NEARLY COST: a `--no-paginate` scan returned ONE SmartX Lambda while four ENABLED schedules
       named four different targets — one step from reporting "two enabled schedules fire at non-existent
       Lambdas," A FABRICATED PRODUCTION OUTAGE. All four exist. Caught only by re-checking each target
       individually WITH a positive control (`mdpf-daily-trigger` returned its name) AND a negative control
       (`zzz-no-such-fn-9999` returned empty), which proved the command shape discriminates and the earlier
       list was the liar.
       THIS IS THE SIBLING OF THE `--query length()` TRAP AND IT IS NASTIER: that one returns a wrong
       NUMBER, THIS ONE RETURNS A WRONG SET — and a filtered `--query` over a truncated page looks exactly
       like a real absence. THE FAILURE SHAPE IS A CLEAN EMPTY RESULT, the same shape as the mangled grep
       and the `2>/dev/null`'d `git show`. PAGINATE EXPLICITLY AND PRINT PAGES.

    1. VENDOR AUTHORIZATION FOR SMARTX SPECIFICALLY, CITED OR FALLBACK TAKEN. Quote Andrew's per-use word
       and confirm it names SmartX, with channel and time.
       FORBIDDEN SHORTCUT, NAMED: a per-use word granted for Orion/Eclipse DOES NOT COVER SMARTX. Do not
       generalize one vendor grant to another. If SmartX is not named, take the S3-side fallback and record
       the unproven residual as an OPEN OBLIGATION — never silently upgraded to a proof.

    2. THE SMARTX JWT CLOCK IS CONFIRMED AGAINST THE LIVE PLANE, WITH THE EXPRESSION CITED. Confirm
       `smartx-jwt-refresher-daily` is ET-anchored (`cron(0 9 * * ? *)`, TZ America/New_York) by reading the
       live schedule, and state the expression you read.
       FORBIDDEN SHORTCUT, NAMED: do not inherit the expression from this TO, from Clock v3, or from any
       ruling document. Clock v3 RECORDS the Orion mint as 12:15Z while the plane RUNS 12:05Z — THE
       GOVERNING CLOCK DOCUMENT IS WRONG ABOUT THE ONE MEMBER IT EXISTS TO PIN. Cite the plane.
       WHY IT REMAINS A CRITERION even though CTO~Z measured it: H11 was a live collision no pack document
       named, found only because someone did the arithmetic. A second-hand clock number is the same class of
       claim that produced the 12:15Z error.

    3. BOTH LEGS PROBED SEPARATELY: `smartx_model_aum_daily` AND `smartx_model_allocation_roster`. Per leg:
       requested partition, returned partition, returned vintage, PASS/FAIL, and the ET wall time of the
       call. A single combined verdict is REJECTED — they are two feeds and your census reports them
       separately.

    4. SAME DATA CONTRACT PROVEN, NOT ASSUMED (doc 03 Phase 0 item 4: "prove the same data contract").
       Compare the early-pull output against the 09:40 incumbent for the SAME trade date: schema, row count,
       model vocabulary, and numeric equality on a named key field. Assertion level is CORRECTNESS, not
       existence — "a file appeared" and "the schema matched" both pass on a wrong-axis value.
       FORBIDDEN SHORTCUT, NAMED: do not accept "the early pull produced output" as proof of contract
       equivalence. Prefer a DIFFERENTIAL invariant (identical row count AND identical values on the key
       field) over an absolute one.

    5. THE ON-SUCCESS CONVERTER PATH IS RETAINED AND ITS BEHAVIOUR UNDER THE EARLY CLOCK IS STATED. If the
       converter does not fire early, the probe measures our plumbing, not the vendor — say so explicitly
       rather than recording a vendor FAIL.

    6. THE 08-05 PRE-REGISTERED RUN IS SEARCHED FOR, WITH THE DENOMINATOR PRINTED. Either produce its
       evidence, or state exactly what you searched (surfaces + volume) so "not found" is a measured result.
       §6's bare "not found" with no denominator is the unsupported-absence shape this program exists to
       stop repeating.

    7. THIRD STATE PRESENT. Each leg resolves to EARLY-VALID / EARLY-INVALID / NOT-PROBED (with reason:
       vendor word absent, endpoint unreachable, converter did not fire). NOT-PROBED is neither of the other
       two. A report with no NOT-PROBED class must show the check that would have produced one.

    8. CLASS A' LANGUAGE HELD. Assert "valid early ON THE DAYS PROBED" and state the number of days.
       RESERVED WORDS PROHIBITED: proof / provably / definitively / source-confirmed. Your own census shows a
       15:38 tail — one clean morning is a sample, not a property of the vendor.

    9. EVERY LANDING-TIME CLAIM CITES THE s3api ISO-8601 VALUE WITH ITS +00:00 OFFSET. An `aws s3 ls`
       timestamp is NOT acceptable evidence — it prints LOCAL time while s3api returns true UTC, and the two
       disagree SILENTLY. This is your own measured hazard and it is now the project-wide citation form.

    10. THE PROBE-FAIL BRANCH IS EXERCISED IF IT FIRES: schedule does NOT shift; lateness is labeled carry
        per Clock v3; publish is NOT held; H2 closes as EARLY-INVALID on the days probed. A complete outcome.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_H2_SMARTX_EARLY_CLOCK_20260807.md</file>
      <file action="reference">docs/architecture/MDPF_GLOBAL_T2C/CLOCK_V3_DELTA_20260804.md</file>
      <file action="reference">data/mdpf/config/partner_roster.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">No SmartX vendor call without Andrew's per-use word NAMING SmartX.</requirement>
    <requirement id="2">Determine SmartX's JWT constraint before proposing any schedule.</requirement>
    <requirement id="3">Probe both legs separately; prove the data contract, not just output existence.</requirement>
    <requirement id="4">Retain the on-success converter path; distinguish plumbing failure from vendor failure.</requirement>
    <requirement id="5">Search for the 08-05 pre-registered run with the denominator printed.</requirement>
    <requirement id="6">On probe-fail take the Clock v3 labeled-carry branch and close the item.</requirement>
    <requirement id="7">Apply nothing. The schedule change lands in P4-1.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">H2 deliverable committed to your lane on SITEZ (push is MSTR~Z's, :55-:00)</deliverable>
    <deliverable type="document">The resolved design reported to COO~Z so P4-1 is written against a decision</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT CALL SMARTX WITHOUT ANDREW'S EXPLICIT PER-USE WORD NAMING SMARTX. A grant for Orion/Eclipse
    is not a grant for SmartX. Availability is not authorization. Running an existing pull suite early
    instead of a bespoke probe does NOT dodge this — the rule is about the WIRE, not the mechanism.</rule>
    <rule>DO NOT MOVE MDPF LATER. Andrew-direct: shift the upstream chains earlier. A later gold clock
    violates the 10:00 ET publish requirement and is not a fix.</rule>
    <rule>DO NOT HOLD A PUBLISH ON VENDOR LATENESS. Lateness is labeled carry, never a held publish.</rule>
    <rule>DO NOT COUPLE THIS PROBE TO P0-2. SmartX is an independent clock; a joint verdict hides which
    vendor failed and makes both results unusable.</rule>
    <rule>DO NOT APPLY ANY SCHEDULE CHANGE IN THIS TO. Probe and decide only.</rule>
    <rule>NO NEW GATES. No approval step, co-sign, GO requirement, or review hold.</rule>
    <rule>NO SHADOWS. Do not stand up a parallel early pull alongside the incumbent to compare over days —
    that is a standing comparator and it is vetoed. A finite ad-hoc run-and-read is what this TO authorizes;
    nothing stands.</rule>
    <rule>NO ALARMS, SNS TOPICS, SES SENDS, FRESHNESS CHECKERS, OR MONITORS. A clock finding lands as a
    finding, never as a detector.</rule>
    <rule>NEVER call a feed stale/late without resolving the TRADING CALENDAR first, in TRADING DAYS.
    Per-feed cadence is NOT one shared date; SmartX is SAME-DAY and Schwab is T-1 (account 08242234, EIGHT
    digits, never 08335338).</rule>
    <rule>DO NOT use the shared dirty checkout as build input. Never rebase on SITEZ. Commit to your lane;
    push is MSTR~Z's at :55-:00. Working files in the scratchpad.</rule>
  </do_not>
</task_order>
