<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.0.4-refactor-execution</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Execute the CTO-approved file-move plan from W5.0.3. Refactor `portal/src/pages/AdvisorIntelligence/` into `_shared/` primitives + `_partners/49financial/` overrides + `_partners/inflection/` stubs. Wire `index.tsx` to the agreed partner-router pattern. Deliver a build-clean, type-check-clean, 49F-regression-clean tree.
  </objective>

  <context>
    PRD §7.3. Blocked on W5.0.3 CTO sign-off. Execution follows the approved file-move plan exactly — no scope creep. Rule of thumb: prefer composition (shared primitives + partner prop injection) over conditional branches in shared code. Inflection stubs are empty placeholder files — no Inflection data yet.

    This is the biggest DE TO in the wave. Expect 1-2 days of execution. Run `/frontend-dev` against AdvisorIntelligence constitution after every significant file move to catch rendering regressions early.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    <run>comp-transform schema-check AdvisorIntelligence</run>
    <expect>Baseline schema (matches W5.0.1 + W5.0.3 signed-off state). Any drift = something changed — flag before starting.</expect>

    <run>comp-blast AdvisorIntelligence</run>
    <expect>No new downstream nodes vs W5.0.3 review. Blast radius stable.</expect>

    Phase 2 (incremental, after each significant file move):
    <run>bun run build (or bunx tsc -b)</run>
    <expect>Zero TypeScript errors. Run after each batch of moves.</expect>

    <run>/frontend-dev (AdvisorIntelligence constitution)</run>
    <expect>PASS on 49F golden path: leaderboard loads, books tab loads, distribution tab loads. No regressions.</expect>

    Phase 3 (after all moves complete):
    <run>comp-transform schema-check AdvisorIntelligence</run>
    <expect>0 MISSING fields. UNUSED count same or lower vs baseline (refactor should not introduce new UNUSED fields). NOTE fields are expected aliases.</expect>

    <run>comp-blast AdvisorIntelligence</run>
    <expect>Blast radius identical to Phase 1.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `portal/src/pages/AdvisorIntelligence/` — no other concurrent TOs should touch this tree during refactor. Coordinate with DT (W5.5-W5.9 which depend on this landing).
    last_write_owner: 0.4.0_DE_ClientPlatform.
    required_action: "Ping COO when W5.0.4 starts so W5 TOs stay staged until confirmed clean."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Target folder structure (`_shared/`, `_partners/49financial/`, `_partners/inflection/`) exists per approved proposal.
    2. `bun run build` zero errors.
    3. `comp-transform schema-check AdvisorIntelligence` 0 MISSING fields.
    4. `/frontend-dev` AdvisorIntelligence constitution PASS on 49F data.
    5. No inline `'49financial'` string literals in `_shared/` components (those stay in `_partners/49financial/`).
    6. `_partners/inflection/` stubs committed (placeholder `.tsx` files, may render nothing yet — acceptably empty).
    7. Session log at `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-04-{NN}/advi_inflec_w5_0_4_refactor.md` with comp-transform runs, build output, frontend-dev pass record.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/** (all moved per approved plan)</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/_shared/</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/_partners/49financial/</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/_partners/inflection/</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on W5.0.3 CTO sign-off.</requirement>
    <requirement id="2">No new inline 49F hardcodes introduced. Remove any found during moves.</requirement>
    <requirement id="3">Incremental build checks — don't accumulate TS errors across a full-day batch.</requirement>
    <requirement id="4">Inflection stubs are empty/placeholder — no data logic yet.</requirement>
    <requirement id="5">Commit with `--only` per commit scope discipline. Author 0.4.0_DE_ClientPlatform.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Refactored AdvisorIntelligence/ tree — build clean, schema clean.</deliverable>
    <deliverable type="document">Session log with all compiler/frontend-dev runs.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start before W5.0.3 sign-off.</rule>
    <rule>Do NOT add Inflection data logic — stubs only.</rule>
    <rule>Do NOT leave inline '49financial' literals in _shared/ components.</rule>
    <rule>Do NOT skip incremental build checks.</rule>
  </do_not>
</task_order>
