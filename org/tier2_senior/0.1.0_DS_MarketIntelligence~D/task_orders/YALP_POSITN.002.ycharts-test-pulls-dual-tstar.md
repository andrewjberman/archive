<task_order>
<metadata>
  <to_id>YALP_POSITN.002</to_id>
  <project>YALP_POSITN</project>
  <title>YCharts test-pulls for comparable-subset ETF universe (dual-T*)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~D</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <priority>HIGH (fast-lane regime; YALP per-page mandate continues)</priority>
  <go_source>ws COO MCP-body GO 2026-05-26T~18:30Z (broker message `20260526T180204Z_2.0.0_SA_COO__RAVC2-ACCEPT_YALP_POSITN.001_292218f1f__5_5.md`) — TO-002 dispatch authority delivered via RAVC2-ACCEPT message body per LD-0090 ALWAYS-PROCEED; formal TO file authored retroactively by assignee (~D) on TO ship for audit-trail closure</go_source>
  <references>
    <ref type="prd">docs/architecture/YALP_POSITN.md v0.2 commit 6e08c33f1</ref>
    <ref type="parent_to">YALP_POSITN.001 commit 292218f1f (Level-1 mapping; RAVC2-ACCEPTED 18:30Z)</ref>
    <ref type="ds020_consult">docs/briefs/yalp_positn_to003_yang_publication_timing_consult.md (dual-T* T*_positioning=5/22 + T*_holdings=5/18)</ref>
    <ref type="methodology_template">YALP_MKTOVR.002 dcbc50710 (closed 2026-05-26)</ref>
  </references>
  <dependencies>
    <dependency>YALP_POSITN.001 complete (RAVC2-ACCEPTED 18:30Z)</dependency>
    <dependency>YALP_POSITN TO-003 DS 0.2.0~C consult brief (shipped 17:00Z; provides dual-T* binding)</dependency>
  </dependencies>
</metadata>

<scope>
Execute YCharts test-pulls for the comparable-subset ETF universe across dual T* (T*_positioning=2026-05-22 weekly + T*_holdings=2026-05-18 monthly). Capture per-ticker pull-feasibility envelope; surface any structural findings (entitlement-gap / symbol-issue / cadence-anomaly); document dual-T* per-row alignment for TO-004 verdict assembly.

**ETF universe (post-CASH_USD exclusion):**
- 29 ETFs from positioning_data.json current_holdings @ T*=5/22
- 55 ETFs from holdings_attribution_data.json all-periods (QTD/YTD/1Y/SI) @ T*=5/18
- 28 ETFs in both sets pulled at BOTH T* (dual-coverage)
- Total: 84 pull attempts
</scope>

<acceptance_criteria>
- AC1: YCharts test-pulls executed for the comparable subset universe (pull-feasibility surface confirmed)
- AC2: DUAL T* discipline applied per DS 0.2.0 TO-003 brief (per-row t_star column populated)
- AC3: Structural findings surfaced (if any) with class taxonomy
- AC4: Pull-feasibility envelope captured (HTTP status + payload structure + data point count)
- AC5: TO-004 carry-forward path documented (dual-T* per-row alignment + per-finding mitigation)
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1:** YCharts freshness probe + per-ticker fund_data(calc='price') pulls + envelope capture
**Phase 2:** N/A — no portal-side compiler tools applicable (external API pull, not pipeline output)
**Phase 3:** Session log with Compiler Tools section + Lambda-class compiler-graph gap re-documentation
</compiler_tools_mandate>

<cross_domain_coordination>
- **YALP_MKTOVR predecessor:** TO-002 harness pattern (`.runtmp/yalp_mktovr_to002/run_local_pulls.py`) carry-forward per [[predecessor-as-ground-truth pattern]]
- **DS 0.2.0~C TO-003 consult:** dual-T* binding source (shipped 17:00Z)
- **TO-004 downstream consumer:** TO-002 results join per-ticker dual-T* aware
</cross_domain_coordination>

<expected_evidence>
- Brief §13 appendix in `docs/briefs/yalp_positn_positioning_field_comparison_2026-05-22.md`
- Harness + results in `.runtmp/yalp_positn_to002/` (gitignored)
- Per-finding mitigation path in §13.4
- TO-002 RAVC2 readiness in §13.10
</expected_evidence>

<notes>
TO file authored by assignee post-execution (LD-0090 ALWAYS-PROCEED cascade authority; ws COO MCP-body delivered GO without formal TO file landing on disk; per CLAUDE.md TO author + GO pairing rule, the MCP GO + this retroactive file together close the bookkeeping loop). Sister to YALP_MKTOVR pattern where COO authored TO-004+TO-005+TO-VAL files mid-cycle while DS executed cascade.

Owned-paths YAML now includes ~D per ws COO `1e61d10ac` extension commit (post-Andrew session-permission override); this commit lands via `safe-commit.sh` without --force.
</notes>
</task_order>
