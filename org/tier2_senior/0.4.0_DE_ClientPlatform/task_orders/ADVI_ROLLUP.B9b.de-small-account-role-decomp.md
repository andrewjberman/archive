<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-16-advi-rollup-b9b-de2</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-16</date>
    <status>pending</status>
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W3-addendum</wave>
  </metadata>

  <references>
    <ref type="companion">ADVI_ROLLUP.B9b.ds-small-account-book-extension.md — must ship first (role_breakdown.small_account_count comes from D_02).</ref>
    <ref type="companion">ADVI_ROLLUP.B9b.de-small-account-clients-panel.md — parallel FE TO. Ship in the same portal bump if possible.</ref>
  </references>

  <context>
    Compiler pre-check results (run 2026-04-16 by CTO):
    - comp-transform schema-check AdvisorBookView: getPlatinumAdvisorSummary() → PlatinumAdvisorSummary
      has 27 fields, only 3 rendered. role_breakdown is among the 21 UNUSED fields.
      D_02's book.json role_breakdown (aua, account_count, pct_of_tagged per role) IS fetched
      but not rendered in AdvisorBookView. This TO activates it with a small accounts breakdown.
    - PlatinumAdvisorSummary.role_breakdown type (types.ts ~2063):
        Record&lt;string, { aua: number; pct_of_tagged: number; account_count?: number; client_count?: number }&gt;
      Does NOT have small_account_count. This TO adds it.
    - Target: AdvisorBookView.tsx (the Book tab view, non-admin path). This is where the advisor's
      book summary is shown — the natural home for role decomposition of small accounts.

    User request: "should display 'by role' in the role decomposition, so they know if they have
    small accounts as an architect or as an implementor or etc."
  </context>

  <objective>
    Surface small_account_count per role in the advisor book view.

    1. TYPE (portal/src/pages/AdvisorIntelligence/types.ts):
       Extend PlatinumAdvisorSummary.role_breakdown value type (~line 2063):
         Record&lt;string, {
           aua: number
           pct_of_tagged: number
           account_count?: number
           client_count?: number
           small_account_count?: number   // NEW — accounts &lt; $40k in this role
         }&gt;

    2. ROLE BREAKDOWN UI (AdvisorBookView.tsx):
       The role_breakdown is currently fetched but not rendered. Add a "Small Accounts by Role"
       section in the book summary area. Suggested placement: below or alongside the existing
       account/client count stats, within the same card/panel as the book summary.

       For each role present in role_breakdown where small_account_count != null:
         - Show role label (capitalize: "Architect", "Implementor", etc.)
         - Show small_account_count as an integer
         - Optionally show as fraction: e.g. "3 / 12 accounts" (small / total account_count)
           if account_count is available in the role_breakdown entry
         - Highlight any role with small_account_count > 0 in a soft red/amber accent
           (same palette as the client row highlight in B9b-DE1)

       Design note: keep it compact — a horizontal role-pill list or a small table row per role.
       Do not introduce a new chart; a text/badge pattern is sufficient.
       Only render this section when at least one role has small_account_count defined (guard on DS ship).

    3. CONSTANT: reuse SMALL_ACCOUNT_THRESHOLD = 40_000 from B9b-DE1. If defined in a shared
       constants file, import from there. If defined per-component, define again here.
  </objective>

  <wire_contract>
    PlatinumAdvisorSummary.role_breakdown value (types.ts ~2063):
      small_account_count?: number   // non-null int once DS ships

    Rendered: AdvisorBookView.tsx, book summary section.
    Section is hidden (returns null) when no role has small_account_count defined.
  </wire_contract>

  <acceptance_criteria>
    1. bun run build exits 0.
    2. comp-transform schema-check AdvisorBookView clean — no new MISSING. small_account_count
       should appear in rendered set for role_breakdown (transition from UNUSED).
    3. Book view shows a role breakdown section listing small account count per role.
    4. Roles with small_account_count > 0 have a visual indicator (red/amber accent or badge).
    5. Section is not rendered when role_breakdown is absent or all small_account_count values are null.
    6. /frontend-dev Skill invoked with role_breakdown_small_accts constitution. PASS required.
    7. MCP COMPLETE to COO with portal DEV commit hash + /frontend-dev PASS confirmation.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check AdvisorBookView --all-unused</run>
        <expect>role_breakdown listed as UNUSED. Confirms we are activating a field that exists
        in the fetched data. No new fetch or endpoint needed.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bun run build</run>
        <expect>Exit 0.</expect>
      </step>
      <step>
        <run>comp-transform schema-check AdvisorBookView</run>
        <expect>role_breakdown.small_account_count now in rendered set. Overall UNUSED count
        reduced (we are activating the role_breakdown field).</expect>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>/frontend-dev Skill with role_breakdown_small_accts constitution</run>
        <expect>PASS — role section renders, per-role small account counts visible, zero-count
        roles handled gracefully, section hidden when data absent.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.B9b.ds-small-account-book-extension" status="pending"
      description="role_breakdown[role].small_account_count data. Mark type optional (?) until DS artifact lands. Section renders empty/hidden until then."/>
  </dependencies>
</task_order>
