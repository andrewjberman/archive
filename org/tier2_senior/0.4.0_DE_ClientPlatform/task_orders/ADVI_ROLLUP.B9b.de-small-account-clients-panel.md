<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-16-advi-rollup-b9b-de1</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-16</date>
    <status>pending</status>
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W3-addendum</wave>
  </metadata>

  <references>
    <ref type="companion">ADVI_ROLLUP.B9b.ds-small-account-book-extension.md — DS must ship first. Mark new types optional (?) until DS artifact lands, then tighten to required in a follow-up bump.</ref>
    <ref type="precedent">ADVI_ROLLUP.B9.de-small-account-count-column.md — COMPLETE (a2d8f83). FeeEfficiencyPanel already has Small Accts column. Pattern is identical here.</ref>
  </references>

  <context>
    Compiler pre-check results (run 2026-04-16 by CTO before issuing TO):
    - comp-transform schema-check AdvisorBookView: accounts: BooksClientAccount[] is UNUSED —
      the accounts array is fetched inside PlatinumClientSummary but not rendered. This TO
      activates it for red-highlight on drill-down.
    - comp-transform schema-check ClientsTab: same finding — accounts UNUSED.
    - AdvisorClient type (types.ts:1054): has client_key, client_name, aua, is_fee_paying?,
      nna_qtd/ytd/max?. Does NOT have small_account_count. This TO adds it.
    - AdvisorBookResponse.summary (types.ts:1079): has total_aua, client_count, account_count.
      Does NOT have small_account_count. This TO adds it.
    - BooksClientAccount.total_aua already exists (types.ts:1231) — account-level red highlight
      requires NO DS change, only FE rendering.
  </context>

  <objective>
    Four changes across two files + two components:

    1. TYPES (portal/src/pages/AdvisorIntelligence/types.ts):
       a. AdvisorClient (~line 1054): add
            small_account_count?: number  // accounts in this relationship below $40k AUA
       b. AdvisorBookResponse.summary (~line 1079): add
            small_account_count?: number  // advisor aggregate: unique accounts &lt; $40k, any role

    2. CLIENTS LIST (AdvisorBookView.tsx AND ClientsTab.tsx — both render the client list):
       a. Define FE constant at module top:
            const SMALL_ACCOUNT_THRESHOLD = 40_000
       b. Add "Small Accts" column to the clients table, immediately after AUA:
          - Render: client.small_account_count?.toLocaleString() ?? '—'
          - Header: "Small Accts"
          - Tooltip: "Accounts under $40,000 AUA this advisor is attached to for this client."
          - Sortable (same pattern as AUA column).
       c. Red row highlight on any client row where small_account_count > 0:
          - Use subtle red background or left-border accent: e.g. bg-red-500/10 border-l-2 border-red-500
          - Match style of other "alert" states in the portal (not aggressive red, more of a soft indicator).

    3. ACCOUNT DRILL-DOWN red highlight (AdvisorBookAccountDetail.tsx AND AdvisorBookView.tsx
       wherever BooksClientAccount rows are rendered):
       - Each account row: if total_aua < SMALL_ACCOUNT_THRESHOLD, apply same red accent style.
       - No DS change needed — total_aua is already in BooksClientAccount.
       - Guard: only apply if total_aua is defined (not null/undefined).

    4. HEADLINE STAT in advisor book summary area (wherever AdvisorBookResponse.summary is rendered):
       - Add "Small Accts" stat tile alongside client_count / account_count.
       - Render: summary.small_account_count (integer, never null per DS guarantee).
       - Label: "Small Accts (&lt;$40k)"
       - Tooltip: "Total accounts under $40,000 AUA this advisor is attached to, across all roles."
       - Guard: only render if summary.small_account_count != null (optional field until DS ships).
  </objective>

  <wire_contract>
    AdvisorClient (types.ts ~1054):
      small_account_count?: number

    AdvisorBookResponse.summary (types.ts ~1079):
      small_account_count?: number

    BooksClientAccount.total_aua (types.ts:1231): EXISTING — no change.

    FE constant (both components):
      const SMALL_ACCOUNT_THRESHOLD = 40_000
  </wire_contract>

  <acceptance_criteria>
    1. bun run build exits 0.
    2. comp-transform schema-check AdvisorBookView clean — no new MISSING.
    3. comp-transform schema-check ClientsTab clean — no new MISSING.
    4. Client list shows "Small Accts" column with integer value per row.
    5. Rows where small_account_count > 0 have red accent applied.
    6. Account-level rows in drill-down show red highlight where total_aua &lt; 40_000.
    7. Advisor book summary area shows "Small Accts (&lt;$40k)" stat (or is hidden when field absent).
    8. Sort on "Small Accts" column works.
    9. /frontend-dev Skill invoked with clients_panel constitution (create if absent under
       portal/.frontend-dev/testing/ per schema in that folder's README). PASS required.
    10. MCP COMPLETE to COO with portal DEV commit hash + /frontend-dev PASS confirmation.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check AdvisorBookView</run>
        <expect>accounts: BooksClientAccount[] UNUSED (expected). No pre-existing MISSING on AdvisorClient or AdvisorBookResponse fields we are adding.</expect>
      </step>
      <step>
        <run>comp-transform schema-check ClientsTab</run>
        <expect>Same — accounts UNUSED. No new MISSING introduced by our additions.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bun run build</run>
        <expect>Exit 0. No type errors.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check AdvisorBookView</run>
        <expect>Clean after edit. small_account_count in rendered set for summary + clients.</expect>
      </step>
      <step>
        <run>comp-transform schema-check ClientsTab</run>
        <expect>Clean after edit.</expect>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>/frontend-dev Skill with clients_panel constitution</run>
        <expect>PASS — column renders, red rows present for advisors with small accounts, headline stat visible.</expect>
        <if_mismatch>Iterate up to 5 times per Skill protocol, then escalate to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.B9b.ds-small-account-book-extension" status="pending"
      description="AdvisorClient.small_account_count and summary.small_account_count data. Mark types optional until DS artifact lands on DEV. BooksClientAccount.total_aua for account-level highlight is already present — that subset can ship independently."/>
  </dependencies>

  <ordering_note>
    Account-level red highlight (objective #3) can ship immediately — uses existing total_aua.
    Client list column + headline (objectives #2, #4) should wait for DS artifact or be guarded with ?.
    Preferred: ship all at once once DS artifact lands on DEV to avoid two portal bumps.
  </ordering_note>
</task_order>
