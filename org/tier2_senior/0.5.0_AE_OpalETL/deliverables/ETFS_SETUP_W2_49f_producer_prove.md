# ETFS_SETUP W2 -- 49F daily ETF-ownership producer: BUILT + PROVEN (checkpoint)

**Agent:** 0.5.0_AE_OpalETL | **Date:** 2026-06-25 | **archetype:** IMPLEMENT
**TO:** ETFS_SETUP.W2 | **Verify:** 3.0.0_SA_CVO | **Consult:** 0.4.0_DS_ClientPlatform (daily-slice contract)
**Status:** CHECKPOINT HIT -- producer built + proven on 06-09 + full May/June acceptance set landed. Productionization (Lambda/IAM TF + thread-reg) = next phase, RAVC'd to COO.

## What was built

`infra/aws/lambda/bd-pipeline/bd-49f-etf-ownership-daily/lambda_function.py` -- the 49 Financial daily ETF-ownership producer, mirroring the W1 Inflection producer (`inf-etf-ownership-daily`) exactly: same compute contract, same output schema, same zero-vs-missing/completeness-floor logic, same source_as_of=true-vintage. Only the SOURCE shape differs (Schwab RPS silver, Hive `date=` partitions). ds-commit-gate: PASS.

## Grounding (Rule 22 -- live-verified, not self-report)

1. SUBSTRATE EXISTS (corrects the TO's "B1 EMPTY" note + the PRD source path):
   - The TO/PRD cite `opal-data-schwab/silver/RPS/` -- that prefix is NOT FOUND in S3.
   - The CANONICAL 49F positions silver is `opal-data-bd/schwab/silver/rps/` (comp-freshness registered entry `schwab_rps`; the 2026-05-12 bucket-drift UNIFICATION from the legacy opal-data-schwab/silver/RPS path -- the prior stale-canonical-bug source). Partitions present `date=20240112` ... `date=20260618` (deep daily history; all of May + June-MTD available). So COO's "substrate exists now" is CORRECT -- at the canonical path, not the TO's stale path. The producer reads the canonical path.
2. SCHEMA (read date=20260618/data.parquet): columns `account_id, cusip, ticker, closing_price, quantity_settled, market_value, quantity_cash/margin/short, file_date, _source_file`. Clean map: ticker->`ticker`, value->`market_value`, account->`account_id`, vintage->`file_date`.
3. 49F HOLDS the 4 Opal ETFs substantially (06-18): DIVZ $172.48M/5457acct, IDVZ $149.92M/5449, PFDE $127.47M/5420, PFOE $69.62M/5420 -- and DIVZ $172.48M ties EXACTLY to the MDPF aggregate's 49F-DIVZ slice (172480313.82), cross-source consistent.

## Proof (against the SERVED artifact + independent recompute)

- Ran the REAL handler `lambda_handler({"date":"2026-06-09"})` -> wrote schema-valid `s3://opal-data-etfs/daily/49financial/2026-06-09.json` (4 ETF rows: DIVZ $172.50M/5432, IDVZ $148.02M/5424, PFDE $123.02M/5393, PFOE $70.94M/5393; total $514.49M; source_as_of=2026-06-09; source_artifact = the RPS partition).
- INDEPENDENT recompute (fresh read of the raw RPS, different code path) MATCHES the slice to the cent for all 4 ETFs + account counts. (AC3 "sums matching the source" satisfied.)
- ACCEPTANCE SET LANDED: all 34 May-full (05-01..05-29, 20 trading days) + June-MTD (06-01..06-18, 14 days) slices written to `opal-data-etfs/daily/49financial/`, 0 failures. Totals stable ~$510-540M across the period.

## Schema (contract-conformant, identical to W1 Inflection)

`{schema_version:"1.0", partner:"49financial", date, etf_ticker, ownership_value, account_count, source_artifact, source_as_of}` -- one row per ETF, all 4 universe ETFs emitted.

## Cadence (honest, B2)

49F Schwab is a MANUAL MONTHLY batch (S-D2; freshness immaterial, monthly-granular by design). The RPS silver carries a daily partition per Schwab position file (delivered in monthly batches). The producer reads the latest available `date=` partition (or `event["date"]` for a historical re-run) and stamps `source_as_of` from the true `file_date` so AVGCAP never implies daily-fresh 49F. No automated SLA needed (Andrew-resolved S-D2).

## Remaining (productionization -- next phase, RAVC'd to COO)

1. Lambda deploy via Terraform (resource + env: ETFS_BUCKET, SRC_BUCKET=opal-data-bd, RPS_PREFIX=schwab/silver/rps/, CONFIG_KEY=config/etf_universe.json, OUTPUT_PREFIX=daily/49financial/, PARTNER=49financial) + lambda-source-map entry.
2. IAM write-out grant: the producer role needs READ opal-data-bd/schwab/silver/rps/* (own-firm) + WRITE opal-data-etfs/daily/49financial/* ONLY. comp-iam service + comp-iam gaps after the grant (NO firm-bucket-Deny widening, NO cross-firm read) -- the IAM-blast-sensitive step (PRD Sec 10), wants the careful firm-sep verify.
3. Register `opal-data-bd/schwab/silver/rps` as a pipescript-visible canonical 49F-positions thread (CTO-owned per PRD Sec 8; `schwab_rps` is already a comp-freshness entry).
4. Trigger: monthly-batch -> NO daily cron (Andrew S-D2); invoke per-batch / on the next Schwab download (~early-July). "Rides the next batch."
5. On wrap -> signal AVGCAP-W2 (DS re-runs the AVGCAP rollup to fold 49F into the 3-partner monthly).

## Compiler Tools

| Tool | Call | Result |
|---|---|---|
| comp-which | route the 49F positions-source question | PASS |
| comp-freshness | artifact schwab/silver/rps + schwab/silver/RPS (path resolution) + etfs paths | PASS (located the canonical path; corrected the TO's stale path) |
| comp-glob | locate W1 inf/cot producers + etf_universe config + etfs IAM tf | PASS |
| ds-commit-gate | the new producer .py | PASS (py_compile + AST + ruff py39 clean) |

Gap: `opal-data-bd/schwab/silver/rps` (and the ETFS producers) not pipescript-thread-registered -- the substrate-locate relied on the comp-freshness `schwab_rps` entry + direct schema read. Ties to remaining-step #3.
