<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-advi-fntend-b7-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status><!-- INVESTIGATION COMPLETE 2026-04-15 PM (~C). Analysis shipped 7708f0c8 (2026-04-14). Post-rerun measurement appended 2026-04-15 17:55 ET: continuous vs snapshot.aua delta = $0.01 (0.0000%) at Q4 2025 boundary -- no divergence exists. Cause (b) downsample gap did not materialize because _weekly_downsample includes Dec 31 explicitly. Recommend ACCEPT with no FE footnote / no B7b TO. Side finding (geo-donut vs aua-donut $3.73M intra-snapshot gap) flagged for separate ADVI triage. Closeout: docs/data/2026-04-14_q4_aua_continuous_vs_snapshot.md "Measurement results" + "B7 closeout recommendation" sections. -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
    <type>investigation-only</type>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 7: D1)</ref>
  </references>

  <objective>
    Investigate Q4-2025 continuous-vs-snapshot AUA divergence. Identify whether
    `cumulative_chart.json` last-of-quarter differs from `partner_analytics.json`
    asof snapshot due to:
      (a) different source (D_01 path vs pipeline)
      (b) point-in-time selection rule (close-of-day vs end-of-period)
      (c) missing reconciliation of one feed

    Output: reconciliation spec (session log + one-page doc under `docs/data/`).
    No code changes in this TO — FE work gated on findings (may spawn B7b).
  </objective>

  <acceptance_criteria>
    1. Reconciliation spec committed under docs/data/
    2. Doc identifies root cause (a/b/c or combination)
    3. Doc proposes fix path (new B7b TO spec or doc-only explanation)
    4. MCP COMPLETE to COO with commit + summary
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io` on both cumulative_chart producer (D_01 area) and partner_analytics producer; diff the as-of-date selection logic. **`comp-pipescript consumers cumulative_chart.json` + `comp-pipescript consumers partner_analytics.json`** to enumerate every downstream affected by any reconciliation fix.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <next>On COMPLETE: COO reviews + decides whether to spawn B7b FE TO.</next>
</task_order>
