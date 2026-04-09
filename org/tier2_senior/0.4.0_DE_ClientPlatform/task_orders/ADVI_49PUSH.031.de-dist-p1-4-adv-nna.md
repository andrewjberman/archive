<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-031-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~B</issued_to>
    <date>2026-04-09</date>
    <status>partial -- fix_1 (Net NNA rename) DONE across all ADVI components; fix_2 (client NNA drilldown) + fix_3 (count wiring) blocked on AE D_01+D_04 re-run + nna_clients.json availability</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>7</wave>
    <phase>Distribution P1-4</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Distribution tab P1-4: Fix Snapshot-ADV-NNA view. Three issues:
    1. Rename all "Net NNA" labels to "Net New Assets" throughout the NNA views
    2. Fix the non-working client-level drilldown for an advisor's NNA breakdown
    3. Apply the universal radial=Clients / bell=Accounts count rule
    Note PII requirement for client names in drilldown (subject of .032, not this TO).
  </objective>

  <context>
    File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
    The ADV-NNA snapshot top level (advisor ranking) is working correctly:
    top 9 + Other, NNA per advisor as a value and % of total firm NNA for the period.
    Two issues remain: label and the client-level drilldown.

    "Net NNA" is redundant -- NNA already means Net New Assets. The label should be
    "Net New Assets" throughout this view (and wherever "Net NNA" appears in the file).

    The client-level drilldown (advDrillLevel === 'client') does not work. When a user
    clicks an advisor in the ADV-NNA view, the drilldown should show that advisor's
    top 9 clients + Other by NNA contribution, same framework as other client-level views.
    DS .027 issue_4 provides platinum/advisors/{id}/nna_clients.json for this.
  </context>

  <fix_1 label="Rename Net NNA to Net New Assets everywhere">
    <description>
      Search DistributionTab.tsx for all occurrences of "Net NNA" (case-insensitive).
      Replace with "Net New Assets".
      Known locations from grep: lines 705, 782, 815, 948 (and possibly others).
      Also check: the legend label at line ~815 and the tooltip at line ~782.
      Also grep the rest of the ADVI component tree for "Net NNA" to ensure the rename
      is complete across all panels (PartnerAnalytics.tsx, AdvisorsTab.tsx, etc.).
      "NNA" alone as an abbreviation is fine -- only the full phrase "Net NNA" is redundant.
    </description>
  </fix_1>

  <fix_2 label="Fix client-level NNA drilldown for advisor">
    <description>
      When advDrillLevel === 'client' in the ADV-NNA snapshot view, fetch and render
      the client-level NNA breakdown for the selected advisor.

      Data source (after DS .027): platinum/advisors/{id}/nna_clients.json
      Fetch via: the existing advisor-intelligence.ts endpoint pattern, e.g.:
        getPlatinumAdvisorNnaClients(advisorId, firmId)
        → GET /api/scoped/partners/books/advisor/{id}/nna-clients?firmId={firmId}
        OR direct S3: platinum/advisors/{id}/nna_clients.json
        Use whatever routing pattern DT has established for platinum advisor files.

      Client-level NNA view layout (same framework as GEO city drill):
        Radial: top 9 clients + Other by NNA, each segment shows:
          - Client display name (PSEUDONYMIZED -- see .032, stub placeholder for now)
          - NNA value for the period
          - % of advisor's total NNA
          Subtext: relationship_count = 1 (each segment is one client), no % needed
        Bell curve: account_count per client (Accounts)
        Total/center: advisor's total NNA for the period (not firm NNA)

      The drill navigation pattern (breadcrumb: Advisors > {advisor name} > Clients)
      must follow the same UX already established for GEO state → city drill.

      PII gate: client display_name must come from the pseudonymized field in the platinum
      data (DS .027 issue_4 will ensure this). Do NOT use raw relationship names from any
      other source. If pseudonymized names are not yet available (pre-.032 completion),
      render the drilldown with placeholder "[Client {N}]" labels rather than blocking
      the entire drilldown fix. The pseudonymization swap is a one-line change after .032.
    </description>
  </fix_2>

  <fix_3 label="Radial = Clients, Bell = Accounts">
    <description>
      Apply the universal count rule to ADV-NNA:
      Advisor-level radial: relationship_count per advisor (Clients)
      Client-level drilldown radial: relationship_count = 1 per client entry (Clients)
      Bell curve at both levels: account_count (Accounts)
    </description>
  </fix_3>

  <pii_note>
    Client names in the advisor drilldown MUST be pseudonymized. This is tracked under
    ADVI_49PUSH.032. For this TO, use the pseudonymized display_name from the platinum
    nna_clients.json data (DS .027 issue_4 provides it). If placeholder labels are used
    temporarily, they must be clearly marked in code with a TODO referencing .032.
    Do not leave cleartext client names in any rendered output under any code path.
  </pii_note>

  <acceptance_criteria>
    1. Zero occurrences of "Net NNA" in DistributionTab.tsx (replaced with "Net New Assets")
    2. "Net NNA" also eliminated from other ADVI components if found in the grep
    3. Client-level NNA drilldown renders top 9 clients + Other for the selected advisor
    4. Drilldown breadcrumb navigation works (can drill in and back out)
    5. Radial uses relationship_count, bell curve uses account_count
    6. Client names use pseudonymized display_name (or [Client N] placeholder if .032 pending)
    7. Build clean, no TypeScript errors
  </acceptance_criteria>


  <compiler_tools>
    comp-transform schema-check DistributionTab
      -- Run after fix_2 (client drilldown) to confirm the nna_clients data fields
         are wired to JSX. Catches missing field mappings before a manual browser test.

    comp-pii scan DistributionTab
      -- Required gate: run before shipping. Confirms display_name renders only
         pseudonymized values and no raw relationship_name field is accessible
         anywhere in the rendered tree.
  </compiler_tools>

</task_order>
