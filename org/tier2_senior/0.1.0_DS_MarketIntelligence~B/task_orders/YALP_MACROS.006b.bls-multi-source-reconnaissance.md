<task_order>
<metadata>
  <to_id>YALP_MACROS.006b</to_id>
  <project>YALP_MACROS</project>
  <title>BLS multi-source authoritative-source RE reconnaissance (Phase 2a parallel lane B)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~B</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — GO dispatch this cycle</status>
  <priority>HIGH (Andrew sovereign direct Phase 2 RE-OPEN; ws CTO v0.5 7e781ea8c)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MACROS.md v0.5 RE-OPENED `7e781ea8c` Phase 2 charter.</ref>
    <ref type="andrew_quote">"go exploring + parallelize a bunch of DS ... FRED, BLS, any govt source"</ref>
    <ref type="sister_to">YALP_MACROS.006a (FRED reconnaissance ~A lane) — same scope shape, different authoritative source.</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT exploratory reconnaissance.</dependency>
  </dependencies>
</metadata>

<scope>
**BLS exploration lane** per CTO v0.5 §8.

**Scope:** enumerate BLS API endpoints + LNS/CES/CPI/PPI/JOLTS/etc dataset coverage relevant to 79-indicator universe. Match per-indicator BLS authoritative-source candidates for each yang macro_data.json indicator. Document coverage breadth + cadence per BLS series.

**Deliverable:** brief at `docs/briefs/yalp_macros_phase2a_bls_reconnaissance_2026-05-26.md` (~150-200 lines):
- §1 BLS API surface (Public Data API v2 endpoints + series ID convention)
- §2 Per-indicator match-set: for each 79 yang indicators, BLS series ID(s) OR `n/a`
- §3 Cadence per BLS series
- §4 RE harness sketch (BLS API key + series ID lookup + observations endpoint)
- §5 Coverage % + sister-lane handoffs
- §6 Findings: BLS-specific data quirks (revision-vs-release, seasonal-adjustment, etc.)

**Likely BLS coverage focus:** labor stats (unemployment, NFP, payrolls), inflation (CPI, PPI, ECI), productivity, occupations. Sister to FRED — many BLS series duplicate in FRED but BLS is upstream authoritative.
</scope>

<acceptance_criteria>
Mirror YALP_MACROS.006a AC1-AC5 with BLS substitution: API surface enumerated + per-indicator match-set + cadence + harness sketch + coverage %.
</acceptance_criteria>

<compiler_tools_mandate>
N/A — reconnaissance scope.
</compiler_tools_mandate>

<cross_domain_coordination>
- Sister lane to ~A FRED + ~C Census + ~D Treasury-FDIC + ~E Aggregate-orphan. Independent reconnaissance; convergence at TO-007 synthesis.
- BLS series often duplicate in FRED — distinguish upstream authoritative (BLS) from FRED-mirror in your §2 match-set.
- ~B Phase 1 strength: cookie-stale-OK doctrine maturation + cleanest fast-lane cascade today. Apply discipline to BLS API exploration.
</cross_domain_coordination>

<expected_evidence>
- Commit + brief path + 79-indicator match-set + cadence + harness sketch + coverage %
</expected_evidence>

<notes>
**ETA ~2-4h per Phase 2a wall.** Fast-trajectory endorsed by Andrew MSTR LD-0104.

**~B Phase 1 strength:** 6+ days cookie-stale-OK doctrine experience; F1 MATCH-to-bp empirical convergence. Apply rigor to BLS source-mapping.
</notes>
</task_order>
