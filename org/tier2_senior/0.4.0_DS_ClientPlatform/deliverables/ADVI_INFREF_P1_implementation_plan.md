# ADVI_INFREF P1 — DS implementation plan (for CTO arch-gate, per leg)

**Author:** 0.4.0_DS_ClientPlatform~A | **Date:** 2026-06-30 | **TO:** ADVI_INFREF.P1 (DS lane, solo)
**Gate:** CTO arch-gates EACH leg BEFORE build (COO directive 173347Z). CVO validates landed artifacts. 0.6.1_AE owns EC2/EventBridge infra; DS owns pull/silver/gold SCRIPTS + chain composition.
**Design source (RULED, not reopened):** SPEC-1/2/3/4 (inflection-refactor-*.md, CVO de317da67/7e1f18de1) + PRD §1/§5 + ratification 1-5.
**Non-negotiables preserved:** D_04 sole header_metrics writer + shape gate (TO-2); G-R1 Part-2 partition-freshness guard (c76540ebe DEPLOYED); Rule-17 full fidelity; never-widen parallel-run parity before any teardown.

## Sequencing principle
Lowest-risk-first + never-widen. Each leg: build behind a flag / parallel path -> parity-validate several days vs the live output -> CVO co-sign -> cut over -> 0.6.1_AE decommissions the legacy. NO legacy teardown until parity holds. Gold partition-freshness is already deployed (Part-2), so the live freeze fix is in; P1 is the structural unify.

## LEG ORDER (proposed to CTO)

### LEG 0 (do first — low-risk hygiene, no infra): EG-1 flag fixes
- F1: `aua_by_tax_status.json` single-producer. INF_D_00.portal_aggregates.py:903 DELETEs it (stale belief "no current script emits it") while inf-portal-publisher build_snapshots WRITES it. Resolve: confirm whether aua_by_tax_status is live-consumed (portal route check); if dead -> publisher stops emitting + D_00 stops deleting; if live -> publisher sole producer, remove the D_00 delete. (READ-ONLY confirm first, then a minimal edit.)
- F2: remove the dead inf-portal-publisher `build_header_metrics()` (L569, uncalled since INFPUBLISHERDEDUP 2026-05-12) so the overlap can't be re-enabled.
- Both are small, no chain-composition change. Ship early to clear the writer-map for P1 gold.

### LEG 1: SILVER consolidation (SPEC-2) — medium risk, no new infra, GOLD-ACCUSTOMED-governed
- Consolidate the converter sprawl to ONE dispatch (`convert_orion_api_to_silver.py` DIM_BUILDERS model) writing ONE layout `silver/orion-api/{dim}/snapshot_date={date}/data.parquet`.
- Per-dim GOLD-READ reconciliation FIRST (S-R5): confirm which silver copy each gold script reads BEFORE retiring duplicates; repoint gold's read, then retire. (the one real migration risk; gold-accustomed governs.)
- Retire: legacy `convert_orion_to_silver.py`; 3-copy dims (assets/assets_v2, performance/performance_dim) -> one; flat trees (`silver/assets_v2`, `silver/performance`, `silver/transactions`) -> partitioned; stray `silver/accounts_dim`, `silver/orion-rest`.
- KEEP (per census + CVO): `silver/prices/` + historical_prices.parquet (T2 yahoo layer, active input to canonical-prices); `_silver_complete/`, `meta/`.
- Full-fidelity invariant per dim (field-set >= bronze; dtype/snake_case/dedup only). Eclipse silver relocate `silver/eclipse/` -> `silver/eclipse-api/` (stubbed).
- Parity gate: silver output byte-parity through the consolidation (zero value change), several days, before retiring any duplicate.

### LEG 2: BRONZE raw-native single-pull-layer (SPEC-1) — highest change, needs 0.6.1_AE infra
- DS side: the 4-dim de-convert {positions, assets, performance, transactions} — land RAW (positions/assets raw JSON; perf/transactions native CSV) under `bronze/orion-api/{date}/`; ELIMINATE the inline-parquet double-write (`bronze/{positions,assets,performance,transactions}/{date}.parquet`); move the JSON->parquet to the silver converters (LEG 1's dispatch reads raw bronze).
- One pull script per dim (retire the 3 transaction variants + 2 performance variants in data/inf/manual_api/); pull the FULL DATA_PLATFORM-cataloged surface (richer than today's 9), datestamped, native format. Two domains separate (`bronze/orion-api/` + `bronze/eclipse-api/`).
- 0.6.1_AE side (coordinate): the single pull layer runs on the unified EC2; decommission the 9 cron pull Lambdas + EventBridge rules; relocate the eclipse pull onto the EC2. DS provides the pull scripts; AE owns the EC2/trigger/IAM.
- Parity gate: silver output post-de-convert byte-equal to pre (AC7); the de-convert + repoint introduce zero value change.

### LEG 3: GOLD chain-composition (SPEC-3) — scripts UNCHANGED, composition only
- Gold A/B/C/D scripts are NOT rewritten (Andrew-locked). The change is CHAIN_INCREMENTAL composition: insert `INF_B_00..B_03 --date={today}` + `INF_C_00..C_09 --date={today}` before D_* so `gold/canonical/holdings_{today}.parquet` builds every incremental run. (NOTE: the scheduled nightly is `--chain full` which already runs B_00 — this hardens the MANUAL/future incremental path; the nightly's live fix is the deployed timeout-tolerate + Part-2 guard.)
- Partition-freshness assert = G-R1 Part-2 (c76540ebe) — already DEPLOYED. D_04 sole header_metrics writer preserved.
- [DECISION->CTO/DS] which A-stage dims incremental may cache vs rebuild daily (B/C not cacheable).

### LEG 4 (yahoo repoint, §2) — GATED on the EG-2 gap (NOT all-clear)
- INF_B_00 (already positions_mv pass-through) + INF_D_07 (reads pre-priced holdings): SAFE to confirm-on-positions_mv.
- INF_B_01 + INF_B_01b: REAL GAP — they price the HISTORICAL positions_cube + surface unpriced-held tickers (yahoo backfill); positions_mv (current Orion snapshot) does NOT cover the deep history. So yahoo does NOT retire wholesale. Options for CTO: keep canonical_prices/yahoo for the historical timeseries leg, OR accumulate positions_mv going-forward + a one-time frozen historical backfill then retire. Do NOT retire yahoo for B_01/B_01b under P1.

## RUNTIME (SPEC-4) — sequenced LAST (RT-R3/R4), 0.6.1_AE-led
- Single-runner decommission + auth/OTP hardening = after bronze/silver/gold land + parity holds. The FINAL step (Andrew-flagged) = the auth/OTP robustness. Not P1-DS-build.

## Cross-domain / coordination
- 0.6.1_AE: EC2 single-pull-layer, EventBridge decommission, IAM (cloudfront:CreateInvalidation grant for the publisher — currently catch-wrapped per publisher L28). DS: scripts + chain composition.
- CVO: landed-artifact validation per leg (parity + value-parity).
- CTO: arch-gate EACH leg before build.

## Open decisions for CTO
1. LEG order confirm (0/1/2/3 as above; yahoo LEG-4 gated).
2. aua_by_tax_status live-or-dead ruling (F1).
3. A-stage incremental cadence (LEG 3 DECISION).
4. Yahoo historical-pricing approach (LEG 4 — keep vs accumulate+freeze).
