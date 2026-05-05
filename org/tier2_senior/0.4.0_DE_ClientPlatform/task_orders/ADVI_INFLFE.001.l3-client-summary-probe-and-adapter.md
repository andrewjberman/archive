<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLFE.001</id>
    <project>ADVI_INFLFE</project>
    <title>L3 client_summary Lambda probe + adapter decision — ClientsTab + AdvisorBookView wiring</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>pending</status><!-- Phase 0+1 COMPLETE via AUDIT-004 execution (fc88893a). Bug A + Bug B fixed. AC3 awaiting DT Playwright smoke. -->
    <priority>high</priority>
    <estimated_effort>COMPLETE — Phase 0+1 done in AUDIT-004 context; AC3 DT gate outstanding</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/INFLEC_FE_BACKEND_WIRING.md §4 TO-1</ref>
    <ref type="audit_matrix">docs/architecture/ADVI_INFLEC_AUDIT.md v4 (f6ea12221)</ref>
    <ref type="de_execution">AUDIT-004 Phase 0+1 complete: portal fc88893a (CLOUD); session log 947b78bf8</ref>
    <ref type="static_adapter">portal/src/api/endpoints/advisor-intelligence.ts:884-936 — getPlatinumClientDetailStatic</ref>
    <ref type="absorbs">ADVI_INFLEC.AUDIT-004 — scope fully absorbed here; no separate AUDIT-004 dispatch needed</ref>
  </references>

  <context>
    Formalization of AUDIT-004 execution. DE confirmed and fixed two bugs under AUDIT-004 scope:

    Bug A (YELLOW — hooks violation): AdvisorBookView.tsx normalizedClients useMemo was hook #48,
    placed AFTER early returns at lines 303/305-318. When bookLoading=true, 47 hooks run; on
    bookLoading=false, 48 hooks run — React ErrorBoundary crash. Fix: moved useMemo before early
    returns with optional chaining on bookData?.book.clients. All 4 advisor L2 drills now stable.

    Bug B (ORANGE — ClientsTab static adapter not wired): ClientsTab.tsx:387 called
    getPlatinumClientSummary unconditionally. AdvisorBookView already had correct isInflectionFirm
    branching (INFSHIP B5) but ClientsTab has its own L3 path (lines 532-603). Fix: added
    isInflectionFirm const + branched queryFn/queryKey to use getPlatinumClientDetailStatic for
    firmId=inflection. Cache key deduplication gap between ClientsTab + AdvisorBookView resolved.

    AC3 (Playwright smoke) deferred to DT 0.4 — dispatched same session.
  </context>

  <phase id="0" when="COMPLETE — compiler gates">
    <step><run>comp-routes trace getPlatinumClientSummary</run><result>PASS — Lambda path confirmed (APIGateway-portal)</result></step>
    <step><run>comp-transform schema-check ClientsTab</run><result>PASS — All rendered fields match response types; NOTE-class UNUSED only</result></step>
  </phase>

  <phase id="1" when="COMPLETE — code-level probe + fix">
    <step><run>Read AdvisorBookView.tsx:303-318 + useMemo placement</run><result>PASS — Bug A hooks violation confirmed; fix shipped</result></step>
    <step><run>Read ClientsTab.tsx:387 L3 queryFn</run><result>PASS — Bug B unconditional query confirmed; isInflectionFirm branching shipped</result></step>
  </phase>

  <phase id="2" when="COMPLETE (DE gates) — post-fix validation">
    <step><run>comp-transform schema-check ClientsTab (post-fix)</run><result>PASS — no new MISSING fields</result></step>
    <step><run>comp-cache collisions</run><result>PASS — no new collisions on advisor-book-client key variants</result></step>
    <step><run>bun run typecheck</run><result>PASS — exit 0</result></step>
  </phase>

  <phase id="3" when="PENDING — DT Playwright gate (AC3)">
    <step>
      <run>DT 0.4: /frontend-dev Playwright smoke — BooksTab, click advisor, click client, verify L3 renders non-blank with client name + AUA + tax fields</run>
      <expect>L3 panel renders correctly for firmId=inflection after fc88893a fix</expect>
      <if_mismatch>DE re-investigates adapter field mapping; do NOT ship portal bump if L3 blank</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>DT 0.4: owns AC3 Playwright gate. COO dispatched same session (20260505T132300Z). DT reports RAVC3 to COO when AC3 confirmed.</coord>
    <coord>INFLFE.002: gates on INFLFE.001 AC3 pass (envelope shape confirmed end-to-end). DE does NOT start .002 until DT AC3 PASS received by COO.</coord>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">PASS — Bug A (hooks violation) and Bug B (ClientsTab L3 adapter) both confirmed by code-level read + committed in fc88893a</criterion>
    <criterion id="AC2">PASS — comp-transform schema-check ClientsTab clean post-fix; no new MISSING fields</criterion>
    <criterion id="AC3">PENDING DT — Playwright smoke: L3 client detail panel renders non-blank for firmId=inflection; at least one Inflection household shows client name + AUA + tax fields</criterion>
    <criterion id="AC4">PASS — compiler tools all logged in AUDIT-004 session log (947b78bf8)</criterion>
    <criterion id="AC5">RAVC to COO from DT when AC3 confirmed; COO closes INFLFE.001 and issues GO for INFLFE.002</criterion>
  </acceptance_criteria>
</task_order>
