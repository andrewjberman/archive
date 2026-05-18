<task_order>
  <metadata>
    <id>ADVI_INFGRO.009</id>
    <slug>dsc-infc02-twr-factor-rebuild-method-y</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-18 on the CTO Method-Y ruling. No external gate on starting Phase 0 (the probe is read-only). NOTE: when the AE 0.7.0 chain-completion ping lands, PAUSE this TO and prioritize the INFGRO.007 + BIWNDW.002 leaderboard verification + RAVC2 closes (partner-facing-gating) -- resume .009 after.</dispatch_unblock_condition>
    <project_code>ADVI_INFGRO</project_code>
    <priority>P1 -- the single INF_C_02 fix that clears BOTH Finding A (window-TWR ~6x absolute-scale understatement) and Finding B (epsilon-dominance 71.6%). It is now on the partner-facing critical path: INFGRO.005 cannot go partner-facing until this lands + a subsequent chain run.</priority>
    <sla>Phase 0 probe ~2-3h (read-only). Phase 1+ contingent on the Phase-0 data-source outcome; ~4-6h wall if the summaries block or the Orion probe yields a usable series, longer if the guard-railed X fallback is forced (escalates first).</sla>
  </metadata>

  <references>
    <cto_ruling>1.0.0_SA_CTO ruling 2026-05-18 on the INFGRO.008 Phase-0 escalation -- Method Y (authoritative Orion TWR series) ACCEPTED as primary; Method X (reconstruct cumulative from the annualized rate) REJECTED as primary (numerically unsound at daily grain + violates PRD section 2.4 measured-not-assumed) -- X retained ONLY as a guard-railed last-resort fallback; Method Z rejected. The fix is PROBE-FIRST, not blind implementation.</cto_ruling>
    <diagnosis_brief>docs/briefs/infgro-finding-b-epsilon-coverage-diagnosis-20260518.md (DS, 90e502c39) -- ROOT CAUSE: INF_C_02 `_build_daily_factor_table` misinterprets silver/performance_dim `twr_factor_period` (an inception-to-date ANNUALIZED TWR rate) as a cumulative-growth factor; return_$ comes out ~6-10x too small and epsilon_$ absorbs the remainder. Candidates (i) coverage and (ii) staleness were ruled OUT with evidence. SCOPE the fix off this brief's Method X/Y/Z framing -- NOT off the INFGRO.008 TO's A/B/C (which was coverage-framed and is superseded; coverage was ruled out).</diagnosis_brief>
    <prd>docs/architecture/ADVI_INFGRO_PRD.md section 8 -- CTO is folding this finding into a v0.7 amendment himself; do NOT edit the PRD. Section 8.4's "Finding A and Finding B are distinct defects but can share one upstream INF_C_02 root" prediction held exactly -- this one fix clears both.</prd>
    <upstream_dependency>TO-INFGRO.002 (f39550d99) -- persisted a bronze/performance summaries block; Phase 0 Step 1 inspects whether it carries per-client window returns.</upstream_dependency>
    <sibling_shipped>INFGRO.007 (2952a1bee) -- the `_window_twr_two_axis` Axis-1/Axis-2 aggregation in INF_D_00c. It is CORRECT and is NOT reopened by this TO; it only needs corrected inputs from INF_C_02.</sibling_shipped>
  </references>

  <context>
    Finding A (window TWRs ~6x understated in absolute scale) and Finding B (epsilon 71.6% of the AUA-growth decomposition) share ONE upstream root: INF_C_02 `_build_daily_factor_table` treats `twr_factor_period` -- an inception-to-date annualized rate -- as if it were a cumulative-growth factor. The per-row `return_$` is consequently ~6-10x too small; `epsilon_$` (the measured residual, PRD section 2.4) absorbs the gap.

    The fix lands in INF_C_02 `_build_daily_factor_table`. INFGRO.007's `_window_twr_two_axis` aggregation in INF_D_00c is correct and stays untouched -- give it correct inputs and both findings clear. Per the CTO ruling the correct daily/periodic return must come from an AUTHORITATIVE source, not be re-derived from the annualized rate (that re-derivation is the X method, numerically unsound at daily grain and a section-2.4 violation). Hence: probe for the authoritative series first; implement against whatever the probe finds.
  </context>

  <scope>
    <phase id="0" name="PROBE -- find the authoritative return series (read-only)">
      <step>Step 1 -- inspect the bronze/performance summaries block persisted by TO-INFGRO.002 (f39550d99). Does it carry per-client window returns (QTD/YTD/1Y/3Y/MAX) or a periodic return series? Document the exact fields, grain, and coverage.</step>
      <step>Step 2 -- if Step 1 does NOT yield a usable series: probe the Orion `/Clients/{id}/Performance` endpoint for a periodic and/or cumulative TWR field. Document the field, grain, and whether it is obtainable at the cadence INF_C_02 needs.</step>
      <step>Step 3 -- if BOTH Step 1 and Step 2 are empty: the guard-railed Method-X fallback is the only remaining path. Do NOT silently implement X -- STOP and escalate to CTO + COO with the Phase-0 evidence; X is a CTO-approved-fallback-only, and the guard rails are a CTO call.</step>
      <step>Phase 0 OUTPUT: (a) which source supplies the authoritative return; (b) the EMISSION-SHAPE decision -- does INF_C_02 emit per-client WINDOW RETURNS, or a PER-PERIOD return series? Default to the per-period series, which keeps INF_D_00c `_window_twr_two_axis` unchanged. If the data strongly indicates a window-returns emission, see the architectural flag below -- surface it before implementing the consumer side.</step>
    </phase>
    <phase id="1" name="implement the INF_C_02 fix">
      <step>Fix INF_C_02 `_build_daily_factor_table` so the per-row return is built from the Phase-0 authoritative source -- the `twr_factor_period`-as-growth-factor misinterpretation is removed. `return_$` and `epsilon_$` are recomputed correctly; epsilon returns to the measured residual (PRD section 2.4).</step>
      <step>Emit per the Phase-0 emission-shape decision. Preserve `from __future__ import annotations` as the first import (CLAUDE.md Rule 15). No emoji.</step>
    </phase>
    <phase id="2" name="deploy + chain run + verify">
      <step>Commit (safe-commit.sh, agent author) -> push CLOUD -> S3-deploy the gold script -> comp-pipescript deployed MATCH -> a full INF gold chain run materializes corrected client_performance.parquet -> leaderboard.json.</step>
      <step>Verify: (a) window TWRs are now correct in ABSOLUTE scale (not just relative shape) -- cross-check against the authoritative source; (b) epsilon_$ is no longer the dominant decomposition term (return + nna explain the majority). BOTH are the PRD section 8.5 (a)+(b) gates for INFGRO.005 partner-facing.</step>
    </phase>
  </scope>

  <architectural_flag>
    CTO flag: IF the summaries block (Step 1) gives per-client window returns DIRECTLY, then the standard QTD/YTD firm/advisor TWR collapses to single-axis AUA-weighting (no temporal chain-link) -- chain-link is then needed ONLY for MAX and the BIWNDW 1Y/3Y windows. This would change how INF_D_00c consumes the data for QTD/YTD. INFGRO.007's `_window_twr_two_axis` is NOT to be reopened casually -- if Phase 0 lands on the window-returns emission and that implies an INF_D_00c consumer change, STOP and surface to COO/CTO before implementing the consumer side; that consumer change is a separate scoping decision, not silently in this TO.
  </architectural_flag>

  <compiler_tools_mandate>
    <phase id="0" when="before implementation">
      <step>
        <run>comp-pipescript io INF_C_02.client_performance</run>
        <expect>READS include the performance/TWR source + accounts dim; WRITES gold/timeseries/client_performance.parquet consumed by INF_C_04, INF_C_06, INF_D_00, INF_D_00b, INF_D_00d, INF_D_04, INF_D_05a. Check COLUMN GAPS on return_$ / epsilon_$ / twr_factor_period -- the columns the fix touches.</expect>
        <if_mismatch>If COLUMN GAPS appear on the touched columns, resolve the load list before implementing; if the consumer set differs from PRD section 8.4, surface to COO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before the chain run">
      <step>
        <run>comp-pipescript deployed INF_C_02.client_performance</run>
        <expect>MATCH -- the runner has the committed fix before the chain run.</expect>
        <if_mismatch>STALE/MISSING -> re-upload to S3 before triggering the chain.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript postdeps INF_C_02.client_performance</run>
        <expect>Any required post-steps after INF_C_02 in the chain are enumerated -- run them / confirm the chain covers them.</expect>
        <if_mismatch>Run the flagged post-steps; do not leave a partial materialization.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after the chain run">
      <step>
        <run>comp-validate INF_C_02.client_performance --artifact &lt;materialized client_performance.parquet&gt; (if a validate config exists)</run>
        <expect>Exit 0 all-pass. If no validate config exists for INF_C_02, state so in one line and substitute the Phase-2 (a)+(b) verification as the acceptance evidence.</expect>
        <if_mismatch>Exit 1 = BLOCKED; do not signal complete. ADVISORY = read the WARNs.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>
      INF_C_02 is a gold timeseries script; the fix changes the values in gold/timeseries/client_performance.parquet for all dates. Phase 2 includes the chain run that re-materializes client_performance.parquet + every downstream consumer (INF_C_04, INF_C_06, INF_D_00/00b/00d/04/05a -> leaderboard.json). Verify post-chain that the downstream platinum artifacts carry the corrected values (mtime > the fix commit; the section 8.5 (a)+(b) gates). This chain run is SEPARATE from and AFTER the in-flight INFGRO.007/BIWNDW.002 AC4 chain.
    </reprocess_required>
  </data_reprocess_scope>

  <cross_domain_coordination>
    1. INF_C_02.client_performance.py -- same DS~C-owned script as INFGRO.007 (INF_D_00c) and the INFDRF.003 append-gate fix. Sequential single-owner edits; no concurrent-edit hazard.
    2. METHOD-Y / PERF-PATTERN-E SHARED SURFACE (CTO-specified 2026-05-18): the shared surface is `pull_inflection_performance_rest.py` + the Orion `/Clients/{id}/Performance` endpoint. Phase 0 Step 1 reads the bronze/performance summaries block that TO-INFGRO.002 (f39550d99) persisted FROM that endpoint via that puller -- so Step 1 AND Step 2 touch the same puller the PERF Pattern-E TO touches. RULES: (a) do NOT merge the two TOs -- INFGRO.009 is probe-first and may need zero new pull. (b) SINGLE-OWNER `pull_inflection_performance_rest.py` -- whichever TO actually edits the puller owns it; the other coordinates. INFGRO.009 must NOT author parallel pull logic against that endpoint. (c) SEQUENCE: run Step 1 FIRST (the data is already in bronze) -- if it satisfies, INFGRO.009 is a pure INF_C_02 read-and-rescale with ZERO new Orion pull and this coordination never activates. ONLY if Step 2 is reached (new fields needed off the endpoint) does puller work land -- and then it lands ONCE, in or co-scoped with PERF Pattern-E, never duplicated here. MCP COO before ANY edit to pull_inflection_performance_rest.py. This block is mirrored on the PERF Pattern-E TO.
    3. The Phase-2 chain run sequences AFTER the in-flight AE 0.7.0 AC4 chain; coordinate the trigger with COO/AE so it is one clean run on the current dispatcher.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 0 probe documented: Step 1 (summaries block) and, if needed, Step 2 (Orion /Clients/{id}/Performance) findings with exact fields/grain/coverage. The authoritative-source decision + the emission-shape decision (per-period series vs window returns) are both stated with evidence.</ac>
    <ac id="AC2">If Phase 0 reached Step 3 (both sources empty), the guard-railed Method-X fallback was escalated to CTO + COO BEFORE implementation -- not silently implemented.</ac>
    <ac id="AC3">INF_C_02 `_build_daily_factor_table` fixed: the per-row return is built from the authoritative source; the annualized-rate-as-growth-factor misinterpretation is removed. INFGRO.007's `_window_twr_two_axis` is NOT modified.</ac>
    <ac id="AC4">If Phase 0 landed on the window-returns emission and that implies an INF_D_00c consumer change, it was surfaced to COO/CTO before any consumer-side edit -- not silently absorbed.</ac>
    <ac id="AC5">Post-chain leaderboard.json: window TWRs are correct in ABSOLUTE scale (cross-checked vs the authoritative source), and epsilon_$ is no longer the dominant decomposition term -- the PRD section 8.5 (a)+(b) gates both clear.</ac>
    <ac id="AC6">Rule 15 (`from __future__ import annotations` first import); no emoji; deployed per the gold-script S3 path with comp-pipescript deployed MATCH before the chain run.</ac>
    <ac id="AC7">Session log includes the Compiler Tools section reproducing the mandate runs. RAVC2 to COO, CC CTO, with the Phase-0 probe findings + the AC5 post-chain verification numbers.</ac>
  </acceptance_criteria>

  <deliverables>
    - Fixed INF_C_02.client_performance.py committed + S3-deployed.
    - Phase 0 probe findings (in the session log or appended to the diagnosis brief).
    - Post-chain leaderboard.json verification (AC5).
    - Session log under org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-18/ with the Compiler Tools section.
    - RAVC2 to COO (CC CTO). On acceptance this clears the PRD section 8.5 (a)+(b) gates and unblocks INFGRO.005 partner-facing.
  </deliverables>
</task_order>
