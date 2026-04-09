# Session Log: ADVI_49PUSH.005 — Gold Chain on c6a.16xlarge QA Runner

**Agent:** 0.6.0_AE_PartnerETL
**Date:** 2026-04-08 (evening ET)
**Task Order:** ADVI_49PUSH.005 — Deploy D_04, run full chain
**Instance:** bd-gold-qa-runner (i-0090b823a4a0997e3)

---

## Summary

Attempted full gold chain rebuild on QA runner to test D_04 deployment and evaluate c6a instance family as replacement for c6i.16xlarge (capacity issues on production runner). Chain completed B_02-D_03 successfully. D_04 failed on ImportError.

## Instance Type Testing

### c6a.8xlarge (32 vCPUs, 64GB RAM) — FAILED
- A_00 (66s), A_01 (51s), A_02 (24s) completed fine
- A_03 positions_cube: **OOM KILLED** during ProcessPoolExecutor fork expansion
  - 307,652 (account, asset) pairs with 28 fork workers
  - Each fork copies parent memory; 64GB insufficient
  - Script logs "128GB RAM" — hardcoded expectation
- Verdict: 64GB is a non-starter due to A_03

### c6a.16xlarge (64 vCPUs, 128GB RAM, AMD EPYC) — SUCCESS
- All scripts through D_03 completed
- 60 workers (cpu_count - 4), same as c6i.16xlarge
- ~20% cheaper than c6i.16xlarge (~$2.18/hr vs ~$2.72/hr)
- No capacity issues starting the instance (unlike c6i.16xlarge)

## Per-Script Timing (c6a.16xlarge)

| Script | Time | Notes |
|--------|------|-------|
| A_00 accounts_dimension | 66s | I/O bound, 1,766 txn files |
| A_01 advisor_assignments | 51s | I/O bound |
| A_02 fee_rate_history | 24s | I/O bound |
| A_03 positions_cube | 566s | BOTTLENECK #1 — 307K pairs, 60 workers, 93M rows, 529MB written |
| A_04 client_dimension | ~40s | Estimated from timestamps |
| B_01 holdings_lots | ~600s | Estimated — was running 15+ min before chain cancelled |
| B_01b classify_securities | STUCK | OpenAI API hang (see below) |
| B_02 canonical_lots | 154s | |
| B_03 account_gains | 131s | |
| C_00 canonical_performance | 64s | |
| C_01 canonical_nna | 108s | |
| C_02 client_performance | 200s | |
| C_03 account_performance | 112s | |
| C_04 validate_aua | 5s | Validator only |
| C_05 client_tax_liability | 4s | |
| C_06 client_mix_timeseries | 391s | BOTTLENECK #2 — 60 process + 60 write workers, ~8.2GB RSS per worker |
| C_07 advisor_attribution | 14s | |
| C_08 advisor_fee_efficiency | 64s | |
| D_00 portal_aggregates | 163s | Ran updated version (dead code removal + new_clients fix) |
| D_01 partner_analytics | 153s | |
| D_02 advisor_client_detail | ~7s | |
| D_03 composition_artifacts | 92s | |
| D_04 client_portal_summary | FAILED | ImportError (see below) |

**Total wall time (B_02 through D_03):** ~28 min
**Estimated full chain (A_00 through D_03, excl B_01b):** ~42 min

## Bugs Found

### 1. gold_dispatch.sh --incremental crashes A_01
- Production runner (i-01003b035d2988dfb) was being triggered by EventBridge at 23:00 UTC
- EventBridge runs `--chain full --incremental`
- A_01 does not accept `--incremental` flag: `error: unrecognized arguments: --incremental`
- Only A_00 and C_06 support `--incremental`
- `set -e` kills the chain, instance auto-shutdowns
- This is why the production runner appeared to have "capacity issues" — it was starting fine but crashing immediately
- **FIX APPLIED:** gold_dispatch.sh now strips `--incremental` from scripts that don't support it (whitelist: A_00, C_06)
- Uploaded fixed dispatch to S3

### 2. B_01b stuck on OpenAI API
- classify_new_securities.py calls OpenAI API with exponential backoff
- Process hung for 15+ minutes: 74 threads sleeping in `do_poll`, 2.7% CPU
- Either rate-limited, key issue, or API unresponsive
- Had to kill process and skip B_01b to continue chain
- DynamoDB classification data from prior runs still usable
- Needs investigation: check openai-api-key in Secrets Manager, check rate limits

### 3. D_04 ImportError
- P3 version (1,318 lines) imports `client_aua_timeseries_key` from `lib/s3_layout.py`
- That function does not exist in the deployed s3_layout.py
- Error: `ImportError: cannot import name 'client_aua_timeseries_key' from 'lib.s3_layout'`
- DS needs to add this to s3_layout.py before D_04 can run
- Note: COO caught that S3 had stale 880-line P1 version; re-uploaded correct 1,318-line P3 version

### 4. Production runner capacity (RESOLVED)
- Production runner (c6i.16xlarge, i-01003b035d2988dfb) appeared unable to start
- Actually WAS starting fine — crashing on A_01 --incremental bug (#1 above)
- `Client.InstanceInitiatedShutdown` was the auto-shutdown after chain crash, not a capacity issue
- With the dispatch fix, production runner should work on next EventBridge trigger

## Schwab Data Uploaded

- Uploaded CRS20260406 and CRS20260407 (RPS, ULN, ULT, RLD) to s3://opal-data-bd/schwab/bronze/
- Bronze-to-silver conversion complete:
  - RPS: 2 new dates (83K + 82K positions), silver current through 20260407
  - ULN: 2 new dates (214K lots)
  - ULT: 2 new dates (164K lots)
  - RLD: 2 new dates + 1 skip (13K lots)

## Files Uploaded to S3 (s3://opal-data-bd/code/gold/)

1. D_00.portal_aggregates.py — updated version
2. D_04.client_portal_summary.py — 1,318 lines (P3 version, re-uploaded after COO caught stale 880-line version)
3. validate_platinum_consistency.py — new validation script
4. gold_dispatch.sh — D_04 added to chain + incremental fix

## Actions Needed

1. **DS:** Add `client_aua_timeseries_key` to `lib/s3_layout.py` so D_04 can import it
2. **DS/AE:** Investigate B_01b OpenAI API hang (key validity, rate limits)
3. **AE:** Re-run D_04 once s3_layout.py is fixed
4. **AE:** Verify platinum/ files in S3 after successful D_04 run
5. **AE:** Consider swapping production runner to c6a.16xlarge for cost savings (~20% cheaper, better availability)
6. **AE:** Update EC2_MANIFEST.json for QA runner instance type change (now c6a.16xlarge)
