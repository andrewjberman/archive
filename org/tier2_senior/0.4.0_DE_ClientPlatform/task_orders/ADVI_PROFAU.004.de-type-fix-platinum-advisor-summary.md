<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-profau-004</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_PROFAU</project_code>
  </metadata>

  <references>
    <ref type="audit_response">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/profau_gap_audit_response.md (Q6)</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform"
                task="ADVI_OFFICE.W3.de-ofc-frontend"
                status="staged"
                description="Pull latest CLOUD after W3 commit before editing types.ts. Third types.ts edit this session — W6-004 first, then W3, then .004."/>
  </dependencies>

  <objective>
    Fix the declared shape of `PlatinumAdvisorSummary` in `types.ts` to match what
    D_04 actually emits at `platinum/advisors/{id}/summary.json`. This is a type-declaration
    gap only — the data is already live. No gold script changes, no API changes.
    Closes Q6 from the PROFAU gap audit.
  </objective>

  <context>
    comp-transform schema-check AdvisorBookView confirms: PlatinumAdvisorSummary has 27 declared
    fields, only 3 rendered, 21 UNUSED. The root cause is that the declared `book` block is missing
    7 fee/tagged AUA fields that D_04 already emits, and `role_breakdown` is missing at the top level.

    D_04 advisor summary builder (lines 491-521) actually emits:
      book: { book_name, client_count, account_count, fee_earning_account_count,
              non_fee_earning_account_count, total_aua, tagged_aua, fee_earning_aua,
              non_fee_earning_aua, implied_annual_revenue, avg_fee_bps_earned,
              nna_qtd, nna_ytd, nna_mtd, growth, clients }
      role_breakdown: Record<string, { aua, pct_of_tagged, account_count?, client_count? }>
      (plus: concentration, fee_summary, tax_exposure, active_since, mix, mix_periods)

    Current PlatinumAdvisorSummary.book (types.ts 1841-1851) declares ONLY:
      book_name, client_count, account_count, total_aua, nna_qtd, nna_ytd, nna_mtd, growth, clients

    Missing from book: fee_earning_account_count, non_fee_earning_account_count, tagged_aua,
      fee_earning_aua, non_fee_earning_aua, implied_annual_revenue, avg_fee_bps_earned

    Missing at top level: role_breakdown

    getPlatinumAdvisorDrilldownSummary (api.ts 711-734) reads raw as Record<string, unknown>
    precisely BECAUSE the type is incomplete. Fixing the type enables real TypeScript coverage
    on the drilldown summary flatten.

    NOTE: do NOT add role_breakdown[role].fee_paying sub-objects — those only exist in
    leaderboard.json (D_00c), not in platinum/advisors/{id}/summary.json (D_02 path).
    D_02 role_breakdown has {aua, pct_of_tagged, account_count?, client_count?} only.
  </context>

  <scope>
    <files>
      <file action="edit">portal/src/types.ts — PlatinumAdvisorSummary.book block (lines ~1841-1851)</file>
      <file action="edit">portal/src/api/endpoints/advisor-intelligence.ts — tighten getPlatinumAdvisorDrilldownSummary input type from Record&lt;string,unknown&gt; to PlatinumAdvisorSummary once type is complete</file>
    </files>
    <out_of_scope>
      Rendering changes — this TO is type-only. Any new field rendering belongs in .005.
      Do NOT add fee_paying sub-objects to role_breakdown (that is a future DS TO).
    </out_of_scope>
  </scope>

  <acceptance_criteria>
    1. `bun run typecheck` passes with 0 new errors after the change.
    2. `PlatinumAdvisorSummary.book` declares: fee_earning_account_count, non_fee_earning_account_count,
       tagged_aua, fee_earning_aua, non_fee_earning_aua, implied_annual_revenue, avg_fee_bps_earned
       (in addition to existing fields).
    3. `role_breakdown` declared at top level of PlatinumAdvisorSummary with type
       `Record&lt;string, { aua: number; pct_of_tagged: number; account_count?: number; client_count?: number }&gt;`.
    4. `getPlatinumAdvisorDrilldownSummary` input typed as PlatinumAdvisorSummary (not Record&lt;string,unknown&gt;).
    5. comp-transform schema-check AdvisorBookView after change: UNUSED count on PlatinumAdvisorSummary
       reduced (previously 21 UNUSED; fee/tagged fields now declared and TypeScript coverage restored).
    6. Session log with compiler tools section committed.
    7. MCP message to 2.0.0_SA_COO: "PROFAU .004 complete — types.ts PlatinumAdvisorSummary fixed."
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1 (before writing): Run `comp-transform schema-check AdvisorBookView` — confirm baseline
    UNUSED count on PlatinumAdvisorSummary (expected: 21 UNUSED per session 26 COO run).
    Phase 2 (before commit): `bun run typecheck` — 0 new errors.
    Phase 3 (after commit): Run `comp-transform schema-check AdvisorBookView` again — confirm
    UNUSED count reduced and role_breakdown now declared. Append one line to org/compiler-tools-log.md.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>portal/src/types.ts</shared_resource>
    <required_action>
      Pull latest CLOUD before editing types.ts. This is the THIRD types.ts edit in the session
      flow: W6-004 (REBORN) → W3 (OFFICE) → .004 (PROFAU). Do NOT edit types.ts while W3 is
      in-flight. Wait for W3 commit to land on CLOUD before starting .004.
    </required_action>
    <none_if_confirmed>false</none_if_confirmed>
  </cross_domain_coordination>
</task_order>
