<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.011</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-transform schema-check robustness — types resolution (parent-dir walk) + AST-aware handler-local-param filter + machine-readable severity column</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status><!-- Authored by CTO direct per Andrew 2026-05-08 PM "distribute the Task orders" delegation. PRD v0.2 addendum §12.4 TO-11. Sequencing: independent (no dep on other v0.2 TOs). -->
    <priority>normal</priority>
    <estimated_effort>~0.75d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §12.4 TO-11 (v0.2 addendum 2026-05-08 PM)</ref>
    <ref type="anchor_a">SESSION_2026-05-05.md (DE 0.4): "InflectionInsightsPanel: TOOL FAIL (no co-located types.ts) — types confirmed manually via direct read"</ref>
    <ref type="anchor_b">advi_infship_phase2_close.md (DE 0.4 2026-04-28): "comp-transform schema-check PartnerAnalytics --feature inflection: 1 false-positive `period` MISSING flag — Click-handler local param type, not a field-path read; ignored"</ref>
    <ref type="related_failures">5+ comp-transform schema-check FAILs in 2-week compiler-tools-log on AccountDistributionMetrics, AUMGrowthMetrics, FidelityCustodianBar, ReturnVolatilityScatter, BooksTab, InflectionInsightsPanel — mix of false-positives + missing-types modes.</ref>
  </references>

  <context>
    Two distinct sub-issues surfaced in 2-week window:

    **(a) Missing co-located types.ts FAIL:** Tool assumes `types.ts` is co-located with `.tsx`. If not present, FAILs without searching parent dir or shared types modules. InflectionInsightsPanel hit this — types live in shared module; agent had to manually verify via direct file read. Should be a graceful degradation, not a hard FAIL.

    **(b) Handler-local-param false-positive:** Tool flags destructured handler-local params as "missing field" when they're not field-path reads at all. PartnerAnalytics `period` flag from a click-handler destructure (`const period = e.target.value` shape) is not a field read on response data; tool's MISSING classification is wrong.

    Combined effect: 13 comp-transform FAIL entries in 2-week log; manual triage cost ~5-15 min per occurrence. Some are real schema gaps (worth flagging); some are tool false positives (waste of agent attention). Need machine-readable severity to triage fast.
  </context>

  <scope>
    <step>
      <run>Read `comp-transform schema-check` implementation; locate (a) types.ts resolution logic + (b) field-MISSING classification logic.</run>
      <expect>Both surfaces identifiable; refactor scope clear.</expect>
    </step>
    <step>
      <run>(a) Types resolution: when no co-located `types.ts`, walk parent dirs looking for shared types module — search for `_shared/types.ts`, `../types.ts`, `../../types.ts`, etc. (up to 3 levels). If found, resolve types from there + report as INFO severity ("types resolved from {path}"). Only FAIL if no types.ts found anywhere up the directory tree.</run>
      <expect>InflectionInsightsPanel test case: types resolve from shared parent module + tool returns INFO + types-mapped output (not FAIL).</expect>
      <if_mismatch>If portal directory structure varies, document the directory-walk policy + edge cases; default to "first types.ts encountered walking up wins."</if_mismatch>
    </step>
    <step>
      <run>(b) AST-aware handler-local-param filter: classify each "MISSING field" candidate by AST context:
        - JSX `{obj.field}` read → true-positive (flag as ERROR)
        - Transform-chain `data.field` / `result.field` read → true-positive (flag as ERROR)
        - Handler-local-param destructure (`const { field } = e.target` / `(field) =&gt; ...`) → false-positive (suppress; do NOT flag)
        - Type-only reference (`type X = { field: ... }`) → not a runtime read (suppress)</run>
      <expect>PartnerAnalytics `period` test case: not flagged as MISSING (handler local param suppressed). Real missing-field cases still flagged.</expect>
      <if_mismatch>If AST classification is ambiguous on edge cases, default to flagging (false-positive over false-negative) but emit lower severity (WARN not ERROR).</if_mismatch>
    </step>
    <step>
      <run>(c) Machine-readable severity column: emit `INFO` (resolved with degradation, e.g., types from shared module) / `WARN` (suspected gap, ambiguous AST) / `ERROR` (confirmed gap, JSX/transform field-read with no type). Column format consistent across tool output (single severity column per result line).</run>
      <expect>Output triageable at a glance; agents prioritize ERRORs over WARNs over INFOs.</expect>
    </step>
    <step>
      <run>Empirical validation — rerun the 5+ FAIL cases from 2-week log:
        - InflectionInsightsPanel: should be INFO (types resolved from shared module)
        - PartnerAnalytics --feature inflection: `period` should be suppressed (no MISSING flag)
        - AccountDistributionMetrics, AUMGrowthMetrics, FidelityCustodianBar, ReturnVolatilityScatter, BooksTab: re-classify per real AST context (some may stay ERROR; some may flip to WARN/suppress).</run>
      <expect>Materially fewer false-FAILs; triage cost drops; real ERRORs preserved.</expect>
    </step>
    <step>
      <run>Regression — pick 3 known-good schema-check queries (cases that PASSed cleanly); rerun + verify no behavior change on PASS cases.</run>
      <expect>PASS cases unchanged.</expect>
    </step>
    <step>
      <run>Ship via safe-commit.sh; RAVC2 to CTO + COO with re-triaged 5+ FAIL list + 3 regression cases.</run>
      <expect>Clean ship; severity column documented; reduced false-positive rate empirically demonstrated.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">Types resolution walks parent dirs (up to 3 levels) for shared types.ts; reports INFO when resolved via shared module instead of co-located.</ac>
    <ac id="2">AST-aware filter suppresses handler-local-param destructures from MISSING classification; type-only references suppressed.</ac>
    <ac id="3">Machine-readable severity column (`INFO` / `WARN` / `ERROR`) emitted on every result line.</ac>
    <ac id="4">InflectionInsightsPanel test case: returns INFO + types-mapped output (no FAIL).</ac>
    <ac id="5">PartnerAnalytics `period` handler-local case: suppressed (no MISSING flag).</ac>
    <ac id="6">5+ FAIL cases from 2-week log re-classified per real AST context; materially fewer false-FAILs documented.</ac>
    <ac id="7">3 known-good PASS cases regression-clean (no behavior change).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">
      <run>Read tool source; identify types-resolution + field-MISSING classification surfaces.</run>
      <expect>Clean refactor targets.</expect>
    </phase>
    <phase id="2">
      <run>Pre-commit: 8-cell test matrix — 2 anchor cases (a/b) + 5 from 2-week log + 3 regressions.</run>
      <expect>All cells produce expected severities.</expect>
    </phase>
    <phase id="3">
      <run>Post-commit empirical: rerun 8 cases; append rows to org/compiler-tools-log.md with severity tags.</run>
      <expect>8/8 produce expected severities; log captures.</expect>
    </phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>8-cell matrix sample outputs with severity column visible + before/after FAIL-count comparison</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Refactoring portal types.ts file structure (use whatever current structure exists; tool walks for it).</item>
    <item>Adding new schema-check rules (separate scope; agents add rules per-component).</item>
    <item>JSON-format output mode (would be useful but separate; current tool emits human-readable; severity column adds value to current format).</item>
  </out_of_scope>
</task_order>
