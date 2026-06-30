# ADVI_INFREF P1 LEG-1 -- GOLD-READ RECONCILIATION (the gating step before any silver retire)

**Author:** 0.4.0_DS_ClientPlatform~A | **Date:** 2026-06-30 | **TO:** ADVI_INFREF.P1 LEG-1
**Purpose:** per SPEC-2 S-R5 + CTO "GOLD-ACCUSTOMED governs": map which silver copy EACH gold script READS,
BEFORE consolidating/retiring -- the one real migration risk. Source-grounded (grep on data/inf/scripts/gold/*.py).

## HEADLINE: the "duplicate" copies are NOT simply redundant -- they are LIVE-MULTI-CONSUMED by DIFFERENT gold
scripts. SPEC-2's "normalize flat -> partitioned, retire flat" is BACKWARDS for performance/assets_v2/
transactions (gold reads the FLATs). Only `silver/performance_dim/` is a true dead orphan. Consolidation must
repoint EACH consumer atomically + parity-check, NOT bulk-retire.

## Per-dim / per-copy READ + PRODUCER map (grounded)

### PERFORMANCE (3 copies; 2 LIVE, 1 DEAD)
| copy | producer | gold reader(s) | verdict |
|---|---|---|---|
| `silver/performance/` (FLAT) | convert_performance_to_silver.py (INF_API_SILVER_PERF) | **INF_C_02.client_performance:62** (the canonical perf; INFGRO.009 repoint) | LIVE -- gold-critical |
| `silver/api_dims/performance/` | convert_orion_api_to_silver --dim performance | **INF_D_00c.portal_leaderboard:106 + INF_D_02.advisor_client_detail:113** | LIVE -- different consumers |
| `silver/performance_dim/` | NONE (frozen 2026-05-13) | none (INF_C_02 comment: dead phantom path that "neutered INFGRO.009 across 3 chain runs") | **DEAD -> safe retire** |

### ASSETS / ASSETS_V2 (3 copies; all LIVE, split readers)
| copy | producer | gold reader(s) | verdict |
|---|---|---|---|
| `silver/api_dims/assets/` | DS~D assets dim builder | **INF_D_02b.top_holdings:61** | LIVE |
| `silver/api_dims/assets_v2/` | convert_orion_api_to_silver --dim assets_v2 | **INF_D_02d.firm_mix_summary:73** | LIVE |
| `silver/assets_v2/` (FLAT) | convert_assets_v2_to_silver.py (SILVER_KEY_TPL silver/assets_v2/{date}.parquet) | **INF_D_03.composition_artifacts:100** | LIVE -- gold-critical (FLAT) |

### TRANSACTIONS (1 copy, FLAT, single canonical, heavily consumed)
| copy | producer | gold reader(s) | verdict |
|---|---|---|---|
| `silver/transactions/` (FLAT) | convert_*_to_silver (txn) | **INF_A_-1.materialize_txn_cache + INF_A_00.accounts_dimension + INF_A_01.advisor_assignments + INF_A_03.positions_cube** (A-stage txn cache + positions_cube reconstruction) | LIVE -- THE canonical txn |

### Also: INF_B_00 reads `bronze/orion-api/{date}/assets.csv` (BRONZE, not silver) for its holdings reconcile.

## CONSOLIDATION VERDICT (per dim, never-widen) -- DEAD-CONFIRM FINAL (CTO arch-gated)
1. **DEAD-CONFIRMED -> retire-eligible (DOCUMENT-dead-now + DEFER S3 tree delete to RT confirm-first batch,
   Andrew-confirm per CLAUDE.md destructive-delete; NOT a one-off delete):**
   - `silver/performance_dim/` -- no producer, frozen 2026-05-13, no consumer (INF_C_02 comment corroborates
     the dead phantom path). DEAD.
   - `silver/orion-rest/` -- no producer, frozen 2026-04-30, ZERO consumers anywhere (grep data/ + portal/src +
     infra/aws = empty). DEAD-confirmed (final no-FE/non-gold check passed).
   - `silver/accounts_dim/` -- **NOT DEAD (census corrected).** LIVE-consumed by INF_09:22 / INF_C_09:125 /
     INF_D_00:49, but FROZEN 04-29 (legacy convert_orion_to_silver.py:55 stopped). -> REPOINT bucket (#2b),
     NOT retire -- retiring it would break 3 gold consumers; it's a STALENESS finding (flagged COO->Andrew).
2b. **accounts_dim REPOINT = a CORRECTNESS FIX, not byte-parity** (CTO distinction): repoint INF_09/INF_C_09/
   INF_D_00 -> accounts_v2 (live primary, accounts_dim superseded). Output DELIBERATELY changes (stale 04-29 ->
   fresh). Gate: (a) source-confirm accounts_v2 primary; (b) sane 2-month delta (counts/names/first_trade_date),
   not a regression; (c) served AUA UNAFFECTED (holdings/positions_mv-derived, not accounts_dim). Andrew-aware.
2. **LIVE-MULTI-CONSUMED -- atomic per-consumer repoint required (NOT bulk retire):** performance (flat
   silver/performance/ [INF_C_02] + api_dims/performance/ [INF_D_00c, INF_D_02]); assets_v2 (api_dims/assets_v2/
   [INF_D_02d] + flat silver/assets_v2/ [INF_D_03]); assets (api_dims/assets/ [INF_D_02b]); transactions (flat
   silver/transactions/ [A-stage]). For EACH: (a) confirm content-equivalence across the copies (parity), (b)
   pick the canonical partitioned `silver/orion-api/{dim}/snapshot_date={date}/`, (c) repoint EACH gold consumer
   atomically + parity-verify the gold output unchanged, (d) THEN retire the non-canonical copies.
3. **SPEC-2 ADJUSTMENT:** SPEC-2 §5.2 "normalize flat -> partitioned, retire flat" must NOT bulk-retire the
   FLATs -- gold reads silver/performance/, silver/assets_v2/, silver/transactions/ (FLATs). The flat CONTENT is
   canonical-for-those-consumers; the consolidation relocates it to the partitioned layout + repoints the
   consumer in the SAME atomic step (never a flat-retire before the consumer repoint -- that's the INFGRO.009
   phantom-path incident class).

## NEXT (LEG-1 build, post-CTO-arch-gate)
- RAVC CTO this reconciliation + the per-consumer repoint plan -> arch-gate.
- Build dim-by-dim, lowest-risk first: retire the confirmed-dead (performance_dim, accounts_dim/orion-rest after
  dead-confirm); then the live-multi-consumed dims one at a time (parity per consumer). positions_mv/assets
  atomic with LEG-2 de-convert.
- Coordinate the one-converter-dispatch (convert_orion_api_to_silver.py) extension to own every dim.
