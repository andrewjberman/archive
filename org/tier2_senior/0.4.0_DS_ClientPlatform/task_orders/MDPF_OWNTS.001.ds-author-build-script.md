<task_order>
<metadata>
  <to_id>MDPF_OWNTS.001</to_id>
  <project>MDPF_OWNTS</project>
  <title>DS author: build_mdpf_etf_ownership_timeseries.py + aggregate-AUA additive ownership_pct field + trading-day calendar shim + fixtures + comp-validate + self-consistency reconcile check</title>
  <assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — GO dispatched this cycle</status>
  <priority>HIGH (Andrew sovereign direct 2026-05-26 3 asks + 2 methodology refinements; ws CTO PRD v0.1 8a125c682 canonical; substrate-rich brief author this lane)</priority>
  <references>
    <ref type="prd">docs/architecture/MDPF_OWNTS.md v0.1.1 (commit `d30a73cd6` — same-cycle precision-pin amendment supersedes v0.1 `8a125c682`; 3 narrow author-chain refinements folded pre-impl per [[feedback_self_correction_upstream_of_verify_channel]] — Tier-1+Tier-2 pair refinement; /verify-channel REPAIR-AMENDMENT NOT triggered)</ref>
    <ref type="prd_section">§3.1 Option A architecture (CTO selected v1; flagged for Andrew ratification §10 Q1); §4.1 rollup math (v0.1.1 refined); §5.2 artifact shape; §5.3 reconcile dual-gate (v0.1.1 refined); §8.2 AC1-AC7</ref>
    <ref type="substrate">docs/briefs/mdpf-etf-ownership-inflection-tracking-20260526.md (`12f01b4e1` + methodology amendment `d0aa4073b`) — DS-authored substrate, this lane's prior work</ref>
    <ref type="depends_on">MDPF_ASSETS (CLOSED 2026-05-21) — read-only consumer of platinum aggregate-AUA artifact</ref>
    <ref type="andrew_sovereign">2026-05-26 verbal "variation on INF-gold-runner with smaller CPU" (Q1 flagged Andrew ratification) + Refinements 4-5 trading-day-basis + prorated-partial-month methodology</ref>
  </references>
  <dependencies>
    <dependency>None for authoring (PRD canonical + brief substrate ready)</dependency>
    <dependency>MDPF_OWNTS.002 (AE chain wire) gates on this TO's RAVC2-ACCEPT</dependency>
  </dependencies>
</metadata>

<scope>
**Author the DS-side substrate for the MDPF_OWNTS daily chain Stage 4** per PRD v0.1 §3.1 Option A architecture (CTO-selected v1 default; ratification flag §10 Q1 routed to Andrew via ws COO MCP this turn — proceed under v1 default per LD-0084 ALWAYS-PROCEED; if Andrew rules Option B mid-flight, re-cycle scope).

**Substrate (4 deliverables):**

