<task_order>
<metadata>
  <to_id>YALP_MACROS.006e</to_id>
  <project>YALP_MACROS</project>
  <title>Aggregate-class + orphan-indicator multi-source RE reconnaissance (Phase 2a parallel lane E)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~E</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — GO dispatch this cycle</status>
  <priority>HIGH (Andrew sovereign direct Phase 2 RE-OPEN; ws CTO v0.5 7e781ea8c)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MACROS.md v0.5 RE-OPENED `7e781ea8c` Phase 2 charter.</ref>
    <ref type="andrew_quote">"go exploring + parallelize a bunch of DS ... any govt source that might have those data fields/indicators"</ref>
    <ref type="sister_to">YALP_MACROS.006a/b/c/d (FRED/BLS/Census/Treasury-FDIC reconnaissance lanes).</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT exploratory reconnaissance. Sister lanes coordinate via TO-007 synthesis (Phase 2b).</dependency>
  </dependencies>
</metadata>

<scope>
**Aggregate-class + orphan-indicator exploration lane** per CTO v0.5 §8.

**Scope:** for any indicator NOT matched in sister-lane reconnaissance (TO-006a/b/c/d), locate canonical authoritative source. Targets include: NY Fed (recession probabilities, GDPNow), Atlanta Fed (GDPNow), Philly Fed (manufacturing surveys), ECB (Eurozone data if any indicator is non-US), private aggregators (Conference Board for LEI, Michigan for consumer sentiment, ISM for PMI), academic sources (Goyal-Welch ERP), commercial sources (S&P CoreLogic Case-Shiller for housing).

**Deliverable:** brief at `docs/briefs/yalp_macros_phase2a_aggregate_orphan_reconnaissance_2026-05-26.md` (~150-200 lines):
- §1 Aggregate-class source taxonomy (Federal Reserve regional Banks + private aggregators + academic + commercial)
- §2 Orphan-indicator catch-all: per-indicator routing for anything not in FRED/BLS/Census/Treasury-FDIC
- §3 Cadence + access-class (public API / proprietary / scraped / one-off downloadable) per source
- §4 RE harness sketch (heterogeneous-source harness design; not single-API uniform like FRED/BLS)
- §5 Coverage % closure: aim for 100% closure across all 5 reconnaissance lanes combined
- §6 Findings: any indicator that has NO authoritative source (true GAP-class for Phase 2c verdict)

**~E lane special:** catch-all sweep + coverage-closure verification. Last-line-of-reconnaissance ensures no indicator is unmatched.
</scope>

<acceptance_criteria>
Mirror YALP_MACROS.006a AC1-AC5 with aggregate-class focus. AC5 specifically: 100% coverage closure when combined with sister lanes OR explicit GAP-class enumeration for indicators with no source.
</acceptance_criteria>

<compiler_tools_mandate>
N/A — reconnaissance scope.
</compiler_tools_mandate>

<cross_domain_coordination>
- ~E is catch-all lane; coordinate with TO-007 synthesis to ensure full coverage closure.
- Phase 1 ~E strength: D3 §A predecessor-Phase-B-as-Level-2-evidence pattern + cascade ship 12-18x compression. Apply rigor to heterogeneous-source taxonomy.
- Andrew "monthly cadence acceptable" framing extends to aggregate-class — slow-frequency sources are acceptable for low-freq macro indicators.
</cross_domain_coordination>

<expected_evidence>
- Commit + brief path + aggregate-source taxonomy + orphan-indicator routing + coverage % closure
</expected_evidence>

<notes>
**ETA ~2-4h per Phase 2a wall.** Fast-trajectory endorsed.

**~E lane criticality:** without ~E catch-all sweep, coverage gaps would persist undocumented. Phase 2c empirical RE verification depends on Phase 2a coverage completeness.

**True GAP-class findings:** if any indicator has NO authoritative source across all 5 reconnaissance lanes, document as true RE-GAP (acceptable per Andrew direct "if data is pretty low frequency so if Yang has to update it once a month or something that doesnt really matter" + monthly-cadence-acceptable framing).
</notes>
</task_order>
