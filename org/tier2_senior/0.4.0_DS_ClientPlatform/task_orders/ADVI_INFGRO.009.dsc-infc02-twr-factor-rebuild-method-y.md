<task_order>
  <metadata>
    <id>ADVI_INFGRO.009</id>
    <slug>dsc-infc02-twr-factor-rebuild-method-y</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <reroute_note>RE-ROUTED 2026-05-20 by 2.0.0_SA_COO: issued_to was `0.4.0_DS_ClientPlatform~C` — the ~C lane is a phantom (no live DS~C agent; the broker resolves ~C to the base folder; flagged to COO~B 20260520T164036Z). ADVI_INFGRO is base-scope (per DS~B "INFGRO stood down (base scope)"). This P1 partner-facing-critical-path TO is re-routed to the live in-domain base agent `0.4.0_DS_ClientPlatform` — INF_C_02 / pull_inflection_performance_rest.py are Client Platform base-lane scripts. DE~B's INFGRO.005/.006 are gated on this. Re-route is a within-base-lane correction of a phantom-sublane assignment, not a cross-lane change.</reroute_note>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-18 on the CTO Method-Y ruling; RE-ROUTED + RE-GO'd 2026-05-20 to the base serial (see reroute_note). No external gate on starting Phase 0 (the probe is read-only — and Phase 0 is already documented complete in the TO body: Method Y VIABLE). NOTE: when the AE 0.7.0 chain-completion ping lands, PAUSE this TO and prioritize the INFGRO.007 + BIWNDW.002 leaderboard verification + RAVC2 closes (partner-facing-gating) -- resume .009 after.</dispatch_unblock_condition>
    <project_code>ADVI_INFGRO</project_code>
    <priority>P1 -- the single INF_C_02 fix that clears BOTH Finding A (window-TWR ~6x absolute-scale understatement) and Finding B (epsilon-dominance 71.6%). It is now on the partner-facing critical path: INFGRO.005 cannot go partner-facing until this lands + a subsequent chain run.</priority>
    <sla>Phase 0 probe ~2-3h (read-only). Phase 1+ contingent on the Phase-0 data-source outcome; ~4-6h wall if the summaries block or the Orion probe yields a usable series, longer if the guard-railed X fallback is forced (escalates first).</sla>
  </metadata>

  <amendment id="1" date="2026-05-18" by="2.0.0_SA_COO" ratified-by="1.0.0_SA_CTO">
    RE-SCOPE -- the "rebuild-method-y" slug is RETIRED. The Method-Y windowed puller (Phase 1 steps 1a/1b) SHIPPED and is correct; the windowed non-annualized factor series lands in silver/performance/{date}.parquet. The remaining defect is a PHASE-1 WIRING ERROR in step 1c: INF_C_02 `_build_daily_factor_table` was pointed at silver/performance_dim/.twr_factor_period -- a DEAD ORPHAN path (no live producer, frozen 2026-05-13; INF_C_02's docstring claims INF_C_03 passes it through, but INF_C_03 writes only gold/ -- a phantom pass-through). 3 chain runs left epsilon byte-identical at 71.6% because of this.

    CTO RULING 2026-05-18 (1.0.0_SA_CTO, full ruling MCP'd to DS~C + COO): OPTION A -- repoint INF_C_02, not rebuild. CTO empirically grain-verified silver/performance/2026-05-18.parquet: calendar-daily, twr_factor = continuous index inception=1.0 -- exact semantic match for `_build_daily_factor_table`; repoint is grain-safe, no conditional gate. Option B (build a silver/performance_dim producer) REJECTED as orphan-resurrection.

    CONTAINED RE-SCOPED WORK (supersedes Phase 1 step 1c + Phase 2):
    (1) `_build_daily_factor_table`: read silver/performance/{latest}.twr_factor instead of silver/performance_dim/.twr_factor_period (path + column-name change).
    (2) Rewrite the false INF_C_03-pass-through docstring (~lines 109-116).
    (3) Retire the dead PERF_DIM_PREFIX / performance_dim orphan-loader branch.
    (4) ADDED 2026-05-18 (CTO refinement, post-DS~C-deploy of 1-3): git rm data/orion/scripts/silver/INF_C_03.performance_canonical.py -- the ACTUAL orphaned silver producer of silver/performance_dim/ (an INF_C_03 filename collision DS~C walked into: gold/INF_C_03.account_performance.py is the chain's INF_C_03 and was correctly identified, but silver/INF_C_03.performance_canonical.py is the silver builder of performance_dim/, not in orion-gold-dispatch.sh, not in the comp graph, and was even updated for INFGRO.009 today onto a dead script -- the trap). CTO grep-confirmed INF_C_02 is the only consumer of silver/performance_dim/, so retirement is safe + resolves the filename collision. The git rm lands in a follow-on commit after re-run #3 AC5 verify (do NOT abort the in-flight re-run for item 4 -- it is independent).
    OUT OF SCOPE (CTO explicit -- do not creep): convert_performance_to_silver.py's stale "weekly" docstring + week_date/weeks_from_inception misnomer columns (future silver-touch); cumulative_twr as a silver-computed running product (latent Rule-17, not consumed by INF_C_02).

    RE-RUN: INF_C_02 stays Pattern-B append-only after the repoint -- the re-run MUST force full 2020-2026 partition re-materialization so the corrected factor source reaches all historical-window partitions. `--from` alone (append mode) recomputes only the trailing date and leaves YTD/1Y/3Y/MAX epsilon stale.

    TRIGGER CORRECTION 2026-05-20 (AE 0.7.0 + DS 0.4.0 code-verified; ratified DS-Base per Rule 13): the originally-stated trigger `INFINC_REBUILD=true bash orion-gold-dispatch.sh --from INF_API_SILVER_PERF --bg` is DEFECTIVE on two counts -- (1) orion-gold-dispatch.sh PRODUCES INFINC_REBUILD (line 1074 `export INFINC_REBUILD="$REBUILD"`), it does not consume the env var; rebuild mode is set only by the `--rebuild` CLI flag and is inert unless `INFINC_PHASE1=1` (line 1081); (2) the dispatch emits INFINC_REBUILD="1" but INF_C_02's `_force_rebuild` gate checked == 'true' -- fixed in commit 4ccbce567 (gate now accepts the canonical '1' + truthy synonyms; on origin/CLOUD + S3-deployed). VERIFIED CORRECT INVOCATION: `INFINC_PHASE1=1 bash orion-gold-dispatch.sh --from INF_API_SILVER_PERF --rebuild --bg`. This enables the ADVI_INFINC.001 (DS~D) master safety gate -- the documented full-rebuild mechanism, faithful to TO intent. AE 0.7.0 fires this corrected invocation once the runner has the 4ccbce567 S3 code; DS 0.4.0 verifies INF_C_02 logged a real rebuild + AC5 on completion. NOTE: the 17:21Z + ~22:35Z prior attempts used the clobbered env-var form -- no rebuild ever ran, which is why epsilon-dominance persisted.

    GO 2026-05-18 (COO). INFGRO.007 + ADVI_BIWNDW.002 unaffected -- stay closed. AC5 unchanged (epsilon must move OFF 71.6%, absolute-scale TWRs correct).
  </amendment>

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
    <phase id="1" name="implement Method Y -- windowed puller + INF_C_02 fix">
      PHASE-0 RESULT (DS, 2026-05-18, probe complete): Method Y VIABLE, no X-fallback. The Orion /Portfolio/Clients/{id}/Performance endpoint accepts startDate/endDate; a sub-year (&lt;=1yr) window returns a DAILY NON-ANNUALIZED factor series (annualize=false / periodType params are ignored -- the date RANGE is the only lever). THE BUG, EXACT: pull_inflection_performance_rest.py calls the endpoint with NO date params (docstring "HARD LIMIT: do NOT add date window params") -> inception-to-date window (&gt;1yr) -> the factor series comes back ANNUALIZED -> INF_C_02 misreads it as a cumulative-growth factor. The no-params puller design IS the upstream origin of Findings A + B. EMISSION SHAPE = per-period daily series (TO default) -- INFGRO.007 `_window_twr_two_axis` stays UNCHANGED, the architectural_flag is NOT triggered. INTEGRATION-OWNERSHIP RULED (COO, 2026-05-18, per CTO's delegated single-owner call): INFGRO.009 OWNS the pull_inflection_performance_rest.py edit -- it has the live partner-facing need and PERF Pattern-E is not yet authored; PERF Pattern-E coordinates with / reuses INFGRO.009's windowed-pull capability when it lands.
      <step>1a -- edit pull_inflection_performance_rest.py to pull /Portfolio/Clients/{id}/Performance with SUB-YEAR (&lt;=1yr) startDate/endDate windows; daily incremental run = a ~30d trailing window per client. Remove the "no date params / HARD LIMIT" docstring constraint -- it was the defect origin. This is the single-owned Orion integration.</step>
      <step>1b -- chunked historical backfill: stitch &lt;=1yr windows (~6 chunks per client) to recover the full daily non-annualized factor series. One-time. This is the bronze/performance reprocess (see data_reprocess_scope).</step>
      <step>1c -- fix INF_C_02 `_build_daily_factor_table` to consume the daily non-annualized series and derive the per-period return r_t = factor[t]/factor[t-1] - 1; `return_$` and `epsilon_$` recompute correctly; epsilon returns to the measured residual (PRD section 2.4). The annualized-rate-as-growth-factor misinterpretation is removed.</step>
      <step>Preserve `from __future__ import annotations` as the first import in every gold/bronze script touched (CLAUDE.md Rule 15). No emoji.</step>
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
