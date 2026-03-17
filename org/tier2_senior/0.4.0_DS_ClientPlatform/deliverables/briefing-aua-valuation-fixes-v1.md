# AUA Valuation Fix Briefing -- DS to DT

**From:** 0.4.0_DS_ClientPlatform
**To:** 0.4.0_DT_ClientPlatform
**Date:** 2026-03-17
**Subject:** Gold AUA overrides -- deploy updated `05_build_client_performance.py` + `aua_overrides.json`

---

## Summary

Cross-validation of gold AUA (positions_cube x canonical_prices) against silver AUA (BD-reported market values) revealed a **+$37.5M net overvaluation** concentrated in 35 accounts. Root causes fall into three categories. This briefing covers the code changes to fix RC1/RC2 and RC6 immediately, with RC8 deferred to Phase 2.

## What Changed

### 1. New file: `data/black_diamond/scripts/gold/aua_overrides.json`

Configuration file with two sections:

- **`price_overrides`** (RC1/RC2): 5 asset names whose canonical price resolves to the wrong instrument. Action: force price to $0. Combined impact: **-$43.9M phantom overvaluation removed**.

  | Asset Name | Wrong Price | Reason | Impact |
  |---|---|---|---|
  | BNP PARIBAS SA | $97 (BNPQF equity) | Structured deposit, face-value units | -$20.9M |
  | DESTINATIONS LARGE CAP EQUITY I | $546 (wrong NAV) | Brinker Capital model sleeve | -$14.7M |
  | DESTINATIONS INTERNATIONAL EQUITY I | $384 (wrong NAV) | Brinker Capital model sleeve | -$6.2M |
  | NATIONAL BANK OF CANADA | $138 (NTIOF equity) | Structured note, face-value units | -$1.9M |
  | BBVA GLOBAL SECS B V 0% 09/16/2030 | $0.94 (issuer equity) | Structured note | -$0.2M |

- **`ghost_accounts`** (RC6): 4 account IDs where silver reports $0 but gold has a full stale portfolio. Action: exclude from gold AUA. Combined impact: **-$7.4M phantom AUA removed**.

  | Account | Gold AUA | Silver AUA | Reason |
  |---|---|---|---|
  | z0812933851 | $2.3M | $0 | Closed/transferred IRA |
  | z0818413191 | $2.1M | $6K | Synthetic account number |
  | z0819915221 | $1.9M | $1K | Zeroed account |
  | z0815983871 | $1.2M | $0 | Zeroed account |

### 2. Modified file: `data/black_diamond/scripts/gold/05_build_client_performance.py`

- Added `import json` and `AUA_OVERRIDES_PATH` constant
- Added `load_aua_overrides()` function: reads `aua_overrides.json`, returns price override actions and ghost account set
- Modified `process_date_partition()`: accepts `price_override_actions` and `ghost_accounts` params
  - Ghost accounts: positions filtered out before pricing (RC6)
  - Price overrides: matched assets get `price=0.0, source='override_zero'` before market_value calculation (RC1/RC2)
- Modified `build_client_performance()`: passes overrides through to partition processor
- Modified `main()`: loads overrides in new Step 1b, passes to build function

### 3. NOT changed (Phase 2 -- RC8)

Systematic ETF pricing gap (~$6.7M net undervaluation across 11 accounts) is **not addressed** in this deployment. Root cause is likely canonical price timing (T-1 close vs BD's intraday NAV). Requires investigation of price source timestamps before implementing a silver-calibration fallback. The `silver_calibration` section in `aua_overrides.json` is present but `enabled: false`.

## Expected Impact

| Metric | Before | After |
|---|---|---|
| Gold-vs-Silver gap (top 35) | +$37.5M | ~-$13.2M |
| RC1/RC2 overvaluation | +$43.9M | $0 (zeroed) |
| RC6 ghost AUA | +$7.4M | $0 (excluded) |
| RC8 ETF pricing gap | -$6.7M | -$6.7M (unchanged, Phase 2) |
| Net remaining gap | -- | Dominated by RC8 + RC3/RC7 |

## Deployment Steps

1. **Commit** both files to `CLOUD` branch
2. **Upload** `aua_overrides.json` to EC2 alongside the script (same S3 artifact path as `05_build_client_performance.py`)
3. **Run** `05_build_client_performance.py --upload` on EC2 to regenerate `gold/client_performance.parquet`
4. **Run** `05c_validate_aua_vs_silver.py` to confirm gap reduction
5. **Run** downstream scripts (07, 08, 09, 10) that consume `client_performance.parquet` to propagate corrected AUA into portal JSON outputs
6. **Tag** per standard deployment protocol

## Validation

After deployment, run `05c_validate_aua_vs_silver.py --date {latest}` and confirm:
- Aggregate gap drops from ~3.5% to <1.5%
- No new FAIL status accounts introduced
- Ghost accounts no longer appear in gold AUA

The `.tmp_gro_validation.py` script (in workspace root, not deployed) can also be re-run to verify the GRO decomposition values reflect corrected AUA.

## Risk

- **Low risk**: Price overrides zero out 5 specific asset names. If any of these asset names are used by other accounts with legitimate holdings, those positions will also be zeroed. Mitigation: the asset names are highly specific (e.g., "BNP PARIBAS SA" is only held by one account as a structured deposit; genuine BNP equity is not held anywhere in the book).
- **Low risk**: Ghost account exclusion removes 4 specific account_ids. If these accounts are re-opened with new positions, they will need to be removed from the exclusion list.
- **No NNA impact**: Overrides only affect AUA pricing. NNA flows (cum_inflows, cum_outflows) are computed from transactions, not positions x prices, so NNA is unaffected.
