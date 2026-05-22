<task_order>
  <metadata>
    <id>YALP_MDSRC.D3</id>
    <slug>ds-all-surface-confirmation-closure</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <co_owner>0.2.0_DS_PortfolioAnalytics -- owns the WS-2 leg (FT-02/03 spread-definition reconcile + any WS-2 hybrid-leg residual). 0.1.0_DS leads WS-1 (the 71-entity surface confirmation). Same co-owner split as C2/D2.</co_owner>
    <date>2026-05-22</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <!-- GO ON PICKUP 2026-05-22 (Andrew directive, COO dispatch). Andrew verbatim 2026-05-22: "we need to figure out every single surface, if there are 29 that are not confirmed, then we need to figure out how to confirm them. If that is a function of having to adjust to new tickers, or derive data, or etc. then we need to surface that and go through it and get it done." D3 supersedes the D2-brief framing that carried the 29 unconfirmed surfaces "forward to the future D1 cutover" -- they are IN-SCOPE NOW, not deferred. -->
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 -- the active closing work of YALP_MDSRC. D2 produced the diagnosis (42/71 matched, 29 unconfirmed); D3 drives every remaining surface to a terminal confirmed disposition. YALP_MDSRC does not close until D3 + L1 are both RAVC-accepted.</priority>
    <sla>~2-4 days. The 29 surfaces collapse to ~6 systematic work-units (below) -- not 29 independent investigations.</sla>
  </metadata>

  <references>
    <d2>YALP_MDSRC.D2 (complete, RAVC2-accepted 2026-05-22) -- the YCharts-vs-Bloomberg parallel comparison. Brief: docs/briefs/mdsrc-d2-ycharts-bloomberg-comparison-20260522.md. D2 ran the C2 pull and diffed 71 WS-1 surfaces + the WS-2 legs: 42 to-the-cent, 3 MINOR, 26 DIVERGENCE. D3 consumes D2's per-surface diagnosis as its work list.</d2>
    <c2>YALP_MDSRC.C2 -- the YCharts market-data pull module: infra/aws/lambda/ycharts-market-data-pull/ (ycharts_client.py, ws1_surface_pull.py, ws2_*.py, ticker_map.py, lambda_function.py). D3 EDITS this module's source (ticker_map.py symbol re-maps, calc-basis params) and re-runs it. The module stays DORMANT -- repo edits only, no deploy.</c2>
    <credentials>The Menachem ("mchm") YCharts session cookie bundle in AWS Secrets Manager ycharts/credentials. Single-session: the two co-owners MUST stagger pulls (concurrent logins evict -> 403).</credentials>
    <valgate>ADHC_VALGATE Class-C baseline-comparison discipline -- the per-surface match/divergence/magnitude/cause method. D3 reuses it; do not invent a new comparison method.</valgate>
    <prds>docs/architecture/YALP_MDSRC.md + docs/architecture/YALP_MDSRC_PORTAL_ASSESSMENT.md</prds>
  </references>

  <context>
    Andrew rejected partial-closure: a project that confirmed 42 of 71 market-data surfaces and carved the other 29 to a "future cutover" is not done. D3 is the closure pass -- every surface YCharts touches gets driven to a terminal, evidenced verdict. "Confirm" does NOT mean "force a match"; it means REACH A DEFINITIVE ANSWER for each surface, where the answer is one of: re-mapped and now matching; derived from YCharts inputs and matching; a representative-index tracking-confirmed; or evidenced as genuinely not YCharts-sourceable and therefore Bloomberg-pkl-retained. The last is a valid confirmation -- it IS the hybrid end-state -- but it must carry the specific evidence (the 4xx, the missing-entity proof, the by-design basis), not a hand-wave.

    3.0.0_SA_CVO is running a continuous validation loop and will independently verify this work. Keep every per-surface verdict citation-grounded.
  </context>

  <scope>
    <in_scope>
      The 29 D2-unconfirmed surfaces, grouped into systematic work-units. For EACH surface produce a terminal verdict.

      WORK-UNIT 1 -- MSCI variant / TR-vs-PR basis (13 surfaces): MSCI France, Germany, Italy, Netherlands, Spain, ACWI-ex-US, United Kingdom, Sweden, USA Growth, USA Value, USA Size, USA Momentum, USA Minimum Volatility. The YCharts symbol resolves but on the wrong return basis/variant. Find the correct YCharts symbol variant (price-return vs gross vs net-return; USD currency basis), re-map ticker_map.py, re-pull, re-compare. (The MSCI symbols that already MATCH -- EAFE/EM/ACWI/USA/India/Brazil/Japan/Korea/Taiwan/SouthAfrica/Quality -- are the reference for the correct variant convention.)

      WORK-UNIT 2 -- GSCI commodity sub-index basis (4 surfaces): Copper (^SG3J), Crude Oil Brent (^BCOB), Natural Gas (^SG8A), Silver (^SGSA). The ^SG* GSCI sub-indices pull a clean series but on a total-return-index basis vs the portal's spot/near-future price. Find the spot/price-basis YCharts symbol, OR confirm the basis difference is irreconcilable and the surface is Bloomberg-only -- with evidence.

      WORK-UNIT 3 -- security-kind crypto/commodity calc-basis (4 surfaces): Bitcoin, Ethereum, Gold, Crude Oil WTI. Pulled via fund_data calc=price, which on these YCharts security entities returns a non-price-level series. Pin the correct calc parameter (calc=level or the correct metric), re-pull, re-compare.

      WORK-UNIT 4 -- V1A/V1B representative-index (4 surfaces): Bloomberg 0-1 Year Treasury, 0-5 Year High Yield, 0-5 Year TIPS, 20+ Year Treasury. These resolved to a representative Bloomberg index (Andrew V1A/V1B ruling) -- absolute level differs by construction. Confirm via RETURN-CORRELATION that the representative index tracks the portal entity acceptably (document the correlation/tracking evidence), OR locate the exact-entity YCharts symbol if one exists. A confirmed-representative verdict with tracking evidence closes these.

      WORK-UNIT 5 -- Communication Services (1 surface): ^SPXCMSVS, -62.6% vs Bloomberg while the other 10 GICS sectors match to-the-cent. Investigate -- rebased-index vintage (GICS Communication Services reconstituted 2018) or wrong symbol variant. Resolve to a correct symbol or an evidenced reason.

      WORK-UNIT 6 -- MINOR residuals (3 surfaces): MSCI China (-1.15%), MSCI Switzerland (+0.64%), Real Estate (-1.34%). D2 called these "within tolerance." Tighten: either confirm to-the-cent with a corrected symbol/date, or document the specific residual cause (vendor timing, rounding) so the verdict is explicit, not "close enough".

      WS-2 LEG (0.2.0_DS): FT-02/03 factor-spread definition reconcile -- the ws2_factor_tilts_pull spread arithmetic vs Yang model_portfolio_regression_analysis.ipynb section 8 (the methodology source-of-truth). Reconcile to a matching construct, OR document the defined methodology difference. Carry the RSI re-pull check noted in the D2 brief (C2 used rsi_14; confirm whether RSI-30D is the correct portal basis).

      OUTPUT: an updated per-surface confirmation table -- all 71 WS-1 surfaces + the WS-2 legs, each with a terminal verdict + evidence -- as a committed brief (extends or supersedes the D2 brief).
    </in_scope>
    <out_of_scope>
      ANY cutover. ANY PROD / AWS-cloud change. The ycharts-market-data-pull module stays DORMANT -- D3 edits its repo source (ticker_map.py, calc params) and re-runs it ad-hoc on the Menachem session; it does NOT deploy, re-tag, enable the EventBridge schedule, change Terraform/manifest, or touch the yang manifest / portal / data_pkl path. The production cutover remains a future project (D1).
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <note>D3 is an analytical re-map + re-pull + re-compare run -- it edits dormant Lambda-module source (ticker_map.py / ws*_pull calc params) and runs the modules ad-hoc; it touches no gold/silver/bronze script, no portal component, no route, no IAM surface, no Terraform. No comp-* graph tool applies (same determination as D2's mandate note). The comparison discipline is ADHC_VALGATE Class-C (reused per references). The acceptance assertions are empirical: per-surface matched-date diff evidence + the terminal verdict for every surface.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Co-owned 0.1.0_DS (WS-1, 71 surfaces) + 0.2.0_DS (WS-2 FT-02/03 leg). Single shared YCharts Menachem session -- STAGGER pulls; concurrent logins evict to 403 (the C2/D2 single-session constraint).
    - D3 edits the same dormant C2 module (infra/aws/lambda/ycharts-market-data-pull/) that D2's fixes touched (fb053a108, bc139cdd6). D2 is complete -- no in-flight conflict -- but rebase on origin/CLOUD before editing so those fixes are present.
    - 3.0.0_SA_CVO's validation loop will independently verify D3's per-surface verdicts. No coordination block needed -- just keep verdicts citation-grounded.
    - NO portal DE/RD coordination -- D3 changes no artifact shape and no portal code.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Every one of the 71 WS-1 surfaces carries a terminal verdict in the updated per-surface table -- one of: CONFIRMED-MATCH / CONFIRMED-DERIVED / CONFIRMED-REPRESENTATIVE / CONFIRMED-BLOOMBERG-ONLY. ZERO surfaces left as bare "DIVERGENCE", "MINOR", or untriaged. The original 42 D2 to-the-cent matches carry forward as CONFIRMED-MATCH.</ac>
    <ac id="AC2">For every surface moved to CONFIRMED-MATCH or CONFIRMED-DERIVED: the re-map / re-derive was applied, the pull re-run live on the Menachem session, and the YCharts value now matches Bloomberg within ADHC_VALGATE Class-C tolerance on matched dates -- the before/after diff recorded per surface.</ac>
    <ac id="AC3">For every surface that lands CONFIRMED-BLOOMBERG-ONLY or CONFIRMED-REPRESENTATIVE: a specific evidenced reason -- the YCharts 4xx + the entitlement gap, the no-equivalent-entity proof, or the by-design representative-index basis with return-correlation tracking evidence. Not "could not match."</ac>
    <ac id="AC4">Each of the 6 work-units resolved per scope, AND the WS-2 FT-02/03 spread-definition reconciled (matched-construct or documented methodology difference) + the RSI basis check recorded.</ac>
    <ac id="AC5">ZERO production/AWS/portal change -- confirmed: ticker_map.py / module re-map edits committed to dormant C2 source only; no Terraform, no manifest edit, no Lambda-schedule enable, no new ycharts-pipeline tag, no data_pkl-path or portal touch.</ac>
    <ac id="AC6">An updated all-surface confirmation brief committed (docs/briefs/) -- extends/supersedes the D2 brief with the complete 71-surface + WS-2-leg confirmed table; for each of the original 29 it states the fix applied (new symbol / calc param / derivation / Bloomberg-only reason). Session log with the per-surface diff evidence. RAVC2 to 2.0.0_SA_COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The updated all-surface YCharts-vs-Bloomberg confirmation brief (committed, docs/briefs/) -- every surface with a terminal verdict + evidence.
    - The ticker_map.py / module re-map edits committed to the dormant C2 module source.
    - Session log with the matched-date method + per-surface before/after diff evidence. RAVC2 to 2.0.0_SA_COO.
  </deliverables>

  <do_not>
    <rule>Do NOT "confirm" a surface by loosening tolerance to make a divergence pass. A surface that genuinely cannot match is CONFIRMED-BLOOMBERG-ONLY with evidence -- that is the honest verdict, not a forced match.</rule>
    <rule>Do NOT cut any surface over. Do NOT change PROD, the AWS cloud, the yang manifest, the portal, the data_pkl, Terraform, or the module's deploy state. D3 edits dormant repo source + re-runs ad-hoc only.</rule>
    <rule>Do NOT compare mismatched dates -- align YCharts vs Bloomberg to dates both sources have settled (the D2 matched-date method, brief section 1).</rule>
    <rule>Do NOT enable the C2 Lambda EventBridge schedule or any production cadence.</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
