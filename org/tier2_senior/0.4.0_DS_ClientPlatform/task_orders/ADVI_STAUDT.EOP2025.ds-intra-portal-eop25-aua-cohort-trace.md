<task_order>
  <metadata>
    <id>ADVI_STAUDT.EOP2025</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-20</date>
    <status>dispatched</status><!-- DISPATCHED 20260420T18:30Z by 2.0.0_SA_COO. CTO directive 20260420T182548Z; Andrew approval 20260420T181200Z on briefing sequencing. -->
    <project_code>ADVI_STAUDT</project_code>
    <priority>P3 — non-blocking side finding. Pure diagnostic; no fix in this TO.</priority>
    <lane>~B — parallel to ~A's BFIX1/2/3 chain. ~B is idle post-FIX2/bug_attribution close and has the recent bug-attribution / synthesis mental context. (~D alternative; ~B preferred for synthesis-doc continuity.)</lane>
    <bug_reference>~A briefing 20260420 (data/black_diamond/diagnostics/STAUDT/BRIEFING_aua_engine_accuracy_2026-04-20.md §"Side finding — intra-portal inconsistency"): Two portal-visible representations of EOP 2025 firm AUA disagree by $32M on the same date (2025-12-31). Portal monthly chart (`gold/timeseries_chart.json` aua.monthly 2025-12) = $1,446M. Sum of `canonical_nna.aua_current` on 2025-12-31 = $1,478M. Same date, same firm, two different numbers visible to the user via different UI paths.</bug_reference>
    <decision_authority>CTO 20260420T182548Z dispatch directive. Andrew approval 20260420T181200Z on briefing sequencing.</decision_authority>
  </metadata>

  <references>
    <ref type="briefing">data/black_diamond/diagnostics/STAUDT/BRIEFING_aua_engine_accuracy_2026-04-20.md §"Side finding"</ref>
    <ref type="parent">project_bd_is_ground_truth.md — if BD silver/allocations for 2025-12-31 is retrievable, use it as the canonical-correctness anchor</ref>
    <ref type="parent">feedback_no_unverified_theories_as_conclusions.md — "cohort-scope difference" is a hypothesis, not a verified cause; investigate before concluding</ref>
    <ref type="related">BFIX1+BFIX2+BFIX3 (~A) — these are forward-looking engine fixes for current snapshot drift. EOP2025 is a backward-looking diagnostic on a fixed historical date; non-overlapping scope.</ref>
  </references>

  <objective>
    Decompose the $32M delta between two portal-visible EOP 2025 firm AUA representations (`gold/timeseries_chart.json` aua.monthly 2025-12 = $1,446M vs sum of `canonical_nna.aua_current` on 2025-12-31 = $1,478M). Identify which accounts are in one rollup but not the other. If BD silver/allocations for 2025-12-31 is retrievable, identify which of the two rollups (if either) matches BD ground truth. Produce a recommendation on which rollup is canonical for portal display. NO code changes in this TO — diagnostic only.
  </objective>

  <scope>
    **Defect (verbatim from briefing §"Side finding"):**
    Two portal-visible representations of EOP 2025 firm AUA disagree:
    - Portal monthly chart (`gold/timeseries_chart.json` aua.monthly 2025-12): $1,446M
    - Sum of `canonical_nna.aua_current` on 2025-12-31: $1,478M
    - Same date, same firm, $32M delta, two different UI paths

    **Investigation steps:**

    1. **Identify the producer of each rollup:**
       - `gold/timeseries_chart.json` aua.monthly 2025-12 — which gold script writes this? D_00b? D_04? `comp-platinum reverse gold/timeseries_chart.json` should resolve.
       - `canonical_nna.aua_current` for 2025-12-31 — written by C_01.canonical_nna.py per prior wave context.

    2. **Pull both data sources for 2025-12-31:**
       - Per-account `aua_current` from canonical/nna/2025-12-31.parquet (sums to $1,478M per briefing)
       - Per-account contribution to the monthly aggregate that produced $1,446M (need to backtrack the aggregator's per-account inputs)

    3. **Account-level set difference:**
       - Which accounts are in canonical_nna.aua_current sum but NOT in the monthly aggregate?
       - Which accounts are in the monthly aggregate but NOT in canonical_nna?
       - Are values identical for accounts present in both, or are some accounts double-counted / scaled?

    4. **BD silver comparison (if retrievable):**
       - Does `s3://opal-data-bd/silver/allocations/2025-12-31.parquet` exist? If yes, sum to firm-level and compare against both rollups.
       - The rollup closer to BD silver is likely the more correct one (per `project_bd_is_ground_truth.md`).
       - If BD silver for 2025-12-31 is not available (e.g., file missing or different date format), document the gap.

    5. **Hypothesis evaluation (do not pre-commit):**
       - H1: Cohort-scope difference (one rollup includes accounts the other excludes — e.g., closed accounts, sub-accounts, "house" accounts)
       - H2: Date-boundary difference (one uses 2025-12-31 EOD, the other uses 2026-01-02 SOD or similar)
       - H3: Aggregation methodology difference (e.g., one filters by `is_excluded` flag, the other doesn't)
       - H4: Source-of-truth difference (one reads canonical/nna/, the other reads canonical/holdings/ or silver/allocations/)
       - H5: Time-snapshot drift between when the two artifacts were last written (one stale)

    6. **Recommendation:**
       - Which rollup should the portal display? (Canonical-anchored choice per BD comparison or methodology preference.)
       - If neither matches BD silver, both are wrong and a separate fix is needed (escalate).
       - If one matches BD silver, the other should be reconciled toward it (propose a follow-on TO if minimal, or escalate for scope decomposition).

    **OUT OF SCOPE:**
    - NO code changes (diagnostic only)
    - NO fix authoring within this TO — recommendation can propose a follow-on TO
    - Forward-looking snapshot drift (current 2026-04-16 gap is BFIX1/2/3 scope; EOP2025 is historical, fixed-date)
    - canonical_nna schema changes
    - Portal frontend display logic
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="rollup producer identification">
      <step>
        <run>comp-platinum reverse gold/timeseries_chart.json — identify which gold script writes aua.monthly</run>
        <expect>Single producer identified. Likely D_00b or D_04 based on prior wave context.</expect>
        <if_mismatch>If multiple producers contribute to aua.monthly, map all and disambiguate.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript consumers canonical_nna — confirm which scripts consume canonical_nna.aua_current and produce sum-to-firm-level rollups</run>
        <expect>Producer chain for the $1,478M rollup identified.</expect>
        <if_mismatch>If sum-to-firm-level happens at portal frontend (not in a gold script), document.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="account-level decomposition">
      <step>
        <run>Pull both data sources + compute set differences (in-A-not-B, in-B-not-A, in-both-with-value-diff)</run>
        <expect>3 account lists with MV totals reconciling to ±$32M.</expect>
        <if_mismatch>If reconciliation doesn't add up to $32M, the briefing premise is incomplete; document the residual.</if_mismatch>
      </step>
      <step>
        <run>If BD silver/allocations 2025-12-31 retrievable, sum to firm + compare to both</run>
        <expect>BD silver firm AUA for 2025-12-31. Compare to $1,446M and $1,478M.</expect>
        <if_mismatch>If BD silver for that date not retrievable, document and proceed without anchor.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="trace document + recommendation">
      <step>
        <run>Author cohort_delta_trace.md per scope</run>
        <expect>Complete diagnostic doc with rollup producer map, account-level decomposition, hypothesis evaluation, BD comparison (or absence), recommendation on which rollup is canonical.</expect>
        <if_mismatch>If diagnostic is inconclusive, document what additional data is needed.</if_mismatch>
      </step>
      <step>
        <run>MCP COO with trace doc + recommendation</run>
        <expect>COO can authorize follow-on fix TO if recommendation is actionable, or close as documented-known-issue if both rollups are within tolerance and methodology divergence is acceptable.</expect>
        <if_mismatch>If unclear, MCP for adjudication</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/EOP2025/cohort_delta_trace.md</path>
      <description>Cohort-level decomposition of $32M EOP 2025 AUA delta. Rollup producer map, in-A-not-B + in-B-not-A account lists with MV totals, hypothesis evaluation (H1-H5), BD silver comparison (or absence), recommendation on canonical rollup.</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] Both rollup producers identified (which scripts/lines write each)
    - [ ] Account-level set difference computed; reconciles to $32M ± rounding
    - [ ] BD silver/allocations 2025-12-31 comparison performed (or absence documented with reason)
    - [ ] Hypothesis evaluation (H1-H5) against gathered evidence
    - [ ] Recommendation on which rollup is canonical for portal display, with BD-anchored rationale where possible
    - [ ] NO code changes in this TO
  </acceptance_criteria>

  <guardrails>
    - **Diagnostic only.** No code changes; no fix dispatch within this TO.
    - **BD is ground truth.** Where retrievable, anchor the canonical-rollup recommendation against BD silver/allocations 2025-12-31 (per `project_bd_is_ground_truth.md`).
    - **No theory-as-conclusion.** The briefing labels this "likely a cohort-scope difference" but that's H1 — investigate, don't presume.
    - **Parallel to ~A's chain.** Doesn't compete for B_00 working-tree state. Read-only on canonical_nna + gold/timeseries_chart.json.
    - **No emojis, selective staging, agent commit identity** per existing memory rules.
  </guardrails>

  <agent_context_setup>
    1. Register + inbox-watch (first two tool calls)
    2. Read:
       - data/black_diamond/diagnostics/STAUDT/BRIEFING_aua_engine_accuracy_2026-04-20.md §"Side finding"
       - C_01.canonical_nna.py (writes canonical_nna.aua_current — confirm aggregation logic)
       - The script that writes gold/timeseries_chart.json aua.monthly (identify via comp-platinum reverse)
       - data/black_diamond/diagnostics/STAUDT/SYNTHESIS/coo_handoff.md + bug_attribution.md (your prior synthesis context)
    3. Heartbeat every 60s during active work
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1: ACK within 5 min: "ACK STAUDT.EOP2025 — starting Phase 0 rollup producer ID"
    - Phase 0 gate: brief MCP with rollup producers identified
    - Phase 1+2 gate: single MCP with account-level decomposition + recommendation
    - RAVC step 4: trace doc filed; recommendation either actioned via follow-on TO or closed as documented-known-issue
  </completion_protocol>
</task_order>
