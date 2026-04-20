<task_order>
  <metadata>
    <id>ADVI_STAUDT.INV4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-20</date>
    <status>complete</status><!-- DEFERRED 2026-04-20 — Phase 0 trace by ~A determined OFC-NNA asymmetry lives in caller above D_00b L450, not D_00b internal. Investigation outcome satisfied (no code change warranted inside D_00b). Callsite audit folded into B_00 mini-PRD backlog (post-STAUDT). Evidence: DS~A log `staudt_engine_accuracy_bfix12.md`. CTO reconciliation session 35. -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P1 — investigation only, no code change unless finding warrants. Phase 0 of the FIX3B/FIX7 work.</priority>
    <lane>~A — Phase 0 of D-script wave. Report before any code change.</lane>
    <bug_reference>CTO 20260420T162726Z. D_00b OFC aggregation hypothesis: Continuous-OFC-NNA shows different total than Continuous-GEO-NNA / Continuous-ADV-NNA, despite all three being conditional on the same account universe (L457 if account_office_dim:). Hypothesis: D_00b L499-528 cumulative all-time "Continuous" view may handle OFC differently — ofc_agg may not participate in cumulative rollup while ADV/GEO do.</bug_reference>
    <decision_authority>CTO 20260420T162726Z investigation directive.</decision_authority>
  </metadata>

  <references>
    <ref type="cto-directive">CTO 20260420T162726Z — comprehensive fix directive (FIX3B + FIX7 + INV4)</ref>
    <ref type="related-fix">FIX3B — same script (D_00b), same wave</ref>
    <ref type="related-fix">FIX7 — same script (D_00b), same wave</ref>
  </references>

  <objective>
    Trace D_00b's Continuous (cumulative all-time) OFC aggregation path to determine why Continuous-OFC-NNA differs from Continuous-GEO-NNA + Continuous-ADV-NNA when all three should aggregate the same account universe. Either (a) confirm an aggregation-path bug + propose minimal surgical fix in same ~A commit, or (b) confirm legitimate methodology difference + document. Phase 0 of FIX3B/FIX7 wave — report finding before coding any OFC fix.
  </objective>

  <scope>
    **Defect (verbatim from CTO 20260420T162726Z):**
    OFC aggregation in D_00b is conditional (L457: `if account_office_dim:`) and uses the same account universe as GEO/ADV. Theoretically should produce same total NNA. But Andrew observes different numbers.

    Hypothesis: there may be a second aggregation path at D_00b L499-528 (cumulative all-time "Continuous" view) that handles OFC differently from ADV/GEO — ofc_agg may not participate in the cumulative rollup while ADV/GEO do.

    **Investigation steps:**
    1. Read D_00b L450-540 to map every OFC, GEO, ADV aggregation entry point
    2. Identify whether the Continuous (cumulative) rollup path at L499-528 includes ofc_agg participation symmetric to adv_agg + geo_agg
    3. Quick numeric diagnostic: emit D_00b's ofc_agg row-sum + geo_agg row-sum + adv_agg row-sum on a sample run; do they match on the per-row aggregation level (before Continuous rollup), and do they diverge at the Continuous rollup?

    **Decision tree:**
    - **If Continuous rollup excludes ofc_agg by oversight:** propose 2-3 line fix that adds ofc_agg to the cumulative path. Bundle with FIX3B+FIX7 in same ~A commit if minimal.
    - **If Continuous OFC numbers differ for legitimate methodology reason** (e.g., OFC dimension has different accounts populated than GEO):** document the rationale in INV4 evidence file. No code change.
    - **If finding requires more than a 5-line code change:** stop, MCP COO with full diagnostic report, defer to separate FIX-TO.

    **OUT OF SCOPE:**
    - No changes to OFC/GEO/ADV upstream computation logic
    - No changes to account_office_dim or account_geography_dim sources
    - No methodology changes — restoring symmetric aggregation only if that's the bug
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="diagnostic">
      <step>
        <run>Read D_00b L450-540 — full mapping of OFC/GEO/ADV per-row aggregation entries + L499-528 Continuous rollup path</run>
        <expect>Clear identification of whether ofc_agg participates symmetrically with geo_agg and adv_agg in cumulative rollup</expect>
        <if_mismatch>If structure unclear or non-obvious, expand read to L400-600 for full function context</if_mismatch>
      </step>
      <step>
        <run>Local dry-run D_00b on current prod date — emit per-row sums for ofc_agg / geo_agg / adv_agg + Continuous-cumulative sums for each</run>
        <expect>Clear numerical comparison: row-level + cumulative-level deltas. If row-level matches but cumulative diverges, points to rollup path. If row-level also differs, points to upstream universe difference.</expect>
        <if_mismatch>Numerical diagnostic itself can't run = MCP COO with reason</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/INV4/inv4_ofc_aggregation_trace.md</path>
      <description>Code path map (which OFC aggregation participates where) + numerical diagnostic table (row-level vs cumulative-level OFC/GEO/ADV sums) + decision verdict (bug vs methodology) + minimal-fix proposal if applicable.</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Full code-path map of D_00b OFC/GEO/ADV aggregation (which lines do what)
    - [ ] Numerical diagnostic comparing row-level + cumulative sums for OFC/GEO/ADV
    - [ ] Verdict: bug (with proposed fix lines) OR methodology difference (with rationale)
    - [ ] If bug + ≤5-line fix: bundled with FIX3B+FIX7 in same commit
    - [ ] If bug requiring larger fix: MCP COO + defer to separate TO
    - [ ] Evidence file documents finding and decision
  </acceptance_criteria>

  <guardrails>
    - **Investigation first, code second.** Phase 0 mechanism note BEFORE any patch.
    - **Minimal fix only.** If the OFC fix can't be done in 2-3 surgical lines, defer to a separate FIX-TO.
    - **No Option B scope creep** — don't investigate role_aua/ or canonical layer for OFC; INV4 is D_00b-internal only.
    - **Same wave as FIX3B+FIX7** — bundle in the ~A commit if applicable.
    - **No emojis, selective staging, agent commit identity**
  </guardrails>

  <agent_context_setup>
    1. Same context as FIX3B + FIX7
    2. Add: D_00b L450-540 read window
    3. CTO 20260420T162726Z bug analysis
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK bundled with FIX3B + FIX7
    - Phase 0 gate: bundle finding + decision verdict in single MCP with FIX3B + FIX7 Phase 0
    - If code change: RAVC step 4 bundled with FIX3B + FIX7
    - If methodology only: close on Phase 0 evidence file
  </completion_protocol>
</task_order>
