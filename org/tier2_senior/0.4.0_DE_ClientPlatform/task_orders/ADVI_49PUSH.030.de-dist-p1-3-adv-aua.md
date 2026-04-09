<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-030-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~B</issued_to>
    <date>2026-04-09</date>
    <status>COMPLETE -- ADV-AUA center = firm headline AUA (f2e7eca); relationship_count subtext wired; validation blocked on AE D_01+D_04 re-run</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>7</wave>
    <phase>Distribution P1-3</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Distribution tab P1-3: Fix Snapshot-ADV-AUA view. Three issues:
    1. Center radial total must be firm headline AUA (not a sum of advisor AUAs)
    2. Segment subtext must show # Clients per advisor + % of firm clients
    3. "Other" must represent all client relationships not covered by the top 9 advisors
    Also: apply the universal radial=Clients / bell=Accounts rule.
    Note PII requirement for advisor client drilldown (subject of .032, not this TO).
  </objective>

  <context>
    File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
    The ADV-AUA snapshot shows top advisors by AUA in the radial.

    IMPORTANT architectural note: advisor AUA figures use "tagged AUA" -- the total AUA
    of all accounts where an advisor appears in any role (architect/implementor/
    consultant/local_ops). A single account can be tagged to multiple advisors.
    Therefore summing advisor AUAs MEANINGFULLY EXCEEDS firm AUA and must never be used
    as a total. The center value is always the firm headline, not an advisor sum.

    DS .027 will ensure:
      - Segments cover all roles (not just architects)
      - Each segment has relationship_count + pct_of_firm_clients
      - "Other" segment aggregates all non-top-9 advisor client relationships
    This TO handles wiring those fields to the correct UI positions.
  </context>

  <fix_1 label="Center radial: wire to firm headline AUA">
    <description>
      The center of the ADV-AUA radial must display the same AUA figure shown in the
      Assets Overview header panel (the firm-level total AUA).

      The header AUA comes from getHeaderSummary() → platinum/firm/header_metrics.json
      (or once .024 ships, platinum/firm/header_metrics.json directly).

      The DistributionTab receives analyticsData as a prop. Check whether the
      partner_analytics response already carries the firm headline AUA at the top level,
      or whether DE needs to read it from a separate source.

      Options (in preference order):
        A. If analyticsData.headline_aua exists (or similar top-level field that DS .027
           populates), use that directly.
        B. If not, the DistributionTab parent (AdvisorIntelligence page) likely fetches
           the header metrics. Pass the headline AUA down as a prop to DistributionTab.
           Do NOT fire a new fetch just for this value.

      Regardless of source: the center label must say "Total AUA" and the value must
      match the header panel to the dollar. Do not derive it from segment data.
    </description>
  </fix_1>

  <fix_2 label="Segment subtext: # Clients and % of firm clients">
    <description>
      Each advisor segment in the ADV-AUA radial must show in its subtext:
        Line 1: "{N} Clients"  where N = relationship_count for this advisor
        Line 2: "{X.X}% of firm"  where X.X = pct_of_firm_clients for this advisor

      DS .027 issue_3c adds relationship_count and pct_of_firm_clients to each segment.
      DE wires these fields to the subtext render position.

      "Other" segment subtext:
        Line 1: "{N} Clients"  where N = count of relationships not in any top-9 advisor's book
        Line 2: "{X.X}% of firm"

      Do not show AUA percentage as the subtext (that is already conveyed by the donut arc size).
      The subtext is specifically about client relationship coverage.
    </description>
  </fix_2>

  <fix_3 label="Radial = Clients, Bell = Accounts">
    <description>
      Apply the universal count rule (from .028) to ADV-AUA:
      Radial segment count: relationship_count per advisor (Clients)
      Bell curve: account_count per advisor (Accounts)
    </description>
  </fix_3>

  <pii_note>
    IMPORTANT: When a user drills down on an advisor in this view, client names are
    displayed. These client names MUST be pseudonymized. This is a PII requirement
    tracked under ADVI_49PUSH.032 (separate TO). Do NOT implement client name display
    or drilldown in this TO -- leave the drilldown stub/placeholder as-is and note
    that it is blocked on .032. Do not introduce any cleartext client names in the
    ADV-AUA view at any drill level.
  </pii_note>

  <acceptance_criteria>
    1. Center radial shows firm headline AUA matching the Assets Overview header panel exactly
    2. Each advisor segment subtext shows relationship_count (Clients) + pct_of_firm_clients
    3. "Other" segment subtext shows non-top-9 relationship_count + pct
    4. Radial uses relationship_count, bell curve uses account_count
    5. No client names exposed in this view at any drill level (PII gate)
    6. Build clean, no TypeScript errors
    7. Visual: verify center value matches header AUA on opalinvest.dev
  </acceptance_criteria>


  <compiler_tools>
    comp-transform schema-check DistributionTab
      -- Run after wiring relationship_count + pct_of_firm_clients subtext.
         Confirms the new fields are rendering (not UNUSED) and the center total
         is sourced from the correct field (firm headline AUA, not a segment sum).

    comp-pii scan DistributionTab
      -- Run before shipping. Confirms zero client relationship names are rendered
         in this view. Required gate per .032 design decision.
  </compiler_tools>

</task_order>
