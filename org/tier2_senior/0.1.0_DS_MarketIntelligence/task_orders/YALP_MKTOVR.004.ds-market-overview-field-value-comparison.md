<task_order>
<metadata>
  <to_id>YALP_MKTOVR.004</to_id>
  <project>YALP_MKTOVR</project>
  <title>Level-2 value comparison + per-field verdicts (~4-6h or faster per DS 0.1.0 throughput)</title>
  <assigned_to>0.1.0_DS_MarketIntelligence</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending</status>
  <priority>HIGH (Andrew sovereign direct 2026-05-26 ~15:00Z: "finish YALP_MKTOVR end-to-end, call CVO for verify-channel at completion"; LD-0090 ALWAYS-PROCEED authorized; DS 0.1.0 cascading per same direct)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MKTOVR.md v0.4 commit `1f6387616` (1.0.0_SA_CTO; TO-005 add + serialization auth + DRIFT routing). §6 TO-004 block.</ref>
    <ref type="predecessors">TO-001 SHIPPED `cc4a3d575` (RAVC2-ACCEPT 14:51Z) + TO-002 SHIPPED `dcbc50710` (RAVC2-ACCEPT 15:09Z; 18/18 OK + zero 403s) + TO-003 retrospective `<status>complete</status>` (DS 0.2.0 consult brief `8d1d6fcad` = deliverable).</ref>
    <ref type="cto_spreadsheet_skeleton">docs/briefs/yalp_mktovr_side_by_side_spreadsheet_2026-05-22.md (CTO `1f6387616`) — 60+ row 6-column structural skeleton; D/E/F columns populated by TO-005 from THIS TO's outputs.</ref>
  </references>
  <dependencies>
    <dependency>TO-001 + TO-002 complete ✓. T*=2026-05-22 locked ✓.</dependency>
    <dependency>AC9-INDEPENDENT (read-only verification scope per PRD §0).</dependency>
  </dependencies>
</metadata>

<scope>
Per PRD v0.4 §3.1 Level-2 methodology + §6 TO-004:

**Phase 3:** Pull yang-side rendered values for all Level-1 fields from `opal-data-portal-v2/json-tiered/market-overview/*.json` on T*=2026-05-22 (production S3 layer portal renders).

**Phase 4:** Cross-reference per field against TO-002 YCharts values. Assign verdict per PRD §3.1:
- **MATCH** — values equal within tolerance
- **REPRESENTATIVE** — values differ but both valid representations (REPRESENTATIVE-class boundary discipline: include YCharts methodology citation OR delta-magnitude bound per CVO pre-propagate gate `d12028652` preventive flag)
- **DRIFT** — material divergence; route via RAVC2 close-MCP to CTO + COO + Andrew (NOT absorbed into project scope per PRD §6+§7+§9)
- **GAP** — yang has field but YCharts doesn't (or vice versa)

**Output:** populate Level-2 table in `docs/briefs/yalp_mktovr_market_overview_field_comparison_2026-05-22.md` §10 (currently empty placeholder per TO-001 brief).
</scope>

<acceptance_criteria>
- AC1: Every Level-1 field has a Level-2 verdict + per-field note where verdict != MATCH.
- AC2: REPRESENTATIVE verdicts include explicit reasoning (YCharts methodology citation OR delta-magnitude bound) per CVO sharp-test discipline.
- AC3: DRIFT findings surface to CTO + COO + Andrew via RAVC2 close-MCP with field-level evidence (yang value, YCharts value, % delta).
- AC4: Tier-3 sampled tickers per TO-001 §9.4 plan (15 tickers × 2 endpoints = 30 Tier-3 pulls covered).
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 3-4:** No net-new comp-* tools required (external-API + S3-direct pulls). Session log with archetype VALIDATE.
</compiler_tools_mandate>

<expected_evidence>
- Commit hash for brief §10 Level-2 table population
- DRIFT-finding routing MCPs (if any) to CTO + COO + Andrew
- Session log
</expected_evidence>

<notes>
**Andrew direct sovereign 2026-05-26 ~15:00Z** + **15:30Z** authorize completion cascade + serialization. DS 0.1.0 is cascading per LD-0090 ALWAYS-PROCEED — formal GO from me is bookkeeping; do not wait for it to commit.

**Serialization decision (COO):** HOLD on DS 0.1.0~A spawn for now. Your TO-001 (~50min) + TO-002 (~10min) throughput is well ahead of estimates. If TO-004 ETA shifts above 2h mid-flight, MCP me with status — I'll dispatch DS 0.1.0~A for TO-VAL+TO-005 parallel-consolidation at that point.

**Sequential queue (this TO + downstream):** TO-004 → TO-VAL → TO-005 → COO 3-step project-close + CVO `/verify-channel` project-level mode invocation. COO drives the 3-step close per CLAUDE.md Closure Discipline (SA/COO/CTO only); you signal TO-VAL + TO-005 ship + I close.

**REPRESENTATIVE-class discipline reinforcement** (per CVO pre-propagate gate `d12028652` preventive flag): for any REPRESENTATIVE verdict, include YCharts methodology citation OR delta-magnitude bound. Prevents laundering-channel risk on DRIFT-class findings.

**DRIFT-routing rule:** material DRIFT findings route via RAVC2 close-MCP to CTO + COO + Andrew for future-project scoping. Do NOT absorb into THIS project.

Architectural / scope ambiguity → ws CTO. Dispatch / RAVC2 / blockers → me.
</notes>
</task_order>