1. **New gold script** `data/mdpf/scripts/gold/build_mdpf_etf_ownership_timeseries.py`
   - Reads last-N daily `s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/{date}.json` artifacts
   - Builds per-ticker time-series (date-keyed) with per-partner ownership_pct
   - Computes MTD + YTD rollups (trading-day basis only per Refinement-4) with **canonical headline = (b) full-window-with-pre-onboard-zeros** (default v1 per PRD §10 Q2; Andrew ratification flag pending — proceed under default)
   - Emits all 3 methodology variants per PRD §5.2 audit fields: `present_only_pct` + `full_window_pct` + `coverage_fraction`
   - Writes per-ticker artifact `s3://opal-data-portal-v2/platinum/mdpf/etf_ownership_timeseries/{ticker}.json`
   - Methodology version: `mdpf_ownts_v1_0`
   - Zero-ownership tickers emit `{by_partner: {}}` daily entries (preserve aggregate's skip-zero pattern per PRD §5.2)

2. **Modify** `data/mdpf/scripts/gold/mdpf_aggregate_aua.py`
   - Add additive `ownership_pct = held / etf_total_net_assets` per `held_by_partner` entry inside `etf_decomposition`
   - 6-decimal precision per PRD §8.1 R1
   - Methodology version bump v0_9 → v0_9_1
   - **Reconciliation invariants UNCHANGED** (additive field only; not replacing any existing identity)

3. **New shim** `data/mdpf/scripts/lib/trading_day_calendar.py`
   - NYSE schedule via `pandas_market_calendars`
   - Pin lib version in `requirements.txt` per PRD §8.1 R3 mitigation
   - Functions: `is_trading_day(date)`, `trading_days_between(start, end)`, `trading_days_mtd(date)`, `trading_days_ytd(date)`

4. **Fixtures (5+ cases)** under `data/mdpf/tests/gold/fixtures/mdpf_ownts/`:
   - Partial-onboard-window (Inflection's PFOE actual case; n=6 post-onboard days into May 2026)
   - DoD-anomaly emit (PFOE 5/21-5/22 trajectory >1.5pp DoD soft-flag — should fire flag, NOT block reconciliation per PRD §8.1 R2)
   - Zero-ownership tickers (DIVZ + IDVZ for Inflection)
   - Missing-trading-day null (explicit null, NOT interpolation per PRD §10 Q8)
   - Multi-month YTD compose (>30 trading-days across month boundary)

5. **comp-validate config** + new **self-consistency reconcile DUAL gate** (per PRD v0.1.1 §5.3 — replaces ambiguous v0.1 "0.001%"):
   - Absolute gate (a): `$0.01` on `held` reconstruction (`abs(held - ownership_pct * etf_total_net_assets) < 0.01`)
   - Absolute gate (b): `0.0001` on `ownership_pct` recompute (= 0.01 percentage points; `abs(ownership_pct - held/etf_total_net_assets) < 0.0001`)
   - EITHER gate failing → chain step fails LOUD + skip emit + preserve prior version

**PRD v0.1.1 §4.1 null-vs-pre-onboard-zero rollup math (binding):**
- Pre-onboard zeros COUNT in numerator + denominator (full-window canonical headline)
- Missing-emit nulls EXCLUDED from BOTH numerator and denominator
- Fixture coverage: ADD a `mixed pre-onboard-zero + missing-emit-null` row to verify the right code path on each (folds into the 5+ fixtures list)

**Per CLAUDE.md Rule 13:** DS owns the FULL commit → push CLOUD → S3 upload → `comp-pipescript deployed` MATCH → SSM dispatch (or RAVC2 ACK to AE for PROD).

**Per CLAUDE.md Rule 14:** `.tools/ds-commit-gate.sh` MUST run + exit 0 on every Python edit (py_compile + ds-precommit-check.py + ruff).

**Per CLAUDE.md Rule 15:** all `data/mdpf/scripts/gold/*.py` + `data/mdpf/scripts/lib/*.py` MUST begin `from __future__ import annotations`.
</scope>

<acceptance_criteria>
- AC1: Augmented `mdpf_aggregate_aua.py` emits `ownership_pct` per partner per ETF; existing aggregate-AUA reconciliation invariants UNAFFECTED (per PRD §8.2 AC1).
- AC2: New `build_mdpf_etf_ownership_timeseries.py` emits per-ticker artifact for all 4 Opal ETFs (DIVZ + IDVZ + PFDE + PFOE) cleanly on fixture-run.
- AC3: MTD + YTD rollups arithmetically verify to-the-cent against DS brief findings — May 2026 = **16 emitted trading days** (NOT 17 calendar trading-day count; 5/1 missing-emit excluded from denom per PRD v0.1.1 §4.1 null-rule); post-onboard window n=6 PFOE 6.520% + PFDE 7.413% present-only; pre-onboard-zero full-window PFOE ~2.30% + PFDE ~2.61%. Brief findings table is canonical AC3 ground-truth.
- AC4: Trading-day calendar binding enforced; missing-trading-day emit is explicit `null`.
- AC5: DoD anomaly soft-flag fires on PFOE 5/21-5/22 fixture (no block; audit-only).
- AC6: comp-validate config PASS on fixture run + self-consistency reconcile gate runs PASS.
- AC7: 5+ fixtures all pass; ds-commit-gate.sh exit 0 across all touched Python files.

**Pass requires all 7 ACs MET.**
</acceptance_criteria>

<compiler_tools_mandate>
- `comp-pipescript io` on `build_mdpf_etf_ownership_timeseries.py` before edit (column gaps + portal consumers + S3-DYNAMIC reads)
- `comp-pipescript deployed` after S3 upload (verifies runner has the code MATCH)
- `comp-validate [script] --artifact /tmp/[file]` post-fixture-run (exit 0 all-pass = SAFE; ADVISORY WARNs = read; ERROR = BLOCKED)
- `comp-pipescript postdeps` if any post-step dispatch dependencies emerge during authoring
</compiler_tools_mandate>

<cross_domain_coordination>
- **MDPF_OWNTS.002 (AE) gates on this RAVC2-ACCEPT** — your S3-deployed scripts must be in place before AE wires Stage 4 to dispatch them.
- **No portal consumer v1** — JSON shape documented in PRD §5.2 absorbs future portal binding without breaking change. No DE/RD coordination this v1.
- **Andrew Q1/Q2 ratification flags** — surfaced via ws COO MCP to Andrew this cycle alongside this TO dispatch. Proceed under v1 defaults (Option A + headline (b)). If Andrew rules differently mid-authoring (within 1 /drive cycle), I'll MCP scope-amendment. Per [[feedback_andrew_non_response_1tick_route_to_cvo]] + LD-0026 joint-decide: if Andrew silent >1 cycle, ws COO consults ws CVO for CORROBORATE/COUNTER on Q1+Q2 → joint-decide outcome.
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion citing:
- Commit hashes (DS-cycle commit + AE-deploy pre-S3-upload commit)
- S3 object paths + sha256 for deployed scripts
- comp-validate output (exit 0 all-pass or ADVISORY-with-rationale)
- Reconcile gate output on fixture-run
- AC1-AC7 evidence inline

**Target wall-time ETA:** ~1d per PRD §6. Sub-day plausible if substrate-rich (you authored the brief; substrate is your own prior work).

**Post-RAVC2-ACCEPT:** MDPF_OWNTS.002 GO-dispatch to AE 0.7 (chain-wire stage 4 + alarm + RUNBOOK update). Then MDPF_OWNTS.003 RAVC consolidation back to you for end-to-end live-run verification.
</deliverable_disposition>

<notes>
- Substrate-richness factor: you authored the source brief 12f01b4e1 + methodology amendment d0aa4073b. The PRD codified your recommendations. Sub-day delivery plausible.
- The Q1 Option A vs B decision affects ONLY this TO's scope (script location + chain-vs-dedicated-runner). v1 defaults Option A LEAN CHAIN EXTENSION — scripts go into existing `data/mdpf/scripts/gold/` + `lib/` per current MDPF layout. If Andrew rules Option B, scope amendments include: new EC2 module + new IAM role + new EC2_MANIFEST.json entry + separate EventBridge cron — would be substantial scope-amendment.
- The Q2 headline-methodology question is LABEL-ONLY per PRD §10 Q2 (artifact emits all 3 regardless). Your authoring can proceed unblocked.
</notes>
</task_order>
