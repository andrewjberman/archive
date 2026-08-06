<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-h1-inflection-early-clock</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-06</date>
    <status>staged</status>
    <project_code>MDPF_CANRTE</project_code>
  </metadata>

  <objective>
    Establish whether the Inflection binding inputs (Orion Assets + Eclipse portfolios) can land in canonical
    silver by 08:40 ET, so the 09:00 ET gold floor sees them — WITHOUT moving MDPF later and WITHOUT
    re-opening the Orion JWT race. Determine whether the Wave B (14:16Z) schedule can move earlier as a unit.
  </objective>

  <context>
    Andrew's Clock v3 requirement is binding: platinum publishing complete by 10:00 ET for all four scopes.
    His words, 2026-08-04 ~00:10 ET, VERBATIM: "we are not waiting for 12:15p to publish all that, it needs
    to be published by 10a ET. Which means that any chains associated with that publishing need to be
    identified and shifted earlier as needed." SHIFT THE UPSTREAM CHAINS EARLIER; DO NOT MOVE MDPF LATER.
    That conclusion is his sentence, not a reviewer's inference.

    YOUR OWN 30-DAY CENSUS ALREADY RESHAPED THIS ITEM and it is accepted:
    - Eclipse misses the 08:40 bar 1 of 21 days (normal landing 23:30 ET, 9.2h EARLY). The two exceptions
      reproduce the pack's July 16 / August 6 observations exactly.
    - ORION MISSES 20 OF 21, every day, at 10:16 ET. The "prior-settled semantics" the pack treats as an
      edge case IS THE EVERYDAY PATH.
    - Two waves: WAVE A (23:30 ET prior day — Eclipse normally, bd_holdings, bd_allocations; already 9.2h
      early, DOES NOT MOVE) and WAVE B (14:16Z / 10:16 ET — Orion every day, and the destination of both
      Eclipse exceptions). ONE MOVE OF WAVE B fixes Orion's structural miss AND removes the Eclipse
      exception, because the exception is Eclipse falling into Wave B.

    That collapses doc 03 Phase 0 item 4's branch (move-as-a-unit vs MDPF-row-subset): the unit has a
    concrete identity. Prove or refute THAT shape; do not re-open the question from scratch.

    ### H11 — HARD FLOOR ON PROBE DESIGN (CTO~Z @70733b907, and no pack document names it)

    Clock v3 Amendment 1 pins the Orion JWT renewal UTC-FIXED at 12:15Z, both regimes, deliberately off the
    12:00/12:30 hazard marks. It exists because the chain's stage-0 read an expired `orion/jwt/current`
    TWELVE SECONDS before the fresh one landed -> 401 x 9 MODELS.

    | | EDT | EST |
    |---|---|---|
    | Orion JWT mint (UTC-fixed 12:15Z) | 08:15 ET | 07:15 ET |
    | Required: silver present | 08:40 ET | 08:40 ET |
    | USABLE ORION PULL WINDOW | 08:15-08:40 ET = 25 MINUTES | 85 min |

    EDT IS THE BINDING REGIME AND THE WINDOW IS 25 MINUTES. Any Orion pull earlier than 08:15 ET in EDT
    reads an expired token and re-opens exactly the race Amendment 1 closed.

    THE FAILURE THIS PREVENTS: a probe run at 07:45 ET would very possibly PASS — and that pass is
    WORTHLESS, because it certifies an hour production can never use. It would then be recorded as closing
    H1 while licensing a schedule move that re-opens the 401 race.

    ### H12 — THE PROBE-FAIL BRANCH IS ALREADY RULED. DO NOT INVENT ONE.

    Doc 03 Phase 0 item 4 enumerates two branches and BOTH PRESUPPOSE early data exists. There is no branch
    for "the vendor cannot deliver earlier at all" — the outcome this probe exists to test for. The branch
    is not missing from the estate; the pack dropped it. Clock v3 rules it:

      SHIFTS LAND ON PROBE PASS. VENDOR LATENESS SURFACES AS LABELED CARRY (2 TD window, every carried point
      labeled, transition visible) — NEVER AS A HELD PUBLISH.

    So a negative probe is a COMPLETED probe, not a blocked one: the schedule does not shift, lateness is
    carried with an honest label, the 10:00 ET publish deadline still holds. Do not stall, do not escalate
    for a new design, do not invent a compensating path.

    ### CLASS A' — WHAT THIS PROBE MAY AND MAY NOT ASSERT

    CTO~Z classifies H1 as Class A': measurement of a VENDOR WE DO NOT CONTROL. The result is a SAMPLE, not
    a durable fact. A closure may assert "valid early ON THE DAYS PROBED" and nothing stronger. Run the
    probe, then build a design that DOES NOT DEPEND ON THE SAMPLE GENERALIZING — which is exactly what
    Clock v3's labeled-carry rule already provides.

    ### VENDOR EGRESS — READ THIS BEFORE YOU RUN ANYTHING

    Probing the Orion/Eclipse endpoints is an EXTERNAL VENDOR API CALL. CLAUDE.md Agent Autonomy: never call
    a non-Opal vendor API without Andrew's explicit per-use word. AVAILABILITY IN THE TOOLSET IS NOT
    AUTHORIZATION. You flagged this correctly before the TO was written.

    MSTR~Z surfaced the ask to Andrew in-session. MSTR also confirmed there is NO WAY AROUND IT: running our
    existing INF pull suite early as an ad-hoc QA run does NOT dodge the rule — the rule is about THE WIRE,
    not the mechanism.

    IF HIS WORD HAS ARRIVED: run the vendor probe inside the H11 window.
    IF IT HAS NOT ARRIVED BY YOUR WINDOW: execute the S3-SIDE FALLBACK BELOW. It is PRE-APPROVED by MSTR~Z
    and needs NO second escalation. Do not cross the vendor line on schedule pressure.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-which "what feeds the inflection MDPF silver and on what schedule"</run>
      <expect>Routes to comp-estate / comp-trigger, or runs comp-grep on-rails.</expect>
      <if_mismatch>Repeat override for one intent = COVERAGE GAP -> report to COO~Z (Rule 21).</if_mismatch>

      <run>comp-trigger inf</run>
      <expect>The INF mirror + pull-suite schedules with the DENOMINATOR PRINTED (rules + schedules scanned).</expect>
      <if_mismatch>comp-trigger renders scheduler rows as `schedule: -` — it structurally does not expose
      ScheduleExpression/timezone. Ground-truth expressions on the live primitive per Rule 22a; do NOT read
      a `-` as "no schedule".</if_mismatch>

    Phase 2 — before committing:
      <run>comp-blast &lt;each schedule/handler you propose to move&gt;</run>
      <expect>Blast radius WITH DENOMINATOR. Every consumer of a moved schedule named.</expect>
      <if_mismatch>A consumer outside MDPF in the radius = STOP, message COO~Z. A zero is a LOWER BOUND, not absence.</if_mismatch>

    Phase 3 — after committing: record the probe outcome + the branch taken (PASS -> shift, FAIL -> labeled carry) in the session log Compiler Tools table.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>The INF ingest-mirror + Orion pull schedules (upstream modules)</shared_resource>
    <also_in_to>P4-1 (TF route cutover applies the pre-resolved clock changes) · P5-1 (Phase 5 step 7 applies upstream clock modules FIRST)</also_in_to>
    <last_write_owner>0.7.0_AE_CloudOps~Z</last_write_owner>
    <required_action>THIS TO PROBES AND DECIDES; IT APPLIES NOTHING. The schedule change lands in P4-1.
    Report the resolved design to COO~Z so P4-1 can be written against a decided branch rather than an open
    one — doc 03 Phase 0 is explicit that the branch resolves BEFORE the apply and that both designs are
    never deployed and compared in production (that would also be a shadow).</required_action>

    <shared_resource>Orion JWT (`orion/jwt/current`, UTC-fixed 12:15Z mint)</shared_resource>
    <also_in_to>H11 standing constraint — binds any Orion clock work in any TO</also_in_to>
    <required_action>Do not propose moving the JWT mint to widen the window. The UTC-fixed clock IS
    Amendment 1's remedy. If 25 minutes proves insufficient, that is a FINDING about the achievable clock,
    reported to COO~Z -> CTO~Z, not a constraint to engineer around.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. THE PROBE RAN INSIDE THE H11 WINDOW, OR DID NOT RUN AT ALL. Cite the wall-clock ET time of each
       Orion call and confirm every one is >= 08:15 ET (EDT). A probe executed before 08:15 ET is REJECTED
       even if it succeeded.
       FORBIDDEN SHORTCUT, NAMED: do not "prove earlier is fine" by probing at 07:45 and reporting a PASS.
       That pass certifies an hour production can never use and would license re-opening the 401x9 race.

    2. ROW-LEVEL RESULT, NOT AN AGGREGATE VERDICT. Per endpoint AND per row-family the all-row INF mirror
       carries: requested partition, returned partition, returned source vintage, PASS/FAIL. State the
       DENOMINATOR — rows the mirror carries vs rows probed.
       WHY: your own census showed the pack's emphasis was backwards (Orion 20/21 vs Eclipse 1/21). An
       aggregate verdict hides exactly that asymmetry.

    3. THE MOVE-AS-A-UNIT SHAPE IS EXPLICITLY PROVEN OR REFUTED. State whether every row Wave B carries is
       valid at the earlier hour. If some rows are not, name them and state which branch you took:
       move-the-unit, or MDPF-row-subset early with the later invocation retained as full reconciliation.
       THE BRANCH IS RESOLVED IN THIS TO. Doc 03: do not deploy both designs and compare them in production.

    4. THIRD STATE PRESENT AND NAMED. Every endpoint/row resolves to exactly one of: EARLY-VALID /
       EARLY-INVALID / NOT-PROBED (with the reason: vendor word absent, endpoint unreachable, out of window).
       NOT-PROBED != EARLY-INVALID and NOT-PROBED != EARLY-VALID. A report with no NOT-PROBED class must show
       the check that would have produced one.

    5. CLASS A' LANGUAGE HELD. The deliverable asserts "valid early ON THE DAYS PROBED" and states the number
       of days probed. RESERVED WORDS PROHIBITED: proof / provably / definitively / source-confirmed. A
       single morning's PASS is a sample of a vendor we do not control.

    6. THE PROBE-FAIL BRANCH IS EXERCISED IF IT FIRES. On a negative result the deliverable records: schedule
       does NOT shift; lateness is labeled carry per Clock v3 (2 TD window, every carried point labeled,
       transition visible); publish is NOT held; H1 closes as EARLY-INVALID on the days probed. That is a
       COMPLETE outcome. Do not stall, do not escalate for a new design, do not invent a compensating path.

    7. VENDOR AUTHORIZATION CITED OR FALLBACK TAKEN. Either quote Andrew's per-use word with its channel and
       time, or state plainly that it did not arrive and that the S3-SIDE FALLBACK was executed:
       bound what S3 landing evidence can bound, and RECORD THE UNPROVEN RESIDUAL AS AN OPEN OBLIGATION —
       never silently upgraded into a proof. The fallback is pre-approved; no second escalation.

    8. EVERY LANDING-TIME CLAIM CITES THE s3api ISO-8601 VALUE WITH ITS +00:00 OFFSET. An `aws s3 ls`
       timestamp is NOT acceptable evidence.
       WHY, MEASURED BY YOU: `s3 ls` prints LastModified in LOCAL time while s3api returns true UTC. Your
       first two passes read Eclipse landing 06:16 ET, which WOULD HAVE COLLAPSED H1 and pointed the whole
       clock workstream at a problem that does not exist. The two instruments disagree SILENTLY and both
       look like evidence.

    9. BULK-BACKFILL EXCLUSION STATED. Carry your structural rule (>1 partition sharing one landing minute
       is a backfill rewrite, excluded from the daily clock) and say so in the deliverable — without it a
       backfill makes an on-time feed read late forever after.

    10. THE METHOD LIMIT IS CARRIED VERBATIM: silver LastModified measures WHEN THE CONVERTER WROTE, not
        when the vendor made data available. An S3-side census BOUNDS THE CURRENT PIPELINE CLOCK and DOES
        NOT PROVE data is obtainable earlier. No sentence in this deliverable may claim otherwise.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_H1_INFLECTION_EARLY_CLOCK_20260807.md</file>
      <file action="reference">docs/architecture/MDPF_GLOBAL_T2C/CLOCK_V3_DELTA_20260804.md</file>
      <file action="reference">data/mdpf/config/partner_roster.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Orion calls occur at or after 08:15 ET (EDT). Cite each call's ET wall time.</requirement>
    <requirement id="2">Prove or refute the Wave B move-as-a-unit shape at row level, with denominator.</requirement>
    <requirement id="3">Resolve the Phase 0 item 4 branch in this TO. Never deploy both designs to compare.</requirement>
    <requirement id="4">On probe-fail, take the Clock v3 labeled-carry branch and close the item.</requirement>
    <requirement id="5">No vendor call without Andrew's explicit per-use word. Fallback needs no escalation.</requirement>
    <requirement id="6">Apply nothing. The schedule change lands in P4-1.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">H1 deliverable committed to your lane on SITEZ (push is MSTR~Z's, :55-:00)</deliverable>
    <deliverable type="document">The resolved branch, reported to COO~Z so P4-1 is written against a decision</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT CALL AN EXTERNAL VENDOR API WITHOUT ANDREW'S EXPLICIT PER-USE WORD. Availability is not
    authorization. Running the existing INF pull suite early instead of a bespoke probe does NOT dodge this
    — the rule is about the WIRE, not the mechanism.</rule>
    <rule>DO NOT PROBE ORION BEFORE 08:15 ET IN EDT. The JWT is UTC-fixed at 12:15Z and an earlier read
    re-opens the 401x9 race Amendment 1 closed.</rule>
    <rule>DO NOT propose moving the JWT mint earlier to widen the window.</rule>
    <rule>DO NOT MOVE MDPF LATER. Andrew-direct: shift the upstream chains earlier. A later gold clock
    violates the 10:00 ET publish requirement and is not a fix.</rule>
    <rule>DO NOT HOLD A PUBLISH ON VENDOR LATENESS. Lateness is labeled carry, never a held publish.</rule>
    <rule>DO NOT APPLY ANY SCHEDULE CHANGE IN THIS TO. Probe and decide only.</rule>
    <rule>NO NEW GATES. No approval step, co-sign, GO requirement, or review hold.</rule>
    <rule>NO SHADOWS. Do not deploy both branch designs and compare them in production — doc 03 forbids it
    and it is also a standing-comparator violation.</rule>
    <rule>NO ALARMS, SNS TOPICS, SES SENDS, FRESHNESS CHECKERS, OR MONITORS. Standing moratorium. A clock
    finding lands as a finding, never as a detector.</rule>
    <rule>NEVER call a pipeline stale/late without resolving the TRADING CALENDAR first, counting in TRADING
    DAYS. Per-feed cadence is NOT one shared date: SmartX same-day / Schwab T-1 (account 08242234, EIGHT
    digits) / Eclipse T-1 / Orion same-day-declared with prior-settled semantics / Cottonwood roster
    same-day / Cottonwood holdings + allocations D+2.</rule>
    <rule>DO NOT use the shared dirty checkout as build input. Never rebase on SITEZ. Commit to your lane;
    push is MSTR~Z's. Working files in the scratchpad.</rule>
  </do_not>
</task_order>
