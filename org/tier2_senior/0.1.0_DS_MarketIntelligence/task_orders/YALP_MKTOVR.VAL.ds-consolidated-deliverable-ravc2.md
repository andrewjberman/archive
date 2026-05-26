<task_order>
<metadata>
  <to_id>YALP_MKTOVR.VAL</to_id>
  <project>YALP_MKTOVR</project>
  <title>Consolidated deliverable RAVC2 + CVO /verify-channel project-mode pass (~1-2h)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <completed>2026-05-26</completed>
  <closure_ship>TO-VAL deliverable: §15+§16 of source brief. Per-component cutover-trust verdict: 3 TRUST + 4 NEEDS-INVESTIGATION-representative-bound + 3 n/a-out-of-cutover-scope; no NO-TRUST. 8/8 project-level ACs met per §16.1 scorecard. CVO /verify-channel project-level MCP fired this cycle.</closure_ship>
  <priority>HIGH (Andrew sovereign direct 2026-05-26 ~15:00Z)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MKTOVR.md v0.4 §6 TO-VAL block.</ref>
    <ref type="predecessor">TO-004 (Level-2 value comparison) — gates this TO.</ref>
  </references>
  <dependencies>
    <dependency>TO-004 ship + per-field Level-2 verdicts populated in §10.</dependency>
  </dependencies>
</metadata>

<scope>
Final assembly of `docs/briefs/yalp_mktovr_market_overview_field_comparison_2026-05-22.md`:
- Per-component sections (already populated by TO-001)
- Level-1 + Level-2 tables (populated by TO-001 + TO-004)
- **Per-component cutover-trust verdict** (new): TRUST / NEEDS-INVESTIGATION / NO-TRUST based on aggregate per-component verdicts (e.g., all MATCH = TRUST; any DRIFT = NO-TRUST or NEEDS-INVESTIGATION based on materiality).

RAVC2 to COO + CC CTO when assembled. **MCP CVO `3.0.0_SA_CVO`** with `/verify-channel` project-level mode invocation request for closeout adequacy gate.
</scope>

<acceptance_criteria>
- AC1: Consolidated deliverable on origin/CLOUD with per-component cutover-trust verdict explicit.
- AC2: CVO surface-pass via `/verify-channel` project-level mode = GREEN (closeout adequacy gate).
- AC3: RAVC2-Request to COO + CC CTO + Andrew with consolidated deliverable summary.
</acceptance_criteria>

<expected_evidence>
- Commit hash for consolidated deliverable
- Per-component cutover-trust verdict table
- CVO `/verify-channel` project-mode verdict (GREEN/CONCERN/REPAIR-AMENDMENT) — banking dimension for project close
</expected_evidence>

<notes>
**COO drives 3-step project-close** (per CLAUDE.md Closure Discipline — SA/COO/CTO only):
1. JSON `org/projects/YALP_MKTOVR.json` `status: "complete"` + `completed: "YYYY-MM-DD"` + closure summary narrative
2. REGISTRY.md row → "Completed / Archived Projects" table (newest-first)
3. PRD `Status:` line update if present

DS 0.1.0 signals TO-VAL ship; COO does 3-step close in same commit window post-CVO surface-pass.

**DRIFT-finding aggregation:** if any TO-004 DRIFT findings landed mid-flight + route-to-future-project per PRD §6+§7+§9, surface them in this consolidated deliverable's top-of-doc summary section as well (Andrew explicit visibility).

Standing for TO-004 ship signal → fire this TO + close-out chain.
</notes>
</task_order>
