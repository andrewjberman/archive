<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.018</id>
    <project>ADHC_COMPIL_V4</project>
    <title>Phase 2 validation pass — run all V4 tools against current Inflection state, surface retroactive findings</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status><!-- Closed 2026-05-08T~PM as SUPERSEDED by V4.OPS triage portfolio per CTO ratification (1.0.0_SA_CTO RAVC2 ACK 20260508T~PM). Original .018 scope ("run all V4 tools against current Inflection state, surface retroactive findings") substantially subsumed by today's same-session ships: .017 OPS test matrix validated all 21 tools across 108 cases; .019 fixed 2 BLOCKING bugs surfaced; .020 fixed cross-layer graph gap (Tier reclassification); .021 fixed 16 doc-drift + UX issues; .022 surfaced 9 BD Lambda permission gaps via IAM backfill. Collectively more thorough than .018's narrower Phase 2 validation. Standing-backlog observations from .020 (INF gold HARDCODED writes) + .022 (22 unresolved Lambdas + 9 perm-gap remediation candidates) tracked separately. -->
    <priority>medium</priority>
    <estimated_effort>~0.5d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §7 (TO decomposition) + §12 (v0.2 addendum) + §13 (v0.3 addendum)</ref>
    <ref type="prerequisite">All V4 P1 active TOs SHIPPED 2026-05-08: .002 (Auto-Rule #6) + .003 (comp-constants) + .007 (lambda-layer-deps doc) + .008 (Inflection-graph) + .009 (--config + symbolic) + .010 (strict-mode) + .011 (schema-check robustness) + .012 (STALE_NODE_WARN) + .013 (EC2 role) + .014 (symbol-lookup) + .016 (synthetic-test). Only .015 (DDB freshness) deferred to post-FIRMSEP.10.</ref>
    <ref type="seed_inputs">org/modules/graph/comp-constants-seed-{bd,inf,multifirm}.yaml + comp-shell-dup-source-baseline.json (DS~B/~C/~D 2026-05-08)</ref>
  </references>

  <context>
    Phase 2 validation: run each newly-shipped V4 tool against the current Inflection codebase state and capture findings.

    **Goal:** zero false-positive gate before declaring V4 Phase 1 fully validated. Surface any retroactive findings (production drift the tools detect that nobody flagged before) for COO/CTO routing.

    **Tools to validate against current state:**
    1. `comp-constants check` (TO-3) — already empirically verified at ship; re-run for compleness
    2. `comp-constants new` (TO-3) — capture full discovery list
    3. `comp-validate <script> --config <path>` (TO-9) — pick 2-3 representative scripts (e.g. INF_D_04 build_dashboard, INF_C_01 canonical_nna)
    4. `comp-platinum reverse --strict` (TO-10) — full repo
    5. `comp-transform schema-check` (TO-11) — pick 2-3 representative React components
    6. `comp-build` STALE_NODE_WARN check (TO-12) — full repo
    7. `comp-iam service ec2-i-XXXX` (TO-13) — pick 2-3 representative EC2 instances
    8. `comp-xref symbol-lookup` (TO-14) — pick 5-10 known multi-site symbols
    9. `comp-pipescript io <inflection-manual_api-script>` (TO-8 extension) — pick 2-3 manual_api scripts

    **Spot-check coordination:** DS~A is currently heads-down on INFNNA cascade INF_C_01 patch. DS~A spot-check (per PRD §7) can happen async — flag findings to COO; will route to DS~A when bandwidth opens.
  </context>

  <scope>
    <step>
      Run each tool with appropriate test inputs (representative samples; not exhaustive). Capture output + any FAIL/WARN findings.
    </step>

    <step>
      Categorize findings:
      - **CLEAN PASS** — tool ran, no findings, expected
      - **EXPECTED FINDING** — tool surfaced known gap (e.g., INFLECTION_REP_IDS drift sites already in queue)
      - **NEW FINDING** — tool surfaced something not previously known; potential production drift
      - **FALSE POSITIVE** — tool surfaced something that should NOT be flagged (gate fail)
    </step>

    <step>
      For each NEW FINDING: brief describe; route to COO with severity assessment. COO routes to DS or other appropriate lane.
    </step>

    <step>
      For each FALSE POSITIVE: file as standing-low backlog item against the originating tool's TO; would be fixed in v1.1 or v2.
    </step>

    <step>
      Append to `org/compiler-tools-log.md` per logging convention. One row per tool run.
    </step>

    <step>
      RAVC2 to COO + CTO with: tool-by-tool pass/fail summary table, NEW finding count, FALSE POSITIVE count, recommendation on whether V4 Phase 1 fully validated or requires touch-up.
    </step>
  </scope>

  <acceptance_criteria>
    1. All 8 V4 tools (excluding .015 deferred) run against current Inflection state with representative inputs.
    2. Each run produces a categorized finding entry (CLEAN PASS / EXPECTED / NEW / FALSE POSITIVE).
    3. NEW findings routed to COO with severity assessment.
    4. FALSE POSITIVES filed as standing-low against originating tool.
    5. compiler-tools-log.md appended with one row per run.
    6. RAVC2 with full tool-by-tool pass/fail summary table + V4 Phase 1 validation verdict.
    7. Session log Compiler Tools section reproduces each run with output.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>ls .tools/comp-constants .tools/comp-pipescript .tools/comp-iam .tools/comp-validate .tools/comp-build .tools/comp-platinum .tools/comp-transform .tools/comp-xref 2&gt;&amp;1 | head -20</run>
        <expect>All 8 tools present and executable.</expect>
        <if_mismatch>If any missing: indicates V4 P1 ship gap; surface to COO before validation.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after ship">
      <step>
        <run>tail -20 org/compiler-tools-log.md</run>
        <expect>Latest entries are this validation pass; one row per tool run.</expect>
        <if_mismatch>Log entries missing; ensure append cycle ran.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure tool-validation pass; no data side-effects.</no_reprocess_needed>
  </data_reprocess_scope>

  <dependencies>
    All V4 P1 active TOs shipped (8/9 done; .015 deferred). DS~A spot-check is async — can land post-cascade-close.
  </dependencies>
</task_order>
