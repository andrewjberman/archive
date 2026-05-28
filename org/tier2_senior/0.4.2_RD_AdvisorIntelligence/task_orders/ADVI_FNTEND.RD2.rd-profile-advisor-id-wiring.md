<task_order>
  <metadata>
    <id>0.4.2_RD_AdvisorIntelligence-2026-04-16-advi-fntend-rd2-profile-advisor-id</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-16</date>
    <status>complete</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>RD2</wave>
    <reconciled note="Shipped + committed 5df929b97 (profileAdvisorId threaded AdvisorBookView->AdvisorBookClientDetail->FeeSummaryPanel; ClientsTab unwired per AC4). Parent ADVI_FNTEND merged into ADVI_ROLLUP. Status reconciled active->complete by /work entity-truth sweep 2026-05-28."/>
  </metadata>

  <context>
    FeeSummaryPanel already accepts profileAdvisorId?: string | null (line 88,
    FeeSummaryPanel.tsx). When non-null it:
      - Pins the profiled advisor's row to the top of the Accounts table
      - Filters team_attribution to show only that advisor's split bps
      - Populates Advisor Split + Advisor Revenue in Relationship Summary

    The prop is never passed today. AdvisorBookView knows its advisorId (the
    profile subject) but the value is dropped at the AdvisorBookClientDetail
    boundary. ClientsTab (admin multi-advisor view) must NOT receive it.

    This is a pure prop-threading change: no new data fetches, no new state,
    no component restructuring. Two files, three call sites.
  </context>

  <objective>
    Thread profileAdvisorId from AdvisorBookView down through
    AdvisorBookClientDetail into the FeeSummaryPanel slot.

    NON-ADMIN BOOK PATH ONLY. ClientsTab call site is explicitly excluded.

    Step 1 — AdvisorBookClientDetail.tsx
    Add to AdvisorBookClientDetailProps interface (around line 38):
      /** Non-null on the advisor profile path. Pins the advisor's row in
       *  FeeSummaryPanel and filters team_attribution to their split. */
      profileAdvisorId?: string | null

    Destructure in the component function signature (around line 78).

    Pass the value into the FeeSummaryPanel call inside feeSummarySlot
    (around line 153-165):
      <FeeSummaryPanel
        ...existing props...
        profileAdvisorId={profileAdvisorId}
      />

    Step 2 — AdvisorBookView.tsx
    In the L3 render block (around line 317), pass advisorId as
    profileAdvisorId on AdvisorBookClientDetail:
      <AdvisorBookClientDetail
        ...existing props...
        profileAdvisorId={advisorId}
      />

    DO NOT touch ClientsTab.tsx. Its AdvisorBookClientDetail call site (line 498)
    must remain without profileAdvisorId so the admin view stays multi-advisor
    neutral (no pinning, no split filtering).
  </objective>

  <acceptance_criteria>
    1. bun run build exits 0 — no new TypeScript errors.
    2. comp-transform schema-check AdvisorBookClientDetail clean — no new MISSING.
    3. comp-transform schema-check FeeSummaryPanel clean — profileAdvisorId
       appears USED (not UNUSED) after the wiring lands.
    4. ClientsTab.tsx diff shows zero changes.
    5. On the non-admin advisor profile L3 view (Book -> Client), the advisor's
       own row appears pinned at the top of the Accounts Summary table.
       (Pre-team_attribution: Split bps column shows em-dash; pinning is visible.)
    6. MCP COMPLETE to COO with commit hash + confirmation that ClientsTab is
       unchanged.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check AdvisorBookClientDetail</run>
        <expect>profileAdvisorId not yet present. Note any pre-existing MISSING fields to distinguish from new issues.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bun run build</run>
        <expect>Exit 0.</expect>
      </step>
      <step>
        <run>comp-transform schema-check AdvisorBookClientDetail</run>
        <expect>No new MISSING fields vs baseline.</expect>
      </step>
      <step>
        <run>comp-transform schema-check FeeSummaryPanel</run>
        <expect>profileAdvisorId USED.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <notes>
    - advisorId in AdvisorBookView is the profile subject's ID, available at
      component scope from the advisorId prop (line 60, AdvisorBookView.tsx).
    - No auth-claims lookup needed — advisorId is already the correct value.
    - Prop is optional (string | null) so the component compiles cleanly even
      when called without it (ClientsTab path remains valid as-is).
    - Advisor Split + Advisor Revenue in Relationship Summary will remain
      em-dash until DS B3b team_attribution artifact lands. Pinning activates
      immediately (no data dependency).
  </notes>
</task_order>
