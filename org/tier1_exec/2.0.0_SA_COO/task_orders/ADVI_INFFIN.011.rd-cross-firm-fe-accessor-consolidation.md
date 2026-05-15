<task_order>
  <metadata>
    <id>ADVI_INFFIN.011</id>
    <slug>rd-cross-firm-fe-accessor-consolidation</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-13</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 by COO. Original conditions met: DS~B audit 9c3a4693e shipped + DS~C INFFIN.003 c5d98d41f + .010 5e5f18edd aligned INF schema (top-level book block + fee_summary.by_account[] per CTO Q1 Option A) + RD bench-available this session (per RD .002 log "Bench-available for .006 unblock"). 49F BD-pipeline retrofit per CTO Q1 ruling is a separate follow-on TO not yet authored — RD ships consolidation where alignment exists and documents fork-preserved divergences (per AC5).</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P2 — cross-firm FE accessor consolidation (49F + Inflection share one accessor); architectural cleanup; non-blocking for partner-demo</priority>
    <sla>~1-2h wall post-unblock; awaits DS~B audit alignment + RD next-session bandwidth</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inflection-finalize-20260513.md §Cross-Cutting Theme 2 (Fee-paying/No-fee/Combined as platform-wide concept)</ref>
    <ref type="audit_brief">docs/briefs/inffin-49f-fee-split-audit-20260513.md (DS~B INFFIN.005 ship 9c3a4693e — 9-section audit + normalization recommendations)</ref>
    <ref type="cto_routing">CTO INFFIN.006 RAVC2 triage 22:55Z — scope-split to INFFIN.011 (post-DS~B-audit-alignment + RD bandwidth)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="cross_link">Sibling: .005 DS~B 49F audit (audit deliverable shipped) + .006 RD Phase 2 wiring (10/12 items ACCEPTED + 1 HOLD + 2 scope-splits) + .012 Surface #8 reactive toggle (companion scope-split)</ref>
  </references>

  <context>
    DE 0.4 INFFIN brief §Cross-Cutting Theme 2: "Fee-paying / No-fee / Combined as platform-wide concept — must reactively partition every metric in AdvisorPublicProfile... 49F has mostly figured this out for BD pipeline; Inflection should mirror the same emit shape."

    DS~B INFFIN.005 (`9c3a4693e`, 360-line 9-section audit) shipped normalization recommendations:
    - 5 INF-missing fields (49F-ONLY): book.non_fee_earning_aua + book.non_fee_earning_account_count + book.implied_annual_revenue + book.avg_fee_bps_earned + top-level fee_summary block
    - 3 renames: total_fee_amount → implied_annual_revenue; weighted_avg_annual_fee_pct → avg_fee_bps_earned (pct→bps unit conversion); display_name → client_name
    - Structural divergence: 49F top-level book + fee_summary blocks vs INF headline + headline.billing scattered (phased reshape recommended)

    DS~C INFFIN.003 (`c5d98d41f`) + extension `5e5f18edd` partially aligned INF schema to 49F (top-level book block + fee_summary.by_account[] per CTO Q1 Option A). FE-side accessor consolidation is the natural completion: instead of two adapters (one for 49F, one for Inflection), share one accessor for partners with aligned schema.

    Per CTO INFFIN.006 RAVC2 22:55Z: scope-split because:
    - Cross-firm consolidation requires DS~B audit recommendations integrated into both 49F BD-pipeline emit + Inflection INF_D_02 emit
    - INF_D_02 already aligned partial (book block + fee_summary); 49F BD-pipeline retrofit per CTO Q1 ruling pending (separate follow-on TO not yet authored)
    - Gates on DS~B-audit-alignment full completion + RD bandwidth opens next session
  </context>

  <objective>
    Consolidate 49F + Inflection FE accessors where DS~B-audit-aligned schema exists. Single source of truth for fee-split rendering; both partners consume.

    Specifically:
    1. Identify all FE call-sites currently branching on firmId between 49F + Inflection accessors for fee-split data
    2. For each, verify DS~B-audit-aligned schema is available in both partner emits
    3. Consolidate into shared `_shared/accessors/` (or similar) primitive
    4. Remove redundant per-partner adapters where consolidated
    5. Document any remaining divergences requiring fork (not all fields will align)
  </objective>

  <scope>
    <surfaces>
      <surface id="cross-firm-consolidation">FE accessor consolidation across 49F + Inflection for fee-split rendering</surface>
    </surfaces>
    <files>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/_partners/49financial/ + _partners/inflection/ — enumerate firmId-branching accessors for fee-split data</file>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/_shared/ — locate existing shared accessor primitives</file>
      <file action="extract_or_create">portal/src/pages/AdvisorIntelligence/_shared/accessors/feeSplitAccessor.ts (or similar) — shared primitive</file>
      <file action="modify">FE call-sites — replace per-partner accessor calls with shared</file>
    </files>
  </scope>

  <phase id="1" when="pre-unblock-verify">
    <run>Verify DS~B audit recommendations integrated into both 49F + Inflection schemas (via DS~B INFFIN.005 audit + DS~C INFFIN.003/.010 ships + 49F BD-pipeline retrofit per CTO Q1 ruling separate TO)</run>
    <expect>Schema alignment confirmed empirically.</expect>
    <if_mismatch>If 49F retrofit hasn't shipped, surface to COO — gates on that work first.</if_mismatch>
  </phase>

  <phase id="2" when="investigation">
    <step>
      <description>Enumerate all FE call-sites currently branching on firmId between 49F + Inflection for fee-split data. Use `grep -rn "firmOverride === 'inf'" portal/src/pages/AdvisorIntelligence/` or similar.</description>
      <expect>Branching call-sites enumerated.</expect>
    </step>
    <step>
      <description>For each branching site, verify both partner emits have DS~B-audit-aligned schema. If alignment incomplete, document the gap.</description>
      <expect>Per-site alignment status documented.</expect>
    </step>
  </phase>

  <phase id="3" when="implementation">
    <step>
      <description>Extract or create shared accessor primitive in `_shared/accessors/`. Consume from typed shape (DS~B audit canonical).</description>
      <expect>Shared primitive landed.</expect>
    </step>
    <step>
      <description>Replace per-partner accessor calls at aligned call-sites. Preserve per-partner branching where alignment is incomplete (documented divergences only).</description>
      <expect>Branching reduced where alignment supports.</expect>
    </step>
    <step>
      <description>tsc 0 errors + bun run dev smoke against both 49F partner login + Inflection partner login.</description>
      <expect>Both partners render correctly.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: All FE call-sites previously branching on firmId between 49F + Inflection for fee-split data enumerated.
    AC2: Per-site alignment status documented (aligned → consolidate, divergent → fork preserved).
    AC3: Shared accessor primitive extracted; aligned call-sites converted.
    AC4: Per-partner adapters removed where consolidated.
    AC5: Documented divergences requiring fork (with rationale).
    AC6: tsc 0 errors; bun run dev smoke against both partners.
    AC7: Session log captures consolidation map + remaining divergences.
    AC8: MCP RAVC2 to COO.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>grep enumeration of firmId branching; comp-transform schema-check on shared accessor sites</phase_1>
    <phase_2>tsc + bun run dev smoke per partner</phase_2>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES:
    - DS~B INFFIN.005 audit recommendations integrated into 49F BD-pipeline emit (separate follow-on TO not yet authored; CTO Q1 Option A 49F retrofit candidate)
    - DS~C INFFIN.003/.010 INF schema alignment (mostly done; verify per-site)
    - RD bandwidth opens next session

    PARALLEL ACTIVITY:
    - .012 Surface #8 reactive toggle (companion scope-split; sibling .011)
    - AE 0.7 v1.7.56 Lambda mirror (Lambda parity; this TO is FE-only)

    NO PORTAL CONFLICT during dispatch_held; once unblocked, normal portal DEV → CLOUD cycle.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Pure FE consolidation. No data emit changes; no Lambda redeploys; no chain re-fires.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. FE consolidation map (per-site alignment status)
    2. Shared accessor primitive (extracted or created)
    3. Aligned call-sites converted
    4. Documented divergences (with rationale)
    5. Single or multiple commits under 0.4.2_RD_AdvisorIntelligence author per RD discipline
    6. tsc + bun run dev smoke evidence per partner
    7. MCP RAVC2 to COO
  </deliverables>

  <ravc>
    RD 0.4.2 RAVC2 to COO post-AC1-8 PASS. COO ratifies + relays to Andrew on partner-symmetry consolidation completion.
  </ravc>

  <notes>
    **Dispatch hold:** dispatch_held=true until DS~B audit alignment full completion + RD next-session bandwidth. COO unblocks via MCP.

    **49F BD-pipeline retrofit:** CTO Q1 ruling Option A requires 49F retrofits to `by_account[]` (currently emits `by_role[]`). Separate follow-on TO not yet authored. If 49F retrofit ships before this TO unblocks, consolidation is easier. If not, more divergences will need fork-preservation.

    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"` per protocol.
  </notes>
</task_order>
