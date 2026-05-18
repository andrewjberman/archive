<task_order>
  <metadata>
    <id>ADVI_INFGRO.008</id>
    <slug>dsc-infc02-epsilon-coverage-diagnosis</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-18. No external gate -- Finding B diagnosis is independent of the INFGRO.007 chain run. Proceed immediately.</dispatch_unblock_condition>
    <project_code>ADVI_INFGRO</project_code>
    <priority>P1 -- gates ADVI_INFGRO.005 partner-facing close (criterion (b): epsilon no longer dominant). Criterion (a) is delivered by .007 (shipped). .005 does not go partner-facing until the post-chain leaderboard.json clears BOTH gates. Does NOT block the .007 + BIWNDW.002 co-landing chain run.</priority>
    <sla>Phase 0 diagnosis ~3-5h wall (read INF_C_02 + 2-3 parquet coverage probes + the brief). The TO ENDS at the CTO escalation -- it does not implement a fix.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_INFGRO_PRD.md section 8.4 ("Finding A and Finding B are DISTINCT") + 8.7 ("Finding B confirmed distinct -- separate upstream INF_C_02 decomposition defect; COO to scope a separate INF_C_02 TO"). Section 8.4 IS the ruling basis for this TO.</prd>
    <cto_ruling>1.0.0_SA_CTO MCP 2026-05-18 -- Finding B is a standalone INFGRO.008 INF_C_02 TO, Phase-0-DIAGNOSIS-FIRST. The reconciliation method is a CTO call (it touches the section-2.4 "epsilon MEASURED-not-assumed" invariant); the TO ends Phase 0 with an escalation, NOT an implementation.</cto_ruling>
    <prior_diagnosis>ADVI_INFGRO.007 RAVC2 (DS, 2026-05-18, session log INFGRO_007_window_twr_axis2_chainlink_fix.md d9717d16f) -- AC3 Finding B: epsilon-dominance reproduced (YTD epsilon $16.50M vs return $2.21M = 71.6%); leading hypothesis = magnitude divergence between aua_change (day-over-day total_aua delta, full real book movement) and return_$ (prior_total_aua x return_pct_twr, modeled off performance_dim TWR factors); perf-coverage scope mismatch -- TWR factors cover a narrower (managed-only) account set than the total_aua sums.</prior_diagnosis>
    <invariant>PRD section 2.4 -- epsilon (the AUA-growth residual) is MEASURED, not assumed. An epsilon that dominates the decomposition is a measurement failure regardless of whether return_pct_twr renders plausibly (PRD section 3.1 reconciliation-invariant).</invariant>
  </references>

  <context>
    ADVI_INFGRO.007 (window-TWR Axis-2 chain-link fix) shipped 2026-05-18 and corrects Finding A -- the *_return_pct_twr field. PRD section 8.4 rules that Finding A and Finding B are DISTINCT defects in different columns and code paths: fixing the Axis-2 arithmetic mean in INF_D_00c does NOT change epsilon_$ at all.

    Finding B: firm_epsilon_$ is 72-73% of the AUA-growth decomposition (AUA growth = NNA + Return + epsilon). In INF_D_00c, firm_epsilon_$ is a faithful straight .sum() of a per-row epsilon_$ column produced UPSTREAM by INF_C_02.client_performance.py. The defect, if any, is in INF_C_02's per-row decomposition -- specifically the relationship between aua_change and return_$.

    PRD section 8.4 names three candidate causes for DS Phase 0 to diagnose:
      (i)  incomplete perf coverage -- per-advisor account_count_with_perf < account_count (PRD cites Peter Lee 609/627). Accounts with no performance row contribute $0 modeled return; epsilon absorbs the entire real AUA movement of those accounts.
      (ii) bronze/performance staleness -- performance_dim is 05-13-only at PRD authoring; return computed off ~2-day-stale perf. Ties to the section-2.5.1 Lambda-cadence health item.
      (iii) an INF_C_02 per-row scaling error -- a unit / cumulative-vs-period mistake in how return_$ is derived.

    This TO is DIAGNOSIS ONLY. It quantifies the coverage delta and attributes the epsilon dominance, then escalates the reconciliation method to CTO. It does NOT modify INF_C_02, INF_D_00c, or any script.
  </context>

  <scope>
    <in_scope>
      - Read INF_C_02.client_performance.py and document exactly how it derives the per-row return_$ and epsilon_$ columns, and what account/entity set each term ranges over.
      - Quantify the two account sets empirically: (set P) the accounts/households that carry a performance/TWR row feeding return_$, vs (set A) the accounts/households whose total_aua feeds aua_change. Report the coverage delta -- count AND AUA-weighted dollar magnitude -- at firm level and per-advisor.
      - Attribute the epsilon dominance: how much of firm_epsilon_$ is explained by set-A-minus-set-P accounts (candidate (i)) -- accounts present in aua_change but absent from return_$, whose full real AUA movement lands in epsilon.
      - Rule candidates (ii) staleness and (iii) per-row scaling error in or out with evidence -- so the diagnosis is complete, not a single-hypothesis confirmation.
      - Produce a diagnosis brief framing the three reconciliation methods (A/B/C below) against the Phase 0 numbers.
      - Escalate the reconciliation-method choice to CTO via MCP.
    </in_scope>
    <out_of_scope>
      - ANY fix to INF_C_02, INF_D_00c, or epsilon_$ computation. The reconciliation method is a CTO call; implementation is a follow-on TO authored after the CTO ruling.
      - The INFGRO.007 / BIWNDW.002 chain run (separate, AE-0.7.0-sequenced).
      - The Finding A *_return_pct_twr field (shipped under .007).
      - Absorbing the bronze/performance --run-date catalog item -- if Finding B traces to candidate (ii) staleness, SURFACE the linkage to the catalog item; do NOT scope-creep it into this or a follow-on INF_C_02 TO.
    </out_of_scope>
  </scope>

  <reconciliation_methods note="frame these in the brief; the choice is the CTO escalation, not a DS decision">
    <method id="A">Restrict the decomposition's aua_change to the perf-covered (set P) accounts. Epsilon shrinks, but the decomposition then only describes the managed/perf-covered book -- it no longer reconciles to the full firm total_aua.</method>
    <method id="B">Obtain or derive a TWR for the uncovered (set A minus set P) accounts so return_$ has full coverage. Full-coverage decomposition; heavier -- depends on whether a return signal for those accounts is obtainable.</method>
    <method id="C">REJECTED on its face -- reclassifying the uncovered-account return out of epsilon is "epsilon assumed, not measured" and violates the section-2.4 invariant. Listed only so the brief is complete; do not recommend it.</method>
  </reconciliation_methods>

  <compiler_tools_mandate>
    <phase id="0" when="before the diagnosis work -- establish the I/O surface">
      <step>
        <run>comp-pipescript io INF_C_02.client_performance</run>
        <expect>READS list includes the performance/TWR source and the accounts dimension; WRITES gold/timeseries/client_performance.parquet consumed by INF_C_04, INF_C_06, INF_D_00, INF_D_00b, INF_D_00d, INF_D_04, INF_D_05a. No COLUMN GAPS reported for return_$ / epsilon_$ / total_aua / return_pct_twr.</expect>
        <if_mismatch>If the I/O surface differs from PRD section 8.4's model, or COLUMN GAPS are reported on the decomposition columns, STOP and MCP COO -- the diagnosis premise has drifted and the TO scope needs reconciliation before proceeding.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript feeds INF_C_02.client_performance</run>
        <expect>Output confirms INF_C_02 reads from silver / external (no upstream gold-pipeline dependency) -- i.e. the performance_dim / canonical-performance feed and the accounts feed are silver-tier or external. This is the basis for identifying set P vs set A sources.</expect>
        <if_mismatch>If an unexpected upstream gold dependency appears, note it in the brief -- it widens the set-P/set-A source map and must be reflected in the coverage comparison.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before committing the brief">
      <step>
        <run>Self-check: the brief reports the set-P/set-A coverage delta (count + AUA-weighted $) at firm + per-advisor grain, the epsilon attribution to candidate (i), and an explicit in/out verdict on candidates (ii) and (iii).</run>
        <expect>All four diagnosis elements present with empirical numbers, not hypotheses. The A/B/C reconciliation framing is populated against the Phase 0 numbers.</expect>
        <if_mismatch>The brief is incomplete -- do not commit or escalate until every element carries a number.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after committing the brief">
      <step>
        <run>Session log Compiler Tools section reproduces both Phase 0 comp runs verbatim with observed output and pass/fail vs expect.</run>
        <expect>Both runs logged; the section is the audit record per TO_COMPILER_GATE.</expect>
        <if_mismatch>The TO is not complete until the Compiler Tools section is present and reproduces the runs.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>This TO modifies no script and writes no silver/bronze/gold artifact. It is a read-only diagnosis producing a brief + an escalation MCP. No re-ingestion or reprocess applies. The follow-on fix TO (authored post-CTO-ruling) will carry its own data_reprocess_scope block.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    INF_C_02.client_performance.py is the same DS~C-owned script touched by INFGRO.007 (INF_D_00c) and the INF_C_02/C_03 append-gate fix (INFDRF.003, 2f580143f) -- no concurrent-edit hazard because this TO does NOT edit it (read-only). The INFGRO.007 + BIWNDW.002 chain run (AE 0.7.0 sequenced) is independent -- Finding B diagnosis does not depend on or block it. If Phase 0 attributes Finding B to candidate (ii) performance staleness, the bronze/performance --run-date catalog item (ADVI_INFETL lane, RUNDATE-DISPATCH-IMPL in flight under AE 0.7.0) is the linked surface -- surface the linkage to COO, do not absorb it.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Set P (perf/TWR-covered accounts feeding return_$) and Set A (accounts whose total_aua feeds aua_change) are each enumerated empirically from the live artifacts. The coverage delta (Set A minus Set P) is reported as BOTH a count and an AUA-weighted dollar magnitude, at firm level and per-advisor.</ac>
    <ac id="AC2">The epsilon dominance is attributed: the fraction of firm_epsilon_$ (and per-advisor epsilon_$) explained by Set-A-minus-Set-P accounts -- accounts present in aua_change but absent from return_$ -- is quantified against the reproduced 71.6% YTD figure.</ac>
    <ac id="AC3">Candidates (ii) bronze/performance staleness and (iii) INF_C_02 per-row scaling error are each ruled IN or OUT with cited evidence (e.g. performance_dim max date vs run date for (ii); a unit/period spot-check of return_$ derivation for (iii)). The diagnosis is complete -- not a single-hypothesis confirmation of (i).</ac>
    <ac id="AC4">A diagnosis brief is committed under docs/briefs/ presenting AC1-AC3 plus the A/B/C reconciliation-method framing populated against the Phase 0 numbers (method C explicitly marked rejected per the section-2.4 invariant).</ac>
    <ac id="AC5">The reconciliation-method choice is escalated to 1.0.0_SA_CTO via MCP, CC 2.0.0_SA_COO, citing the brief path + the AC1-AC3 numbers. The TO ENDS here -- NO fix to INF_C_02 / INF_D_00c is implemented. A fix TO is authored only after the CTO ruling.</ac>
    <ac id="AC6">Session log includes the Compiler Tools section reproducing both Phase 0 comp runs with observed output and pass/fail vs expect.</ac>
  </acceptance_criteria>

  <deliverables>
    - docs/briefs/infgro-finding-b-epsilon-coverage-diagnosis-20260518.md -- the diagnosis brief (AC1-AC4).
    - An escalation MCP to 1.0.0_SA_CTO (CC COO) with the reconciliation-method decision request (AC5).
    - Session log under org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-18/ with the Compiler Tools section (AC6).
    - This TO flipped to <status>complete</status> when AC1-AC6 are met -- "complete" here means the diagnosis + escalation are delivered, NOT that Finding B is fixed.
  </deliverables>
</task_order>
