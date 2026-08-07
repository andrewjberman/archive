<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-07-r19-freshness-gate-class</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-08-07</date>
    <status>pending</status>
    <project_code>MDPF_CANPLAT</project_code>
  </metadata>

  <objective>
    Execute R-19 of the MDPF remediation register: **retire the FRESHNESS-GATE CLASS.** A gate that
    defers SILENTLY is the wrong mechanism; labelled carry publishes with the truth attached. Retire
    the gates (a)–(f); **KEEP every numerical assertion.**
  </objective>

  <context>
    PRD: `docs/architecture/MDPF_REMEDIATION_REGISTER.md` @e5e932caf6 §2f. Andrew took the register AS
    THE PRD 2026-08-07 ~1910Z, VERBATIM: *"take the remediation plan as the PRD and decompose it to TOs
    for the relevant agents."*

    ANDREW-DIRECT 2026-08-07 ~0310Z, VERBATIM: *"There should be no freshness gates, all of this needs
    to go, add it to the remediation doc"* — consistent with his 08-06 word: *"clean up a lot of these
    extraneous gates and halt functions because i suspect that miscalibrated halts or gates are
    preventing us from publishing."*

    >> **THE DISTINCTION THAT MAKES THIS EXECUTABLE — carry it into every change:**
    **A GATE BLOCKS. AN ASSERTION RECORDS. THE GATES GO; THE ASSERTIONS STAY.**
    ⚠ *"No freshness gates"* must NOT be read as *"stop measuring freshness."* **Measuring is how carry
    gets labelled honestly. What dies is freshness measurement WIRED TO A DISPATCH DECISION.**

    ⛔ **THIS IS A DESIGN REMEDIATION, NOT A GOAL-3 UNBLOCK — base-CTO ADJUDICATED 2026-08-07 191307Z
    AND THE DISTINCTION IS LOAD-BEARING.** The register poses a tension: Andrew FILED R-19 behind the
    build, but gate (a) is the measured blocker on goal 3. **It dissolves.** `_check_inf_spine` reads
    `pipeline-complete.json`, which I re-measured at the COO seat today: **`run_date` 2026-07-31,
    unadvanced, eight days.** The gate is **NOT miscalibrated — it is correctly reporting that INF is
    down**, and the root cause (INF_C_01's coverage guard refusing on five accounts assigned to a rep
    missing from a hand-drawn allowlist) is **separately dispatched**. So goal 3 unblocks via the INF
    fix, not via this TO. **Do not treat retiring the gate as the way to make current data appear, and
    do not route a promotion question to Andrew — that answer arrived as a bug fix.**
    The DESIGN direction stands on its own merits regardless: *a gate that defers silently for seven
    days is the wrong mechanism whether or not its input is currently true.*

    THE INVENTORY (register §2f):
      a  `_check_inf_spine` — sentinel gate, `mdpf-daily-trigger:349-363`, LIVE, deferring 7 days
      b  `GATE_ENFORCE` + the trigger convergence gate — LIVE (=1)
      c  `_check_bd_silver` — BD silver vs its own cadence — LIVE
      d  Stage 0.5 — wait for Eclipse gold sentinel — on the EC2
      e  Stage 2.5 — hard-defer custody gate — **RETIRE AS HALT, KEEP THE NUMERICAL ASSERTION**
      f  Stage 0 — Orion token approval gate — on the EC2
      g  `inf-gold-freshness-guard.tf` — INF's OWN alarm, same sentinel, **CROSS-PROGRAM**
      h  `mdpf-freshness-checker` — **ALREADY ABSENT** (COO re-verified: ResourceNotFoundException)

    WHAT REPLACES THEM: **read the DATA's own frontier, never a marker** —
    `lib/trading_calendar`'s `expected_last_trading_day` / `trading_days_behind`, per feed, per its
    roster cadence. **The working reference implementation is IN THE SAME FUNCTION as the broken one:**
    the 49financial leg reads `latest_partition` and returns `trading_days_behind: 2, read_status: OK`
    while the inflection leg reads a marker. Copy the leg that works.
  </context>

  <compiler_tools_mandate>
    Phase 1: <run>comp-blast _check_inf_spine</run> — every caller before you touch it.
             <run>comp-iam service mdpf-daily-trigger</run> — permissions before any deploy.
    Phase 2: <run>.tools/commit-gate.sh</run>
    Phase 3: <run>comp-aws</run> / live `aws lambda get-function-configuration` on the changed function
             — DESIRED and APPLIED both, per Rule 22a. A comp-tool cannot tell landed from planned.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: `mdpf-daily-trigger` Lambda · the `mdpf-daily-runner` EC2 stages · **and (g)
      `inf-gold-freshness-guard.tf`, which is CROSS-PROGRAM (INF, not MDPF).**
    - required_action: **(g) is NOT yours to retire unilaterally.** It is INF's own alarm on the same
      sentinel. Surface it to CTO with your finding and STOP there.
    - >> **W1-3 (the R-20 sentinel census) IS SEQUENCED BEHIND THIS TO on `pipeline-complete.json`.
      See criterion 1.**
  </cross_domain_coordination>

  <acceptance_criteria>

    >> 1. ⛔ **THE HARD ORDERING CONSTRAINT — RETIRE THE READER BEFORE ANYONE TRASHES THE OBJECT.**
       `pipeline-complete.json` is R-20's first TRASH example **AND** the object gate (a) reads.
       **R-19(a) LANDS FIRST. R-20's sentinel deletion SECOND. NEVER THE REVERSE.**
       Delete the sentinel while `_check_inf_spine` is live and you get a live reader against a deleted
       object — **and we exercised that exact failure TWICE today.** A bare `ddb.scan()` against the
       table Andrew deleted **RAISES** and would hard-fail tomorrow's 09:00 fire; the
       comp-surface-check retirement is its **silent twin** — a gate whose target cannot be found does
       not fail loudly, it **SKIPS**. *One fails loud, one fails silent, and you do not get to choose
       which.* **When (a) is retired, tell COO in the same turn — that is what releases W1-3.**

    2. GATES (a)–(f) NO LONGER BLOCK DISPATCH. For each, state in the deliverable: retired / kept-as-
       assertion / not-found, with the file:line and a vintage.

    3. >> **EVERY NUMERICAL ASSERTION SURVIVES — this is the criterion that can be failed by doing the
       TO too well.** (e) specifically: *"RETIRE AS HALT. Preserve the numerical assertion per
       channel."* Per-channel validation, numerical identities, schema checks and reconciliation
       **remain data assertions and must not become approval gates or cross-partner halts.**
       ⛔ A run in which assertion COUNT dropped has removed safety, not a gate. Report the count
       before and after with its denominator.

    4. THE REPLACEMENT IS EXERCISED, NOT CONFIGURED. Show the frontier read returning
       `trading_days_behind` for at least one feed **and** a mutant in which a stale feed produces a
       LABELLED CARRY rather than a held dispatch. ⛔ Rule 22a: a config read is not a behavioural
       claim.

    5. (g) SURFACED TO CTO, NOT RETIRED. (h) confirmed already-absent rather than assumed.

    6. Session log with a Compiler Tools section and an archetype tag.

  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py</file>
      <file action="modify">infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh</file>
      <file action="reference">infra/aws/terraform/.../inf-gold-freshness-guard.tf</file>
      <file action="reference">lib/trading_calendar.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Retire (a)–(f) as BLOCKERS; keep every assertion.</requirement>
    <requirement id="2">Replace marker-reading with the data's own frontier, copying the 49F leg.</requirement>
    <requirement id="3">Notify COO the moment (a) is retired — it releases W1-3.</requirement>
    <requirement id="4">Terraform is the only Lambda deploy mechanism; `safe-apply`, never bare apply.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">The retirements, gate-passed and deployed via Terraform.</deliverable>
    <deliverable type="document">Per-gate disposition table + assertion count before/after + the
    exercised frontier read and its mutant.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section.</deliverable>
  </deliverables>

  <do_not>
    <rule>⛔ DO NOT delete `pipeline-complete.json` or any sidecar object. This TO retires READERS.
    Deletion is W1-3 and it comes SECOND.</rule>
    <rule>DO NOT remove any numerical assertion, identity check, schema check or reconciliation.</rule>
    <rule>DO NOT retire (g) `inf-gold-freshness-guard.tf` — cross-program. Surface it.</rule>
    <rule>DO NOT treat this as the goal-3 unblock, and do not route a promotion question to Andrew.</rule>
    <rule>DO NOT build a replacement alert, alarm, SNS topic, SES send, freshness checker or monitor.
    The moratorium is standing and this TO is the opposite of that instinct.</rule>
    <rule>DO NOT run bare `terraform apply` or `aws lambda update-function-code`.</rule>
  </do_not>
</task_order>
