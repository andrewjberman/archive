<task_order>
<metadata>
  <to_id>YALP_MACROS.006c</to_id>
  <project>YALP_MACROS</project>
  <title>Census Bureau multi-source RE reconnaissance (Phase 2a parallel lane C)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~C</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete — Census Bureau Phase 2a reconnaissance brief shipped `ba147dbc5` 22:35Z (~50min wall spawn→ship); 5/5 ACs MET (API surface + per-indicator match-set + cadence + harness sketch + coverage %); 10/79 (~12.7%) Census-PRIMARY across 6 EITS datasets; all 10 also FRED-mirror → FRED-PRIMARY + Census-SECONDARY recommended for TO-007 synthesis; 8 Census-specific quirks documented (stateless API-key auth = zero session-eviction class — sister-distinct from YCharts 403 risk); RAVC2-Request filesystem+broker delivered to ws COO 22:11Z. Standing for RAVC2-ACCEPT + Phase 2b TO-007 co-author dispatch.</status>
  <priority>HIGH (Andrew sovereign direct Phase 2 RE-OPEN; ws CTO v0.5 7e781ea8c)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MACROS.md v0.5 RE-OPENED `7e781ea8c` Phase 2 charter.</ref>
    <ref type="andrew_quote">"go exploring + parallelize a bunch of DS ... any govt source"</ref>
    <ref type="sister_to">YALP_MACROS.006a/b/d/e parallel reconnaissance lanes.</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT exploratory reconnaissance.</dependency>
  </dependencies>
</metadata>

<scope>
**Census Bureau exploration lane** per CTO v0.5 §8.

**Scope:** enumerate Census Bureau API endpoints + dataset coverage relevant to 79-indicator universe. Focus areas:
- **Housing & Construction**: building permits, housing starts, housing completions, new-home sales, existing-home sales (via Census + HUD partnership)
- **Retail & Manufacturing**: retail sales, durable goods orders, manufacturing surveys, business inventories, wholesale trade
- **Demographics & Employment**: ACS labor data (where overlapping BLS), population estimates
- **Trade**: international trade in goods + services

Match per-indicator Census authoritative-source candidates for each yang macro_data.json indicator. Document API surface + cadence (most Census series are monthly).

**Deliverable:** brief at `docs/briefs/yalp_macros_phase2a_census_reconnaissance_2026-05-26.md` (~150-200 lines):
- §1 Census API surface (data.census.gov API + topic-specific endpoints)
- §2 Per-indicator match-set: 79 yang indicators → Census dataset+series ID OR `n/a`
- §3 Cadence per Census dataset (most monthly; some quarterly/annual)
- §4 RE harness sketch (Census API key + topic-specific endpoints + series ID lookup)
- §5 Coverage % + sister-lane handoffs
- §6 Census-specific quirks (revision schedules, seasonal-adjustment availability, advance-vs-revised releases)

**Likely Census coverage focus:** housing/construction (high-priority macro indicators) + retail/manufacturing + trade.
</scope>

<acceptance_criteria>
Mirror sister-lane AC1-AC5 with Census substitution: API surface + per-indicator match-set + cadence + harness sketch + coverage %.
</acceptance_criteria>

<compiler_tools_mandate>
N/A — reconnaissance scope.
</compiler_tools_mandate>

<cross_domain_coordination>
- Sister lanes: ~A FRED (some Census series duplicate in FRED via Federal Reserve mirroring; distinguish upstream Census from FRED-mirror)
- TO-007 synthesis convergence with ~A primary author
- Andrew "monthly cadence acceptable" framing — Census monthly cadence is appropriate
</cross_domain_coordination>

<expected_evidence>
- Commit + brief path + 79-indicator match-set + cadence + harness sketch + coverage %
</expected_evidence>

<notes>
**ETA ~2-4h per Phase 2a wall.** Fast-trajectory regime endorsed by Andrew MSTR LD-0104.

**Phase 2b TO-007 synthesis** co-author with ~A primary post all-5-lanes ship.

**Welcome back to active dispatch** post-Phase-1 KEEP-EPHEMERAL standby. Your ~C Phase 1 strength = sister-pattern BLOCKED-ASK at spawn-time + honest-partial-coverage with .006-EMPIRICAL follow-on banking; apply rigor to Census taxonomy.
</notes>
</task_order>
