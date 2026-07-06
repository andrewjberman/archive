# VERIFY #18 -- target: INF_B_01.holdings_lots.py

- is_real: **True**
- confidence: **confirmed**
- corrected_severity: high

## Reasoning
REAL, actively-firing silent data-correctness defect. Traced end-to-end and could not refute it.

(1) INF_D_07:50 still reads ACCTS_DIM_KEY='silver/accounts_dim/latest.parquet'. The freeze is triple-corroborated by sibling repoint comments: INF_C_09:125-127, INF_D_00:57-58, and INF_D_00c:228-229 all state 'ADVI_INFREF P1 LEG-1 repoint (2026-06-30): silver/accounts_dim/ froze 04-29 (legacy convert_orion_to_silver.py stopped)' and were moved to live silver/api_dims/accounts_v2. INF_D_07 was NOT repointed. gold_freshness_config.yaml:186-196 still lists readers [INF_D_07, INF_D_00] at cadence:daily — stale metadata proving the cleanup was incomplete and INF_D_07 was overlooked.

(2) INF_B_01 output schema (INF_B_01.holdings_lots.py:10-19) is exactly date,account_id,ticker,units,price,market_value,price_source,custodian — NO household_id. So the guard at INF_D_07:117 ('if household_id not in df.columns') ALWAYS runs the left-merge at line 118.

(3) The flag correctly does NOT claim a dtype-mismatch join: account_id is astype('int64') on both sides (dim :74-76, holdings :112-114), so the merge succeeds; accounts absent from the frozen dim get household_id=NaN and are unconditionally dropped at line 120 (df.dropna(subset=['household_id'])). There is NO fallback/enrichment (contrast INF_D_00 and INF_C_07 which backfill household_id from live accounts_v2).

(4) Reachability confirmed: INF_D_07 is in CHAIN_COMPUTE (orion-gold-dispatch.sh:335) and CHAIN_GOLD_D (:347), so it runs on the daily full chain (and the D-chain in incremental). Output platinum/firm/concentration_risk.json is a live portal route (INFETL_PORTAL_ROUTE_MATRIX.md:100, getInflectionConcentrationRisk / InflectionInsightsPanel), so wrong numbers are user-facing.

Mechanism confirmed: holdings is derived from live positions_mv (current account universe), so any account funded after 2026-04-29 appears in holdings but is missing from the frozen 04-29 dim -> household_id NaN -> dropped. Result: (a) purely-new households vanish from the served artifact (under-count); (b) mixed households (pre+post 04-29 accounts) have aua/total_mv understated (build_concentration_risk :144-145,:160-161) and top1_pct/HHI computed on a partial portfolio — a genuinely concentrated household can be served as 'diversified'. rc=0, no crash — silent.

Adversarial refutation fails on every axis: not guarded (no fallback at :120), path reachable (daily chain), mode assumption holds (runs in full AND incremental D-chain), freeze verified. The only element not directly observed in live S3 is the specific present-day post-04-29 funded account — but that is the expected steady state after 68 days of daily accounts_v2 growth, and the very existence of the ADVI_INFREF repoint of three siblings proves the team already recognized the frozen dim is missing current accounts. The triggering path is concrete and deterministic; only the magnitude (how many households) is unquantified.

Severity high (not critical): does not crash the chain or corrupt the whole artifact — the majority pre-04-29 households remain correct — but it silently serves wrong concentration-RISK numbers on a customer-facing portal panel, with a blast radius that grows monotonically the longer the freeze persists. The inf_silver_accounts_dim freshness monitor (ERROR at 48h) should be alarming on this frozen artifact, but that guards freshness of the dim, not the correctness of INF_D_07's dropped-rows output.
