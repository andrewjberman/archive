<task_order>
  <metadata>
    <id>YALP_MDSRC.D2</id>
    <slug>ds-ycharts-bloomberg-parallel-comparison</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <co_owner>0.2.0_DS_PortfolioAnalytics -- owns the WS-2 hybrid-input-leg comparison; 0.1.0_DS leads WS-1. Same co-owner split as C2 (they built the pulls, they run + diff them).</co_owner>
    <date>2026-05-22</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <!-- GO ON PICKUP 2026-05-22 (COO /loop drive). Andrew directive 2026-05-22, verbatim: "we definitely want to run the pulls and compare with what we currently have from bloomberg (on the same dates for accuracy/consistency, as bloomberg data in the portal is a few days lagged). However we do not want to cut over or make any switches in PROD or aws cloud, that will be a future project not now." + "we have the menachem cookie bundle available for pulling/testing whatever we need ... no holdup on exploring the ycharts data and validating." D2 is the comparison/validation half of the original D1; the production cutover (D1) is CARVED OUT to a future project. NO dedicated-seat gate -- D2 runs on the Menachem session NOW. -->
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 -- the active closing work of YALP_MDSRC: validate the YCharts pull against Bloomberg. Unblocked NOW (Menachem session); not seat-gated.</priority>
    <sla>~2-4 days.</sla>
  </metadata>

  <references>
    <c2>YALP_MDSRC.C2 (complete) -- the YCharts market-data pull. infra/aws/lambda/ycharts-market-data-pull/ : ycharts_client.py + ws1_surface_pull.py + 4 ws2_*.py + ticker_map.py + lambda_function.py. D2 RUNS this pull and diffs the output.</c2>
    <credentials>The Menachem ("mchm") YCharts session cookie bundle in AWS Secrets Manager ycharts/credentials (refreshed by C6). Andrew-confirmed available for pulling/testing -- D2 has NO dedicated-seat gate.</credentials>
    <valgate>ADHC_VALGATE -- the Class-C baseline-comparison discipline. D2's per-surface YCharts-vs-Bloomberg diff REUSES it; do not invent a new comparison method.</valgate>
    <d1>YALP_MDSRC.D1 (ae-yang-pipeline-per-surface-cutover) -- the production cutover. CARVED OUT to a FUTURE project per Andrew 2026-05-22; NOT executed now. D2 produces the accuracy evidence a future cutover decision rests on.</d1>
  </references>

  <context>
    Andrew 2026-05-22: run the YCharts pulls and compare against the current Bloomberg portal data -- on matched dates, for accuracy/consistency -- but make NO cutover and NO PROD/AWS changes (the cutover is a future project). D2 is that comparison run. C2 built the YCharts pull; D2 executes it against the live Menachem session and diffs the result against the Bloomberg values the portal currently serves, surface by surface, producing an accuracy/consistency report.
  </context>

  <scope>
    <in_scope>
      - Run the C2 YCharts pull (the ycharts-market-data-pull module) against the live Menachem session (ycharts/credentials) for the 17 YCharts-touched surfaces -- the 7 YCharts-replaceable + the 10 hybrid-input legs (PRD v0.3 5.2 matrix). Run it as an analytical/ad-hoc execution (the modules are plain Python + urllib; run locally or read-only-invoke the dormant Lambda) -- capture the YCharts output.
      - For each surface/entity, obtain the CURRENT Bloomberg value the portal serves (from the live data_pkl / portal artifacts).
      - MATCHED-DATE comparison: Bloomberg data in the portal lags a few days. Align every YCharts-vs-Bloomberg comparison to the SAME observation date(s) -- never compare a YCharts value as-of-today against a Bloomberg value as-of-a-few-days-ago. Choose comparison date(s) where BOTH sources have a settled observation.
      - Diff YCharts vs Bloomberg per surface within tolerance, reusing the ADHC_VALGATE Class-C baseline-comparison discipline. Per surface record: match / divergence / magnitude / the likely cause of any divergence (vendor methodology, TR-vs-PR basis, representative-index residual, etc.).
      - Output: a per-surface YCharts-vs-Bloomberg comparison report (a committed brief) -- the accuracy/consistency evidence.
    </in_scope>
    <out_of_scope>
      - ANY cutover. ANY switch in PROD or in the AWS cloud. ANY change to the yang manifest, the portal, the data_pkl path, the C2 Lambda configuration/Terraform, or the production data flow. Enabling the C2 Lambda EventBridge schedule / any production cadence. The cutover is YALP_MDSRC.D1 -- a FUTURE project, explicitly NOT now (Andrew 2026-05-22). D2 changes NOTHING that is live; it only reads + compares.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <note>D2 is an analytical comparison run -- no gold/portal/route/IAM/Terraform change, so no comp-* graph tool applies. The comparison discipline is ADHC_VALGATE Class-C (reused, per references). Assertions are empirical: the matched-date alignment and the per-surface diff evidence.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Co-owned 0.1.0_DS (WS-1 surfaces) + 0.2.0_DS (WS-2 hybrid-input legs) -- same split as C2; coordinate the shared YCharts session (single-session: stagger pulls, concurrent logins evict -> 403).
    - Carries the C2 first-live-run checklist into this run: TR2/TR3 (dropped), ERP forward-P/E (I:SP500PND), VAL-01 (pe_ratio YCharts / 5 multiples stay-pkl, hybrid), the ~10-case A3 P4 symbol set, per-symbol fidelity. The D2 comparison IS the first real live run -- fold those checks in.
    - NO portal DE/RD coordination needed -- D2 changes no artifact shape and no portal code.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The C2 YCharts pull run against the live Menachem session for the 17 YCharts-touched surfaces; YCharts output captured. Single-session use staggered between the two co-owners.</ac>
    <ac id="AC2">Per surface, the current Bloomberg portal value obtained and compared YCharts-vs-Bloomberg on MATCHED observation dates (Bloomberg portal-lag accounted for -- both sources settled on the compared date). The matched-date method documented.</ac>
    <ac id="AC3">Per-surface diff recorded reusing the ADHC_VALGATE Class-C discipline: match / divergence / magnitude / likely cause. A committed comparison-report brief (docs/briefs/).</ac>
    <ac id="AC4">ZERO production/AWS/portal change -- confirmed: no Terraform, no manifest edit, no Lambda-schedule enable, no data_pkl-path touch. RAVC2 to 2.0.0_SA_COO (no CC CTO per Andrew directive 2026-05-22).</ac>
  </acceptance_criteria>

  <deliverables>
    - The per-surface YCharts-vs-Bloomberg comparison report (committed brief, docs/briefs/).
    - Session log with the matched-date method + per-surface diff evidence. RAVC2 to 2.0.0_SA_COO.
  </deliverables>

  <do_not>
    <rule>Do NOT cut any surface over. Do NOT change PROD, the AWS cloud, the yang manifest, the portal, or any production data flow -- D2 reads + compares ONLY. The cutover is a future project (D1), explicitly not now.</rule>
    <rule>Do NOT compare mismatched dates -- Bloomberg lags; align to a date both sources have settled.</rule>
    <rule>Do NOT enable the C2 Lambda EventBridge schedule or any production cadence.</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
