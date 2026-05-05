<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.AUDIT-004</id>
    <project>ADVI_INFLEC</project>
    <title>L3 client summary Lambda shape probe — getPlatinumClientSummary Inflection envelope</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>staged</status><!-- GO withheld — DE not online at time of issue. COO will send GO when DE registers. -->
    <priority>high</priority>
    <estimated_effort>0.5d — probe only; ~1d if adapter wiring needed</estimated_effort>
  </metadata>

  <references>
    <ref type="audit_matrix">docs/architecture/ADVI_INFLEC_AUDIT.md v3 — TODO-empirical: L3 client_summary probe</ref>
    <ref type="de_mapping_draft">docs/architecture/_drafts/INFLEC_AUDIT_DE_MAPPING.md — HIGH-PRIORITY ORANGE: "ClientsTab L3 getPlatinumClientSummary Lambda response shape — Lambda may 404 for Inflection households (Inflection envelope is summary.tax, not detail.tax). Static adapter exists (getPlatinumClientDetailStatic at endpoints/advisor-intelligence.ts:884-936) but NOT wired into ClientsTab L3 fetch."</ref>
    <ref type="compiler_evidence">comp-routes trace getPlatinumClientSummary → URL: /api/scoped/partners/books/relationship/{param}/platinum-summary?firmId={param} → APIGateway-portal Lambda (NOT bucket-swap); components: AdvisorBookView, ClientsTab</ref>
    <ref type="static_adapter">portal/src/api/endpoints/advisor-intelligence.ts:884-936 — getPlatinumClientDetailStatic</ref>
  </references>

  <context>
    ClientsTab L3 drill (relationship/household detail) calls getPlatinumClientSummary which routes
    through opal-partners-data Lambda via /api/scoped/partners/books/relationship/{hhId}/platinum-summary.
    This is NOT a bucket-swap path — it goes through the Lambda.

    For Inflection households, the Lambda may return data under a summary.tax envelope
    rather than the detail.tax shape that ClientsTab L3 expects. If so, the component either
    renders empty/undefined fields or throws an unhandled undefined error.

    A static adapter getPlatinumClientDetailStatic exists at endpoints/advisor-intelligence.ts:884-936
    and can convert the Inflection envelope to the BD-shaped detail.tax format. However, it is
    not currently wired into the ClientsTab L3 fetch path for firmId=inflection.

    This TO probes whether the bug is real, then fixes it if confirmed.
  </context>

  <phase id="0" when="discovery — before any code write">
    <step>
      <run>comp-routes trace getPlatinumClientSummary</run>
      <expect>URL: /api/scoped/partners/books/relationship/{param}/platinum-summary — Lambda path confirmed (not bucket-swap)</expect>
      <if_mismatch>If bucket-swap path — static adapter is irrelevant; investigate S3 artifact shape instead</if_mismatch>
    </step>
    <step>
      <run>comp-transform schema-check ClientsTab</run>
      <expect>Clean or NOTE-class only on AdvisorBookResponse / PlatinumClientSummary; no MISSING fields on L3 path</expect>
      <if_mismatch>Any MISSING fields on L3 client summary → list them for fix scope</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="empirical probe — trigger L3 drill in browser under firmId=inflection">
    <step>
      <run>Using portal dev server (bun run dev --port 5175) with firmId=inflection auth: navigate to BooksTab → click advisor (e.g. Peter Lee) → click a client/household in L2 drill → observe Network tab for getPlatinumClientSummary response; log: HTTP status + response body shape (top-level keys)</run>
      <expect>HTTP 200 with body containing either detail.tax OR summary.tax. If 404/500 → Lambda routing gap. If 200 but wrong shape → adapter wiring needed.</expect>
      <if_mismatch>If 404: Lambda does not handle Inflection households — DE files separate report as RED-(a) and escalates scope to AE. If 200 wrong shape: proceed to Phase 1 Step 2.</if_mismatch>
    </step>
    <step>
      <run>Read portal/src/api/endpoints/advisor-intelligence.ts lines 884-936 (getPlatinumClientDetailStatic) — confirm it maps summary.tax → detail.tax correctly for Inflection shape</run>
      <expect>Static adapter covers: name, total_aua, accounts[], tax.realized, tax.unrealized, inflecBilling{} fields at minimum</expect>
      <if_mismatch>If adapter gaps exist — extend it to cover missing fields before wiring</if_mismatch>
    </step>
    <step>
      <run>Read ClientsTab.tsx:386-388 — confirm fetch is getPlatinumClientSummary (not getPlatinumClientDetailStatic)</run>
      <expect>L3 fetch uses getPlatinumClientSummary unconditionally (no firmId branch)</expect>
      <if_mismatch>If already branched by firmId → investigate why it's still broken</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before committing fix (only if Phase 1 confirms adapter wiring needed)">
    <step>
      <run>comp-transform schema-check ClientsTab (re-run after wiring change)</run>
      <expect>No new MISSING fields introduced; existing NOTE-class unchanged</expect>
      <if_mismatch>Fix any new schema gaps before committing</if_mismatch>
    </step>
    <step>
      <run>comp-cache collisions (if new query key introduced for firmId-branched fetch)</run>
      <expect>No collisions on new key pattern</expect>
      <if_mismatch>Rename key to avoid collision</if_mismatch>
    </step>
    <step>
      <run>/frontend-dev — Playwright smoke on BooksTab L3 drill for firmId=inflection; screenshot L3 client detail panel</run>
      <expect>L3 panel renders tax fields without undefined errors; non-blank client name + AUA visible</expect>
      <if_mismatch>Investigate adapter field mapping; do not ship if L3 renders blank panel</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">Session log documents Phase 1 probe result: HTTP status + response shape observed + verdict (bug confirmed / no bug / 404-Lambda-gap)</criterion>
    <criterion id="AC2">If fix shipped: comp-transform schema-check ClientsTab shows no new MISSING fields post-wiring</criterion>
    <criterion id="AC3">If fix shipped: /frontend-dev Playwright smoke passes L3 drill for at least one Inflection household</criterion>
    <criterion id="AC4">Session log Compiler Tools section reproduces each &lt;run&gt; + observed result + PASS/FAIL vs &lt;expect&gt;</criterion>
    <criterion id="AC5">RAVC3 to COO: probe verdict + commit hash (if fix) + AC1-4 status. If 404-Lambda-gap found (RED-(a)): escalate immediately without waiting for fix.</criterion>
  </acceptance_criteria>
</task_order>
