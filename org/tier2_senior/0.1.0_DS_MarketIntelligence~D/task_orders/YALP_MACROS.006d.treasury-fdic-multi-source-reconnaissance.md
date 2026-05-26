<task_order>
<metadata>
  <to_id>YALP_MACROS.006d</to_id>
  <project>YALP_MACROS</project>
  <title>Treasury/FDIC/other federal-source multi-source RE reconnaissance (Phase 2a parallel lane D)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~D</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete — brief shipped 2026-05-26; 5/5 ACs MET; standing RAVC2-ACCEPT</status>
  <priority>HIGH (Andrew sovereign direct Phase 2 RE-OPEN; ws CTO v0.5 7e781ea8c)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MACROS.md v0.5 RE-OPENED `7e781ea8c` Phase 2 charter.</ref>
    <ref type="andrew_quote">"go exploring + parallelize a bunch of DS ... any govt source"</ref>
    <ref type="sister_to">YALP_MACROS.006a/b/c/e parallel reconnaissance lanes.</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-INDEPENDENT exploratory reconnaissance.</dependency>
  </dependencies>
</metadata>

<scope>
**Treasury/FDIC/other federal-source exploration lane** per CTO v0.5 §8.

**Scope:** enumerate non-FRED/BLS/Census federal-source endpoints. Focus areas:
- **Treasury Direct**: daily Treasury yield curve rates (alternative to FRED for UST yields), Treasury auction data, federal debt data
- **FDIC**: bank failure data, deposit insurance fund metrics, banking statistics
- **OCC, Federal Reserve Banks**: Beige Book, FOMC minutes, regional Fed surveys (Empire State manufacturing, Philly Fed manufacturing, KC Fed surveys)
- **CFPB**: consumer financial complaint data, lending data
- **SSA**: cost-of-living adjustments, demographic data
- **Other federal**: any government source NOT covered by FRED/BLS/Census/Treasury core

Match per-indicator authoritative-source candidates for each yang macro_data.json indicator not covered by sister lanes. Document API surface + cadence per source.

**Deliverable:** brief at `docs/briefs/yalp_macros_phase2a_treasury_fdic_reconnaissance_2026-05-26.md` (~150-200 lines):
- §1 Treasury Direct API surface + FDIC BankFind API + regional Fed survey access patterns
- §2 Per-indicator match-set: any yang indicators sourced via these endpoints
- §3 Cadence per source (Treasury yields daily; FDIC quarterly; Fed surveys monthly)
- §4 RE harness sketch (multi-endpoint orchestration per source-class)
- §5 Coverage % + sister-lane handoffs
- §6 Source-specific quirks (Treasury yield-curve methodology, FDIC reporting-lag, regional Fed survey participation rates)

**Likely focus:** UST yields cross-validation against FRED (~A lane) + regional Fed manufacturing surveys + any indicator not in FRED/BLS/Census.
</scope>

<acceptance_criteria>
Mirror sister-lane AC1-AC5 with Treasury/FDIC substitution.
</acceptance_criteria>

<compiler_tools_mandate>
N/A — reconnaissance scope.
</compiler_tools_mandate>

<cross_domain_coordination>
- Sister-lane overlap: UST yields covered by FRED ~A lane; distinguish Treasury Direct as upstream-authoritative vs FRED-mirror in §2 match-set
- Regional Fed surveys distinct from FRED aggregates
- TO-007 synthesis convergence with ~A primary author
</cross_domain_coordination>

<expected_evidence>
- Commit + brief path + per-indicator match-set + cadence + harness sketch + coverage %
</expected_evidence>

<notes>
**ETA ~2-4h per Phase 2a wall.** Fast-trajectory endorsed.

**Phase 2b TO-007 synthesis** co-author with ~A primary.

**Welcome back to active dispatch** post-Phase-1 KEEP-EPHEMERAL standby. Your ~D Phase 1 strength = dual-T* discipline + GAP-heavy probe + iterative-verdict refinement + harness envelope-shape upstream-wrapper unaware banking; apply rigor to multi-endpoint federal-source orchestration.
</notes>
</task_order>
