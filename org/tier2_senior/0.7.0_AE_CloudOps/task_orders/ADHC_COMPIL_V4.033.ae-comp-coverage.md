<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.033</id>
    <slug>ae-comp-coverage</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-14</date>
    <status>done</status>
    <completed>2026-05-15</completed>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED — Wave 3 RAVC2 received (890f8d2fe). Wave 4 dispatched 2026-05-15. Not gated on other Wave 4 tools — ships in parallel.</dispatch_unblock_condition>
    <project_code>ADHC_COMPIL_V4</project_code>
    <priority>P2 — Wave 4 standing-discipline hygiene; monthly compliance ratchet</priority>
    <sla>~1.5-2 days wall per PRD §15.4 sizing</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-033 (CTO addition per Andrew direct 2026-05-14)</ref>
    <ref type="anchor">CTO compliance-data dive: 2,435 logged comp-tool runs / 218 unique TOs with ≥1 logged run / 917 completed TOs = 23.8% raw coverage. 298 FAIL results (12.2%). DT 0.4 (321 runs) + DS~D (299) + AE 0.7 (290) lead; RD 0.4.2 (66 runs) outlier.</ref>
    <ref type="cross_link">Wave 4 sibling: .025 skipgate + .030 stale-marker + .032 vectorize-audit. All standing-discipline class.</ref>
  </references>

  <context>
    Raw 23.8% TO compliance coverage on `org/compiler-tools-log.md` is ambiguous: distinguishes "exempt unlogged TO" (legitimate; e.g., status flips, doc-only changes) vs "gated TO that should have logged a comp run but didn't" (noncompliance).

    TO-033 turns the ambiguity into per-agent / per-TO actionable data:
    - Cross-references each completed TO's session log against gated-work classification (FRONTEND / GOLD / API / EXEMPT)
    - Cross-references with `org/compiler-tools-log.md` row matches by TO ID
    - `--by-agent` ranks compliance rate per agent (turns "feels uneven" into "DT 0.4 at 95% / RD 0.4.2 at 30% on gated TOs")
    - CTO runs monthly as compliance ratchet pass

    AE 0.7 primary lane. Implementation: AST walks each TO XML for `<files>` declarations → classifies by path glob → cross-references comp-log row matches by TO ID → emits compliance matrix.
  </context>

  <objective>
    Land `comp-coverage report` subcommand:
    - Walks all completed TOs in `org/tier*/*/task_orders/`
    - Classifies each TO as FRONTEND / GOLD / API / DOC / EXEMPT (path glob on `<files>` declarations)
    - Cross-references `org/compiler-tools-log.md` for matching TO ID rows
    - Emits per-agent compliance matrix + per-TO outlier list (gated TO with 0 logged runs)
    - `--by-agent` per-agent compliance rate ranking
    - `--gated-only` filter to gated-class TOs (drops EXEMPT)
  </objective>

  <scope>
    <files>
      <file action="create">.tools/comp-coverage (new binary OR subcommand under comp-pipescript / comp-validate — your design choice; .tools/comp-coverage cleaner)</file>
      <file action="create">org/modules/graph/coverage-report/REPORT.md (chain-wide rollup; CTO monthly pull artifact)</file>
      <file action="create">org/modules/graph/coverage-report/per-agent/{agent_serial}.yaml (per-agent compliance manifest)</file>
      <file action="readonly_reference">org/compiler-tools-log.md (the corpus this audits against)</file>
      <file action="readonly_reference">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-033</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>find org/tier*/*/task_orders -name "*.md" | wc -l</run>
      <expect>~900+ TO files enumerated (matches CTO's 917 completed TOs baseline).</expect>
      <if_mismatch>If significant drift from 917, surface — corpus may have grown/shrunk meaningfully.</if_mismatch>
    </step>
    <step>
      <run>grep -c "^|" org/compiler-tools-log.md</run>
      <expect>~2,400+ logged rows (matches CTO's 2,435 baseline).</expect>
      <if_mismatch>If significant drift, surface for re-calibration.</if_mismatch>
    </step>
    <step>
      <run>Sample 5 completed TOs across tiers to design path-glob classifier (FRONTEND / GOLD / API / DOC / EXEMPT)</run>
      <expect>Glob taxonomy covers ≥95% of TO file-scope patterns; edge cases (mixed-class TOs) policy decided.</expect>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>comp-coverage report</run>
      <expect>Per-agent matrix + per-TO outlier list. Empirical baseline: ~23.8% raw coverage; ~80%+ gated-only coverage expected for DT 0.4 / DS~D / AE 0.7 leaders.</expect>
      <if_mismatch>STOP. Validate classifier + log-row-matching logic before declaring done.</if_mismatch>
    </step>
    <step>
      <run>comp-coverage report --by-agent</run>
      <expect>Per-agent compliance rate ranked. DT 0.4 / DS~D / AE 0.7 at top. RD 0.4.2 lower (matches CTO's "active-agent outlier" observation).</expect>
    </step>
    <step>
      <run>comp-coverage report --gated-only</run>
      <expect>Drops EXEMPT class. Compliance rate jumps (most exempts are legitimately unlogged).</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>Surface monthly REPORT.md to CTO + Andrew for compliance ratchet review</run>
      <expect>Per-agent outliers flagged for follow-up coaching / TO-template improvements.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `comp-coverage report` walks all completed TOs + classifies + cross-references comp-log.
    AC2: Per-agent compliance matrix matches CTO's manual baseline (~24% raw / higher gated-only).
    AC3: `--by-agent` ranking surfaces outliers (DT/DS~D/AE 0.7 leaders; RD 0.4.2 lower per CTO data).
    AC4: `--gated-only` filter functional + raises compliance rate as expected.
    AC5: REPORT.md + per-agent yaml manifests persisted.
    AC6: Tested empirically against CTO's 2,435 / 917 baseline (matches within ±5%).
    AC7: Session log + RAVC2 MCP to COO + CTO.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: TO file enumeration + comp-log row count + path-glob classifier design
    Phase 2: comp-coverage report + --by-agent + --gated-only
    Phase 3: monthly REPORT surface to CTO + Andrew
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: Wave 1+2+3 RAVC2.

    PARALLEL-OK with Wave 4 siblings.

    DOWNSTREAM CONSUMER: CTO monthly compliance pull + per-agent coaching follow-up + TO-template improvements.

    NO PORTAL / NO DATA-LAYER changes.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Compiler-tool development reading org/* + comp-log; no pipeline touch.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `comp-coverage report` subcommand
    2. REPORT.md chain-wide rollup
    3. Per-agent yaml manifests
    4. Empirical-baseline-match validation
    5. Session log + RAVC2 MCP
  </deliverables>

  <ravc>AE 0.7 RAVC2 to COO + CTO on AC1-7 PASS. CTO surfaces monthly compliance ratchet pulls thereafter.</ravc>

  <notes>
    **Banking observation:** the 23.8% raw coverage IS a meaningful signal even if ambiguous on EXEMPT-vs-gated split — surfaces possible TO-template improvements (clearer EXEMPT marking; mandatory comp-log row when gated).

    **Author identity:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"`.
  </notes>
</task_order>
