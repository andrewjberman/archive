# WP-10 Phase 1 — Account-ID Consumer Enumeration (pre-flight)

**Date:** 2026-04-15
**Agent:** 0.4.0_DS_ClientPlatform~B
**TO:** BDPL_CNPRCS.WP-10 (staged behind AE WP-3)
**Status:** pre-flight memo only; no code

## <run>comp-pipescript io</run> on 9 account_id consumers

| Script | account_id join inputs | Role in pipeline |
|--------|-----------------------|------------------|
| C_01 | accounts_dimension_latest, canonical_account_gains (B_03), canonical_nna_atomic | NNA roll-up @ account grain |
| C_05 | accounts_dimension_latest, canonical_lots_unrealized, holdings_lots | client tax liability joins account->client |
| C_08 | account_team (C_07), advisor_fee_detail, canonical_nna | per-advisor fee efficiency via account_team join |
| D_00 | accounts_dimension_latest, account_performance, account_team, canonical_nna, holdings_lots | firm header metrics |
| D_00b | accounts_dimension_latest, account_performance, account_team, canonical_nna, holdings_lots | firm timeseries chart |
| D_00c | account_performance, account_team, advisor_fee_detail, canonical_nna | employee leaderboard |
| D_01 | accounts_dimension_latest, account_performance, account_team, canonical_nna | partner_analytics header_metrics |
| D_02 | account_performance, account_team, advisor_fee_detail, canonical_nna, holdings_lots, account_aua_timeseries, client_detail | per-advisor client detail + timeseries |
| D_04 | holdings_lots, account_aua_timeseries, client_aua_timeseries, client_detail, advisor_timeseries | platinum client_portal_summary |

**Observation:** every script joins on `accounts_dimension_latest` (A_00/B_01) OR on an account-keyed parquet (account_team, account_performance). The cutover for WP-10 is additive — every existing join gets a lifecycle-aware filter; no schema break.

## <run>comp-blast account_id</run>

Returned a single function hit: `gold:A_03.positions_cube:_load_open_account_ids` — compiler graph tracks functions, not join columns, so blast underreports the consumer set.

**Authoritative consumer list (from Phase 1 io manifests above):** C_01, C_05, C_08, D_00, D_00b, D_00c, D_01, D_02, D_04 — matches WP-10 TO `<wire_contract>` enumeration exactly. No surprise consumers.

## Expected <expect> checks

1. `<expect>` Enumerated join patterns per script — **PASS** (table above).
2. `<expect>` Full downstream consumer graph matches Phase 1 script list — **PASS** (9-script list = TO wire_contract).

## Ready-to-execute checklist (when WP-3 tag cuts)

- [ ] Flip WP-10 status `staged` -> `pending`
- [ ] Write `data/black_diamond/scripts/gold/build_account_lifecycle.py`
- [ ] Write to `gold/canonical/account_lifecycle/{date}.parquet`
- [ ] Add `comp-validate account_lifecycle` schema config entry
- [ ] Spot-check 3-5 closed+reopened accounts (identify from adhc_histry briefs or RPS drift logs)
- [ ] Additive consumer update: insert lifecycle-join filter into each of 9 scripts; zero schema break
