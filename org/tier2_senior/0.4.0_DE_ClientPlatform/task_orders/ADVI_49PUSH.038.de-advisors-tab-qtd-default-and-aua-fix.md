<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-038-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~A</issued_to>
    <date>2026-04-09</date>
    <status>pending -- unblocked (fix_1 is a 1-line change; fix_2 can proceed once DS .037 confirms field)</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>9</wave>
    <phase>Advisors tab UI fixes</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Two fixes for the Advisors tab: (1) change the default period toggle from YTD to QTD,
    (2) fix the Top 3 Highlights aggregation to use total_aua (tagged AUA) not managed_aua.
  </objective>

  <fix_1 label="Default period: YTD → QTD">
    <description>
      File: portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx
      Line 167: const [period, setPeriod] = useState&lt;PeriodKey&gt;('ytd')
      Change 'ytd' to 'qtd'.

      That is the entire change for this fix. One character. Do it now, do not wait for DS.
    </description>
  </fix_1>

  <fix_2 label="Top 3 Highlights: replace managed_aua with total_aua">
    <description>
      File: portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx
      Line ~206: aua += data.managed_aua

      managed_aua is a legacy field from the non-platinum leaderboard JSON (C_08-derived,
      fee-weighted). The platinum leaderboard entry has total_aua = tagged AUA (confirmed
      by DS .037).

      Fix: replace data.managed_aua with data.total_aua wherever it appears in the
      Top3Highlights component and any related aggregation logic in this file.

      Also search the entire AdvisorsTab.tsx for any other reference to managed_aua and
      replace with total_aua. managed_aua should not appear anywhere in the Advisors tab
      after this fix.

      Dependency: wait for DS .037 to confirm that PlatinumLeaderboardEntry.total_aua
      is indeed tagged_aua (~$427M for Travis Penfield) before deploying this change.
      The one-line fix_1 (QTD default) can be committed and deployed immediately without
      waiting for DS .037.
    </description>
  </fix_2>

  <acceptance_criteria>
    1. Advisors tab opens with QTD selected by default
    2. No reference to managed_aua anywhere in AdvisorsTab.tsx
    3. Top 3 Highlights AUA figures match the leaderboard table AUA figures for the same advisors
    4. Build clean, no TypeScript errors
    5. fix_1 committed independently and deployable without fix_2
  </acceptance_criteria>


  <compiler_tools>
    comp-transform schema-check AdvisorsTab
      -- Run after fix_2 (managed_aua → total_aua). Confirms total_aua is wired
         to all JSX render sites and no managed_aua reference remains in the
         rendered field tree. This is faster than grepping the 900-line file.
  </compiler_tools>

</task_order>
