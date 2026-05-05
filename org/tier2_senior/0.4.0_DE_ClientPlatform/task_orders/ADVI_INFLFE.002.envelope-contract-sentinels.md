<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLFE.002</id>
    <project>ADVI_INFLFE</project>
    <title>Envelope contract sentinels — ClientsTab, AdvisorBookView, InflectionInsightsPanel</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- 72a6c1f4 portal DEV. AC1-4 PASS. 3 sentinels: ClientsTab warnOnInflectionClientDrift, AdvisorBookView warnOnInflectionAdvisorDrift, InflectionInsightsPanel 3x warnOnInflection*Shape. typecheck exit 0. -->
    <priority>high</priority>
    <estimated_effort>0.5-1d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/INFLEC_FE_BACKEND_WIRING.md §4 TO-2</ref>
    <ref type="audit_matrix">docs/architecture/ADVI_INFLEC_AUDIT.md v4 — 3 highest-risk components for Inflection envelope drift</ref>
    <ref type="schema_check_baseline">comp-transform schema-check ClientsTab (INFLFE.001 Phase 2 baseline: All fields match; 14 UNUSED on AdvisorBookResponse = by-design BD-subset)</ref>
    <ref type="gate">INFLFE.001 AC3 DT PASS — envelope shape empirically known before sentinels written</ref>
  </references>

  <context>
    Three components carry the highest Inflection envelope-drift risk:
    1. ClientsTab — drives BooksTab L3; post-INFLFE.001 now properly branched for Inflection
    2. AdvisorBookView — wraps L2 advisor drill (getPlatinumAdvisorSummary envelope)
    3. InflectionInsightsPanel — owns 3 RevOps sub-panels (currently all RED with AUA=0; will flip when AUDIT-002 lands)

    Add type-level + runtime guards so envelope drift throws early (logged, not crash) rather
    than silently rendering undefined. Pattern: assertInflectionShape(response) at the fetch
    hook, logging mismatch to console.warn in dev + CloudWatch in prod. Do NOT fail the request
    in v1 — observability-mode first per PRD §8 risk mitigation.

    NOTE: The 14 UNUSED fields on AdvisorBookResponse are expected — Inflection envelope is a
    by-design subset of the BD envelope. Sentinels must distinguish "field unused AND absent" (WARN)
    from "field unused but present" (OK). comp-transform schema-check already supports this nuance.
  </context>

  <phase id="0" when="before any code write">
    <step>
      <run>comp-transform schema-check AdvisorBookView</run>
      <expect>MISSING = runtime undefined; NOTE-class = expected alias; UNUSED = investigate if Inflection-specific</expect>
      <if_mismatch>Any MISSING on AdvisorBookView → add to sentinel scope</if_mismatch>
    </step>
    <step>
      <run>comp-transform schema-check InflectionInsightsPanel</run>
      <expect>Clean or NOTE-class only; UNUSED fields for RED cells (AUA=0 current) are expected</expect>
      <if_mismatch>MISSING fields → sentinel must cover these</if_mismatch>
    </step>
    <step>
      <run>comp-blast InflectionInsightsPanel</run>
      <expect>3 endpoints (activity/cash/concentration), 1 Lambda (opal-partners-data), 6 downstream nodes — confirm scope before editing</expect>
      <if_mismatch>Any new downstream nodes not in PRD §5 blast evidence → flag to COO before proceeding</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="code implementation">
    <step>
      <action>ClientsTab — add type guard at L3 fetch hook for isInflectionFirm path. Guard asserts: client_key, total_aua, accounts[], tax.realized, tax.unrealized present. Log console.warn on mismatch in dev; no request failure.</action>
    </step>
    <step>
      <action>AdvisorBookView — add type guard at getPlatinumAdvisorSummary response. Assert envelope keys: book, mix, composition, fee_summary, summary. Log console.warn on missing keys. No crash.</action>
    </step>
    <step>
      <action>InflectionInsightsPanel — add type guard for each of 3 sub-panel responses (activity_scan, cash_drag, concentration_risk). Assert: rows array present + numeric AUA field present. When AUA=0 (current RED state), do NOT fire guard — zero is valid; only fire if the key is absent entirely.</action>
    </step>
  </phase>

  <phase id="2" when="before committing">
    <step>
      <run>comp-transform schema-check ClientsTab (post-sentinel)</run>
      <expect>No new MISSING fields vs INFLFE.001 baseline; UNUSED count unchanged or reduced</expect>
      <if_mismatch>Sentinel introduced type narrowing that broke a field — revert and rethink guard placement</if_mismatch>
    </step>
    <step>
      <run>comp-transform schema-check AdvisorBookView (post-sentinel)</run>
      <expect>Same — no new MISSING vs Phase 0 baseline</expect>
      <if_mismatch>Fix before committing</if_mismatch>
    </step>
    <step>
      <run>comp-cache collisions</run>
      <expect>Zero new collisions — sentinels do not introduce new React Query keys</expect>
      <if_mismatch>Rename any new query key to avoid collision</if_mismatch>
    </step>
    <step>
      <run>bun run typecheck</run>
      <expect>exit 0</expect>
      <if_mismatch>Fix TypeScript errors before commit</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>INFLFE.001: gate — DO NOT start until INFLFE.001 AC3 DT PASS confirmed by COO.</coord>
    <coord>INFLFE.003: both modify InflectionInsightsPanel. INFLFE.003 pre-wires rendering; INFLFE.002 adds type guards. Sequence: .002 first on InflectionInsightsPanel; .003 can proceed on other components in parallel but must NOT modify InflectionInsightsPanel until .002 commits it.</coord>
    <coord>portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookView.tsx: .001 and .002 both modify. .001 committed first (fc88893a). .002 adds sentinels on top — do not revert .001 Bug A fix.</coord>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">comp-transform schema-check snapshot baseline committed for all 3 components — no new MISSING vs INFLFE.001 baseline</criterion>
    <criterion id="AC2">Each of the 3 components has a runtime type guard at the fetch hook that logs on envelope drift without crashing the request</criterion>
    <criterion id="AC3">comp-cache collisions shows zero new collisions post-sentinel</criterion>
    <criterion id="AC4">bun run typecheck exit 0</criterion>
    <criterion id="AC5">RAVC3 to COO: portal commit hash + AC1-4 status + comp-transform diff excerpt showing baseline committed</criterion>
  </acceptance_criteria>
</task_order>
