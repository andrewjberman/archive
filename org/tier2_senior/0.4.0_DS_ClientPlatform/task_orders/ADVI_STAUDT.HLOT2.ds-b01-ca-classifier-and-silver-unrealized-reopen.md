<task_order>
  <id>ADVI_STAUDT.HLOT2</id>
  <title>B_01 holdings_lots dual-patch: CA-Merger classifier (Patch A) + silver/unrealized-authoritative 3-tier re-open (Patch B)</title>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
  <status>pending</status>
  <priority>P1</priority>
  <sla>3h end-to-end from GO (TO dispatch → ~A commit 30 min → DT S3 upload → AE qa-runner --from B --chain → comparison pack → PROD deploy). Held since 2026-04-20 21:38Z Andrew directive "I want a solution immediately."</sla>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md</ref>
    <ref type="brief">docs/briefs/coo_briefing_hlot2_dual_patch.md (DS~A authoring packet, CTO-signed-off 2026-04-20 22:14Z)</ref>
    <ref type="evidence">data/black_diamond/diagnostics/STAUDT/HLOT1/ (7 files: hlot1_attribution_report.md, hlot1_correction_three_mechanisms.md, transaction_history_spot_check.md, top9_gap_profile.{csv,parquet}, model_vs_current.csv, divz_silent_close_gate_eval.parquet, iefa_silent_close_gate_eval.parquet, iefa_overlap_unit_shortfall.parquet)</ref>
    <ref type="mcp">CTO scope-lock 20260420T221414Z (HLOT2 single TO dual-patch)</ref>
    <ref type="mcp">CTO HLOT2 guardrails 20260420T215315Z (5 acceptance guardrails) + shape review 20260420T220829Z (orthogonality concurred)</ref>
    <ref type="predecessor">ADVI_STAUDT.HLOT1 (Phase 0 attribution, COMPLETE — ruled out all 4 pre-enumerated gates cd00ff2c / ae759bbb+1db831aa / 7e57576f / cb6d78e2)</ref>
  </references>

  <scope>
    **Class 2 — holdings_lots meter close.** Portal Books tab Firm Overview Top Holdings reads 3-6 percentage points below Opal aggregate model weights on six of the top-9 positions (DIVZ -5.87pp / IEFA -3.30pp / SPYM -2.64pp / IDVZ -0.96pp / IEMG -0.89pp / SPHY -0.53pp). HLOT1 attribution ruled out the 4 pre-enumerated gates; root cause is TWO orthogonal upstream mechanisms starving B_01.holdings_lots.py current_units output. HLOT2 ships one commit on B_01 with both patches. Expected combined recovery ~$181M across six tickers; firm total_aua unchanged at $1.649B (D_03 scales via account_performance, not holdings_lots sums).

    **Patch A — CA-Merger classifier fix (DIVZ, ~$78.6M):**
    B_01.holdings_lots.py L2186-2213 classifies every Corporate Action row whose transaction_sub_type ∈ {Merger, Conversion Out, Exchange, Tender, Cash in Lieu} as CA_SELL. BD records identity-migration events (ticker renames, share-class consolidations) as TWO paired rows on the same (account_id, asset_id, trade_date) where BOTH carry positive units and MV signs distinguish direction (incoming +MV, outgoing -MV). Current classifier fires CA_SELL on both; FIFO double-sells 2X against BUY total of X; lots zero.

    Fix: `paired_subs = frozenset({'Merger','Conversion Out','Exchange','Tender','Cash in Lieu'})`. For rows where `transaction_sub_type in paired_subs AND market_value >= 0`: classify as CA_BUY. Otherwise unchanged. ~6 lines added; zero refactor.

    Evidence: 7,540 Merger rows = 3,770 +MV / 3,770 -MV pairs across 12m window, 100pct on DIVZ rename (asset_id 3680584, OPAL DIVIDEND → POLEN DIVIDEND 2025-06-16). 20/20 DIVZ silent-close sample accts have this exact pattern. Reverse Split (6 rows +MV) + Spinoff (14 rows asymmetric -MV) surfaced in Extension 1 — DO NOT add to paired_subs this commit; flagged as HLOT3a+HLOT3b follow-ups.

    **Patch B — silver/unrealized-authoritative 3-tier re-open (IEFA+IDVZ+SPYM+IEMG+SPHY, ~$102.7M):**
    silver/transactions is systematically incomplete for held-away positions on these cohorts (confirmed across 20-acct probes per ticker): IEFA 41 Sales vs 17 Buys (18/19 net-negative), IDVZ missing ~635 BUY units of validated acct, SPYM 8 Buys vs 11 Sales, IEMG 5 Buys vs 12 Sales, SPHY 5 Buys vs 5 Sales with net-negative pattern. FIFO correctly reconstructs against the present transactions → produces net-zero or partial current_units. Snapshot sources (silver/unrealized, canonical/holdings source='reconciled') say the position is open. Fix is not to correct silver/transactions (upstream ingestion; separate workstream) but to make B_01 respect snapshot authority when the transaction log is incomplete.

    Widen the existing SL-P1 sleeve-shadow path (B_01 L860+, `_build_uln_sleeve_shadow_lots`) from 598-acct sleeve cohort to universal billable. Priority chain:
    1. **Tier 1** — silver/unrealized confirms (acct, cusip) open → inject synth lot from silver/unrealized units, `source='silver_unrealized_reopen'`. Coverage: 99.6pct DIVZ / 98.9pct IEFA / 95.5pct IDVZ.
    2. **Tier 2** — silver/unrealized silent AND canonical/holdings confirms position → inject synth lot from canonical units, `source='canonical_holdings_reopen'`. Coverage: 25 uncovered accts across DIVZ/IEFA/IDVZ (0.2pct, ~$1-2M).
    3. **Stay closed** — both sources silent → preserve Gate 3 (cd00ff2c) / RPS sell-correction (ae759bbb+1db831aa) / PIVOT 5 (7e57576f) legitimate closures.

    Cohort predicate: `alloc_billable >= $1000` (inherits PIVOT 5 held-away-exclusion gate; alloc_billable load already in scope from existing code path). Per-(acct, cusip) predicate: `(FIFO current_units == 0 OR no lot exists) AND (Tier 1 OR Tier 2)`. Call-site insertion: after `_apply_rps_lot_corrections` and before `_apply_silver_noncash_cap` (so re-opened lots receive cap treatment if needed). Existing SL-P1 call pattern at L2538 for reference.

    ~40-60 lines. Prefer factoring into new `_build_authoritative_reopen_lots` function over widening existing `_build_uln_sleeve_shadow_lots` (cleaner separation; SL-P1 sleeve semantics preserved). Author's call on final structure.

    **Orthogonality (CTO concurred 20260420T220829Z):** Patch A fires at FIFO classifier stage (pre-zeroing); Patch B fires post-FIFO (post-zeroing re-open). On DIVZ: Patch A restores FIFO correctness so Patch B's `current_units == 0` predicate is false → Patch B does not fire. On IEFA/IDVZ/SPYM/IEMG/SPHY: Patch A is null (no Merger pairs); Patch B activates solo. Additive by construction, single commit, single qa-runner cycle.

    **Scope negatives (explicit non-goals):**
    - DO NOT revert cd00ff2c (Gate 3) / ae759bbb+1db831aa (RPS sell-correction) / 7e57576f (PIVOT 5) / cb6d78e2 (tiered unit cap). All four landed for legitimate reasons; HLOT2 ADDS re-open authority, does NOT remove existing gates.
    - DO NOT fix silver/transactions ingestion. Upstream completeness issue; separate workstream (candidate CP-AE1 extension or new DE TO).
    - DO NOT extend paired_subs to Reverse Split or Spinoff in this commit. File HLOT3a (Reverse Split +MV audit) and HLOT3b (Spinoff asymmetric -MV mirror logic) as follow-up TOs.
    - DO NOT address PCHI / QQQ / ICSH / UTWO "missing from top-9 display" observations — below top-9 cutoff, not a data-quality issue at this scope.
    - DO NOT change D_03.composition_artifacts.py, D_04, or any downstream consumer. Fix is strictly in B_01 at FIFO classifier + re-open path. Downstream gets correct input, re-emits deterministically.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io B_01</run>
        <expect>READS = {ACCOUNTS_DIMENSION, silver/bd_assets_dim}. WRITES = {holdings_lots_key, holdings_lots_backfill_key, holdings_lots_shadow_key, holdings_lots_v2_dryrun_key}. No COLUMN GAPS. (Silver-corpus reads silver/transactions + silver/unrealized + silver/RPS not indexed per ADHC_ROUTER Phase 2 known gap; confirm via direct grep in B_01 source that load paths for silver/unrealized + canonical/holdings exist and surface them in comment in the new function.)</expect>
        <if_mismatch>STOP. If COLUMN GAPS non-empty, fix the load list first. If WRITES set changed, surface to COO — Patch B should not add a new WRITE key (in-place widening of existing holdings_lots output only).</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse platinum/firm/firm_composition.json</run>
        <expect>CONSUMED BY enumerates advisor-intelligence consumers (speculative-match directory-prefix fallback OK — index gap acknowledged). Presence of AdvisorBookView / ClientsTab / AdvisorsTab / PartnerAnalytics / DistributionTab among speculative consumers confirms blast surface for Books tab Top Holdings + Firm Overview composition panel.</expect>
        <if_mismatch>If new non-speculative consumer appears that wasn't in HLOT1 evidence (PartnerAnalytics, AdvisorBookView, ClientsTab, AdvisorsTab, DistributionTab, AdvisorIntelligence), surface to COO before commit — may indicate a new Mix composition reader shipped mid-flight that HLOT1 model_vs_current.csv didn't account for.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check AdvisorBookView</run>
        <expect>No MISSING fields on the Top Holdings / Mix composition render path. UNUSED fields limited to already-documented aliases. Low-cost confirmation that the FE reads the fields HLOT2's re-opened lots propagate through (source tag, units, market_value — schema-stable).</expect>
        <if_mismatch>If MISSING surfaces on fields in the Patch B synth-lot emit path (units / market_value / cusip / source / is_open), STOP — possible FE schema drift during W3/W4. Message COO; may block fix shape.</if_mismatch>
      </step>
      <step>
        <run>comp-cache collisions</run>
        <expect>Exactly the 4 existing shared keys (advisor-book-view/firmOverride, advisor-intelligence/timeseries-overview/firmOverride, firm-leaderboard/firmOverride, partner-analytics/granularity/firmOverride). No new collision.</expect>
        <if_mismatch>If a new key appears: HLOT2 inadvertently changes a cache shape (should NOT happen — Patch B is a value correction on existing emit path). STOP and surface.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -c "import ast; ast.parse(open('data/black_diamond/scripts/gold/B_01.holdings_lots.py').read())"</run>
        <expect>Exit 0. AST parse clean — syntactic validity confirmed before upload.</expect>
        <if_mismatch>STOP. Do not commit until ast.parse exits clean. Same-class gate that would have caught 081223b5 NameError + 048a6fa3 KeyError locally.</if_mismatch>
      </step>
      <step>
        <run>python -c "import importlib.util; spec=importlib.util.spec_from_file_location('B_01','data/black_diamond/scripts/gold/B_01.holdings_lots.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)"</run>
        <expect>Exit 0. All module-level imports resolve; no NameError, no ImportError. Specifically exercises `from collections import defaultdict` + any frozenset / pandas / numpy imports Patch A/B introduce.</expect>
        <if_mismatch>STOP. Fix missing imports before commit. This is the specific gate that would have caught 081223b5 `defaultdict` NameError before PROD nightly 23:00Z fired.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed B_01</run>
        <expect>STALE (edit in flight, commit not yet uploaded to S3). Captures pre-deploy state for the DT upload cycle.</expect>
        <if_mismatch>If MATCH appears before commit, someone else uploaded — coordinate with DT before proceeding.</if_mismatch>
      </step>
      <step>
        <run>comp-blast holdings_lots</run>
        <expect>Same downstream surface as HLOT1 baseline (positions_cube / C_00 client_perf+account_perf / D_02 advisor_client_detail / D_03 Mix+Top-Holdings / D_04 leaderboards / fee_calcs / tax_exposure). Known ADHC_ROUTER Phase 2 graph-gap: tool may report "No downstream consumers found for: gold:B_01.holdings_lots" — acceptable; fall back to evidence-file-trace from HLOT1 briefing §4 (blast enumerated there manually). No NEW downstream nodes appearing. Source='silver_unrealized_reopen' + 'canonical_holdings_reopen' tags are lot-internal metadata, not new artifacts.</expect>
        <if_mismatch>If a new downstream node appears post-Patch B, surface to COO — likely another agent committed a new consumer mid-flight, or Patch B accidentally added a new WRITE target.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-validate B_01 --artifact gold/timeseries/holdings_lots/{DATE}.parquet</run>
        <expect>SKIP-by-default (B_01 has no dedicated validator block in gold_validate_config.yaml per known gap; see ADVI_ROLLUP carryover "B_01 comp-validate config block"). Document the SKIP in session log Compiler Tools section explicitly; DO NOT treat as pass.</expect>
        <if_mismatch>If validator returns non-SKIP, capture output and treat as authoritative. If any ERROR-class check fails, DO NOT signal DT — fix-forward first.</if_mismatch>
      </step>
      <step>
        <run>Substitute verification (since comp-validate SKIPs): per-patch + per-ticker + per-tier attribution sum matches briefing expected-recovery table within ±10pct</run>
        <expect>DIVZ Patch A ~$78.6M; IEFA Patch B Tier 1 ~$49.8M; SPYM Patch B Tier 1 ~$43.5M; IDVZ Patch B Tier 1 ~$15.9M; IEMG Patch B Tier 1 ~$14.8M; SPHY Patch B Tier 1 ~$8.8M; Tier 2 (canonical_holdings_reopen) ~25 accts / ~$1-2M. Any recovery on wrong patch = FLAG.</expect>
        <if_mismatch>Surface to COO + CTO with per-ticker attribution table. May indicate Patch A/B interaction (should be orthogonal).</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    - [ ] **Patch A code shape:** `paired_subs = frozenset({'Merger','Conversion Out','Exchange','Tender','Cash in Lieu'})` declared at B_01.holdings_lots.py near L2186. For rows where `transaction_sub_type in paired_subs AND market_value >= 0`, classify as CA_BUY (not CA_SELL). Otherwise unchanged. ~6 lines added.
    - [ ] **Patch B code shape:** new function `_build_authoritative_reopen_lots` (or widened `_build_uln_sleeve_shadow_lots`) emits synth lots for (acct, cusip) pairs where (a) `alloc_billable >= $1000` AND (b) `FIFO current_units == 0 OR no lot exists` AND (c) Tier 1 `silver/unrealized` OR Tier 2 `canonical/holdings` confirms position open.
    - [ ] **Patch B priority chain:** Tier 1 `silver_unrealized_reopen` fires first; Tier 2 `canonical_holdings_reopen` fires only when Tier 1 silent. Source tag on every injected lot: `source='silver_unrealized_reopen'` (Tier 1) or `source='canonical_holdings_reopen'` (Tier 2). Per-tier countable in comparison pack.
    - [ ] **Patch B regression guard:** zero re-opens for (acct, cusip) where BOTH silver/unrealized AND canonical/holdings are silent. Preserves Gate 3 / RPS sell-correction / PIVOT 5 / tiered cap legitimate closures.
    - [ ] **Pre-commit syntax+import gate (same-class D_02/B_00 defense):** `python -c "import ast; ast.parse(...)"` + `python -c "importlib.util.spec_from_file_location + exec_module"` both exit 0 against the commit file. Session log captures both outputs.
    - [ ] **Pre-commit Patch A regression guard:** run Patch A against 100 random accts with paired_subs rows where MV signs already disambiguate correctly (non-DIVZ). Expected zero behavior delta. Captured in session log Compiler Tools section.
    - [ ] **Post-fix comp-pipescript io B_01:** no new COLUMN GAPS vs Phase 1 baseline.
    - [ ] **qa-runner --from B --chain on c6a.8xlarge (or c6i.16xlarge if capacity-constrained):** completes without regression. BFIX1+BFIX2 (1a54d46a fix-forward of 081223b5) ships in same cycle if sequencing permits; else ships in next cycle.
    - [ ] **Per-patch + per-ticker + per-tier attribution in comparison pack:**
      - DIVZ recovery attributable to Patch A: expected ~$78.6M (±10pct)
      - IEFA recovery attributable to Patch B Tier 1: expected ~$49.8M (±10pct)
      - SPYM recovery attributable to Patch B Tier 1: expected ~$43.5M (±10pct)
      - IDVZ recovery attributable to Patch B Tier 1: expected ~$15.9M (±10pct)
      - IEMG recovery attributable to Patch B Tier 1: expected ~$14.8M (±10pct)
      - SPHY recovery attributable to Patch B Tier 1: expected ~$8.8M (±10pct)
      - Tier 2 (`canonical_holdings_reopen`) coverage: expected ~25 accts, ~$1-2M
      - Any recovery on wrong patch: FLAG as unexpected interaction (investigate + MCP COO).
    - [ ] **BFIX2 subsumption probe:** measure post-HLOT2 BFIX2 re-inject cohort size (currently 62 accts / $14.2M at 081223b5/1a54d46a). Expected shrinkage post-HLOT2 (silver/unrealized re-open absorbs part of bd_only cohort). Document in comparison pack; GROWTH flags unexpected interaction.
    - [ ] **Post-fix firm_composition.json Top-9 percentages within ±1pp of model targets** (assumes 80pct firm-in-model coverage):
      DIVZ ~9-10pct / IEFA ~10-11pct / IDVZ ~8-9pct / SPYM ~6-7pct / PFDE ~6-7pct / PFOE ~6-7pct / IEMG ~3-4pct / BIV ~3-4pct / SPHY ~3pct.
    - [ ] **Firm total_aua invariant:** unchanged at $1.649B (D_03 scales via account_performance, not affected by holdings_lots delta). Document the check in comparison pack — if firm total_aua shifts, Patch B is writing outside its lane.
    - [ ] **Schema invariants:** `units`, `market_value`, `cusip`, `asset_name`, `is_open` columns unchanged in schema. `source` column gains two new enum values (`silver_unrealized_reopen`, `canonical_holdings_reopen`). Only count of lots + MV totals shift; no column rename or type drift.
    - [ ] **Session log with Compiler Tools section** reproducing every `<run>` from `<compiler_tools_mandate>` with observed output and explicit pass/fail vs. `<expect>`. Missing rows = REWORK. Includes Phase 1 (io + platinum-reverse + schema-check + cache-collisions), Phase 2 (ast.parse + import-smoke + deployed + blast), Phase 3 (validate SKIP + substitute attribution).
    - [ ] **Session log path:** `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-21/staudt_hlot2_b01_dual_patch.md`.
  </acceptance_criteria>

  <cross_domain_coordination>
    **Bundled cycle with BFIX1+BFIX2 fix-forward (1a54d46a):**
    - B_00.canonical_holdings.py carries BFIX1 (build_persistent_rps_accts) + BFIX2 (bd_only re-injection) + NameError fix (`defaultdict` import) at 1a54d46a. DT dispatched for reupload + `--chain bcd` re-run at 2026-04-21 ~12:17Z.
    - Scenario A (preferred): HLOT2 commit lands before current --chain bcd completes → DT batches HLOT2 (B_01) + 1a54d46a (B_00) as a single upload → AE runs `--from B --chain` once, validating both. Single PROD deploy.
    - Scenario B (fallback): current --chain bcd validates 1a54d46a before HLOT2 commit lands → B_00 BFIX1/2 PROD-deploy alone via nightly fallback or manual → HLOT2 runs a second qa-runner cycle post-commit. Two PROD deploys.
    - Decision gate: DT calls the batching. AE coordinates. ~A does NOT delay HLOT2 commit to force batching — commit when ready, coordination happens downstream.

    **Shared artifacts under active work (comp-pipescript overlap check):**
    - Both B_00 BFIX1/2 and B_01 HLOT2 write `gold/timeseries/{canonical_holdings,holdings_lots}/{date}.parquet`. Different output keys; no file conflict.
    - Downstream: both feed `positions_cube` (A_03) and `account_performance` (C_03) and `Mix/TopHoldings composition` (D_03). Comparison pack must distinguish HLOT2 delta from BFIX1/2 delta at ticker level (HLOT2 = top-9 DIVZ/IEFA/etc. meter close; BFIX1/2 = bd_stale overreach + newly-opened admit).
    - No portal-side cross-domain — HLOT2 is a value correction on existing emit paths; no new TypeScript types, no new React Query keys, no new component state.

    **ADHC_ROUTER Phase 2 graph gap (accepted):**
    - `comp-blast holdings_lots` returns "No downstream consumers found" — known indexer gap. Evidence-file-trace from HLOT1 briefing §4 is authoritative substitute. COO validates downstream blast manually if fix-behavior surprises.

    **No other active TO overlaps** as of 2026-04-21 12:18Z:
    - CP-DS1 (B_01 cusip/RPS cutover) is staged but not in flight; paused for HLOT2.
    - WP-10b gold↔silver recon harness is diagnostic-only; doesn't touch B_01.
  </cross_domain_coordination>

  <evidence>
    <item>docs/briefs/coo_briefing_hlot2_dual_patch.md — DS~A decision-ready authoring packet (Section 1-10: TL;DR, observed gap, Patch A, Patch B, orthogonality, acceptance_criteria, scope negatives, code sites, evidence index, ask)</item>
    <item>data/black_diamond/diagnostics/STAUDT/HLOT1/hlot1_attribution_report.md — Phase 0 attribution: all 4 pre-enumerated gates ruled out</item>
    <item>data/black_diamond/diagnostics/STAUDT/HLOT1/hlot1_correction_three_mechanisms.md — post-Andrew-pushback three-mechanism correction (DIVZ=CA-classifier, IEFA=sale-asymmetry, IDVZ=missing-BUYs)</item>
    <item>data/black_diamond/diagnostics/STAUDT/HLOT1/transaction_history_spot_check.md — 20/20 DIVZ Merger CA verification + 20-acct per-ticker probes</item>
    <item>data/black_diamond/diagnostics/STAUDT/HLOT1/top9_gap_profile.{csv,parquet} — All Top-9 per-ticker gap + mechanism fingerprint</item>
    <item>data/black_diamond/diagnostics/STAUDT/HLOT1/model_vs_current.csv — 28-ticker model target vs current firm composition</item>
    <item>data/black_diamond/diagnostics/STAUDT/HLOT1/divz_silent_close_gate_eval.parquet — 2,600-row DIVZ per-acct gate evaluation</item>
    <item>data/black_diamond/diagnostics/STAUDT/HLOT1/iefa_silent_close_gate_eval.parquet — 559-row IEFA per-acct gate evaluation</item>
    <item>data/black_diamond/diagnostics/STAUDT/HLOT1/iefa_overlap_unit_shortfall.parquet — 4,143-row IEFA overlap per-acct unit gap</item>
    <item>MCP: CTO HLOT2 scope LOCKED 20260420T221414Z (paired_subs unchanged + canonical/holdings fallback Tier 2 added)</item>
    <item>MCP: CTO HLOT2 guardrails 20260420T215315Z (5 acceptance guardrails)</item>
    <item>MCP: CTO scope update 20260420T220853Z (single TO dual-patch concurred)</item>
    <item>MCP: DS~A Phase 0 extensions complete 20260420T221341Z (paired_subs = {Merger,Conversion Out,Exchange,Tender,Cash in Lieu} unchanged; 99.8pct coverage + 25 uncovered accts need canonical fallback)</item>
    <item>MCP: DS~A B_00 NameError fix-forward 20260421T121710Z (1a54d46a; smoke-import gate added to HLOT2 Phase 2 acceptance)</item>
  </evidence>

  <deliverables>
    <item>B_01.holdings_lots.py commit: Patch A (~6 lines at L2186-2213) + Patch B (~40-60 lines, new function `_build_authoritative_reopen_lots` or widened `_build_uln_sleeve_shadow_lots`)</item>
    <item>Session log at org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-21/staudt_hlot2_b01_dual_patch.md — full Compiler Tools section (all 10 `<run>` steps with observed output + pass/fail vs `<expect>`)</item>
    <item>Comparison pack post-qa-runner: per-patch + per-ticker + per-tier recovery attribution table + BFIX2 subsumption probe + firm total_aua invariance check + Top-9 firm_composition.json percentages</item>
    <item>RAVC4 close MCP to COO on commit: commit SHA + attribution table + evidence citations + pass/fail on each acceptance criterion</item>
    <item>Compiler-tools-log auto-append for every `<run>` (enabled via .comp-graph/.agent_context TO_ID=ADVI_STAUDT.HLOT2)</item>
  </deliverables>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~A" task="HLOT1 Phase 0 attribution + Phase 0 extensions" status="complete">
      HLOT1 ruled out all 4 gates; Ext 1 (paired_subs complete set) + Ext 2 (silver/unrealized coverage + canonical fallback need) landed 2026-04-20 22:13Z.
    </dependency>
    <dependency agent="1.0.0_SA_CTO" task="HLOT2 scope lock" status="complete">
      CTO scope-locked 2026-04-20 22:14:34Z (paired_subs unchanged; 3-tier priority chain; 5 guardrails).
    </dependency>
  </dependencies>
</task_order>
