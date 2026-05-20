<task_order>
  <metadata>
    <id>MDPF_ASSETS.016</id>
    <slug>ds-cohort0-historical-backfill-from-2026-01-17</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (Andrew direct, this session). Backfill scope only; daily-forward chain is undisturbed (mdpf-pipeline-v1.0.0 LIVE per AE 0.7.0 ENABLE 12ec0b93d / 864c6b250). The amendment field (41f0b2605) is wired; this TO populates the historical Cohort 0 component so the Model Portfolios page reads amendment-correct opal_aggregate_aua across the full series.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- Andrew direct: "the AUA numbers that appear on Model Portfolios page are done with this logic with the daily AUA figure adjusted accordingly back to 1/17/2026." Today the historical opal_aggregate_aua field on each pre-RPS-onboarding partition is partner-only (~$91M under amendment-correct each date) because the daily-process backfill ran 1a + 1b feeders only, not WS-D.1 / WS-D.2 historically. This is a contained data-fix, not a structural change.</priority>
    <sla>~0.5-1 effort-day. ~83 trading dates 2026-01-17 -> 2026-05-18; ~83 ETF-NAV pulls (4 tickers each) + ~83 RPS reads (already-present partitions) + ~83 aggregator re-runs + 1 timeseries.json regen. Stretch if Filepoint historical-NAV availability surfaces gaps -> honest-null per AC5 (no bandaid).</sla>
  </metadata>

  <amendment id="2026-05-20-cto-disposition" supersedes="Phase 3 mechanism + opal_aggregate_aua formula + the $1.488B anchor in the body below">
    AUTHORITATIVE CORRECTION 2026-05-20 (CTO~B disposition on DS Base's Phase-0 brief b680ea294; COO~B re-issue). DS Base's Phase-0 probe correctly HELD execution -- the TO's original mechanism was stale (authored 2026-05-18, methodology drifted) and DESTRUCTIVE. Where the body below conflicts with this block, THIS BLOCK GOVERNS.

    CORRECTION 1 -- Phase 3 mechanism (the critical fix). The body's Phase 3 ("re-run mdpf_aggregate_aua.py standalone per date") is INFEASIBLE + DESTRUCTIVE: there are no historical mdpf/feeds/ partitions, so a standalone aggregator run reads empty -> emits an empty artifact -> reconcile PASSES on empty -> OVERWRITES good historical platinum with empties (the identity-PASS-on-empty masking class; memory feedback_identity1_masks_absolute_value_class.md). DO NOT run the standalone aggregator per-date. INSTEAD: extend build_mdpf_process_backfill.py (which already imports mdpf_aggregate_aua and iterates per-date with 1a/1b in hand) with an inline agg.build_etf_decomposition() step; re-run SCOPED to 2026-01-17 -> 2026-05-17. RPS silver historical availability is confirmed (587 partitions back to 2024).

    CORRECTION 2 -- NEW HARD AC (AC8, empty-overwrite guard). Each rewritten partition's partner_total MUST be non-zero AND within a tolerance band of the pre-existing partition's partner_total. A semi-destructive historical rewrite must not be able to silently zero or materially move a partition's partner figure. If a rewritten partition's partner_total is zero or outside the band, the rewrite for that date is rejected (the pre-existing partition is preserved) and the date is surfaced to COO. This AC is mandatory.

    CORRECTION 3 -- opal_aggregate_aua formula (ANDREW 2026-05-20 HEADLINE RULING; SUPERSEDES the §7-Q3 "sum of Na+Nb" record and the earlier partner-only framing). The Model Portfolios global headline opal_aggregate_aua = Cohort 1a + 1b + 1c + 2a ONLY. Cohort 2b (Inflection non-model, ~$106.11M) is EXCLUDED from the headline -- computed + tracked daily, retained as an AUDIT field, NOT in the AUA total. Cohort 0 (ETF public residual) is EXCLUDED from the headline AND not emitted to the portal-facing slice -- retained as an AUDIT field only. So .016's historical partitions: opal_aggregate_aua = 1a+1b+1c+2a; etf_decomposition + etf_public_residual_total + the 2b figure all populate as AUDIT fields (not in the headline). The body's "$1.488B amendment-correct" anchor + the "page MUST consume opal_aggregate_aua incl Cohort 0" line (context, AC6, Phase-4 spec note, Phase-5 anchor) are STALE -- DROP them; the page-wire note states the page consumes the 1a+1b+1c+2a headline. GATING: .016 inherits this formula via build_mdpf_process_backfill.py's import of mdpf_aggregate_aua -- so .016 is SEQUENCED AFTER MDPF_ASSETS.024 (the live-aggregator formula fix: mdpf_aggregate_aua.py changes opal_aggregate_aua to the 1a+1b+1c+2a headline + 2b/Cohort-0 as audit fields). .024 ships the formula; .016's backfill picks it up automatically through the import. DO NOT run .016 until .024 has landed + RAVC-accepted.

    CORRECTION 4 -- Phase 4 target. .016 backfills ONLY the PLATINUM timeseries platinum/mdpf/aggregate_aua_timeseries.json (the Stage-4 rollup output). It does NOT touch the legacy json/portfolios/aum-timeseries.json (build_legacy_compat_emit.py's separate SoT -- that legacy-vs-platinum methodology alignment is MDPF_ASSETS.022's job, not .016's).

    CORRECTION 5 -- ANDREW 2026-05-20 "RULING 2" (custody scope; PRD v0.7 §3.4, commit dc780bcc4). The 49 Financial total contribution = the FULL Black Diamond book `certified_aua` (~$1,812.4M), NOT the Schwab-custodied subset (~$1,655.4M) -- this REVERSES the 2026-05-18 Schwab-only basis the body assumes. For .016's historical partitions: the 49F basis per date = certified_aua read from s3://opal-data-bd/gold/aua_certification/{date}.json `.certified_aua` (daily-available historically); Cohort 1b = certified_aua - model_aua(1a) - sma_aua(1c). This matches the WS-E re-scope shipped under MDPF_ASSETS.025. UPDATED GATING: .016 now gates on BOTH MDPF_ASSETS.024 (aggregator headline-selection) AND MDPF_ASSETS.025 (WS-E full-book re-scope) -- do .024 + .025 (parallel-OK), THEN .016. Consequence: historical Cohort 1b ~$294.7M -> ~$451.6M, the historical headline moves up accordingly (~$1,906M-class on recent dates). The body's partner_custody_total / Schwab-crosswalk references and the "$1.488B" anchor are SUPERSEDED by this correction.

    CORRECTION 6 -- ANDREW 2026-05-20 TAXONOMY CORRECTION (verbatim: "1c is a subdivision of 1b, so cant double count that"; PRD v0.8 pending). SUPERSEDES the "1a+1b+1c+2a" headline phrasing in Correction 3 and the "certified_aua - model_aua(1a) - sma_aua(1c)" formula in Correction 5. Cohort 1c (SMA) is a NAMED SUB-SLICE of Cohort 1b (non-model), NOT a disjoint sibling. CORRECTED for .016's historical partitions: Cohort 1b (49F non-model) = certified_aua - model_aua(1a) -- SMA-INCLUSIVE; there is NO "- sma_aua(1c)" / "- 1c" term. sma_aua(1c) is emitted as a display-only sub-breakdown field of 1b ("of which SMA: $X"), never subtracted, never summed separately. Headline opal_aggregate_aua = 1a + 1b + 2a (1c is NOT an additive term). Historical 1b ~$294.7M -> ~$476.4M (SMA-inclusive full-book; the Correction-5 "~$451.6M" had SMA carved out -- WRONG). This matches the corrected MDPF_ASSETS.024 (partner_total = Sigma(model + non_model), 2 terms) and MDPF_ASSETS.025 (non_model = certified_aua - model_aua(1a)) -- .016 still gates on BOTH and inherits both corrections.

    UNCHANGED: DS Base's Phase-1 prep (date-aware wsd2 feeder, commit 57e2ca4d5) is mechanism-independent and stands. Phase 0 (Filepoint NAV-depth probe) is COMPLETE per b680ea294 -- Finding 1: PFDE/PFOE honest-null pre-2026-05-18 (Filepoint integration started 5/18), historical Cohort 0 = DIVZ+IDVZ residual, a documented-provenance gap (~5.4%), NOT an error, no bandaid. AC5 (no bandaid / honest-null) governs as written.
  </amendment>

  <references>
    <contract>docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md (the WS-A contract -- specifically the 41f0b2605 amendment redefining opal_aggregate_aua = partner_aua_subtotal + etf_public_residual_total; Cohort 0 IS Opal-advised, fee-paying via the ETF expense ratio).</contract>
    <amendment>41f0b2605 (DS Base, 2026-05-18, Andrew-direct). Adds etf_public_residual_total to the aggregate block; redefines opal_aggregate_aua. Partner-only $1,848,563,071.88 + etf_public_residual_total $91,328,983.13 = $1,939,892,055.01 (2026-05-18 canonical).</amendment>
    <daily_process_v2>fb9a910b8 (DS Base, 2026-05-18). v2 daily-process backfill -- 96 partitions 2025-12-23 -> 2026-05-18 with 1a + 1b coverage; etf_decomposition[] empty on all historical partitions; meta.cohort_coverage tags '0_etf_float: null:no_partner_held_pre_rps' honestly. SmartX EndMarketVal==0 day-1 zero-row + full-5-model 1a coverage gate already structurally landed; this TO does NOT re-touch 1a/1b logic.</daily_process_v2>
    <wsd1>data/mdpf/scripts/feeders/wsd_etf_net_assets.py (WS-D.1, MDPF_ASSETS.005). ETF NAV source: Filepoint issuer CSV (DS~A .002 ruled OUT Yahoo at ~22% stale). Confirm Filepoint historical-window depth in Phase 0 -- if Filepoint pre-2026-01-17 thin, surface honest-null per AC5.</wsd1>
    <wsd2>data/mdpf/scripts/feeders/wsd_partner_held_etf.py (WS-D.2, the .015-superseding fix). 49F-only (RPS, single-partner Schwab custody). Inflection stays target_weight estimate (model-only) -- no historical-feasibility issue because Cohort 2b holds zero Opal-ETF (Andrew-confirmed 2026-05-18: 1b + 2b hold $0 of DIVZ/IDVZ/PFDE/PFOE; the RPS<model_estimate gap is cash drag inside model accounts, ~2%).</wsd2>
    <rps_history>s3://opal-data-bd/schwab/silver/rps/date={YYYYMMDD}/ -- COO verified 587 partitions, earliest 2024-01-12; no historical RPS coverage risk for the 2026-01-17 -> 2026-05-18 window.</rps_history>
    <aggregator>data/mdpf/scripts/gold/mdpf_aggregate_aua.py (WS-A canonical). Consumes the 4 WS-D / 1 WS-B / 1 WS-C / 1 WS-E feeders; emits per-date platinum + the WS-D-amendment etf_decomposition[]. Re-run on each backfill date; the latest-snapshot logic (post §7-Q1 ruling) means re-runs overwrite prior partitions in place.</aggregator>
    <target_partitions>s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/{date}.json + the timeseries at s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua_timeseries.json. 2026-01-17 itself is a Saturday -- nearest business day is 2026-01-20; backfill the existing business-day partitions only, no synthetic weekend dates.</target_partitions>
    <memory_rule>memory/reference_opal_etfs_model_accounts_only.md -- Opal-ETFs are model-accounts only on the partner side (Cohort 1b + 2b hold $0); non-model AUA of these tickers = Cohort 0. This rule means the historical Cohort 0 is well-defined per date as etf_total_net_assets - sum(partner_held_etf, partner=49F-RPS, partner=Inflection-model-estimate); no partner-non-model-positions feed is needed for these ETFs at any historical date.</memory_rule>
  </references>

  <context>
    Andrew this session: "the AUA numbers that appear on Model Portfolios page are done with this logic with the daily AUA figure adjusted accordingly back to 1/17/2026... i think we already have all of that sorted in the backend but just to make it extra clear."

    What's already sorted: (1) the aggregator carries the amendment field; daily-forward runs correctly emit opal_aggregate_aua = partner_aua_subtotal + etf_public_residual_total. (2) the timeseries.json structure carries opal_aggregate_aua as an array. (3) Cohort 0 is well-defined per-date (Andrew confirmed Opal-ETF non-model partner exposure = $0; non-model AUA of these ETFs = Cohort 0 only).

    What's NOT sorted: every historical partition in the daily-process series (2025-12-23 -> 2026-05-18, 96 dates) has etf_decomposition[] empty and the opal_aggregate_aua array carries partner-only values for every pre-RPS-onboarding date. The Model Portfolios page reading the historical series today sees AUA figures under by ~$91M per date relative to amendment-correct values. Anchor probe (COO verified 2026-05-19T~02:00Z this session): 2026-01-20 partition aggregate = $1,396,901,692.73 partner-only; amendment-correct is ~$1.488B (49F-only Cohort 0 component back-of-envelope, will sharpen in Phase 0).

    Scope is contained: re-run WS-D.1 (ETF NAVs) + WS-D.2 (49F partner_held_etf) historically across the target window, re-run the WS-A aggregator on each date so etf_decomposition[] populates and the opal_aggregate_aua field updates, then regenerate the timeseries.json. The RPS history is fully present (587 partitions back to 2024-01-12); ETF NAV history depth is the only Phase 0 unknown.

    Discipline mandate (carried from the bandaid-rejection thread + the SmartX-zero-row v2 fix earlier today): NO bandaid, NO interpolation, NO carry-forward. Dates where Filepoint historical NAV genuinely doesn't materialize stay honest-null in etf_decomposition; opal_aggregate_aua on those dates falls back to partner-only with meta tagging the partial coverage (mirror the existing meta.cohort_coverage pattern). Andrew's "no bandaids" rejection of the $1.886B fabrication is the precedent; honor it.

    Inflection on the historical leg is target_weight x model_aua (model-only estimate) -- the same logic that runs daily-forward today. We have Inflection model_aua_positions / model_composition daily-process partitions; the inputs exist. Per the memory rule, Inflection Cohort 2b holds zero Opal-ETF, so target-weight-only is the correct historical scope (no Eclipse-positions historical feed needed for this TO).
  </context>

  <scope>
    <step>Phase 0 -- Filepoint historical-NAV depth probe (read-only, ~30-60min). Verify Filepoint coverage for DIVZ + IDVZ + PFDE + PFOE back to 2026-01-17. If full coverage: proceed to Phase 1. If gaps: enumerate the gap dates, surface to COO, proceed honest-null per AC5 (Phase 1 backfills the dates we CAN, leaves gap dates etf_decomposition-empty + meta-tagged). Do NOT introduce a non-Filepoint NAV source mid-flight without CTO ratify -- DS~A .002 already ruled out Yahoo on staleness; any new source is a contract question.</step>

    <step>Phase 1 -- WS-D.1 historical backfill (etf_net_assets). For each business-day date in 2026-01-17 -> 2026-05-18 (inclusive both ends), pull Filepoint NAV for the 4 Opal ETFs, write per-date feeder partition s3://opal-data-mdpf/mdpf/feeds/etf_net_assets/{date}.parquet conforming to the WS-D.1 schema. Phase-0-surfaced gap dates: skip (honest-null). Idempotent: overwrite existing partitions (same artifact, same source, same date -> deterministic). ds-commit-gate exit 0 on any wsd_etf_net_assets.py edit; Rule 15 compliance.</step>

    <step>Phase 2 -- WS-D.2 historical backfill (49F partner_held_etf). For each date in scope, run wsd_partner_held_etf.py with --date {as_of} (the WS-D.2 feeder's existing roll-forward picks the latest-on-or-before RPS partition per contract §3.4 -- 3-day RPS lag is baked in). Write s3://opal-data-mdpf/mdpf/feeds/partner_held_etf/49financial/{date}.parquet. Dates where RPS lag pulls a partition from an earlier date: keep the contract roll-forward (rps_date_used column already records the partition consumed -- the audit trail is intact). Inflection NOT in this phase (no per-position feed; target_weight estimate carried by the aggregator on the Inflection side).</step>

    <step>Phase 3 -- WS-A aggregator re-run per date. For each date in scope, run mdpf_aggregate_aua.py (latest-snapshot logic; overwrite the existing s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/{date}.json). Each re-run consumes the freshly-written WS-D.1 + WS-D.2 partitions, plus the existing 1a + 1b feeders from the v2 daily-process backfill (DO NOT re-touch 1a/1b -- they are SmartX-zero-row-gated already per fb9a910b8). identity_1 / identity_2 / identity_3 must PASS per date (or the partition stays partner-only and meta tags the failure -- no bandaid). meta.cohort_coverage updates to reflect '0_etf_float: real:wsd2_rps_co_measured' on backfilled dates.</step>

    <step>Phase 4 -- timeseries.json regen + Model-Portfolios-page-wire spec note. Re-emit s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua_timeseries.json from the freshly-rewritten partitions. The opal_aggregate_aua array now carries amendment-correct values for every backfilled date; pre-2026-01-17 and any honest-null gap dates stay partner-only and the array element is the partner-only value (preserves chart continuity without fabrication). Land a short spec note in the TO ship log AND in MDPF_ASSETS_WSA_CONTRACT.md (sidecar OK; do NOT amend the canonical contract without CTO ratify) that explicitly states: Model Portfolios page consumers MUST read aggregate.opal_aggregate_aua (the amended field), NOT partner_aua_subtotal. This is the "extra clear" Andrew requested -- structural-doc-level, not implementation.</step>

    <step>Phase 5 -- end-to-end probe + RAVC2 to COO. Pull 3 spot-check dates (2026-01-20 / 2026-03-16 / 2026-05-15), report opal_aggregate_aua + etf_public_residual_total + identity_2_min_public_residual per date. Confirm the 2026-05-18 value remains $1,939,892,055.01 (the daily-forward partition is NOT in backfill scope -- spot-check that it didn't move). RAVC2 evidence: 3 partition diffs (before/after), the regenerated timeseries.json metadata block, the Filepoint Phase-0 verdict, and the Model-Portfolios-page-wire spec note diff.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="before write">
      <step>
        <run>comp-pipescript io data/mdpf/scripts/gold/mdpf_aggregate_aua.py</run>
        <expect>Confirms the script reads the 4 WS-D / 1 WS-B / 1 WS-C / 1 WS-E feeders; flag COLUMN GAPS if any feeder schema has drifted.</expect>
        <if_mismatch>Resolve schema drift in the feeder, not in the aggregator -- single-owner per WS-A contract section 3.3.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io data/mdpf/scripts/feeders/wsd_etf_net_assets.py AND data/mdpf/scripts/feeders/wsd_partner_held_etf.py</run>
        <expect>Both feeders have their existing input contracts (Filepoint for D.1, Schwab RPS for D.2); no COLUMN GAPS.</expect>
        <if_mismatch>Surface before Phase 1.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-blast on mdpf_aggregate_aua + the two feeders touched</run>
        <expect>Blast radius unchanged from current state (this TO does NOT add new consumers; it only re-materializes existing artifacts on historical dates).</expect>
        <if_mismatch>If new downstream nodes appeared, surface to COO before signaling complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>YES -- historical only. Backfills WS-D.1 + WS-D.2 partitions for ~83 business dates 2026-01-17 -> 2026-05-18 AND re-runs WS-A aggregator on those dates AND regenerates the timeseries.json. The 2026-05-18 daily-forward partition (the canonical AE 0.7.0 ENABLE'd partition) is OUT of backfill scope -- spot-check only, do not overwrite.</reprocess_required>
    <not_in_scope>The pre-2026-01-17 partitions (2025-12-23 -> 2026-01-16) -- 6 dates per the timeseries -- stay partner-only honestly; Andrew's directive scopes the backfill from 2026-01-17 forward. If Phase 0 surfaces Filepoint depth allowing earlier coverage, surface to COO; do not extend scope without Andrew direct.</not_in_scope>
  </data_reprocess_scope>

  <cross_domain_coordination>
    SINGLE-LANE (DS Base). NO AE coordination required: the daily-forward chain (mdpf-pipeline-v1.0.0 ENABLED, runner i-02448edb624a7a7cf, EventBridge schedule LIVE) is OUT of scope and undisturbed; backfill writes only to historical partitions and the timeseries blob. NO DE coordination required: this is a data-only fix; portal wiring lands separately under WS-F (Phase 3, not yet decomposed). DS-tilde lanes (~A/~B/~C/~D) are NOT engaged today per Andrew's sole-DS MDPF pattern this session (the .015 wire-up reassigned DS~A->DS Base after the tilde-routing-asymmetry / attestation gap; this TO follows the same routing).

    Concurrent-edit hazard check: DS~C MDPF_ASSETS.014 (WS-C cohort_class re-tag, status=pending P2 cleanup, lane DS~B) edits the WS-C feeder; this TO edits WS-D.1 + WS-D.2 + WS-A aggregator re-runs -- different files, no contention. If .014 runs concurrently and touches the WS-A aggregator (it should not -- .014 scope is WS-C feeder re-tag only), coordinate by running this TO's Phase 3 aggregator re-runs AFTER .014 lands.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Filepoint historical-NAV depth probe (Phase 0) completed; verdict landed. Any gap dates enumerated + honest-null path declared per AC5 (no bandaid).</ac>
    <ac id="AC2">For every business-day date 2026-01-17 -> 2026-05-17 (inclusive; 2026-05-18 is daily-forward, spot-check only) where Filepoint NAV is available: s3://opal-data-mdpf/mdpf/feeds/etf_net_assets/{date}.parquet present (4 rows DIVZ/IDVZ/PFDE/PFOE) AND s3://opal-data-mdpf/mdpf/feeds/partner_held_etf/49financial/{date}.parquet present (4 rows). Honest-null on gap dates allowed -- no synthesized values.</ac>
    <ac id="AC3">For every backfilled date: s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/{date}.json carries etf_decomposition[] populated (4 ETF entries) AND aggregate.opal_aggregate_aua reflects partner_aua_subtotal + etf_public_residual_total. identity_1 / identity_2 / identity_3 PASS per partition (or the partition stays partner-only and meta tags the identity-failure -- no bandaid).</ac>
    <ac id="AC4">timeseries.json regenerated. aggregate.opal_aggregate_aua array carries amendment-correct values for every backfilled date; pre-2026-01-17 + gap dates carry partner-only honestly; meta.backfill_methods includes a new entry naming this TO (e.g. "cohort0_historical_backfill_20260518_MDPF_ASSETS_016").</ac>
    <ac id="AC5">NO bandaid / NO interpolation / NO carry-forward on any null upstream input. Andrew's "no bandaids" rejection of the $1.886B fabrication + the SmartX-zero-row v2 fix (fb9a910b8 same day) are the standing precedent. Honest-null + meta-tag is the only acceptable handling for genuine source-data absence.</ac>
    <ac id="AC6">Model-Portfolios-page-wire spec note landed: explicit statement in the TO ship log AND in a contract-sidecar (or canonical contract amendment if CTO ratifies) that the Model Portfolios page MUST consume aggregate.opal_aggregate_aua, NOT partner_aua_subtotal. Per Andrew "i think we already have all of that sorted in the backend but just to make it extra clear" -- this is the extra-clear documentation step.</ac>
    <ac id="AC7">Session log with the Compiler Tools section. comp-pipescript io results captured. No emojis. ds-commit-gate exit 0 on every .py edit. Rule 15 compliance on any feeder/aggregator touch. RAVC2 to COO with the 3-date spot-check evidence per Phase 5.</ac>
  </acceptance_criteria>

  <deliverables>
    - Phase 0 Filepoint NAV-depth verdict (one short brief; OK in session log).
    - ~83 WS-D.1 etf_net_assets partitions backfilled (s3://opal-data-mdpf/mdpf/feeds/etf_net_assets/{date}.parquet, honest-null on Filepoint gaps).
    - ~83 WS-D.2 partner_held_etf/49financial partitions backfilled (s3://opal-data-mdpf/mdpf/feeds/partner_held_etf/49financial/{date}.parquet).
    - ~83 WS-A aggregator re-runs (s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/{date}.json overwritten in place per latest-snapshot semantics).
    - Regenerated s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua_timeseries.json.
    - Model-Portfolios-page-wire spec note (TO ship log + contract sidecar).
    - Session log with Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
