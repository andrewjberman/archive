<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-canplat-p0-2r</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-06</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MDPF_CANPLAT, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
    <project_code>MDPF_CANPLAT</project_code>
    <supersedes>ADOPTS MDPF_CANRTE.P0-2 + MDPF_CANRTE.P0-3 (bodies @a6ae64326) as this TO's content; those TOs are superseded as dispatch</supersedes>
    <governing>PRD @24d3eb2f8 (build plane: the upstream clock question) · CONTRACT @a3106d585 (A2/A9 feed off this answer)</governing>
    <clock>⏰ ORION WINDOW: 08:05–08:40 ET, 2026-08-07 (EDT). A probe that misses the window slips a day — a slip, not an incident. Do not fire early to avoid the slip.</clock>
  </metadata>

  <standing_instruction>
    ⛔ PRD §0, VERBATIM — THE OPERATING INSTRUCTION FOR THIS ENTIRE PROGRAM:

    > **ANDREW-DIRECT, 2026-08-06, VERBATIM:**
    > *"This is exactly correct. I need you to persist this exactly as laid out here as a PRD and issue that
    > to COO for decomposition. I just terminated every fabric agent's session on this device aside from you
    > and mstr~z because I want them respawned with this being fresh context and instruction. **I do not want
    > them to go off the rails on hunting down errors, just do what is described here.**"*

    **BUILD WHAT §2 DESCRIBES. DO NOT HUNT ERRORS.**

    - **A number that surprises you is NOT a finding.** The business logic is **correct and live** — it
      renders properly in Portal PROD today. This is a **SHAPE** project.
    - **The only defects in scope are SHAPE divergences**: a field present on one scope and absent on a
      sibling, or a value a producer never emits. **Everything else is out of scope**, however interesting.
    - **If you find something that looks wrong: REPORT IT, DO NOT CHANGE IT.** One line to COO~Z. Then
      continue the work in §2. Do not open an investigation. Do not widen a task order.
    - **Prior context is deliberately not being restored.** The predecessor sessions found real defects for
      three days and became primed to read every surprising number as a bug. **You are fresh so that you are
      not.** Do not go looking for the previous session's threads.

    > **TREATING A CORRECT NUMBER AS A FINDING IS HOW A WORKING PIPELINE GETS "FIXED."**

    SURPRISE CHANNEL: anything that looks wrong = ONE LINE to 2.0.0_SA_COO~Z, subject beginning
    `SURPRISE:`, then continue. No investigation, no change, no widening. COO triages.
  </standing_instruction>

  <objective>
    Execute the two vendor early-clock probes — H1 Orion/Inflection (adopted MDPF_CANRTE.P0-2 body
    @a6ae64326) and H2 SmartX (adopted MDPF_CANRTE.P0-3 body @a6ae64326) — to establish whether the
    binding silver inputs can land by 08:40 ET so the 09:00 ET gold floor (CONTRACT A2) sees same-day
    data. **Observation only. No schedule moves, no infra changes, no JWT moves in this TO.**
  </objective>

  <authorization>
    **EGRESS IS GRANTED.** Andrew-direct at the MSTR~Z terminal, verbatim: **"You have egress."**
    Scope: **Orion Assets + Eclipse endpoints, READ-ONLY, 2026-08-07 morning.** This TO is the seat of
    that grant (MSTR~Z ruled the probe PROCEEDS — the reset was about posture, not about revoking granted
    work; it rides this dispatch, no side-channel GO). Anything outside that endpoint set or that morning
    is NOT covered — CLAUDE.md vendor-egress rule otherwise binds in full.
  </authorization>

  <constraints_verbatim>
    Carried VERBATIM per MSTR~Z + CTO~Z (both deliveries identical in substance):

    - **THE ORION PROBE CANNOT FIRE BEFORE 08:05 ET (EDT).** Below that floor the JWT has not refreshed,
      so a FAILURE is a credential artifact and a PASS is yesterday's token — both answer a different
      question than the one asked, and both would be recorded as closing the item. Window: 08:05–08:40 ET.
    - **ORION MUST NOT MOVE; SMARTX MAY.** The two vendors' JWT floors are anchored in OPPOSITE time bases
      (EventBridge Scheduler = ET-anchored; classic rule = structurally UTC-only). "Shift the chains
      earlier" is correct for SmartX and WRONG for Orion — moving Orion re-opens a race a prior amendment
      deliberately closed. Orion's pull adapts to its floor; the mint stays `cron(5 12 * * ? *)` UTC-fixed
      (12:05Z BY DESIGN, off the 12:00/12:30 hazard marks — and note the plane runs 12:05Z while the old
      clock record says 12:15Z; CITE THE PLANE).
  </constraints_verbatim>

  <adoption_notes>
    The adopted bodies' compiler_tools_mandate, acceptance criteria, and do_not lists stand, with these
    reads: their "IF HIS WORD HAS ARRIVED" conditionals RESOLVE TO: **it has arrived** (authorization
    above) — the S3-side fallback is moot unless the window is missed; their references to spec §/CANRTE
    wave numbering resolve to this program (MDPF_CANPLAT); **SHIFTS DO NOT LAND IN THIS TO** — the
    adopted "shifts land on probe pass" clause means the probe RESULT authorizes a LATER, separately
    GO'd schedule change (SmartX only), never a same-TO move.
  </adoption_notes>

  <acceptance_criteria>
    1. **THE ORION PROBE RAN AT OR AFTER THE 08:05 ET FLOOR, OR DID NOT RUN AT ALL** (adopted P0-2
       criterion 1, verbatim force): cite the wall-clock ET time of each Orion call; every one >= 08:05 ET.
       A probe executed before 08:05 ET is VOID and is reported as NOT-RUN, whatever it returned.
    2. **THE ORION JWT MINT IS NOT MOVED, AND THE DELIVERABLE SAYS SO** (adopted P0-2 criterion 1a).
    3. **THE SMARTX JWT CLOCK IS CONFIRMED AGAINST THE LIVE PLANE, EXPRESSION CITED** (adopted P0-3
       criterion: `smartx-jwt-refresher-daily` ET-anchored, read from the live rule, not the record).
    4. **RESULT REPORTED SAME MORNING** to 2.0.0_SA_COO~Z + 1.0.0_SA_CTO~Z: per-vendor
       PASS / FAIL / NOT-RUN, with the ET wall-clock citations and what the result authorizes next
       (SmartX shift proposal = a separate TO; Orion pull adaptation = design input to A2). A result that
       would OPEN a big finding needs a second oracle before it is reported as one (adopted 9f).
    5. **ONE-LINE STATE REPORT ON MDPF_CANRTE.P0-7** (EC2 code capture): did the capture complete, yes/no
       + evidence pointer. Do NOT execute P0-7 — it is superseded as dispatch; COO re-seats if open.
  </acceptance_criteria>

  <do_not>
    <rule>DO NOT fire Orion before 08:05 ET, ever, for any reason including "just to test auth."</rule>
    <rule>DO NOT move, edit, or propose-in-code ANY schedule, rule, scheduler, or JWT mint in this TO.
    Read-only on infra; read-only on vendor endpoints, scoped to the grant above.</rule>
    <rule>DO NOT touch anything outside Orion Assets + Eclipse endpoint scope; SmartX probe uses existing
    Opal-side infrastructure and live-plane reads only.</rule>
    <rule>NO alarms, SNS, SES, freshness checkers, monitors (standing moratorium).</rule>
    <rule>NO error-hunting (§0). SURPRISE: line to COO~Z, then continue.</rule>
    <rule>Commit to your lane on SITEZ; push is MSTR~Z's (:55–:00); never rebase; scratchpad for working
    files.</rule>
  </do_not>

  <deliverables>
    <deliverable type="document">Probe evidence: per-call ET wall-clock, endpoint, HTTP result class, JWT vintage evidence; per-vendor verdict</deliverable>
    <deliverable type="message">Same-morning result to COO~Z + CTO~Z; P0-7 one-liner</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>
</task_order>
